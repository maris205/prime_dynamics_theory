from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/conditional_audit.json").read_text())
    constants = data["constants"]
    diagnostics = data["finite_diagnostics"]
    checklist = data["finite_checklist"]
    fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.3), constrained_layout=True)

    ax = axes[0, 0]
    labels = ["overlap", "weak eig./tail", "finite spread", "lag cross", "lag path", "archives"]
    numerators = [
        checklist["overlap_positive_count"], checklist["native_subunit_count"],
        checklist["finite_spread_count"], checklist["lagged_four_mode_count"],
        checklist["positive_lag_path_count"], checklist["archive_publication_hash_count"],
    ]
    denominators = [120, 130, 120, 120, 120, 108]
    fractions = np.asarray(numerators) / np.asarray(denominators)
    ax.bar(np.arange(len(labels)), fractions, color=["#55a868"] * 3 + ["#4c72b0"] * 2 + ["#8172b2"])
    ax.set_ylim(0, 1.12)
    ax.set_xticks(np.arange(len(labels)), labels, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("finite pass fraction")
    for index, (numerator, denominator) in enumerate(zip(numerators, denominators)):
        ax.text(index, 1.025, f"{numerator}/{denominator}", ha="center", fontsize=7)
    ax.set_title("A. Every conditional clause passes on the frozen atlas")

    ax = axes[0, 1]
    distributions = [
        diagnostics["overlap_lowers"],
        diagnostics["selected_eigenvalue_to_twice_tail_margins"],
        diagnostics["selected_spread_ratios"],
        diagnostics["lagged_normalized_base_lowers"],
        diagnostics["lagged_path_overlap_lowers"],
    ]
    ax.boxplot(distributions, showfliers=False)
    ax.set_yscale("log")
    ax.set_xticks(range(1, 6), ["overlap", "eig./2tail", "spread", "lag base", "path"], rotation=25, ha="right", fontsize=8)
    ax.set_ylabel("finite diagnostic (typed scales)")
    ax.set_title("B. Passing margins remain highly nonuniform")

    ax = axes[1, 0]
    floor_labels = ["native\nlocal", "native\nglobal", "lag base\nlocal", "lag path\nglobal", "step overlap\nworst"]
    floors = [
        constants["minimum_local_native_support_floor"], constants["native_interface_support_floor"],
        constants["minimum_local_lagged_base_floor"], constants["directional_observed_path_floor"],
        constants["directional_consecutive_overlap_floor"],
    ]
    ax.bar(np.arange(5), floors, color=["#55a868", "#55a868", "#4c72b0", "#4c72b0", "#c44e52"])
    ax.set_yscale("log")
    ax.set_xticks(np.arange(5), floor_labels, fontsize=8)
    ax.set_ylabel("positive lower")
    ax.set_title("C. Globalization is valid but can be extremely lossy")

    ax = axes[1, 1]
    indices = np.asarray(data["witness_indices"], dtype=float)
    labels = {
        "overlap_omission": "overlap",
        "tail_separation_omission": "tail gate",
        "spread_omission": "spread",
        "cross_omission": "fourth cross",
        "bounded_lag_omission": "bounded lag",
    }
    for key, values in data["omission_witnesses"].items():
        normalized = np.asarray(values, dtype=float) / float(values[0])
        ax.loglog(indices, normalized, "o-", ms=3, label=labels[key])
    ax.set_xlabel("witness index")
    ax.set_ylabel("floor relative to first witness")
    ax.set_title("D. Each omitted interface admits floor collapse")
    ax.legend(frameon=False, fontsize=7, ncol=2)

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.17)
    output = ROOT / "figures/conditional_all_level_reset_dichotomy"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
