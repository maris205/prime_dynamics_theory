"""Create the RH-109 exterior-power support figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "exterior_fourth_support_audit.json").read_text(encoding="utf-8"))
    thresholds = [float(value) for value in data["thresholds"]]
    colors = ["tab:blue", "tab:orange", "tab:green"]
    sigmas = [float(row["sigma"]) for row in data["rows"]]

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.45))
    ax = axes[0]
    for threshold, color in zip(thresholds, colors):
        record = data["threshold_summary"][f"{threshold:.0e}"]
        scales = record["scale_summary"]
        spectral = [max(float(item["minimum_spectral_volume_lower_bound"]), 1e-24) for item in scales]
        trace = [max(float(item["minimum_trace_volume_lower_bound"]), 1e-24) for item in scales]
        ax.semilogy(
            sigmas,
            spectral,
            marker="o",
            linewidth=2.0,
            color=color,
            label=rf"spectral, $\tau={threshold:.0e}$",
        )
        ax.semilogy(
            sigmas,
            trace,
            marker="x",
            linestyle=":",
            linewidth=1.4,
            color=color,
            alpha=0.85,
            label=rf"trace/$\sqrt{{D}}$, $\tau={threshold:.0e}$",
        )
        ax.axhline(threshold, color=color, linestyle="--", linewidth=0.9, alpha=0.55)
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"scale $\sigma$")
    ax.set_ylabel(r"minimum exterior lower bound for $s_4/s_1$")
    ax.set_title("Five-snapshot exterior certificates")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=7.2, ncol=2)

    ax = axes[1]
    volume_grid = np.logspace(-14, 0, 500)
    lower = volume_grid
    upper = volume_grid ** (1.0 / 3.0)
    ax.fill_between(volume_grid, lower, upper, color="0.88", label=r"sharp interval $\nu_4\leq q_4\leq\nu_4^{1/3}$")
    ax.loglog(volume_grid, lower, color="black", linewidth=1.2, label=r"linear endpoint $q_4=\nu_4$")
    ax.loglog(volume_grid, upper, color="tab:red", linewidth=1.5, label=r"cubic endpoint $q_4=\nu_4^{1/3}$")
    markers = ["o", "s", "^"]
    for threshold, color, marker in zip(thresholds, colors, markers):
        points = [
            step
            for row in data["rows"]
            if float(row["sigma"]) <= 0.02
            for channel in row["channels"]
            for record in channel["thresholds"]
            if float(record["threshold"]) == threshold
            for step in record["steps"]
        ]
        ax.scatter(
            [step["actual_normalized_spectral_volume"] for step in points],
            [step["actual_ratio"] for step in points],
            s=18,
            marker=marker,
            facecolors="none",
            edgecolors=color,
            linewidths=0.75,
            alpha=0.75,
            label=rf"fine replay, $\tau={threshold:.0e}$",
        )
    ax.set_xlabel(r"normalized spectral four-volume $\nu_4$")
    ax.set_ylabel(r"fourth-mode ratio $q_4=s_4/s_1$")
    ax.set_title("Sharp scalar-volume information barrier")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=7.2, loc="lower right")

    fig.tight_layout()
    output = ROOT / "figures" / "exterior_power_fourth_cross_support"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
