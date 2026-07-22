"""Make the RH-91 ten-layer route-review figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    review = json.loads((ROOT / "results" / "route_review.json").read_text(encoding="utf-8"))
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 7.8))

    ax = axes[0, 0]
    labels = [row["paper"] for row in review["layer_ledger"]]
    effects = ["clock", "factor", "energy", "snapshot", "memory", "inject", "P/C", "Ritz", "Schur"]
    colors = ["#4c78a8", "#f58518", "#54a24b", "#54a24b", "#54a24b", "#54a24b", "#e45756", "#54a24b", "#54a24b"]
    ax.bar(range(len(labels)), [1] * len(labels), color=colors)
    for index, effect in enumerate(effects):
        ax.text(index, 0.5, effect, rotation=90, ha="center", va="center", color="white", fontsize=8)
    ax.set_xticks(range(len(labels)), labels, rotation=45, ha="right")
    ax.set_yticks([]); ax.set_ylim(0, 1.15)
    ax.set_title("(a) RH-82--RH-90 route compression")

    ax = axes[0, 1]
    budget = review["bootstrap_budget"]
    ax.plot([row["updates"] for row in budget], [row["tolerance"] for row in budget], marker="o")
    ax.set_yscale("log"); ax.invert_yaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel("consecutive certified Schur updates")
    ax.set_ylabel("relative-tail tolerance")
    ax.set_title(r"(b) $\rho=0.24$ bootstrap budget")

    ax = axes[1, 0]
    ax.axis("off")
    ax.text(0.5, 0.92, "Stage A", ha="center", va="center", fontsize=12, weight="bold")
    ax.text(0.24, 0.68, "L\nfull-block law", ha="center", va="center", bbox=dict(boxstyle="round", fc="#dbe9f6"))
    ax.text(0.72, 0.68, "S + R + O\nSchur packet bundle", ha="center", va="center", bbox=dict(boxstyle="round", fc="#dff2df"))
    ax.text(0.5, 0.40, "either corridor", ha="center", va="center")
    ax.annotate("", xy=(0.45, 0.45), xytext=(0.27, 0.61), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.55, 0.45), xytext=(0.69, 0.61), arrowprops=dict(arrowstyle="->"))
    ax.text(0.5, 0.20, "polylog Hardy budget\nconditional Stage A1/A4", ha="center", va="center", bbox=dict(boxstyle="round", fc="#fff2cc"))
    ax.set_title("(c) Revised Stage-A completion frontier")

    ax = axes[1, 1]
    names = ["coordinate", "unweighted\nGram", "angle gap", "global norm", "point packet"]
    ax.barh(names, [1] * len(names), color="#e45756")
    ax.set_xlim(0, 1.15); ax.set_xticks([])
    ax.set_title("(d) Branch-specific negative markers")
    for index in range(len(names)):
        ax.text(0.5, index, "closed shortcut", ha="center", va="center", color="white", fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "schur_packet_route_review"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
