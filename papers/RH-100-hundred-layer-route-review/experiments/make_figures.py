"""Create the RH-100 hundred-layer route review figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "results" / "hundred_layer_route_review.json"
PDF = ROOT / "figures" / "hundred_layer_route_review.pdf"
PNG = ROOT / "figures" / "hundred_layer_route_review.png"


def box(ax, x, y, width, height, text, color, edge="#333333"):
    patch = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.02", facecolor=color, edgecolor=edge, linewidth=1.0)
    ax.add_patch(patch)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=7.5, wrap=True)


def main() -> None:
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    phases = review["inventory_summary"]["phase_counts"]
    milestones = review["exact_milestones"]
    negatives = review["negative_route_markers"]
    bundles = review["stage_A_minimal_completion_bundles"]

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9})
    figure, axes = plt.subplots(2, 2, figsize=(12.2, 8.2), constrained_layout=True)

    ax = axes[0, 0]
    palette = plt.cm.Set3(np.linspace(0.05, 0.95, len(phases)))
    for index, phase in enumerate(phases):
        ax.barh(0, phase["last"] - phase["first"] + 1, left=phase["first"] - 0.5, color=palette[index], edgecolor="white", height=0.5)
        ax.text((phase["first"] + phase["last"]) / 2, 0, f"{phase['first']}-{phase['last']}", ha="center", va="center", fontsize=7)
    ax.scatter([item["layer"] for item in milestones], np.full(len(milestones), 0.38), marker="^", color="#1b9e77", s=28, label="exact milestone")
    ax.scatter([item["layer"] for item in negatives], np.full(len(negatives), -0.38), marker="v", color="#d95f02", s=28, label="negative marker")
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.65, 0.65)
    ax.set_yticks([])
    ax.set_xlabel("RH layer")
    ax.set_title("(a) Ninety-nine layers: exact structure and route barriers")
    ax.legend(frameon=False, fontsize=8, ncol=2, loc="upper left")
    ax.grid(alpha=0.2, axis="x")

    ax = axes[0, 1]
    ax.axis("off")
    box(ax, 0.02, 0.72, 0.22, 0.16, "finite Stage-A chain\nclosed", "#b2df8a")
    box(ax, 0.31, 0.78, 0.24, 0.12, "L: all-level\nfull-block law", "#ffe082")
    box(ax, 0.31, 0.55, 0.14, 0.12, "Q: uniform\nquotient", "#ffe082")
    box(ax, 0.48, 0.55, 0.14, 0.12, "G: packet\nGram action", "#ffe082")
    box(ax, 0.65, 0.61, 0.15, 0.12, "H-stop\npreferred", "#ffd180")
    box(ax, 0.65, 0.43, 0.15, 0.12, "H-tube\nblocked", "#ffab91")
    box(ax, 0.83, 0.55, 0.14, 0.12, "O: prefix +\nobservability", "#ffe082")
    box(ax, 0.31, 0.20, 0.18, 0.12, "moving-cloud\nRiesz projection", "#ffe082")
    box(ax, 0.53, 0.20, 0.18, 0.12, "coefficient\nbridge", "#ffe082")
    box(ax, 0.75, 0.20, 0.18, 0.12, "trace-class\ncomplement", "#ffe082")
    ax.annotate("OR", xy=(0.28, 0.76), xytext=(0.25, 0.76), arrowprops=dict(arrowstyle="->", lw=1))
    ax.annotate("packet corridor", xy=(0.31, 0.61), xytext=(0.22, 0.54), arrowprops=dict(arrowstyle="->", lw=1), fontsize=7)
    ax.annotate("then A5 needs all three", xy=(0.53, 0.34), xytext=(0.46, 0.38), arrowprops=dict(arrowstyle="->", lw=1), fontsize=7)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("(b) Revised minimal Stage-A/A5 frontier")

    ax = axes[1, 0]
    labels = ["L fallback", "packet-stop", "packet-tube"]
    sizes = [len(bundle) for bundle in bundles]
    colors = ["#7570b3", "#1b9e77", "#d95f02"]
    ax.bar(labels, sizes, color=colors)
    for index, bundle in enumerate(bundles):
        ax.text(index, sizes[index] + 0.15, "\n".join(name.split("_")[0] for name in bundle), ha="center", va="bottom", fontsize=7)
    ax.set_ylim(0, max(sizes) + 1.5)
    ax.set_ylabel("number of open primitive gates")
    ax.set_title("(c) Three inclusion-minimal Stage-A completion bundles")
    ax.grid(alpha=0.25, axis="y")

    ax = axes[1, 1]
    ax.axis("off")
    plans = review["next_three_layers"]
    y = 0.78
    for plan, color in zip(plans, ("#a6cee3", "#b2df8a", "#fdbf6f")):
        box(ax, 0.08, y, 0.84, 0.15, f"RH-{plan['layer']}: {plan['paper']}", color)
        y -= 0.23
    ax.text(0.5, 0.08, "After RH-103: only the uniform gap-aware quotient law remains\ninside the preferred packet Stage-A bundle; A5 stays separate.", ha="center", va="center", fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("(d) Selected post-centennial sequence")

    figure.suptitle("RH-100: a hundred-layer audit leaves a precise Stage-A frontier, not a zero theorem", fontsize=12.5)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF)
    figure.savefig(PNG, dpi=220)
    plt.close(figure)
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT)), "papers": review["inventory_summary"]["paper_count"], "bundles": len(bundles)}, sort_keys=True))


if __name__ == "__main__": main()
