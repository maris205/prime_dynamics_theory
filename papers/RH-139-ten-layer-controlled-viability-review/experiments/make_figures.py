from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def box(axis, xy, width, height, text, color):
    patch = FancyBboxPatch(xy, width, height, boxstyle="round,pad=0.02", facecolor=color, edgecolor="black", linewidth=0.8)
    axis.add_patch(patch)
    axis.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=8)


def main() -> None:
    data = json.loads((ROOT / "results" / "ten_layer_review.json").read_text(encoding="utf-8"))
    layers = data["layers"]
    fig, axes = plt.subplots(2, 2, figsize=(13.0, 8.5))

    axes[0, 0].set_xlim(0, 5)
    axes[0, 0].set_ylim(0, 2.2)
    colors = {"constructive": "#b8e0c2", "mixed": "#f4cf8b"}
    for index, layer in enumerate(layers):
        row = 1 if index < 5 else 0
        column = index if index < 5 else index - 5
        box(axes[0, 0], (column + 0.06, row + 0.18), 0.82, 0.58, f"RH-{layer['number']}\n{layer['kind']}", colors[layer["kind"]])
        if column < 4:
            axes[0, 0].add_patch(FancyArrowPatch((column + 0.88, row + 0.47), (column + 1.06, row + 0.47), arrowstyle="->", mutation_scale=10))
    box(axes[0, 0], (4.06, 0.18), 0.82, 0.58, "RH-139\nsynthesis", "#a9c9ee")
    axes[0, 0].add_patch(FancyArrowPatch((4.47, 1.18), (0.47, 0.78), arrowstyle="->", mutation_scale=10, connectionstyle="arc3,rad=0.16"))
    axes[0, 0].axis("off")
    axes[0, 0].set_title("RH-130--139: support, memory, gauge, viability, validation")

    labels = ["RH-130\ncomplete chains", "RH-135\npolar contractive", "RH-136\nbalanced contractive", "RH-137\npolar safe chains", "RH-137\ngreedy safe chains", "RH-138\noutward chains"]
    values = [0 / 24, 51 / 216, 183 / 216, 21 / 30, 28 / 30, 28 / 30]
    axes[0, 1].bar(np.arange(len(values)), values, color=["tab:red", "tab:gray", "tab:green", "tab:gray", "tab:blue", "tab:purple"])
    axes[0, 1].set_xticks(np.arange(len(values)), labels, rotation=18, ha="right")
    axes[0, 1].set_ylim(0, 1.02)
    axes[0, 1].set_ylabel("fraction of relevant transitions/chains")
    axes[0, 1].set_title("Finite route progression")
    axes[0, 1].grid(True, axis="y", alpha=0.2)

    threshold_labels = [">0", r"$\geq10^{-8}$", r"$\geq10^{-6}$", r"$\geq10^{-4}$"]
    terminal_counts = [28, 21, 16, 12]
    axes[1, 0].bar(threshold_labels, terminal_counts, color=["tab:blue", "tab:green", "tab:orange", "tab:red"])
    axes[1, 0].axhline(30, color="black", linestyle=":", label="30 audited chains")
    axes[1, 0].set_ylabel("terminal outward-positive chains")
    axes[1, 0].set_title("RH-138 terminal directional floors")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(True, axis="y", alpha=0.2)

    axes[1, 1].set_xlim(0, 10)
    axes[1, 1].set_ylim(0, 6)
    box(axes[1, 1], (0.3, 3.8), 2.2, 1.0, "source exact/interval\nenclosure", "#f4cf8b")
    box(axes[1, 1], (3.0, 3.8), 2.7, 1.0, "eventual controlled tail\nlimsup $y_n<1$", "#b8e0c2")
    box(axes[1, 1], (3.0, 1.5), 2.7, 1.0, "positive normalized-base\nliminf $a_n>0$", "#b8e0c2")
    box(axes[1, 1], (6.3, 2.65), 2.7, 1.0, "positive eventual\ndirectional support", "#a9c9ee")
    for start, end in [((2.5, 4.3), (3.0, 4.3)), ((5.7, 4.3), (6.3, 3.4)), ((5.7, 2.0), (6.3, 2.9))]:
        axes[1, 1].add_patch(FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=12))
    axes[1, 1].text(1.4, 2.55, "independent assembly adds\noutward radii/guards", ha="center", va="center", fontsize=8, color="tab:red")
    axes[1, 1].axis("off")
    axes[1, 1].set_title("Revised minimal frontier: per-step contraction removed")

    fig.tight_layout()
    output = ROOT / "figures" / "ten_layer_controlled_viability_review"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
