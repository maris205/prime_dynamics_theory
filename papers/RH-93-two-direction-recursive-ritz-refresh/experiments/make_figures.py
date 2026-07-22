"""Create the RH-93 recursive-refresh audit figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "results" / "two_direction_refresh_audit.json"
PDF = ROOT / "figures" / "two_direction_recursive_ritz_refresh.pdf"
PNG = ROOT / "figures" / "two_direction_recursive_ritz_refresh.png"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    labels = [f"{row['sigma']:.2g}{channel['side'][0].upper()}" for row in audit["rows"] for channel in row["channels"]]
    one_means = np.array([channel["one_direction_chain"]["interval_block_geometric_mean_lower"] for channel in channels])
    two_means = np.array([channel["two_direction_chain"]["interval_block_geometric_mean_upper"] for channel in channels])
    three_means = np.array([channel["three_direction_diagnostic"]["interval_block_geometric_mean_upper"] for channel in channels])
    budgets = np.array([[step["budget_factor"] for step in channel["two_direction_chain"]["steps"]] for channel in channels])
    two_steps = [step for channel in channels for step in channel["two_direction_chain"]["steps"]]
    top_one = np.sort(np.array([step["top_one_cross_energy_fraction"] for step in two_steps]))
    top_two = np.sort(np.array([step["selected_cross_energy_fraction"] for step in two_steps]))
    reference_one = np.array([channel["one_direction_chain"]["interval_endpoint_to_reference_upper"] for channel in channels])
    reference_two = np.array([channel["two_direction_chain"]["interval_endpoint_to_reference_upper"] for channel in channels])
    reference_three = np.array([channel["three_direction_diagnostic"]["interval_endpoint_to_reference_upper"] for channel in channels])

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9})
    figure, axes = plt.subplots(2, 2, figsize=(11.2, 7.4), constrained_layout=True)

    ax = axes[0, 0]
    x = np.arange(len(channels))
    ax.plot(x, one_means, "o-", color="#d95f02", label="one direction")
    ax.plot(x, two_means, "s-", color="#1b9e77", label="two directions")
    ax.plot(x, three_means, "^-", color="#7570b3", label="three directions")
    ax.axhline(0.24, color="#222222", linestyle=":", linewidth=1.2, label="0.24 target")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylim(0.0, 0.34)
    ax.set_ylabel("recursive four-step geometric mean")
    ax.set_title("(a) The second direction closes the block")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    image = ax.imshow(budgets, aspect="auto", cmap="viridis", vmin=0.0, vmax=0.46)
    ax.set_xticks(range(4), ["step 1", "step 2", "step 3", "step 4"])
    ax.set_yticks(range(len(labels)), labels)
    ax.set_title("(b) Exact two-direction budgets")
    for row in range(budgets.shape[0]):
        for column in range(budgets.shape[1]):
            value = budgets[row, column]
            color = "white" if value > 0.28 else "black"
            ax.text(column, row, f"{value:.3f}", ha="center", va="center", fontsize=7, color=color)
    colorbar = figure.colorbar(image, ax=ax, fraction=0.046, pad=0.03)
    colorbar.set_label(r"$\rho_j$")

    ax = axes[1, 0]
    index = np.arange(len(top_one))
    ax.plot(index, top_one, "o", markersize=3.5, color="#e7298a", label="top one")
    ax.plot(index, top_two, "s", markersize=3.5, color="#66a61e", label="top two")
    ax.set_ylim(0.55, 1.01)
    ax.set_xlabel("sorted audited update")
    ax.set_ylabel("projected-cross energy fraction")
    ax.set_title("(c) Two directions capture the cross tail")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    width = 0.24
    ax.semilogy(x - width, reference_one, "o", color="#d95f02", label="one direction")
    ax.semilogy(x, reference_two, "s", color="#1b9e77", label="two directions")
    ax.semilogy(x + width, reference_three, "^", color="#7570b3", label="three directions")
    ax.axhline(1.0, color="#222222", linestyle=":", linewidth=1.2, label="leading-packet tail")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("endpoint tail / leading-packet tail")
    ax.set_title("(d) Three directions nearly track the reference")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    figure.suptitle("RH-93: recursive two-direction Ritz refresh removes the ambient in-block packet reset", fontsize=12)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF)
    figure.savefig(PNG, dpi=220)
    plt.close(figure)
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT)), "channels": len(channels)}, sort_keys=True))


if __name__ == "__main__":
    main()
