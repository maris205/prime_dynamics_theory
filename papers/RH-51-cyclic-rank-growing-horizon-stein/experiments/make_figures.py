"""Render the RH-51 Gramian-complexity and block-horizon figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "structured_stein_pilot.json"
OUTPUT_PDF = ROOT / "figures" / "structured_stein_geometry.pdf"
OUTPUT_PNG = ROOT / "figures" / "structured_stein_geometry.png"


def main() -> None:
    data = json.loads(PILOT.read_text(encoding="utf-8"))
    rows = data["rows"]
    colors = plt.cm.viridis(np.linspace(0.08, 0.92, len(rows)))
    figure, axes = plt.subplots(2, 2, figsize=(11.7, 8.5))

    axis = axes[0, 0]
    for color, row in zip(colors, rows):
        values = np.asarray(
            row["left_gramian"]["normalized_eigenvalues"],
            dtype=np.float64,
        )
        index = (np.arange(values.size) + 1) / values.size
        axis.semilogy(
            index,
            np.maximum(values, 1.0e-18),
            color=color,
            linewidth=1.5,
            label=rf"$N={int(row['fine_dimension'])}$",
        )
    axis.set_xlabel("normalized eigenvalue index $j/N$")
    axis.set_ylabel(r"$lambda_j(G_B)/\operatorname{tr}G_B$")
    axis.set_title("(a) Exact left Gramians develop longer spectral tails")
    axis.set_ylim(1.0e-18, 1.0)
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5, ncol=2)

    axis = axes[0, 1]
    dimension = np.asarray([row["fine_dimension"] for row in rows])
    left_effective = np.asarray(
        [row["left_gramian"]["participation_rank"] for row in rows]
    )
    right_effective = np.asarray(
        [row["right_gramian"]["participation_rank"] for row in rows]
    )
    left_99 = np.asarray(
        [row["left_gramian"]["rank_for_99_percent_trace"] for row in rows]
    )
    right_99 = np.asarray(
        [row["right_gramian"]["rank_for_99_percent_trace"] for row in rows]
    )
    axis.loglog(dimension, left_effective, "o-", label="left participation rank")
    axis.loglog(dimension, right_effective, "s-", label="right participation rank")
    axis.loglog(dimension, left_99, "^-", label="left 99% trace rank")
    axis.loglog(dimension, right_99, "v-", label="right 99% trace rank")
    axis.set_xlabel("fine dimension $N$")
    axis.set_ylabel("Gramian complexity rank")
    axis.set_title("(b) Energy stays moderate while state complexity grows")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5)

    axis = axes[1, 0]
    for color, row in zip(colors, rows):
        profile = row["left_cyclic_rank_profile"]
        powers = [item["maximum_power"] for item in profile]
        fractions = [item["rank_fraction"] for item in profile]
        axis.plot(
            powers,
            fractions,
            "o-",
            color=color,
            linewidth=1.5,
            markersize=3.5,
            label=rf"$N={int(row['fine_dimension'])}$",
        )
    axis.set_xlabel("largest Krylov power $m$")
    axis.set_ylabel(r"$\operatorname{rank}[X,AX,\ldots,A^mX]/N$")
    axis.set_title("(c) The directional cyclic span rapidly fills about $0.64N$")
    axis.set_ylim(0.0, 0.75)
    axis.grid(True, alpha=0.22)
    axis.legend(fontsize=7.5, ncol=2)

    axis = axes[1, 1]
    horizons = np.asarray(
        [row["left_block_completion"]["selected_horizon"] for row in rows]
    )
    axis.plot(np.log2(dimension), horizons, "o-", linewidth=1.8, color="tab:blue")
    fit = np.polyfit(np.log2(dimension), horizons, 1)
    grid = np.linspace(np.log2(dimension[0]), np.log2(dimension[-1]), 100)
    axis.plot(grid, fit[0] * grid + fit[1], "--", color="tab:blue", alpha=0.75)
    axis.set_xlabel(r"$\log_2 N$")
    axis.set_ylabel("selected block horizon $M$", color="tab:blue")
    axis.tick_params(axis="y", labelcolor="tab:blue")
    axis.set_title("(d) A growing horizon restores a sharp positive certificate")
    axis.grid(True, alpha=0.22)
    twin = axis.twinx()
    left_excess = np.asarray(
        [
            row["left_block_completion"]["energy_upper"]
            / row["left_exact_hardy_energy"]
            - 1.0
            for row in rows
        ]
    )
    right_excess = np.asarray(
        [
            row["right_block_completion"]["energy_upper"]
            / row["right_exact_hardy_energy"]
            - 1.0
            for row in rows
        ]
    )
    twin.semilogy(
        np.log2(dimension),
        left_excess,
        "s:",
        color="tab:red",
        linewidth=1.5,
        label="left relative excess",
    )
    twin.semilogy(
        np.log2(dimension),
        right_excess,
        "^:",
        color="tab:orange",
        linewidth=1.5,
        label="right relative excess",
    )
    twin.set_ylabel("block upper / exact energy $-1$", color="tab:red")
    twin.tick_params(axis="y", labelcolor="tab:red")
    twin.legend(fontsize=7.5, loc="center right")

    figure.suptitle(
        "Structured Stein certificates: high-dimensional Gramians and a viable growing-horizon closure",
        fontsize=13.0,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PDF, bbox_inches="tight")
    figure.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
