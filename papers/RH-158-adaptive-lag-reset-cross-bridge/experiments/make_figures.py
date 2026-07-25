from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/lag_audit.json").read_text())
    summary = data["audit_summary"]
    targets = [item for row in data["rows"] for item in row["targets"]]
    selected = [item["selected"] for item in targets]
    horizons = np.arange(1, data["maximum_lag"] + 1)
    fig, axes = plt.subplots(2, 2, figsize=(11.3, 7.1), constrained_layout=True)

    ax = axes[0, 0]
    full = [summary["certificate_counts_by_lag_horizon"][str(lag)] / 120 for lag in horizons]
    half = [summary["half_suffix_certificate_counts_by_lag_horizon"][str(lag)] / 62 for lag in horizons]
    terminal = [summary["terminal_certificate_counts_by_lag_horizon"][str(lag)] / 10 for lag in horizons]
    ax.plot(horizons, full, "o-", label="all updates")
    ax.plot(horizons, half, "s-", label="delayed half")
    ax.plot(horizons, terminal, "^-", label="terminals")
    ax.set_ylim(-0.03, 1.06)
    ax.set_xlabel("allowed lag horizon")
    ax.set_ylabel("certified fraction")
    ax.set_title("A. Eight past resets close the finite atlas")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    histogram = [summary["selected_lag_histogram"][str(lag)] for lag in horizons]
    ax.bar(horizons, histogram, color="#4c72b0")
    ax.set_xlabel("selected lag")
    ax.set_ylabel("target count")
    ax.set_title("B. Base-maximizing lag is genuinely adaptive")

    ax = axes[1, 0]
    nominal = [item["nominal_fourth_cross_singular"] for item in selected]
    radius = [item["cross_operator_radius"] for item in selected]
    colors = [item["lag"] for item in selected]
    scatter = ax.scatter(nominal, radius, c=colors, cmap="viridis", s=23, alpha=0.78)
    lo = min(nominal + radius); hi = max(nominal + radius)
    ax.plot([lo, hi], [lo, hi], "--", color="black", lw=1)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("selected nominal fourth singular value")
    ax.set_ylabel("centered outward radius")
    ax.set_title("C. Every selected fourth mode clears its radius")
    fig.colorbar(scatter, ax=ax, label="lag", fraction=0.05)

    ax = axes[1, 1]
    bases = [item["normalized_base_lower"] for item in selected]
    paths = [item["path_overlap_lower"] for item in selected]
    ax.scatter(paths, bases, c=colors, cmap="viridis", s=23, alpha=0.78)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("selected path-overlap lower")
    ax.set_ylabel("selected normalized cross-base lower")
    ax.set_title("D. Cross and transport remain finite, not uniform")

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(alpha=0.18)
    output = ROOT / "figures/adaptive_lag_reset_cross_bridge"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
