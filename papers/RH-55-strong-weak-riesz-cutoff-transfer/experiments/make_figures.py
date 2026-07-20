"""Create the RH-55 four-panel publication figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "riesz_cutoff_pilot.json"
PNG = ROOT / "figures" / "strong_weak_riesz_cutoff_transfer.png"
PDF = ROOT / "figures" / "strong_weak_riesz_cutoff_transfer.pdf"


def main() -> None:
    data = json.loads(PILOT.read_text(encoding="utf-8"))
    midpoint = data["midpoint_ulam_audit"]
    factors = data["archived_intrinsic_factor_audit"]
    adaptive = data["adaptive_exponent_audit"]
    fixed = data["fixed_window_route_no_go"]

    figure, axes = plt.subplots(2, 2, figsize=(11.2, 8.2))

    axis = axes[0, 0]
    mesh = np.asarray([row["mesh"] for row in midpoint])
    row_l1 = np.asarray([row["maximum_row_l1"] for row in midpoint])
    row_bv = np.asarray([row["maximum_row_bv_density"] for row in midpoint])
    axis.loglog(mesh, row_l1, "o-", label=r"max row $L^1$")
    axis.loglog(mesh, row_bv, "s-", label=r"max lifted BV")
    axis.loglog(mesh, row_l1[-1] * (mesh / mesh[-1]) ** 2, "--", label=r"$h^2$")
    axis.invert_xaxis()
    axis.set_xlabel(r"mesh $h$")
    axis.set_ylabel("measured defect")
    axis.set_title("(a) Midpoint-to-Ulam bridge")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(fontsize=8)

    axis = axes[0, 1]
    for multiple, marker in ((5.0, "o"), (6.0, "s"), (8.0, "^")):
        selected = [row for row in factors if row["declared_multiple"] == multiple]
        sigma = np.asarray([row["sigma"] for row in selected])
        actual = np.asarray([row["actual_sum"] for row in selected])
        axis.loglog(sigma, actual, marker + "-", label=rf"actual $L={multiple:g}$")
    stress = [row for row in factors if row["declared_multiple"] == 5.0]
    axis.loglog(
        [row["sigma"] for row in stress],
        [row["gaussian_shape_riesz_envelope_unit_constant"] for row in stress],
        "k--",
        label="shape envelope (unit constant)",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise $sigma$")
    axis.set_ylabel(r"$epsilon_P+epsilon_W$")
    axis.set_title("(b) Recomputed intrinsic factors")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(fontsize=7)

    axis = axes[1, 0]
    for kappa in (1.0, 1.25, 1.5, 1.75, 2.0):
        selected = [row for row in adaptive if row["kappa"] == kappa]
        axis.loglog(
            [row["sigma"] for row in selected],
            [row["gaussian_shape_riesz_envelope"] for row in selected],
            "o-",
            markersize=3,
            label=rf"$kappa={kappa:g}$",
        )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise $sigma$")
    axis.set_ylabel(r"$h^kappasigma^{-5/2}$")
    axis.set_title(r"(c) Near-critical $h=sigma^2/\log(1/\sigma)$")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(fontsize=7, ncol=2)

    axis = axes[1, 1]
    sigma = np.asarray([row["sigma"] for row in fixed])
    axis.loglog(
        sigma,
        [row["strong_bv_route_proxy"] for row in fixed],
        "o-",
        label=r"BV proxy $e^{-L^2/2}\sigma^{-1}$",
    )
    axis.loglog(
        sigma,
        [row["riesz_route_proxy"] for row in fixed],
        "s-",
        label=r"Riesz proxy $e^{-L^2/2}\sigma^{-5/2}$",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise $sigma$")
    axis.set_ylabel("fixed-window route proxy")
    axis.set_title("(d) Fixed-window proof-route no-go")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(fontsize=8)

    figure.suptitle(
        "Strong--weak adaptive cutoff transfer for intrinsic Riesz factors",
        fontsize=14,
    )
    figure.tight_layout(rect=(0, 0, 1, 0.96))
    figure.savefig(PNG, dpi=220)
    figure.savefig(PDF)
    plt.close(figure)
    print(json.dumps({"png": str(PNG), "pdf": str(PDF)}, sort_keys=True))


if __name__ == "__main__":
    main()
