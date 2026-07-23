"""Create RH-110 capacity and recovery figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "three_mode_capacity_audit.json").read_text(encoding="utf-8"))
    sigmas = [float(row["sigma"]) for row in data["rows"]]
    primary = []
    for row in data["rows"]:
        primary.append(
            [
                step
                for channel in row["channels"]
                for record in channel["thresholds"]
                if float(record["threshold"]) == 1e-8
                for step in record["steps"]
            ]
        )

    fig, axes = plt.subplots(1, 2, figsize=(11.1, 4.35))
    ax = axes[0]
    minima = [min(step["actual_capacity"] for step in steps) for steps in primary]
    maxima = [max(step["actual_capacity"] for step in steps) for steps in primary]
    ax.fill_between(sigmas, minima, maxima, alpha=0.22, color="tab:blue", label="observed range")
    ax.loglog(sigmas, minima, marker="o", color="tab:blue", label="minimum")
    ax.loglog(sigmas, maxima, marker="s", color="tab:orange", label="maximum")
    ax.invert_xaxis()
    ax.set_xlabel(r"scale $\sigma$")
    ax.set_ylabel(r"capacity $\Lambda_{23}=(s_2/s_1)(s_3/s_1)$")
    ax.set_title("Relative three-mode capacity")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False)

    ax = axes[1]
    colors = {1e-8: "tab:blue", 1e-6: "tab:orange", 1e-4: "tab:green"}
    all_values = []
    for threshold, color in colors.items():
        steps = [
            step
            for row in data["rows"]
            for channel in row["channels"]
            for record in channel["thresholds"]
            if float(record["threshold"]) == threshold
            for step in record["steps"]
            if step["direct_weyl_ratio_lower"] > 0.0
        ]
        x = np.asarray([step["direct_weyl_ratio_lower"] for step in steps])
        y = np.asarray([step["capacity_recovered_ratio_lower"] for step in steps])
        all_values.extend(x.tolist())
        ax.loglog(x, y, linestyle="none", marker="o", markersize=3.5, alpha=0.62, color=color, label=rf"$\tau={threshold:.0e}$")
    low, high = min(all_values), max(all_values)
    grid = np.logspace(np.log10(low), np.log10(high), 200)
    ax.loglog(grid, grid, color="black", linewidth=1.2, label="direct equality")
    ax.set_xlabel("direct Weyl lower bound")
    ax.set_ylabel("volume/capacity recovered lower bound")
    ax.set_title("Capacity factorization recovers the direct gate")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "finite_memory_three_mode_capacity"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
