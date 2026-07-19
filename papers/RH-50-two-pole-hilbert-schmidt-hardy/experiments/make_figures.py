"""Render the RH-50 two-pole Hardy-energy summary figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "two_pole_hardy_pilot.json"
OUTPUT_PDF = ROOT / "figures" / "two_pole_hardy_energy.pdf"
OUTPUT_PNG = ROOT / "figures" / "two_pole_hardy_energy.png"


def main() -> None:
    data = json.loads(PILOT.read_text(encoding="utf-8"))
    rows = data["rows"]
    colors = plt.cm.viridis(np.linspace(0.08, 0.92, len(rows)))
    figure, axes = plt.subplots(2, 2, figsize=(11.7, 8.5))

    axis = axes[0, 0]
    powers = np.arange(data["maximum_power"] + 1)
    for color, row in zip(colors, rows):
        axis.semilogy(
            powers,
            row["left_power_gain_sequence"],
            color=color,
            linewidth=1.55,
            label=rf"$\sigma={float(row['sigma']):g}$",
        )
    axis.set_xlabel("bulk time power $m$")
    axis.set_ylabel(r"$\|U^*N^mQUB\|_{S_2}/\|B\|_{S_2}$")
    axis.set_title("(a) Left two-pole directional powers")
    axis.set_ylim(1.0e-10, 1.5)
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5, ncol=2)

    axis = axes[0, 1]
    for color, row in zip(colors, rows):
        axis.semilogy(
            powers,
            row["right_power_gain_sequence"],
            color=color,
            linewidth=1.55,
            label=rf"$\sigma={float(row['sigma']):g}$",
        )
    axis.set_xlabel("bulk time power $m$")
    axis.set_ylabel(r"$\|CN_A^mQ_A\|_{S_2}/\|C\|_{S_2}$")
    axis.set_title("(b) Right two-pole directional powers")
    axis.set_ylim(1.0e-10, 1.5)
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5, ncol=2)

    axis = axes[1, 0]
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    left_energy = np.asarray(
        [
            float(row["hardy_energies"]["r=0.85"][
                "left_truncated_hardy_energy"
            ])
            for row in rows
        ]
    )
    right_energy = np.asarray(
        [
            float(row["hardy_energies"]["r=0.85"][
                "right_truncated_hardy_energy"
            ])
            for row in rows
        ]
    )
    bulk_product = np.asarray(
        [
            max(
                float(branch["maximum_bulk_gain_product_candidate"])
                for branch in row["branches"].values()
            )
            for row in rows
        ]
    )
    axis.semilogx(sigma, left_energy, "o-", linewidth=1.8, label="left Hardy energy")
    axis.semilogx(sigma, right_energy, "s-", linewidth=1.8, label="right Hardy energy")
    axis.semilogx(sigma, bulk_product, "^-", linewidth=1.8, label="max bulk gain product")
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$ (decreasing to the right)")
    axis.set_ylabel("normalized candidate")
    axis.set_title(r"(c) $r=0.85$ Hardy energies remain on a plateau")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=8)

    axis = axes[1, 1]
    fields = (
        ("fine_left", 0, "left Perron", "o"),
        ("fine_left", 1, "left parity", "s"),
        ("coarse_right", 1, "right parity", "^"),
    )
    for ledger, index, label, marker in fields:
        key = (
            "left_residue_action_over_B_hilbert_schmidt"
            if ledger == "fine_left"
            else "right_residue_action_over_C_hilbert_schmidt"
        )
        values = [
            float(row["residue_action_ledgers"][ledger][index][key])
            for row in rows
        ]
        axis.loglog(
            sigma,
            values,
            marker=marker,
            linewidth=1.8,
            label=label,
        )
    anchor = float(
        rows[-1]["residue_action_ledgers"]["fine_left"][0][
            "left_residue_action_over_B_hilbert_schmidt"
        ]
    )
    axis.loglog(
        sigma,
        anchor * (sigma / sigma[-1]) ** 0.5,
        "k--",
        linewidth=1.2,
        label=r"reference $\sigma^{1/2}$",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$ (decreasing to the right)")
    axis.set_ylabel("normalized residue action")
    axis.set_title("(d) The peripheral residues leave the coupling ranges")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=8)

    figure.suptitle(
        "Two-pole Hilbert--Schmidt Hardy energies: directional decay without global contraction",
        fontsize=13.0,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PDF, bbox_inches="tight")
    figure.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
