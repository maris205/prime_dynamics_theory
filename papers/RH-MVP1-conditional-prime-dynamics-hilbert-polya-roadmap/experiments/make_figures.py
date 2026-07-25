from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def box(ax, x: float, y: float, width: float, height: float, text: str, color: str, edge: str = "#333333") -> None:
    patch = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        linewidth=1.0, edgecolor=edge, facecolor=color,
    )
    ax.add_patch(patch)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=8)


def arrow(ax, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10, lw=1.0, color="#444444"))


def main() -> None:
    data = json.loads((ROOT / "results/mvp_audit.json").read_text())
    summary = data["audit_summary"]
    fig, axes = plt.subplots(2, 2, figsize=(11.8, 7.4), constrained_layout=True)

    ax = axes[0, 0]
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    positions = [0.02, 0.185, 0.35, 0.515, 0.68, 0.845]
    labels = [
        "F\nfoundation\nPROVED",
        "A\ndeterminant\nOPEN",
        "B\nscattering\nOPEN",
        "C\ngenerator\nOPEN",
        "D\nprime trace\nOPEN",
        "E\nzeta divisor\nOPEN",
    ]
    colors = ["#55a868", "#c9c9c9", "#c9c9c9", "#c9c9c9", "#c9c9c9", "#c9c9c9"]
    for index, (x, label, color) in enumerate(zip(positions, labels, colors)):
        box(ax, x, 0.39, 0.12, 0.24, label, color)
        if index < len(positions) - 1:
            arrow(ax, (x + 0.12, 0.51), (positions[index + 1], 0.51))
    ax.text(0.5, 0.84, "A. Minimum viable proof architecture", ha="center", fontsize=11, fontweight="bold")
    ax.text(0.5, 0.14, "A has a conditional reset-support spine only; every A--E arrow is an obligation, not a result.", ha="center", fontsize=8)

    ax = axes[0, 1]
    phase_labels = ["symbolic", "determinant", "packet/Feshbach", "continuum", "Stage A tools", "support", "reset"]
    phase_widths = [3, 12, 22, 23, 40, 39, 21]
    starts = np.cumsum([0] + phase_widths[:-1]) + 1
    phase_colors = ["#4c72b0", "#55a868", "#8172b2", "#64b5cd", "#ccb974", "#dd8452", "#937860"]
    for start, width, label, color in zip(starts, phase_widths, phase_labels, phase_colors):
        ax.barh([0], [width], left=[start - 1], color=color, height=0.45, label=label)
    for review in [50, 71, 81, 91, 100, 119, 129, 139, 149, 159, 160]:
        ax.axvline(review, color="black", lw=0.5, alpha=0.35)
    ax.set_xlim(0, 160); ax.set_yticks([]); ax.set_xlabel("RH paper number")
    ax.set_title("B. 160 layers built a foundation and narrowed Stage A")
    ax.legend(frameon=False, fontsize=7, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.36))

    ax = axes[1, 0]
    labels = ["directories", "README", "main TeX", "PDF", "summaries", "archives", "test dirs"]
    values = [
        summary["numbered_paper_count"], summary["readme_count"], summary["main_tex_count"],
        summary["pdf_directory_count"], summary["summary_archive_count"],
        summary["verification_archive_count"], summary["test_directory_count"],
    ]
    colors = ["#4c72b0"] * 4 + ["#8172b2"] * 3
    ax.bar(np.arange(len(labels)), values, color=colors)
    ax.set_xticks(np.arange(len(labels)), labels, rotation=30, ha="right", fontsize=8)
    ax.set_ylim(0, 178); ax.set_ylabel("count")
    for index, value in enumerate(values):
        ax.text(index, value + 3, str(value), ha="center", fontsize=8)
    ax.set_title(f"C. Repository audit; {summary['declared_publication_hash_count']} declared hashes match")

    ax = axes[1, 1]
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    rows = [
        ("A fails", "publish transfer-spectrum theory; stop HP escalation"),
        ("B fails", "no canonical orientation/scattering route"),
        ("C fails", "spectral object has wrong reality or counting law"),
        ("D fails", "self-adjoint model is non-arithmetic"),
        ("E fails", "partial match only; no zero or RH conclusion"),
    ]
    for index, (left, right) in enumerate(rows):
        y = 0.78 - 0.16 * index
        box(ax, 0.04, y, 0.16, 0.10, left, "#c44e52", edge="#8b2d2d")
        arrow(ax, (0.20, y + 0.05), (0.27, y + 0.05))
        box(ax, 0.27, y, 0.68, 0.10, right, "#f0f0f0")
    ax.text(0.5, 0.94, "D. Explicit stopping and downgrade rules", ha="center", fontsize=11, fontweight="bold")

    output = ROOT / "figures/conditional_mvp_roadmap"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
