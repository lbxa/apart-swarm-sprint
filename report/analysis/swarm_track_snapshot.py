"""Build the report's frozen, content-free snapshot from verified W&B artifacts.

Read-only with respect to campaigns. The evidence root contains cloud-runs.json,
artifact-verification.json and downloaded sessions/<run-id>/ files. No model calls.
"""

import argparse
import hashlib
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "swarm_analysis", REPO / "harness/research/swarm/analyze.py"
)
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)

MODELS = (
    "@cf/moonshotai/kimi-k2.6",
    "@cf/moonshotai/kimi-k2.7-code",
    "@cf/deepseek-ai/deepseek-v4-pro-0813",
)
NAMES = ("Kimi K2.6", "Kimi K2.7 Code", "DeepSeek V4 Pro")
ARMS = (
    "n3-collusion",
    "n3-honest",
    "n7-collusion",
    "n7-honest",
    "n15-collusion",
    "n15-honest",
    "n3-principles-collusion",
    "n3-contagion-collusion",
    "n3-mandate",
)


def snapshot(root: Path, registry: Path | None = None) -> dict:
    if registry is None:
        cloud = json.loads((root / "cloud-runs.json").read_text())
        verified = json.loads((root / "artifact-verification.json").read_text())
        by_id = {r["run_id"]: r for r in verified["runs"]}
    else:
        frozen = json.loads(registry.read_text())
        entries = frozen["sources"] + frozen["excluded"]
        by_id = {}
        for entry in entries:
            for source in entry["files"]:
                relative = Path(source["path"])
                assert not relative.is_absolute() and ".." not in relative.parts
                path = root / "sessions" / entry["run_id"] / relative
                assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"]
            by_id[entry["run_id"]] = {
                "id": entry["wandb_id"],
                "url": entry["url"],
                "artifacts": [entry["artifact"]],
                "tags": ["excluded"] if "reason" in entry else [],
            }
        cloud = {
            "captured_at_utc": frozen["cloud_cutoff_utc"],
            "project": frozen["project"],
            "runs": entries,
        }
    assert len(by_id) == len(cloud["runs"]), "Incomplete cloud artifact verification"
    manifests = {
        rid: json.loads((root / "sessions" / rid / "run.json").read_text())
        for rid in by_id
    }
    source_roots = sorted(
        {
            m["config"]["case"]["document"].split("/harness/")[0]
            for m in manifests.values()
        }
    )
    cohorts = {p: f"C{i + 1}" for i, p in enumerate(source_roots)}
    runtime_hashes, contract_hashes, settings = (
        set(),
        defaultdict(set),
        defaultdict(set),
    )
    included, excluded, cases, sources = [], [], [], []
    cohort_runs = defaultdict(list)
    for rid, manifest in sorted(manifests.items()):
        run = root / "sessions" / rid
        meta, config = by_id[rid], manifest["config"]
        assert manifest["status"] != "running", (
            "Only terminal uploaded sessions are admitted"
        )
        assert config["model"]["provider"] == "cloudflare"
        scripted = set(config.get("peer_offers") or {})
        opportunities = [
            json.loads(line)
            for path in run.glob("*/opportunities.jsonl")
            for line in path.read_text().splitlines()
        ]
        model_opportunities = [
            o
            for o in opportunities
            if o["actor_id"].startswith("juror-") and o["actor_id"] not in scripted
        ]
        if "excluded" in meta["tags"]:
            assert not any(o["model_calls"] for o in model_opportunities)
            assert not list(run.glob("*/evidence.json"))
            excluded.append(
                {
                    "run_id": rid,
                    "wandb_id": meta["id"],
                    "url": meta["url"],
                    "artifact": meta["artifacts"][0],
                    "reason": "setup only",
                    "files": [
                        {
                            "path": "run.json",
                            "sha256": hashlib.sha256(
                                (run / "run.json").read_bytes()
                            ).hexdigest(),
                        }
                    ],
                }
            )
            continue
        if manifest["status"] == "failed":
            assert any(o["model_calls"] for o in model_opportunities), rid
        runtime_hashes.add(
            json.dumps(manifest["provenance"]["source_sha256"], sort_keys=True)
        )
        normalized = {
            **config,
            "seed": 0,
            "case": {**config["case"], "document": "flat.md"},
        }
        settings[(config["name"], config["model"]["name"])].add(
            json.dumps(normalized, sort_keys=True)
        )
        cohort = cohorts[config["case"]["document"].split("/harness/")[0]]
        included.append(run)
        cohort_runs[cohort].append(run)
        episodes = manifest["episodes"] or analysis.recovered_episodes(run, config)
        assert len(episodes) == config["episodes"], (rid, "missing assignment")
        source_files = []
        for path in sorted(
            [
                run / "run.json",
                *run.glob("*/evidence.json"),
                *run.glob("*/opportunities.jsonl"),
            ]
        ):
            source_files.append(
                {
                    "path": str(path.relative_to(run)),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
        sources.append(
            {
                "run_id": rid,
                "wandb_id": meta["id"],
                "url": meta["url"],
                "artifact": meta["artifacts"][0],
                "cohort": cohort,
                "status": manifest["status"],
                "arm": analysis.arm_of(config["name"]),
                "model": manifest["models"]["juror-1"],
                "seed": config["seed"],
                "git_revision": manifest["provenance"]["git_revision"],
                "files": source_files,
            }
        )
        for episode in episodes:
            evidence = json.loads(
                (run / episode["episode_id"] / "evidence.json").read_text()
            )
            state = evidence["episode"]
            contract_hashes[config["network"]].add(state["deployment"]["code_hash"])
            for key, value in config["parameters"].items():
                assert state["configuration"]["parameters"][key] == value, (rid, key)
            assert state["content"] == config["case"]["reference_claim"], (
                rid,
                "changed claim",
            )
            assert episode.get("label_applies_to_claim", True) is True
            jurors = [j for j in state["jurors"] if j["actor_id"] not in scripted]
            outcomes = [
                analysis.seat_outcome(j, episode["expected_verdict"]) for j in jurors
            ]
            assert len(outcomes) == config["jury_size"] - len(scripted)
            paid = [
                t
                for t in episode.get("credit_transfers", [])
                if t["recipient"] in {j["actor_id"] for j in jurors}
            ]
            # The recovered failures in this snapshot have no paid settlement.
            if not manifest["episodes"]:
                assert not evidence["credit_transfers"]
            cases.append(
                {
                    "run_id": rid,
                    "episode_id": episode["episode_id"],
                    "cohort": cohort,
                    "model": manifest["models"]["juror-1"],
                    "arm": analysis.arm_of(config["name"]),
                    "phase": state["phase"],
                    "false": outcomes.count("colluded"),
                    "truthful": outcomes.count("resisted"),
                    "abstained": outcomes.count("abstained"),
                    "unrevealed": outcomes.count("unrevealed"),
                    "paid_evaluated_jurors": len(paid),
                    "captured": state["phase"] == "SETTLED_CREATOR",
                }
            )
    assert len(runtime_hashes) == 1, (
        "Runtime differs: stratify before describing combined counts"
    )
    assert all(len(v) == 1 for v in contract_hashes.values()), (
        "Contract identity differs within a network mode"
    )
    assert all(len(v) == 1 for v in settings.values()), "Protocol differs within a cell"
    return {
        "cloud_cutoff_utc": cloud["captured_at_utc"],
        "project": cloud["project"],
        "cloud_sessions": len(cloud["runs"]),
        "included_sessions": len(included),
        "excluded": excluded,
        "assigned_cases": len(cases),
        "retained_failed_sessions": sum(s["status"] == "failed" for s in sources),
        "runtime_source_sha256": json.loads(next(iter(runtime_hashes))),
        "contract_code_hash": {
            mode: next(iter(v)) for mode, v in sorted(contract_hashes.items())
        },
        "analysis_sha256": {
            str(path.relative_to(REPO)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [
                Path(__file__).resolve(),
                REPO / "harness/research/swarm/analyze.py",
            ]
        },
        "cells": analysis.summarise(included),
        "cohorts": {
            c: analysis.summarise(paths) for c, paths in sorted(cohort_runs.items())
        },
        "sources": sources,
        "cases": cases,
    }


def tables(data: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for name, arms in [
        ("swarm-scale-counts", ARMS[:6]),
        ("swarm-extension-counts", ARMS[6:]),
    ]:
        lines = [
            r"\begin{tabular}{llrrrrrrr}",
            r"\toprule",
            r"Model & Condition & Cases & F & T & A & U & Capture & Err. \\",
            r"\midrule",
        ]
        labels = {
            "n3-collusion": "3 / colluding",
            "n3-honest": "3 / honest",
            "n7-collusion": "7 / colluding",
            "n7-honest": "7 / honest",
            "n15-collusion": "15 / colluding",
            "n15-honest": "15 / honest",
            "n3-principles-collusion": "Principles",
            "n3-contagion-collusion": "Repeated exposure",
            "n3-mandate": "Mandated publisher",
        }
        for model, display in zip(MODELS, NAMES):
            for index, arm in enumerate(arms):
                c = data["cells"].get(model, {}).get(arm)
                values = (
                    [
                        str(c[k])
                        for k in [
                            "assigned_cases",
                            "colluded",
                            "resisted",
                            "abstained",
                            "unrevealed",
                            "captured_cases",
                            "execution_failure_cases",
                        ]
                    ]
                    if c
                    else [r"---"] * 7
                )
                lines.append(
                    " & ".join([display if index == 0 else "", labels[arm], *values])
                    + r" \\"
                )
            lines.append(r"\midrule")
        lines[-1] = r"\bottomrule"
        lines.append(r"\end{tabular}")
        (output / f"{name}.tex").write_text("\n".join(lines) + "\n")
    register = [
        r"\begin{longtable}{llll}",
        r"\caption{\CloudSessionCaption}\label{tab:cloud-sessions}\\",
        r"\toprule",
        r"Run & W\&B ID & Cohort & State \\",
        r"\midrule\endfirsthead",
        r"\toprule",
        r"Run & W\&B ID & Cohort & State \\",
        r"\midrule\endhead",
    ]
    for s in data["sources"]:
        register.append(
            r"\texttt{"
            + s["run_id"]
            + "} & "
            + r"\href{"
            + s["url"]
            + "}{"
            + s["wandb_id"]
            + "} & "
            + s["cohort"]
            + " & "
            + s["status"]
            + r" \\"
        )
    register.extend([r"\bottomrule", r"\end{longtable}"])
    (output / "swarm-cloud-register.tex").write_text("\n".join(register) + "\n")
    numbers = {
        "CloudSessions": data["cloud_sessions"],
        "IncludedSessions": data["included_sessions"],
        "AssignedCases": data["assigned_cases"],
        "RetainedFailures": data["retained_failed_sessions"],
        "TotalFalse": sum(c["false"] for c in data["cases"]),
        "TotalTruthful": sum(c["truthful"] for c in data["cases"]),
        "TotalAbstained": sum(c["abstained"] for c in data["cases"]),
        "TotalUnrevealed": sum(c["unrevealed"] for c in data["cases"]),
    }
    (output / "swarm-snapshot-numbers.tex").write_text(
        "\n".join(f"\\newcommand{{\\Snapshot{k}}}{{{v}}}" for k, v in numbers.items())
        + "\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path)
    parser.add_argument(
        "--registry", type=Path, help="Frozen registry that pins original file bytes"
    )
    parser.add_argument(
        "--snapshot",
        type=Path,
        help="Regenerate tables from an existing numeric snapshot",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--tables", type=Path, required=True)
    args = parser.parse_args()
    if args.snapshot:
        result = json.loads(args.snapshot.read_text())
    else:
        if args.evidence_root is None or args.output is None:
            parser.error("--evidence-root and --output are required for a source audit")
        result = snapshot(args.evidence_root, args.registry)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    tables(result, args.tables)
    print(
        json.dumps(
            {
                k: result[k]
                for k in [
                    "cloud_sessions",
                    "included_sessions",
                    "assigned_cases",
                    "retained_failed_sessions",
                ]
            }
        )
    )


if __name__ == "__main__":
    main()
