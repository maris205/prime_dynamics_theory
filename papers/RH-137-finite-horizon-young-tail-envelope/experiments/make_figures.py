from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "finite_horizon_audit.json").read_text(encoding="utf-8"))
    tagged = [(row["sigma"], step) for row in data["rows"] for step in row["steps"]]
    steps = [step for _, step in tagged]
    recurrent = [step for step in steps if step["recurrent"]]
    positive = [step for step in steps if step["actual_target"]["value"] > 0]

    blocked_points = []
    for row in data["rows"]:
        incoming = 0.0
        for step in row["steps"]:
            if step["recurrent"] and not step["long_run_orthogonal_contractivity_possible"]:
                radius = step["greedy"]["safety_radius"]
                if radius is not None and radius > 0 and incoming > 0:
                    blocked_points.append((incoming, radius, step["greedy"]["safe"]))
            incoming = step["greedy"]["bound"]["value"]

    fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.4))
    grid = np.logspace(-24, 2, 300)
    axes[0, 0].loglog(
        [step["actual_target"]["value"] for step in positive],
        [step["greedy"]["bound"]["value"] for step in positive],
        "o", markersize=4.5, alpha=0.58, color="tab:blue",
    )
    axes[0, 0].plot(grid, grid, color="black", linestyle=":", label="exact-bound diagonal")
    axes[0, 0].axhline(1.0, color="tab:red", linestyle="--", label="support wall")
    axes[0, 0].set_xlabel("actual target relative tail")
    axes[0, 0].set_ylabel("propagated greedy envelope")
    axes[0, 0].set_title("All 330 propagated bounds dominate")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(True, which="both", alpha=0.18)

    axes[0, 1].loglog(
        [point[1] for point in blocked_points],
        [point[0] for point in blocked_points],
        "o", markersize=5.5, alpha=0.72, color="tab:green",
    )
    wall = np.logspace(-18, 1, 200)
    axes[0, 1].plot(wall, wall, color="black", linestyle=":", label="incoming = safety radius")
    axes[0, 1].set_xlabel("exact finite-step safety radius")
    axes[0, 1].set_ylabel("incoming propagated envelope")
    axes[0, 1].set_title("31 long-run walls are crossed with margin")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(True, which="both", alpha=0.18)

    sigmas = sorted({sigma for sigma, _ in tagged}, reverse=True)
    greedy_counts, polar_counts, actual_counts = [], [], []
    for sigma in sigmas:
        group = [step for value, step in tagged if value == sigma]
        greedy_counts.append(sum(step["greedy"]["safe"] for step in group))
        polar_counts.append(sum(step["polar_safe"] for step in group))
        actual_counts.append(sum(step["actual_target"]["value"] < 1 for step in group))
    x = np.arange(len(sigmas))
    width = 0.26
    axes[1, 0].bar(x - width, polar_counts, width, color="tab:gray", label="polar envelope")
    axes[1, 0].bar(x, greedy_counts, width, color="tab:green", label="greedy 33-gauge")
    axes[1, 0].bar(x + width, actual_counts, width, color="tab:blue", label="actual safe")
    axes[1, 0].set_xticks(x, [str(value) for value in sigmas])
    axes[1, 0].set_xlabel(r"scale $\sigma$")
    axes[1, 0].set_ylabel("safe transitions")
    axes[1, 0].set_title("Finite envelope matches the safe/unsafe split")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(True, axis="y", alpha=0.2)

    ratios = [
        step["greedy"]["bound"]["value"] / step["polar_bound"]["value"]
        for step in recurrent if step["polar_bound"]["value"] > 0
    ]
    weights = [step["greedy"]["weight"] for step in recurrent]
    axes[1, 1].scatter(weights, np.log10(ratios), s=25, alpha=0.62, color="tab:purple")
    axes[1, 1].axhline(0.0, color="black", linestyle=":")
    axes[1, 1].set_xlabel("selected interpolation weight toward metric endpoint")
    axes[1, 1].set_ylabel("log10 greedy/polar propagated bound")
    axes[1, 1].set_title("State-dependent gauge selection improves every recurrence")
    axes[1, 1].grid(True, alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "finite_horizon_young_tail_envelope"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
