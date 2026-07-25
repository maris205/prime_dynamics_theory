from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/route_audit.json").read_text())
    metrics = data["metrics"]
    routes = ["recursive", "native", "contemporaneous", "lagged"]
    gate_labels = [
        "1 packet", "2 overlap", "3 congruence", "4 delay", "5 native tail",
        "6 native support", "7 current cross", "8 lagged cross", "9 all-level", "10 assembly",
    ]
    values = {"not_required": -2, "obstruction": -1, "open": 0, "optional": 1, "certified": 2}
    symbols = {"not_required": "--", "obstruction": "X", "open": "?", "optional": "+", "certified": "C"}
    matrix_states = data["route_matrix"]
    matrix = np.asarray([[values[matrix_states[route][row]] for route in routes] for row in range(10)])
    cmap = ListedColormap(["#eeeeee", "#c44e52", "#ddaa44", "#8fb9d8", "#55a868"])
    norm = BoundaryNorm([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5], cmap.N)

    fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.4), constrained_layout=True)
    ax = axes[0, 0]
    ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(np.arange(4), ["recursive", "native", "current", "lagged"], rotation=20, ha="right")
    ax.set_yticks(np.arange(10), gate_labels, fontsize=8)
    for row in range(10):
        for column, route in enumerate(routes):
            state = matrix_states[route][row]
            ax.text(column, row, symbols[state], ha="center", va="center", fontsize=8, fontweight="bold")
    ax.set_title("A. Typed ten-gate route lattice")

    ax = axes[0, 1]
    labels = ["reset", "overlap", "correlated\ncongruence", "native\npair", "native\nsupport", "current\ncross", "lagged\ncross"]
    numerators = [130, 120, 120, 130, 120, 54, 120]
    denominators = [130, 120, 120, 130, 120, 80, 120]
    fractions = np.asarray(numerators) / np.asarray(denominators)
    colors = ["#55a868"] * 5 + ["#c44e52", "#4c72b0"]
    ax.bar(np.arange(len(labels)), fractions, color=colors)
    ax.set_xticks(np.arange(len(labels)), labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("finite certified fraction")
    for index, (numerator, denominator) in enumerate(zip(numerators, denominators)):
        ax.text(index, fractions[index] + 0.025, f"{numerator}/{denominator}", ha="center", fontsize=7)
    ax.set_title("B. Two finite seeds survive; current cross does not")

    ax = axes[1, 0]
    papers = [record["paper"] for record in data["papers"]]
    checks = [record["check_count"] for record in data["papers"]]
    failures = [record["failure_count"] for record in data["papers"]]
    ax.bar(papers, checks, color="#8172b2", label="matching hash checks")
    ax.bar(papers, failures, color="#c44e52", label="failures")
    ax.set_xlabel("paper number")
    ax.set_ylabel("independent checks")
    ax.set_title("C. 319/319 archive checks pass")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    floor_labels = ["native\nsupport", "lag path\noverlap", "lag cross\nbase", "cross-implied\nnative eig."]
    floors = [
        metrics["native_support_floor"], metrics["lagged_path_overlap_floor"],
        metrics["lagged_cross_base_floor"], metrics["lagged_cross_implied_native_fourth_floor"],
    ]
    ax.bar(np.arange(4), floors, color=["#55a868", "#4c72b0", "#4c72b0", "#8172b2"])
    ax.set_yscale("log")
    ax.set_xticks(np.arange(4), floor_labels, fontsize=8)
    ax.set_ylabel("typed positive lower")
    ax.set_title("D. Positive does not mean uniformly conditioned")
    ax.text(0.02, 0.02, "different output types; scales are diagnostic", transform=ax.transAxes, fontsize=7)

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.16)
    output = ROOT / "figures/ten_layer_reset_route_review"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
