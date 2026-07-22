"""Make the RH-81 ten-layer route-review figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]


def box(ax, xy, text, color, width=0.27, height=0.12, fontsize=8):
    x, y = xy
    patch = FancyBboxPatch((x - width / 2, y - height / 2), width, height, boxstyle="round,pad=0.015", facecolor=color, edgecolor="black", linewidth=0.8)
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize)


def arrow(ax, start, end):
    ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "lw": 1.0, "color": "#333333"})


def main() -> None:
    review = json.loads((ROOT / "results" / "route_review.json").read_text(encoding="utf-8"))
    audit = json.loads((ROOT / "results" / "arb_frontier_audit.json").read_text(encoding="utf-8"))
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 7.8))

    ax = axes[0, 0]
    colors = {
        "validated_advance": "#54a24b",
        "finite_scale_closure": "#2ca02c",
        "analytic_corridor": "#eeca3b",
        "branch_no_go": "#e45756",
        "positive_fallback": "#72b7b2",
        "corridor_synthesis": "#4c78a8",
        "advance_and_barrier": "#f2cf5b",
        "route_correction": "#b279a2",
    }
    for row in review["paper_ledger"]:
        ax.scatter(row["paper"], 0, s=135, color=colors[row["route_effect"]], edgecolor="black", zorder=3)
        ax.text(row["paper"], 0.12 if row["paper"] % 2 == 0 else -0.12, f"RH-{row['paper']}", ha="center", va="center", fontsize=8, rotation=45)
    ax.plot([72, 80], [0, 0], color="#777777", linewidth=1.0, zorder=1)
    ax.set_xlim(71.5, 80.5)
    ax.set_ylim(-0.28, 0.28)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("(a) Nine input layers: advances, barriers, corrections")
    for effect, label in (("finite_scale_closure", "closure"), ("branch_no_go", "no-go"), ("positive_fallback", "fallback"), ("route_correction", "correction")):
        ax.scatter([], [], s=65, color=colors[effect], edgecolor="black", label=label)
    ax.legend(ncol=4, fontsize=7, loc="lower center")

    ax = axes[0, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    box(ax, (0.18, 0.82), "all-level\nlog-square law", "#f2cf5b")
    box(ax, (0.50, 0.82), "all-level postblock\neffective-rank law", "#72b7b2", width=0.31)
    box(ax, (0.34, 0.58), "Stage A1 / A4", "#54a24b")
    arrow(ax, (0.18, 0.75), (0.30, 0.65))
    arrow(ax, (0.50, 0.75), (0.38, 0.65))
    box(ax, (0.72, 0.57), "cloud projection\n+ coefficient bridge\n+ complement limit", "#eeca3b", width=0.34, height=0.18)
    box(ax, (0.50, 0.28), "relative fixed-disk\nA5 determinant", "#4c78a8", width=0.30)
    arrow(ax, (0.39, 0.51), (0.46, 0.36))
    arrow(ax, (0.68, 0.48), (0.54, 0.36))
    ax.text(0.34, 0.94, "OR", fontsize=9, fontweight="bold")
    ax.text(0.53, 0.45, "AND", fontsize=9, fontweight="bold")
    ax.set_title("(b) Minimal completion architecture")

    ax = axes[1, 0]
    labels = [
        "finite slack",
        "rank-2 excess",
        "rank-4 excess",
        "shrinking gain",
        "fixed reversal",
        "pole contrast",
    ]
    values = [row["certified_lower"] for row in audit["rows"]]
    ax.barh(labels, values, color=["#54a24b", "#72b7b2", "#72b7b2", "#4c78a8", "#e45756", "#b279a2"])
    ax.set_xscale("log")
    ax.set_xlabel("certified lower value (log scale)")
    ax.set_title("(c) Archived margin audit")
    ax.grid(axis="x", alpha=0.25)

    ax = axes[1, 1]
    stages = ["A1 finite", "A1 uniform", "A4 conditional", "A4 unconditional", "A5 algebra", "A5 dynamics", "B--D"]
    states = ["green", "amber", "green", "amber", "green", "amber", "not started"]
    state_color = {"green": "#54a24b", "amber": "#eeca3b", "not started": "#bab0ac"}
    ax.barh(stages, [1] * len(stages), color=[state_color[state] for state in states])
    for index, state in enumerate(states):
        ax.text(0.5, index, state, ha="center", va="center", fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.invert_yaxis()
    ax.set_title("(d) Revised stage ledger")

    fig.tight_layout()
    output = ROOT / "figures" / "stage_A_to_A5_route_review"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

