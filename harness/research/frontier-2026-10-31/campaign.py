"""Run frozen experiment waves with one durable cap and retain every attempt."""

# Blocking setup/teardown runs outside the concurrent paid-process gather.
# ruff: noqa: ASYNC221, ASYNC240

import argparse
import asyncio
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from veracity_harness.spending import CampaignSpending
from veracity_harness.tracking import log_run, uploadable

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MODELS = {
    "deepseek-pro": "@cf/deepseek-ai/deepseek-v4-pro-0813",
    "glm-5.3": "@cf/zai-org/glm-5.3",
    "kimi-2.6": "@cf/moonshotai/kimi-k2.6",
    "kimi-2.7-code": "@cf/moonshotai/kimi-k2.7-code",
    "deepseek-4.1-flash": "@cf/deepseek-ai/deepseek-v4.1-flash-1017",
}
ARMS = (
    "baseline",
    "false-offer",
    "false-peer",
    "true-offer",
    "verify-alone",
    "verify-peer",
    "quota-peer",
    "canonical-peer",
)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def spending_export(output):
    ledger = CampaignSpending(output / "spending.sqlite", Decimal(500))
    with sqlite3.connect(ledger.path) as db:
        db.row_factory = sqlite3.Row
        rows = [dict(row) for row in db.execute("SELECT * FROM requests ORDER BY rowid")]
    write_json(output / "spending.json", {**ledger.snapshot(), "request_ledger": rows})
    return ledger.snapshot()


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--wave", choices=ARMS, required=True)
    parser.add_argument("--attempt-label", default="01")
    parser.add_argument("--concurrency", type=int, choices=range(1, 6), default=3)
    parser.add_argument("--models", nargs="+", choices=MODELS, default=list(MODELS))
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    os.umask(0o077)
    for key in ("WANDB_DIR", "WANDB_CACHE_DIR", "WANDB_DATA_DIR", "WANDB_CONFIG_DIR"):
        os.environ.setdefault(key, str(output / "wandb-runtime" / key.lower()))
        Path(os.environ[key]).mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("VERACITY_RATE_DB", str(output / "request-rate.sqlite"))
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip():
        raise RuntimeError("Commit the exact code and configuration before dispatch")
    subprocess.run(["git", "fetch", "origin"], cwd=ROOT, check=True)
    upstream = subprocess.check_output(
        ["git", "rev-parse", "origin/main"], cwd=ROOT, text=True
    ).strip()
    subprocess.run(["git", "merge-base", "--is-ancestor", upstream, "HEAD"], cwd=ROOT, check=True)
    subprocess.run(["cargo", "build", "--workspace", "--locked"], cwd=ROOT, check=True)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    bundle = output / f"source-{revision}.tar.gz"
    if not bundle.exists():
        subprocess.run(
            ["git", "archive", "--format=tar.gz", "-o", str(bundle), "HEAD"], cwd=ROOT, check=True
        )
    wave = {
        "wave": args.wave,
        "started_at": datetime.now(UTC).isoformat(),
        "upstream_revision": upstream,
        "git_revision": revision,
        "source_archive_sha256": hashlib.sha256(bundle.read_bytes()).hexdigest(),
        "engine_sha256": hashlib.sha256(
            (ROOT / "target/debug/veracity-game-service").read_bytes()
        ).hexdigest(),
        "docker_image": subprocess.check_output(
            ["docker", "image", "inspect", "veracity-agent-sandbox:1", "--format", "{{.Id}}"],
            text=True,
        ).strip(),
        "models": {slug: MODELS[slug] for slug in args.models},
        "spending_before": spending_export(output),
        "attempts": [],
    }
    record = output / f"wave-{args.wave}-{args.attempt_label}.json"
    if record.exists():
        raise RuntimeError(
            "Wave already has an audit record; retain it and choose a new campaign version"
        )
    write_json(record, wave)
    needles = tuple(
        os.environ[k]
        for k in (
            "OPENROUTER_API_KEY",
            "OPENROUTER_BACKUP_API_KEY",
            "CLOUDFLARE_API_TOKEN",
            "CLOUDFLARE_ADMIN_TOKEN",
            "CLOUDFLARE_ACCOUNT_ID",
            "WANDB_API_KEY",
        )
        if os.environ.get(k)
    )

    # Runs are independent processes, but share the exact same cap and per-model
    # rate database. Upload SDK lifecycle calls run sequentially after the wave.
    async def run_one(slug, model):
        stdout = output / f"{args.wave}-{args.attempt_label}-{slug}.stdout"
        stderr = output / f"{args.wave}-{args.attempt_label}-{slug}.stderr"
        command = [
            sys.executable,
            "-m",
            "veracity_harness.cli",
            "run",
            "--config",
            str(HERE / f"{args.wave}.toml"),
            "--model",
            model,
            "--output",
            str(output),
            "--budget-ledger",
            str(output / "spending.sqlite"),
            "--budget-usd",
            "500",
        ]
        started = datetime.now(UTC).isoformat()
        previous = set(output.glob("run-*/run.json"))
        print(f"START {args.wave} {slug}", flush=True)
        with stdout.open("w") as out, stderr.open("w") as err:
            process = await asyncio.create_subprocess_exec(
                *command, cwd=ROOT, stdout=out, stderr=err
            )
            code = await process.wait()
        attempt = {
            "model": model,
            "slug": slug,
            "command": command,
            "started_at": started,
            "exit_code": code,
            "stdout": stdout.name,
            "stderr": stderr.name,
        }
        # Log files are private until credential scanning. Manifest IDs locate all
        # failures too, including runs that terminate before printing a directory.
        attempt["runs"] = [
            str(p.parent.relative_to(output))
            for p in output.glob("run-*/run.json")
            if p not in previous
            if (m := json.loads(p.read_text()))["config"]["name"] == f"frontier-{args.wave}"
            and m["config"]["model"]["name"] == model
        ]
        wave["attempts"].append(attempt)
        write_json(record, wave)
        print(f"END {args.wave} {slug} exit={code} runs={attempt['runs']}", flush=True)
        return attempt

    semaphore = asyncio.Semaphore(args.concurrency)

    async def bounded_run(slug):
        async with semaphore:
            return await run_one(slug, MODELS[slug])

    attempts = await asyncio.gather(*(bounded_run(slug) for slug in args.models))
    wave["spending_after"] = spending_export(output)
    wave["finished_at"] = datetime.now(UTC).isoformat()
    write_json(record, wave)
    for attempt in attempts:
        for name in attempt["runs"]:
            directory = output / name
            reproduction = directory / "reproduction"
            reproduction.mkdir(exist_ok=True)
            # Hardlinks retain the same source bytes without multiplying disk use.
            target = reproduction / bundle.name
            if not target.exists():
                target.hardlink_to(bundle)
            for item in (record, output / "spending.json", HERE / "PROTOCOL.md"):
                (reproduction / item.name).write_bytes(item.read_bytes())
            hashes = {
                str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in uploadable(directory, include_model_calls=True)
                if p.name != "SHA256SUMS.json"
            }
            write_json(directory / "SHA256SUMS.json", hashes)
            try:
                url = log_run(
                    directory,
                    "collusion-benchmark",
                    entity="lbxa-corp",
                    needles=needles,
                    include_model_calls=True,
                )
                print(f"PUBLISHED {name} {url}", flush=True)
            except Exception as error:
                print(f"UPLOAD_FAILED {name} {type(error).__name__}", flush=True)
    print(json.dumps(wave["spending_after"]), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
