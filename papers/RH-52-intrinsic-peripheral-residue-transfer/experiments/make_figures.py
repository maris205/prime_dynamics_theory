"""Render the RH-52 finite-factor and residue-transfer figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "factor_transfer_pilot.json"
OUTPUT_PDF = ROOT / "figures" / "factor_residue_transfer.pdf"
OUTPUT_PNG = ROOT / "figures" / "factor_residue_transfer.png"


def branch(row, section: str, mode: str):
    return next(item for item in row[section] if item["mode"] == mode)


def values(rows, section: str, mode: str, field: str):
    return np.asarray(
        [float(branch(row, section, mode)[field]) for row in rows]
    )


def main() -> None:
    data = json.loads(PILOT.read_text(encoding="utf-8"))
    rows = data["rows"]
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    figure, axes = plt.subplots(2, 2, figsize=(11.7, 8.5))

    axis = axes[0, 0]
    axis.semilogx(
        sigma,
        values(
            rows,
            "fine_factor_branches",
            "perron",
            "weak_condition_product",
        ),
        "o-",
        label=r"Perron $\|r\|_\infty\|\ell\|_1$",
    )
    axis.semilogx(
        sigma,
        values(
            rows,
            "fine_factor_branches",
            "parity",
            "weak_condition_product",
        ),
        "s-",
        label=r"parity $\|r\|_\infty\|\ell\|_1$",
    )
    axis.semilogx(
        sigma,
        values(
            rows,
            "fine_factor_branches",
            "perron",
            "projector_square_over_log",
        ),
        "^-",
        label=r"Perron $\|P\|^2/\log(1/\sigma)$",
    )
    axis.semilogx(
        sigma,
        values(
            rows,
            "fine_factor_branches",
            "parity",
            "projector_square_over_log",
        ),
        "v-",
        label=r"parity $\|P\|^2/\log(1/\sigma)$",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$ (decreasing to the right)")
    axis.set_ylabel("normalized factor quantity")
    axis.set_title("(a) Weak factors stay uniformly conditioned")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5)

    axis = axes[0, 1]
    axis.semilogx(
        sigma,
        values(
            rows,
            "fine_factor_branches",
            "perron",
            "left_detail_over_sharp_h_sigma_inverse",
        ),
        "o-",
        label=r"Perron detail$/\,(h\sigma^{-1})$",
    )
    axis.semilogx(
        sigma,
        values(
            rows,
            "fine_factor_branches",
            "parity",
            "left_detail_over_sharp_h_sigma_inverse",
        ),
        "s-",
        label=r"parity detail$/\,(h\sigma^{-1})$",
    )
    axis.semilogx(
        sigma,
        [row["B_hilbert_schmidt_over_h_sigma_minus_three_halves"] for row in rows],
        "^-",
        label=r"$\|B\|_{S_2}/(h\sigma^{-3/2})$",
    )
    axis.semilogx(
        sigma,
        [row["C_hilbert_schmidt_over_h_sigma_minus_three_halves"] for row in rows],
        "v-",
        label=r"$\|C\|_{S_2}/(h\sigma^{-3/2})$",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$")
    axis.set_ylabel("scale-normalized quantity")
    axis.set_title("(b) Sharp detail and two-sided coupling clocks")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5)

    axis = axes[1, 0]
    perron_residue = values(
        rows,
        "fine_left_residue_actions",
        "perron",
        "left_residue_action_over_B_hilbert_schmidt",
    )
    parity_residue = values(
        rows,
        "fine_left_residue_actions",
        "parity",
        "left_residue_action_over_B_hilbert_schmidt",
    )
    right_residue = values(
        rows,
        "coarse_right_residue_actions",
        "parity",
        "right_residue_action_over_C_hilbert_schmidt",
    )
    axis.loglog(sigma, perron_residue, "o-", label="fine Perron residue")
    axis.loglog(sigma, parity_residue, "s-", label="fine parity residue")
    axis.loglog(sigma, right_residue, "^-", label="right parity residue")
    anchor_half = parity_residue[-1] / np.sqrt(sigma[-1])
    anchor_one = right_residue[-1] / sigma[-1]
    axis.loglog(
        sigma,
        anchor_half * np.sqrt(sigma),
        "k--",
        linewidth=1.2,
        label=r"reference $\sigma^{1/2}$",
    )
    axis.loglog(
        sigma,
        anchor_one * sigma,
        "k:",
        linewidth=1.2,
        label=r"reference $\sigma$",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$")
    axis.set_ylabel("normalized residue action")
    axis.set_title("(c) Actual residues vanish beyond the O(1) theorem")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5)

    axis = axes[1, 1]
    axis.loglog(
        sigma,
        values(
            rows,
            "adjacent_factor_transfer",
            "parity",
            "left_l1_normalized_adjacent_error",
        ),
        "o-",
        label=r"left $L^1$ adjacent error",
    )
    axis.loglog(
        sigma,
        values(
            rows,
            "adjacent_factor_transfer",
            "parity",
            "right_linf_normalized_adjacent_error",
        ),
        "s-",
        label=r"right $L^\infty$ adjacent error",
    )
    axis.loglog(
        sigma,
        values(
            rows,
            "adjacent_factor_transfer",
            "parity",
            "projector_relative_adjacent_defect",
        ),
        "^-",
        label="relative projector defect",
    )
    axis.loglog(
        sigma,
        values(
            rows,
            "adjacent_factor_transfer",
            "parity",
            "eigenvalue_adjacent_error",
        ),
        "v-",
        label="eigenvalue difference",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$")
    axis.set_ylabel("adjacent fine/coarse defect")
    axis.set_title("(d) Intrinsic factors are stable across one Haar level")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5)

    figure.suptitle(
        "Intrinsic peripheral residues: weak-factor closure and stronger observed transfer",
        fontsize=13.0,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PDF, bbox_inches="tight")
    figure.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
