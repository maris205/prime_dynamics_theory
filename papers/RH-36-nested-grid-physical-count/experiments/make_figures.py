"""Generate the RH-36 publication figure from archived results."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def read_csv(name: str):
    with (ROOT / "results" / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    pilot = load("fine_spectrum_pilot_sigma_1e-02.json")
    block = load("nested_block_certificate_sigma_1e-02.json")
    atlas = load("physical_resolvent_atlas.json")
    centers = read_csv("physical_resolvent_centers.csv")
    leaves = read_csv("physical_resolvent_atlas_leaves.csv")
    with np.load(ROOT / "results" / "nested_grid_snapshot_sigma_1e-02.npz") as data:
        singular = {
            name: np.asarray(data[f"{name}_singular_values"])
            for name in (
                "coarse_consistency",
                "coarse_to_detail",
                "detail_to_coarse",
                "detail_block",
            )
        }

    plt.rcParams.update(
        {
            "font.size": 9.5,
            "axes.titlesize": 10.5,
            "axes.labelsize": 9.5,
            "legend.fontsize": 8.2,
            "figure.dpi": 150,
        }
    )
    figure, axes = plt.subplots(2, 2, figsize=(10.8, 7.7))

    axis = axes[0, 0]
    center = complex(
        pilot["contour_center_real"], pilot["contour_center_imag"]
    )
    radius = float(pilot["contour_radius"])
    theta = np.linspace(0.0, 2.0 * np.pi, 800)
    circle = center + radius * np.exp(1j * theta)
    axis.plot(circle.real, circle.imag, color="black", lw=1.25, label=r"$\Gamma$")
    coarse_values = np.asarray(
        [complex(row["real"], row["imag"]) for row in pilot["coarse_eigenvalues"]]
    )
    fine_values = np.asarray(
        [complex(row["real"], row["imag"]) for row in pilot["fine_eigenvalues"]]
    )
    axis.scatter(
        coarse_values.real,
        coarse_values.imag,
        s=22,
        facecolors="none",
        edgecolors="#1f77b4",
        linewidths=1.0,
        label=r"$A_{2048}$ (floating)",
    )
    axis.scatter(
        fine_values.real,
        fine_values.imag,
        s=13,
        color="#d62728",
        alpha=0.78,
        label=r"$A_{4096}$ (floating)",
    )
    axis.set_xlabel(r"$\operatorname{Re} z$")
    axis.set_ylabel(r"$\operatorname{Im} z$")
    axis.set_title("(a) Sparse spectral localization")
    axis.set_aspect("equal", adjustable="box")
    axis.grid(alpha=0.22)
    axis.legend(loc="lower right")

    axis = axes[0, 1]
    labels = {
        "coarse_consistency": r"$a-A_c$",
        "coarse_to_detail": r"$c$",
        "detail_to_coarse": r"$b$",
        "detail_block": r"$d$",
    }
    colors = {
        "coarse_consistency": "#9467bd",
        "coarse_to_detail": "#ff7f0e",
        "detail_to_coarse": "#2ca02c",
        "detail_block": "#8c564b",
    }
    for name, values in singular.items():
        axis.semilogy(
            np.arange(1, values.size + 1),
            values,
            lw=1.45,
            color=colors[name],
            label=labels[name],
        )
        certified = block["block_certificates"][name]["block_two_norm_upper"]
        axis.scatter([1], [certified], color=colors[name], s=20, zorder=4)
    axis.set_xlabel("stored low-rank index")
    axis.set_ylabel("singular value / certified upper")
    axis.set_title("(b) Ninety-six-channel block compression")
    axis.grid(alpha=0.22, which="both")
    axis.legend(ncol=2)

    axis = axes[1, 0]
    center_theta = np.asarray(
        [
            2.0
            * np.pi
            * float(Fraction(int(row["turn_numerator"]), int(row["turn_denominator"])))
            for row in centers
        ]
    )
    center_bounds = np.asarray(
        [float(row["center_inverse_two_norm_upper"]) for row in centers]
    )
    order = np.argsort(center_theta)
    axis.semilogy(
        center_theta[order],
        center_bounds[order],
        ".",
        ms=4.2,
        color="#1f77b4",
        label="rigorous center bound",
    )
    axis.axhline(
        block["continuation_gate"]["admissible_coarse_resolvent_upper"],
        color="black",
        ls="--",
        lw=1.1,
        label="theorem threshold",
    )
    axis.axhline(
        atlas["atlas_resolvent_budget_lower"],
        color="#d62728",
        ls=":",
        lw=1.2,
        label="0.9 safety budget",
    )
    axis.set_xlim(0.0, 2.0 * np.pi)
    axis.set_xlabel(r"contour angle $\theta$")
    axis.set_ylabel(r"resolvent upper bound")
    axis.set_title("(c) Coarse physical resolvent atlas")
    axis.grid(alpha=0.22, which="both")
    axis.legend()

    axis = axes[1, 1]
    leaf_theta = np.asarray([float(row["theta_midpoint"]) for row in leaves])
    products = np.asarray(
        [float(row["continuation_product_upper"]) for row in leaves]
    )
    order = np.argsort(leaf_theta)
    axis.plot(
        leaf_theta[order], products[order], ".", ms=4.0, color="#d62728"
    )
    axis.axhline(1.0, color="black", ls="--", lw=1.1, label="Rouché gate")
    axis.axhline(0.9, color="#1f77b4", ls=":", lw=1.1, label="archive target")
    axis.set_xlim(0.0, 2.0 * np.pi)
    axis.set_ylim(0.0, 1.04)
    axis.set_xlabel(r"contour angle $\theta$")
    axis.set_ylabel(r"$\|(z-A_c)^{-1}\|\,\varepsilon$")
    axis.set_title("(d) Nested-grid continuation product")
    axis.grid(alpha=0.22)
    axis.legend(loc="lower right")
    axis.text(
        0.03,
        0.94,
        rf"max $={atlas['maximum_continuation_product_upper']:.6f}$",
        transform=axis.transAxes,
        va="top",
    )

    figure.tight_layout()
    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    figure.savefig(output / "nested_grid_physical_count.pdf", bbox_inches="tight")
    figure.savefig(
        output / "nested_grid_physical_count.png", bbox_inches="tight", dpi=220
    )
    plt.close(figure)


if __name__ == "__main__":
    main()
