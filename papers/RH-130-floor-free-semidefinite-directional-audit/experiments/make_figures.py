from __future__ import annotations

import collections
import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "floor_free_audit.json").read_text(encoding="utf-8"))
    states = data["state_rows"]
    pairs = data["pairs"]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))

    for side, marker, color in (("left", "o", "tab:blue"), ("right", "s", "tab:orange")):
        rows = [row for row in states if row["side"] == side]
        axes[0].scatter(
            [row["sigma"] for row in rows], [row["condition_log10"] for row in rows],
            marker=marker, color=color, alpha=0.62, s=26, label=side,
        )
    axes[0].set_xscale("log")
    axes[0].invert_xaxis()
    axes[0].set_xlabel(r"scale $\sigma$")
    axes[0].set_ylabel(r"$\log_{10}\kappa(A)$")
    axes[0].set_title("Floor-free action conditioning")
    axes[0].legend(frameon=False)
    axes[0].grid(True, alpha=0.22)

    positive = [row for row in states if row["directional_candidate"]["log10"] is not None]
    axes[1].scatter(
        [row["condition_log10"] for row in positive],
        [row["directional_candidate"]["log10"] for row in positive],
        c=[row["sigma"] for row in positive], cmap="viridis_r", s=27, alpha=0.72,
    )
    axes[1].set_xlabel(r"$\log_{10}\kappa(A)$")
    axes[1].set_ylabel("candidate log10")
    axes[1].set_title("118/120 local candidates remain positive")
    axes[1].grid(True, alpha=0.22)

    edge_order = [(0.16, 0.08), (0.08, 0.04), (0.04, 0.02), (0.02, 0.01)]
    labels = [".16→.08", ".08→.04", ".04→.02", ".02→.01"]
    categories = collections.defaultdict(lambda: [0] * len(edge_order))
    for pair in pairs:
        index = edge_order.index((pair["source_sigma"], pair["target_sigma"]))
        if pair["positive_transfer"]:
            category = "positive"
        elif pair["optimal_tail_factor"]["infinite"]:
            category = "rank creation"
        else:
            category = r"finite, $\gamma\geq1$"
        categories[category][index] += 1
    bottom = [0] * len(edge_order)
    colors = {"positive": "tab:green", "rank creation": "tab:red", r"finite, $\gamma\geq1$": "tab:purple"}
    for category in ("positive", "rank creation", r"finite, $\gamma\geq1$"):
        axes[2].bar(labels, categories[category], bottom=bottom, color=colors[category], label=category)
        bottom = [a + b for a, b in zip(bottom, categories[category])]
    axes[2].set_ylim(0, 25)
    axes[2].set_ylabel("phase/side/threshold pairs")
    axes[2].set_title("Floor-free adjacent-scale outcome")
    axes[2].tick_params(axis="x", rotation=25)
    axes[2].legend(frameon=False, fontsize=8)
    axes[2].grid(True, axis="y", alpha=0.22)

    fig.tight_layout()
    output = ROOT / "figures" / "floor_free_semidefinite_directional_audit"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
