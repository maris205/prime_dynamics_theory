"""Render the validated parity-continuum contour certificate."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH40 = PAPERS / "RH-40-weighted-riesz-projector-bridge"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    certificate = load(
        ROOT / "results" / "validated_parity_continuum_certificate.json"
    )
    coarse = load(ROOT / "results" / "coarse_grushin_contour_certificate.json")
    midpoint = load(
        ROOT / "results" / "stored_to_midpoint_bridge_certificate.json"
    )
    pilot = load(
        RH40 / "results" / "weighted_projector_pilot_sigma_1e-02.json"
    )
    spectrum = pilot["levels"]["4096"]["leading_spectrum"]
    values = np.asarray(
        [complex(float(row["real"]), float(row["imag"])) for row in spectrum]
    )
    center = float(certificate["contour"]["center"])
    radius = float(certificate["contour"]["radius"])
    angles = np.linspace(0.0, 2.0 * np.pi, 500)
    circle = center + radius * np.exp(1.0j * angles)

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "figure.dpi": 160,
        }
    )
    figure, axes = plt.subplots(2, 2, figsize=(10.4, 7.4), constrained_layout=True)

    axis = axes[0, 0]
    axis.scatter(values.real, values.imag, s=24, color="tab:blue", label="stored leading spectrum")
    axis.plot(circle.real, circle.imag, color="tab:red", linewidth=1.5, label="validated contour")
    axis.axhline(0.0, color="0.75", linewidth=0.8)
    axis.axvline(0.0, color="0.75", linewidth=0.8)
    axis.set_xlim(-1.1, 1.08)
    axis.set_ylim(-0.78, 0.78)
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlabel(r"$\operatorname{Re}z$")
    axis.set_ylabel(r"$\operatorname{Im}z$")
    axis.set_title("(a) A certified circle isolates the negative resonance")
    axis.legend(frameon=False, loc="lower right")
    inset = inset_axes(axis, width="43%", height="43%", loc="upper center", borderpad=1.0)
    inset.scatter(values.real, values.imag, s=18, color="tab:blue")
    inset.fill(circle.real, circle.imag, color="tab:red", alpha=0.08)
    inset.plot(circle.real, circle.imag, color="tab:red", linewidth=1.2)
    inset.scatter([center], [0.0], marker="x", s=36, color="black")
    inset.set_xlim(center - 0.06, center + 0.065)
    inset.set_ylim(-0.06, 0.06)
    inset.tick_params(labelsize=7)
    mark_inset(axis, inset, loc1=2, loc2=4, fc="none", ec="0.55", linewidth=0.7)

    axis = axes[0, 1]
    gates = certificate["gate_summary"]
    names = ["stored→Galerkin", "Schur 1", "Schur 2", "Galerkin→continuum"]
    products = np.asarray(
        [
            gates["stored_to_galerkin_neumann_product_upper"],
            gates["first_schur_product_upper"],
            gates["second_schur_product_upper"],
            gates["continuum_neumann_product_upper"],
        ]
    )
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    bars = axis.bar(np.arange(4), products, color=colors, alpha=0.84)
    axis.axhline(1.0, color="black", linestyle="--", linewidth=1.0, label="Neumann threshold")
    axis.set_xticks(np.arange(4), names, rotation=15, ha="right")
    axis.set_ylim(0.0, 1.08)
    axis.set_ylabel("rigorous product upper")
    axis.set_title("(b) Every transfer gate remains below one")
    axis.bar_label(bars, labels=[f"{value:.4f}" for value in products], padding=3, fontsize=8)
    axis.legend(frameon=False, loc="upper left")

    axis = axes[1, 0]
    first = certificate["dyadic_galerkin_steps"]["4096_to_8192"]["resolvent_step"]
    second = certificate["dyadic_galerkin_steps"]["8192_to_16384"]["resolvent_step"]
    bridge = certificate["stored_to_galerkin_4096"]["neumann_transfer"]
    continuum = certificate["galerkin_to_continuum"]
    labels = [
        "stored\n4096",
        "Galerkin\n4096",
        "Galerkin\n8192",
        "Galerkin\n16384",
        "finite-rank\noperator",
        "continuum",
    ]
    bounds = np.asarray(
        [
            certificate["coarse_stored_theorem"]["contour_resolvent_upper"],
            bridge["transferred_resolvent_upper"],
            first["fine_resolvent_upper"],
            second["fine_resolvent_upper"],
            continuum["finite_rank_operator_resolvent_upper"],
            certificate["continuum_conclusion"]["contour_resolvent_upper"],
        ]
    )
    axis.plot(np.arange(len(bounds)), bounds, marker="o", color="tab:purple")
    axis.fill_between(np.arange(len(bounds)), 0.0, bounds, color="tab:purple", alpha=0.08)
    axis.set_xticks(np.arange(len(bounds)), labels)
    axis.set_ylabel(r"rigorous $L^\infty$ resolvent upper")
    axis.set_title("(c) Resolvent control survives the continuum lift")
    axis.grid(axis="y", color="0.9", linewidth=0.7)

    axis = axes[1, 1]
    scales = np.asarray(
        [
            coarse["residual_infinity_upper"],
            midpoint["maximum_total_row_l1_difference_upper"],
            certificate["stored_to_galerkin_4096"][
                "midpoint_to_cell_average_galerkin_upper"
            ],
            certificate["galerkin_to_continuum"]["operator_norm_defect_upper"],
        ]
    )
    scale_names = ["Grushin\nresidual", "stored→\nmidpoint", "midpoint→\nGalerkin", "Galerkin→\ncontinuum"]
    axis.bar(np.arange(4), scales, color=colors, alpha=0.84)
    axis.set_yscale("log")
    axis.set_xticks(np.arange(4), scale_names)
    axis.set_ylabel("rigorous defect upper")
    axis.set_title("(d) Algebraic, finite-grid, and continuum errors are separated")
    axis.set_ylim(scales.min() / 2.0, scales.max() * 4.0)
    for index, value in enumerate(scales):
        axis.text(index, value * 1.35, f"{value:.2e}", ha="center", va="bottom", fontsize=8)

    output_dir = ROOT / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_dir / "validated_parity_continuum_contour.png", dpi=220)
    figure.savefig(output_dir / "validated_parity_continuum_contour.pdf")
    plt.close(figure)


if __name__ == "__main__":
    main()
