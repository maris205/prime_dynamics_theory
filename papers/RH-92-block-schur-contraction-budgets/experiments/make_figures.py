"""Create the RH-92 four-panel audit figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "results" / "block_schur_budget_audit.json"
PDF = ROOT / "figures" / "block_schur_contraction_budgets.pdf"
PNG = ROOT / "figures" / "block_schur_contraction_budgets.png"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    steps = [step for channel in channels for step in channel["steps"]]
    labels = [f"{row['sigma']:.2g}{channel['side'][0].upper()}" for row in audit["rows"] for channel in row["channels"]]
    budget_means = np.array([channel["block_budget_geometric_mean"] for channel in channels])
    actual_means = np.array([channel["interval_actual_block_geometric_mean_upper"] for channel in channels])
    budgets = np.array([channel["budget_factors"] for channel in channels])

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9})
    figure, axes = plt.subplots(2, 2, figsize=(11.2, 7.4), constrained_layout=True)

    ax = axes[0, 0]
    x = np.arange(len(channels))
    ax.plot(x, budget_means, "o-", color="#1f77b4", label="rational budget mean")
    ax.plot(x, actual_means, "s--", color="#2ca02c", label="interval actual upper")
    ax.axhline(0.24, color="#b22222", linewidth=1.2, linestyle=":", label="0.24 target")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("four-step geometric mean")
    ax.set_title("(a) Block contraction survives")
    ax.set_ylim(0.0, 0.26)
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    image = ax.imshow(budgets, aspect="auto", cmap="viridis", vmin=0.0, vmax=max(0.76, float(budgets.max())))
    ax.set_xticks(range(4), ["step 1", "step 2", "step 3", "step 4"])
    ax.set_yticks(range(len(labels)), labels)
    ax.set_title("(b) Variable one-step budgets")
    for row in range(budgets.shape[0]):
        for column in range(budgets.shape[1]):
            value = budgets[row, column]
            color = "white" if value > 0.35 else "black"
            ax.text(column, row, f"{value:.3f}", ha="center", va="center", fontsize=7, color=color)
    colorbar = figure.colorbar(image, ax=ax, fraction=0.046, pad=0.03)
    colorbar.set_label(r"$\rho_j$")

    ax = axes[1, 0]
    coercive_x = []
    coercive_surplus = []
    negative_x = []
    for index, step in enumerate(steps):
        if step["trial_kind"] == "negative_direction":
            negative_x.append(index)
        else:
            coercive_x.append(index)
            coercive_surplus.append(step["certified_relative_surplus_lower"])
    ax.semilogy(coercive_x, coercive_surplus, "o", markersize=4, color="#6a3d9a", label="coercive surplus lower")
    if negative_x:
        ax.semilogy(negative_x, [min(coercive_surplus)] * len(negative_x), "*", markersize=10, color="#ff7f00", label="negative-direction branch")
    ax.set_xlabel("audited update index")
    ax.set_ylabel("certified relative surplus")
    ax.set_title("(c) All forty Schur signs are strict")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    failures = [step for step in steps if step["pointwise_subquarter_failure"]]
    failure_labels = []
    failure_ratios = []
    failure_pivots = []
    for row in audit["rows"]:
        for channel in row["channels"]:
            for step in channel["steps"]:
                if step["pointwise_subquarter_failure"]:
                    failure_labels.append(f"{row['sigma']:.2g}{channel['side'][0].upper()}@{step['time']}")
                    failure_ratios.append(step["interval_corrected_contraction_lower"])
                    failure_pivots.append(min(step["pointwise_sylvester_pivot_lowers"]))
    fx = np.arange(len(failures))
    ax.bar(fx, failure_ratios, color="#d95f02", alpha=0.82, label="corrected contraction lower")
    ax.axhline(0.24, color="#222222", linestyle=":", linewidth=1.2, label="0.24 target")
    ax.set_xticks(fx, failure_labels, rotation=45, ha="right")
    ax.set_ylabel("one-step contraction")
    ax.set_title("(d) Seven pointwise obstructions")
    ax.grid(alpha=0.2, axis="y")
    twin = ax.twinx()
    twin.semilogy(fx, failure_pivots, "D--", color="#1b9e77", markersize=4, label="minimum positive pivot")
    twin.set_ylabel("Sylvester pivot lower")
    handles, names = ax.get_legend_handles_labels()
    handles2, names2 = twin.get_legend_handles_labels()
    ax.legend(handles + handles2, names + names2, frameon=False, fontsize=7, loc="upper right")

    figure.suptitle("RH-92: pointwise Schur decay fails, but four-step contraction budgets remain green", fontsize=12)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF)
    figure.savefig(PNG, dpi=220)
    plt.close(figure)
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT)), "channels": len(channels), "updates": len(steps)}, sort_keys=True))


if __name__ == "__main__":
    main()
