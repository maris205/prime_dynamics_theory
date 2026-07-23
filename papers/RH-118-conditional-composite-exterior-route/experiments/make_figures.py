"""Create the RH-118 finite-gate and route-ledger figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "conditional_route_audit.json").read_text(encoding="utf-8"))
    thresholds = ("1e-08", "1e-06", "1e-04")
    labels = ("direct_weyl", "trace_concentration", "directional_rayleigh")
    display = ("direct", "trace", "directional", "composite", "adaptive", "actual")
    colors = ("tab:blue", "tab:orange", "tab:green", "tab:purple", "tab:red", "black")
    x = np.arange(len(thresholds))
    width = 0.13

    fig, axes = plt.subplots(1, 2, figsize=(11.1, 4.4))
    ax = axes[0]
    values = []
    for key in thresholds:
        record = data["threshold_summary"][key]
        values.append(
            [
                record["candidate_support_counts"][labels[0]],
                record["candidate_support_counts"][labels[1]],
                record["candidate_support_counts"][labels[2]],
                record["composite_support_count"],
                record["adaptive_support_count"],
                record["actual_support_count"],
            ]
        )
    matrix = np.asarray(values)
    for index, (name, color) in enumerate(zip(display, colors)):
        ax.bar(x + (index - 2.5) * width, matrix[:, index], width=width, color=color, alpha=0.8, label=name)
    ax.set_xticks(x, [r"$10^{-8}$", r"$10^{-6}$", r"$10^{-4}$"])
    ax.set_ylim(85, 121)
    ax.set_xlabel("support threshold")
    ax.set_ylabel("certified updates out of 120")
    ax.set_title("Finite complete-gate coverage")
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(frameon=False, fontsize=7, ncol=2)

    ax = axes[1]
    winners = data["audit_summary"]["selected_route_counts"]
    winner_labels = ("direct_weyl", "spectral_capacity", "trace_concentration", "directional_rayleigh")
    winner_display = ("direct", "spectral/capacity", "trace/concentration", "directional/Rayleigh")
    winner_values = [winners[label] for label in winner_labels]
    bars = ax.barh(np.arange(4), winner_values, color=("tab:blue", "tab:cyan", "tab:orange", "tab:green"), alpha=0.82)
    ax.set_yticks(np.arange(4), winner_display)
    ax.invert_yaxis()
    ax.set_xlabel("times selected by the RH-115 maximum")
    ax.set_title("Route alternation and the remaining boundary")
    ax.grid(True, axis="x", alpha=0.25)
    for bar, value in zip(bars, winner_values):
        ax.text(value + 2, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=9)
    ax.text(
        0.98,
        0.05,
        "all-level physical packets proved: 0 / 3",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color="firebrick",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "firebrick", "alpha": 0.9},
    )

    fig.tight_layout()
    output = ROOT / "figures" / "conditional_composite_exterior_route"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
