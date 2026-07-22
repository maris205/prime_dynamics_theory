"""Create RH-72 validated-assembly figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "interval_assembly_audit.json"
PDF = ROOT / "figures" / "validated_folded_gaussian_assembly.pdf"
PNG = ROOT / "figures" / "validated_folded_gaussian_assembly.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    rows = payload["rows"]
    sigmas = [row["sigma"] for row in rows]
    dimensions = [row["dimension"] for row in rows]
    figure, axes = plt.subplots(2, 2, figsize=(11.8, 7.4))

    axes[0, 0].loglog(
        dimensions,
        [
            row["full_to_repaired_matrix_defect"]["two_norm_upper"]
            for row in rows
        ],
        marker="o",
        linewidth=1.9,
        color="#2f6f9f",
        label="full vs repaired",
    )
    axes[0, 0].loglog(
        dimensions,
        [
            row["sparse_exact_to_frozen_matrix_defect"]["two_norm_upper"]
            for row in rows
        ],
        marker="s",
        linewidth=1.7,
        color="#9c2f2f",
        label="sparse exact vs frozen",
    )
    axes[0, 0].set_xlabel("fine dimension")
    axes[0, 0].set_ylabel("certified matrix 2-norm defect")
    axes[0, 0].set_title("End-to-end assembly defect")
    axes[0, 0].grid(True, which="both", alpha=0.24)
    axes[0, 0].legend(frameon=False)

    axes[0, 1].semilogx(
        sigmas,
        [row["maximum_full_to_sparse_row_l1_upper"] for row in rows],
        marker="o",
        linewidth=1.9,
        color="#5a4a78",
    )
    axes[0, 1].invert_xaxis()
    axes[0, 1].set_xlabel(r"$\sigma$")
    axes[0, 1].set_ylabel("maximum row L1 truncation")
    axes[0, 1].set_title(r"Full to $8\sigma$ sparse normalization")
    axes[0, 1].grid(True, which="both", alpha=0.24)

    axes[1, 0].semilogx(
        sigmas,
        [row["maximum_frozen_row_sum_defect_upper"] for row in rows],
        marker="o",
        linewidth=1.9,
        color="#d07a22",
        label="row-sum defect",
    )
    axes[1, 0].semilogx(
        sigmas,
        [row["haar"]["embedding_two_norm_defect_upper"] for row in rows],
        marker="s",
        linewidth=1.7,
        color="#2f7d5b",
        label="Haar embedding defect",
    )
    axes[1, 0].invert_xaxis()
    axes[1, 0].set_xlabel(r"$\sigma$")
    axes[1, 0].set_ylabel("certified defect")
    axes[1, 0].set_title("Dyadic repair and Haar constants")
    axes[1, 0].grid(True, which="both", alpha=0.24)
    axes[1, 0].legend(frameon=False)

    layers = [
        ("Algebraic parameter", "green", "#2f7d5b"),
        ("Full/sparse Gaussian rows", "green", "#2f7d5b"),
        ("Exact stochastic repair", "green", "#2f7d5b"),
        ("Haar coarse/cross assembly", "green", "#2f7d5b"),
        ("Perron right vector", "green", "#2f7d5b"),
        ("Stationary left vector", "amber", "#d07a22"),
        ("Parity Riesz pair", "amber", "#d07a22"),
    ]
    positions = list(range(len(layers)))
    axes[1, 1].barh(
        positions,
        [1.0] * len(layers),
        color=[entry[2] for entry in layers],
        height=0.62,
    )
    axes[1, 1].set_yticks(positions, [entry[0] for entry in layers])
    axes[1, 1].invert_yaxis()
    axes[1, 1].set_xlim(0.0, 1.0)
    axes[1, 1].set_xticks([])
    axes[1, 1].set_title("Upstream validation split")
    for position, (_, status, _) in zip(positions, layers, strict=True):
        axes[1, 1].text(
            0.5,
            position,
            status,
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=8.5,
        )
    for spine in axes[1, 1].spines.values():
        spine.set_visible(False)

    figure.tight_layout()
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)
    print(PDF.relative_to(ROOT))
    print(PNG.relative_to(ROOT))


if __name__ == "__main__":
    main()
