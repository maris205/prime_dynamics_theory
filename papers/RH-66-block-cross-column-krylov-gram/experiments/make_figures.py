"""Create RH-66 block-Gram comparison figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "block_gram_pilot.json"
PDF = ROOT / "figures" / "block_cross_column_krylov_gram.pdf"
PNG = ROOT / "figures" / "block_cross_column_krylov_gram.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    models = payload["models"]
    labels = ("cancel", "chain", "phase")
    keys = (
        ("directional_gain", "block directional", "#2f7d5b"),
        ("uniform_gram_gain", "uniform PSD Gram", "#4f7cac"),
        ("independent_column_gain", "independent columns", "#9c2f2f"),
        ("rank_matched_fused_gain", "rank-matched fused", "#d07a22"),
    )
    figure, axes = plt.subplots(1, 2, figsize=(10.7, 4.25))
    positions = np.arange(len(models), dtype=float)
    width = 0.19
    for offset, (key, label, color) in enumerate(keys):
        values = [model["depths"][0][key] for model in models]
        axes[0].bar(
            positions + (offset - 1.5) * width,
            values,
            width=width,
            label=label,
            color=color,
        )
    axes[0].set_yscale("log")
    axes[0].set_xticks(positions, labels)
    axes[0].set_ylabel("upper / exact directional energy")
    axes[0].set_title("One block level")
    axes[0].grid(True, axis="y", which="both", alpha=0.24)
    axes[0].legend(frameon=False, fontsize=8)

    for model, color, marker in zip(
        models[1:], ("#9c2f2f", "#4f7cac"), ("o", "s"), strict=True
    ):
        ranks = [record["krylov_rank"] for record in model["depths"]]
        short = "chain" if "chain" in model["name"] else "phase"
        axes[1].plot(
            ranks,
            [record["directional_gain"] for record in model["depths"]],
            marker=marker,
            linewidth=1.9,
            color=color,
            label=f"{short}: block directional",
        )
        axes[1].plot(
            ranks,
            [record["independent_column_gain"] for record in model["depths"]],
            marker=marker,
            linestyle="--",
            linewidth=1.5,
            color=color,
            alpha=0.75,
            label=f"{short}: independent",
        )
    axes[1].set_yscale("log")
    axes[1].set_xlabel("block Krylov rank")
    axes[1].set_ylabel("upper / exact directional energy")
    axes[1].set_title("Closure with increasing block rank")
    axes[1].grid(True, which="both", alpha=0.24)
    axes[1].legend(frameon=False, fontsize=8)
    figure.tight_layout()
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)
    print(PDF.relative_to(ROOT))
    print(PNG.relative_to(ROOT))


if __name__ == "__main__":
    main()
