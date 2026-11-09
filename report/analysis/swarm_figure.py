"""Draw the swarm peer-pressure figure from harness/research/swarm/analyze.py output.

  python report/analysis/swarm_figure.py --data report/data/swarm-summary.json \
      --output-dir report/figures

Each model gets two bars: collusion resistance with honest scripted peers and with
colluding scripted peers. Error bars are case-clustered standard errors; labels give
the number of scored cases. No message bodies or prompts are read.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

STYLE = Path(__file__).with_name("baseline.mplstyle")
ARMS = (
    ("honest", "Honest peers", "#E69F00"),
    ("collusion", "Colluding peers", "#0072B2"),
)
NAMES = {
    "@cf/moonshotai/kimi-k2.6": "Kimi K2.6",
    "@cf/moonshotai/kimi-k2.7-code": "Kimi K2.7 Code",
    "@cf/zai-org/glm-5.3": "GLM-5.3",
    "@cf/deepseek-ai/deepseek-v4-pro-0813": "DeepSeek V4 Pro",
    "@cf/deepseek-ai/deepseek-v4.1-flash-1017": "DeepSeek V4.1 Flash",
}


def draw(summary: dict, output_dir: Path) -> None:
    def key(model: str) -> float:
        cell = summary[model].get("collusion") or {}
        return (
            cell.get("resistance_pct") if cell.get("resistance_pct") is not None else -1
        )

    models = sorted(summary, key=key)
    plt.style.use(STYLE)
    fig, ax = plt.subplots(figsize=(6.5, 0.62 * len(models) + 1.1))
    height = 0.36
    for offset, (arm, label, colour) in zip((height / 2, -height / 2), ARMS):
        for row, model in enumerate(models):
            cell = summary[model].get(arm)
            if not cell or cell["resistance_pct"] is None:
                continue
            value, se = cell["resistance_pct"], cell["resistance_se_pct"]
            ax.barh(
                row + offset,
                value,
                height,
                color=colour,
                label=label if row == 0 else None,
            )
            if se:
                ax.errorbar(
                    value, row + offset, xerr=se, color="#26343E", capsize=2, lw=0.8
                )
            ax.text(
                min(value + (se or 0), 100) + 1.5,
                row + offset,
                f"{value:.1f}%  (n={cell['cases']})",
                va="center",
                fontsize=7.5,
            )
    ax.set_yticks(range(len(models)), [NAMES.get(m, m) for m in models])
    ax.set_xlim(0, 122)
    ax.set_xticks(range(0, 101, 25), [f"{t}%" for t in range(0, 101, 25)])
    ax.set_xlabel("Collusion resistance (truthful share of revealed evaluated votes)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncols=2, frameon=False)
    fig.tight_layout()
    output_dir.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(output_dir / f"swarm-peer-pressure.{suffix}")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    draw(json.loads(args.data.read_text()), args.output_dir)


if __name__ == "__main__":
    main()
