"""Render the RH-61 horizon-scaling audit figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "horizon_scaling_audit.json"
PDF = ROOT / "figures" / "directional_horizon_scaling.pdf"
PNG = ROOT / "figures" / "directional_horizon_scaling.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    rows = payload["rows"]
    inverse_sigma = np.asarray([1.0 / float(row["sigma"]) for row in rows])
    colors = {"left": "#1f77b4", "right": "#d62728"}
    labels = {"left": "left channel", "right": "right channel"}

    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.0))
    axis = axes[0, 0]
    for side in ("left", "right"):
        gaps = np.asarray([row[side]["contraction_gap"] for row in rows])
        fit = payload["fits"][f"{side}_gap"]
        predicted = np.exp(float(fit["log_intercept"])) * (
            1.0 / inverse_sigma
        ) ** float(fit["power"])
        axis.loglog(inverse_sigma, gaps, "o", color=colors[side], label=labels[side])
        axis.loglog(inverse_sigma, predicted, "--", color=colors[side], alpha=0.75)
    axis.set_xlabel(r"$1/\sigma$")
    axis.set_ylabel(r"maximal packet gap $1-q$")
    axis.set_title("Stored metric contractions")
    axis.grid(True, which="both", alpha=0.24)
    axis.legend(frameon=False, fontsize=8)

    axis = axes[0, 1]
    for side in ("left", "right"):
        geometric = np.asarray(
            [row[side]["geometric_horizons"]["0.05"] for row in rows]
        )
        observed = np.asarray(
            [row[side]["observed_phase_horizons"]["0.05"] for row in rows]
        )
        axis.loglog(
            inverse_sigma,
            geometric,
            "o-",
            color=colors[side],
            label=f"{labels[side]} geometric envelope",
        )
        axis.loglog(
            inverse_sigma,
            observed,
            "s:",
            color=colors[side],
            label=f"{labels[side]} stored phase completion",
        )
    axis.set_xlabel(r"$1/\sigma$")
    axis.set_ylabel("first stored / guaranteed horizon")
    axis.set_title("5% relative tail target")
    axis.grid(True, which="both", alpha=0.24)
    axis.legend(frameon=False, fontsize=7)

    endpoint = rows[-1]
    horizons = np.asarray(sorted(int(key) for key in endpoint["left"]["horizons"]))
    axis = axes[1, 0]
    for side in ("left", "right"):
        records = endpoint[side]["horizons"]
        actual = np.asarray(
            [records[str(horizon)]["phase_tail_ratio_to_initial"] for horizon in horizons]
        )
        geometric = np.asarray(
            [
                records[str(horizon)]["geometric_tail_ratio_to_initial"]
                for horizon in horizons
            ]
        )
        axis.semilogy(horizons, actual, "o-", color=colors[side], label=f"{labels[side]} directional")
        axis.semilogy(horizons, geometric, "--", color=colors[side], alpha=0.8, label=f"{labels[side]} norm envelope")
    axis.set_xlabel("finite phase horizon $L$")
    axis.set_ylabel("tail / initial metric tail")
    axis.set_title(r"Endpoint $\sigma=0.01$: tail profile")
    axis.grid(True, which="both", alpha=0.24)
    axis.legend(frameon=False, fontsize=7)

    axis = axes[1, 1]
    for side in ("left", "right"):
        records = endpoint[side]["horizons"]
        ratios = np.asarray(
            [records[str(horizon)]["phase_upper_over_exact"] for horizon in horizons]
        )
        axis.semilogy(
            horizons,
            np.maximum(ratios - 1.0, 1.0e-16),
            "o-",
            color=colors[side],
            label=labels[side],
        )
    axis.set_xlabel("finite phase horizon $L$")
    axis.set_ylabel("completion excess over exact energy")
    axis.set_title(r"Endpoint $\sigma=0.01$: recovered phase fusion")
    axis.grid(True, which="both", alpha=0.24)
    axis.legend(frameon=False, fontsize=8)

    figure.tight_layout(pad=1.0)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=180, bbox_inches="tight")
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT))}, sort_keys=True))


if __name__ == "__main__":
    main()
