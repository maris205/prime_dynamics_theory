"""Render the RH-49 quarter-power directional-resolvent figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "directional_reduced_resolvent_certificate.json"
OUTPUT_PDF = ROOT / "figures" / "directional_reduced_resolvent.pdf"
OUTPUT_PNG = ROOT / "figures" / "directional_reduced_resolvent.png"


def main() -> None:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    rows = data["floating_five_scale_audit"]["rows"]
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    figure, axes = plt.subplots(2, 2, figsize=(11.6, 8.5))

    axis = axes[0, 0]
    series = (
        ("B_hilbert_schmidt_norm", r"$\|B\|_{S_2}$", "o", "#355f8a"),
        ("B_operator_candidate", r"$\|B\|$ candidate", "s", "#2a9d8f"),
        ("C_hilbert_schmidt_norm", r"$\|C\|_{S_2}$", "^", "#b56576"),
        ("C_operator_candidate", r"$\|C\|$ candidate", "D", "#e9a03b"),
    )
    for field, label, marker, color in series:
        axis.loglog(
            sigma,
            [float(row[field]) for row in rows],
            marker=marker,
            linewidth=1.65,
            markersize=4.5,
            color=color,
            label=label,
        )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$ (decreasing to the right)")
    axis.set_ylabel("coupling norm")
    axis.set_title("(a) Exact Haar Frobenius and operator candidates")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=8)

    axis = axes[0, 1]
    b_rank = np.asarray(
        [float(row["B_sqrt_stable_rank_candidate"]) for row in rows]
    )
    c_rank = np.asarray(
        [float(row["C_sqrt_stable_rank_candidate"]) for row in rows]
    )
    axis.loglog(sigma, b_rank, "o-", linewidth=1.8, label=r"$B$ channel")
    axis.loglog(sigma, c_rank, "s-", linewidth=1.8, label=r"$C$ channel")
    anchor = b_rank[-1]
    axis.loglog(
        sigma,
        anchor * (sigma / sigma[-1]) ** (-0.25),
        "k--",
        linewidth=1.2,
        label=r"reference $\sigma^{-1/4}$",
    )
    axis.loglog(
        sigma,
        c_rank[-1] * (sigma / sigma[-1]) ** (-0.5),
        color="0.4",
        linestyle=":",
        linewidth=1.2,
        label=r"reference $\sigma^{-1/2}$",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$ (decreasing to the right)")
    axis.set_ylabel(r"$\|\cdot\|_{S_2}/\|\cdot\|$")
    axis.set_title("(b) The outgoing channel selects the quarter power")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=8)

    axis = axes[1, 0]
    axis.semilogx(
        sigma,
        [float(row["reduced_hilbert_schmidt_gain_sum"]) for row in rows],
        "o-",
        linewidth=1.8,
        label="residue-deflated HS sum",
    )
    axis.semilogx(
        sigma,
        [float(row["full_hilbert_schmidt_gain_sum"]) for row in rows],
        "s-",
        linewidth=1.8,
        label="full HS sum",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$ (decreasing to the right)")
    axis.set_ylabel("sum over Perron and parity branches")
    axis.set_title("(c) Eight-node Hilbert--Schmidt directional plateau")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=8)

    axis = axes[1, 1]
    direct = np.asarray(
        [float(row["direct_mixed_gain_sum_candidate"]) for row in rows]
    )
    transferred = np.asarray(
        [
            float(row["stable_rank_transferred_full_candidate"])
            for row in rows
        ]
    )
    axis.loglog(
        sigma,
        direct,
        "o-",
        linewidth=1.8,
        label="direct mixed candidate",
    )
    axis.loglog(
        sigma,
        transferred,
        "s-",
        linewidth=1.8,
        label="stable-rank transferred candidate",
    )
    critical_anchor = transferred[0]
    axis.loglog(
        sigma,
        critical_anchor * (sigma / sigma[0]) ** (-0.5),
        "k--",
        linewidth=1.2,
        label=r"RH-48 boundary $\sigma^{-1/2}$",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$ (decreasing to the right)")
    axis.set_ylabel("combined directional gain")
    axis.set_title("(d) Both floating routes remain below the critical slope")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.8)

    figure.suptitle(
        "Residue-deflated directional resolvents and the quarter-power bridge",
        fontsize=13.2,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PDF, bbox_inches="tight")
    figure.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
