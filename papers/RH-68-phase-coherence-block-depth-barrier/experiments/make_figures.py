"""Create RH-68 phase-depth barrier figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "depth_barrier_pilot.json"
PDF = ROOT / "figures" / "phase_coherence_block_depth_barrier.pdf"
PNG = ROOT / "figures" / "phase_coherence_block_depth_barrier.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    figure, axes = plt.subplots(1, 3, figsize=(12.2, 3.85))

    rings = payload["exact_rings"]
    horizons = [row["horizon"] for row in rings]
    required = [row["required_depth_for_10_percent_error"] for row in rings]
    axes[0].plot(
        horizons,
        required,
        marker="o",
        linewidth=1.9,
        color="#9c2f2f",
        label="exact Fourier ring",
    )
    axes[0].plot(
        horizons,
        [value + 1 for value in horizons],
        linestyle="--",
        color="#333333",
        linewidth=1.2,
        label=r"$k=L+1$",
    )
    axes[0].set_xlabel("tail horizon $L$")
    axes[0].set_ylabel("depth for error $\leq0.1$")
    axes[0].set_title("Exact depth obstruction")
    axes[0].grid(True, alpha=0.24)
    axes[0].legend(frameon=False, fontsize=8)

    for row, color in zip(
        payload["jittered_rings"],
        ("#333333", "#2f7d5b", "#4f7cac", "#d07a22"),
        strict=True,
    ):
        records = row["depths"][:-1]
        axes[1].semilogy(
            [record["depth"] for record in records],
            [record["projection_error"] for record in records],
            marker="o",
            linewidth=1.7,
            color=color,
            label=f"jitter={row['jitter_in_phase_cells']:g}",
        )
    axes[1].set_xlabel("block depth $k$")
    axes[1].set_ylabel("normalized projection error")
    axes[1].set_title("Perturbed rings remain hard")
    axes[1].grid(True, which="both", alpha=0.24)
    axes[1].legend(frameon=False, fontsize=8)

    arcs = payload["phase_arcs"]
    axes[2].plot(
        [row["arc_width_radians"] for row in arcs],
        [row["required_depth_for_10_percent_error"] for row in arcs],
        marker="o",
        linewidth=1.9,
        color="#4f7cac",
    )
    axes[2].set_xlabel("phase arc width (radians)")
    axes[2].set_ylabel("depth for error $\leq0.1$")
    axes[2].set_title("Phase compression opens the route")
    axes[2].grid(True, alpha=0.24)
    figure.tight_layout()
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)
    print(PDF.relative_to(ROOT))
    print(PNG.relative_to(ROOT))


if __name__ == "__main__":
    main()
