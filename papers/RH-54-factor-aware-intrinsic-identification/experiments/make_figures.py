"""Render the RH-54 factor-aware transfer figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "factor_aware_transfer_pilot.json"
OUTPUT_PDF = ROOT / "figures" / "factor_aware_intrinsic_identification.pdf"
OUTPUT_PNG = ROOT / "figures" / "factor_aware_intrinsic_identification.png"


def main() -> None:
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    rows = pilot["rows"]
    dimensions = np.asarray([row["fine_dimension"] for row in rows])
    stress = [row["comparisons"][0] for row in rows]
    figure, axes = plt.subplots(2, 2, figsize=(11.7, 8.5))

    axis = axes[0, 0]
    for multiple, marker, color in (
        (5.0, "o", "tab:red"),
        (6.0, "s", "tab:orange"),
        (8.0, "^", "tab:blue"),
    ):
        values = [
            next(
                item["matrix_defects"]["markov_spectral"]
                for item in row["comparisons"]
                if item["cutoff_multiple"] == multiple
            )
            for row in rows
        ]
        axis.loglog(
            dimensions,
            values,
            marker + "-",
            color=color,
            label=rf"actual $L={multiple:g}$",
        )
    axis.set_xlabel("fine dimension $N$")
    axis.set_ylabel(r"$\|T^{(L)}-T\|_2$")
    axis.set_title("(a) Deliberate five-sigma cutoff stress test")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5)

    axis = axes[0, 1]
    quantities = (
        ("fine_projector_spectral", "fine projector", "o", "tab:green"),
        ("fine_weighted_riesz_spectral", "fine weighted Riesz", "s", "tab:purple"),
        ("fine_bulk_spectral", "fine bulk", "^", "tab:brown"),
        ("normalized_coupling_b_actual", "normalized $B$", "d", "tab:cyan"),
    )
    for key, label, marker, color in quantities:
        axis.loglog(
            dimensions,
            [item["intrinsic_factor_defects"][key] for item in stress],
            marker + "-",
            color=color,
            label=label,
        )
    axis.set_xlabel("fine dimension $N$")
    axis.set_ylabel("actual binary64 defect")
    axis.set_title("(b) Cutoff transfer through intrinsic factors")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.4)

    axis = axes[1, 0]
    for side, marker, color in (
        ("left", "o", "tab:blue"),
        ("right", "s", "tab:orange"),
    ):
        actual = np.asarray(
            [item[side]["actual_full_energy_squared_difference"] for item in stress]
        )
        finite = np.asarray(
            [item[side]["finite_energy_squared_perturbation_upper"] for item in stress]
        )
        axis.loglog(
            dimensions,
            actual,
            marker + "-",
            color=color,
            label=f"{side} actual full $E^2$ defect",
        )
        axis.loglog(
            dimensions,
            finite,
            marker + "--",
            color=color,
            markerfacecolor="none",
            label=f"{side} finite-time upper",
        )
    axis.set_xlabel("fine dimension $N$")
    axis.set_ylabel("Hardy energy-squared defect")
    axis.set_title("(c) Conservative but valid factor-aware transfer")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.0)

    axis = axes[1, 1]
    for side, marker, color in (
        ("left", "o", "tab:blue"),
        ("right", "s", "tab:orange"),
    ):
        actual = [item[side]["actual_block_power_defect"] for item in stress]
        telescope = [item[side]["semigroup_telescope_upper"] for item in stress]
        axis.loglog(
            dimensions,
            actual,
            marker + "-",
            color=color,
            label=f"{side} actual $A^M$ defect",
        )
        axis.loglog(
            dimensions,
            telescope,
            marker + "--",
            color=color,
            markerfacecolor="none",
            label=f"{side} semigroup ledger upper",
        )
    axis.set_xlabel("fine dimension $N$")
    axis.set_ylabel("block-power defect")
    axis.set_title("(d) Growing-horizon contraction survives recomputation")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.0)

    figure.suptitle(
        "Factor-aware sparse-to-full transfer for intrinsic Hardy triples",
        fontsize=13.0,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PDF, bbox_inches="tight")
    figure.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
