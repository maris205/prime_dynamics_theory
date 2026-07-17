"""Render the RH-33 center and refined-leaf certificate atlas."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    centers = read_csv(ROOT / "results" / "center_certificates_sigma_1e-02.csv")
    leaves = read_csv(ROOT / "results" / "refined_atlas_sigma_1e-02_leaves.csv")

    center_real = np.asarray([float(row["spectral_parameter_real"]) for row in centers])
    center_imag = np.asarray([float(row["spectral_parameter_imag"]) for row in centers])
    contour_center = complex(-0.3233504401504541, -0.5508412474453575)
    center_turn = np.mod(
        np.angle((center_real + 1.0j * center_imag) - contour_center),
        2.0 * np.pi,
    ) / (2.0 * np.pi)
    inverse = np.asarray(
        [float(row["center_inverse_two_norm_upper"]) for row in centers]
    )
    residual = np.asarray([float(row["residual_frobenius_upper"]) for row in centers])
    adaptive = np.asarray(
        [row["source_kind"] == "adaptive_gap_midpoint" for row in centers],
        dtype=bool,
    )

    leaf_turn = np.asarray([float(row["theta_midpoint"]) for row in leaves]) / (
        2.0 * np.pi
    )
    product = np.asarray([float(row["neumann_product_upper"]) for row in leaves])
    budget_ratio = np.asarray([float(row["budget_ratio_upper"]) for row in leaves])

    order_centers = np.argsort(center_turn)
    order_leaves = np.argsort(leaf_turn)
    figure, axes = plt.subplots(2, 2, figsize=(11.4, 7.4), sharex="col")

    first = axes[0, 0]
    first.scatter(
        center_turn[~adaptive],
        inverse[~adaptive],
        s=25,
        color="#3b6ea8",
        alpha=0.82,
        label="RH-28 parent midpoint",
    )
    first.scatter(
        center_turn[adaptive],
        inverse[adaptive],
        s=38,
        marker="x",
        linewidths=1.5,
        color="#c55a32",
        label="adaptive gap midpoint",
    )
    first.plot(
        center_turn[order_centers],
        inverse[order_centers],
        color="#8b8b8b",
        linewidth=0.7,
        alpha=0.45,
        zorder=0,
    )
    first.set_ylabel(r"certified $\|A(z_j)^{-1}\|_2$ upper bound")
    first.set_title("109 direct center certificates")
    first.grid(True, alpha=0.22)
    first.legend(frameon=False, fontsize=8.5)

    second = axes[1, 0]
    second.semilogy(
        center_turn[~adaptive],
        residual[~adaptive],
        "o",
        markersize=4.2,
        color="#3b6ea8",
        alpha=0.82,
    )
    second.semilogy(
        center_turn[adaptive],
        residual[adaptive],
        "x",
        markersize=5.2,
        markeredgewidth=1.4,
        color="#c55a32",
    )
    second.axhline(1.0, color="#8b2f2f", linestyle="--", linewidth=1.0)
    second.set_xlabel("normalized contour turn")
    second.set_ylabel(r"$\|I-A(z_j)R_j\|_F$ upper bound")
    second.set_title("Exact-target residual recheck")
    second.grid(True, which="both", alpha=0.22)

    third = axes[0, 1]
    third.plot(
        leaf_turn[order_leaves],
        product[order_leaves],
        ".",
        markersize=3.1,
        color="#6b4c9a",
        alpha=0.85,
    )
    third.axhline(1.0, color="#8b2f2f", linestyle="--", linewidth=1.1)
    third.set_ylim(0.0, 1.035)
    third.set_ylabel("Neumann product upper bound")
    third.set_title("949-leaf exact rational cover")
    third.grid(True, alpha=0.22)

    fourth = axes[1, 1]
    fourth.semilogy(
        leaf_turn[order_leaves],
        budget_ratio[order_leaves],
        ".",
        markersize=3.1,
        color="#2c8c5a",
        alpha=0.85,
    )
    fourth.axhline(1.0, color="#8b2f2f", linestyle="--", linewidth=1.0)
    fourth.set_xlabel("normalized contour turn")
    fourth.set_ylabel("transported bound / RH-28 budget")
    fourth.set_title("Arcwise Rouché-budget margins")
    fourth.grid(True, which="both", alpha=0.22)

    for axis in axes[:, 0]:
        axis.set_xlim(0.0, 1.0)
    for axis in axes[:, 1]:
        axis.set_xlim(0.0, 1.0)
    figure.tight_layout(h_pad=2.0, w_pad=2.1)
    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    figure.savefig(output / "certified_resolvent_atlas.pdf", bbox_inches="tight")
    figure.savefig(
        output / "certified_resolvent_atlas.png",
        dpi=220,
        bbox_inches="tight",
    )
    plt.close(figure)


if __name__ == "__main__":
    main()
