"""Render the RH-37 block-scaling, spectrum, atlas, and product figure."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RH36 = ROOT.parent / "RH-36-nested-grid-physical-count"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    first = load(RH36 / "results" / "nested_block_certificate_sigma_1e-02.json")
    second = load(ROOT / "results" / "second_dyadic_block_certificate_sigma_1e-02.json")
    pilot = load(ROOT / "results" / "second_dyadic_spectrum_pilot_sigma_1e-02.json")
    atlas = load(ROOT / "results" / "propagated_resolvent_atlas.json")
    leaves = read_csv(ROOT / "results" / "propagated_resolvent_atlas_leaves.csv")

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "figure.dpi": 160,
        }
    )
    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.2), constrained_layout=True)

    names = [
        "coarse_consistency",
        "coarse_to_detail",
        "detail_to_coarse",
        "detail_block",
    ]
    labels = [r"$E$", r"$C$", r"$B$", r"$D$"]
    first_values = [
        first["block_certificates"][name]["block_two_norm_upper"] for name in names
    ]
    second_values = [
        second["block_certificates"][name]["block_two_norm_upper"] for name in names
    ]
    x = np.arange(len(names))
    width = 0.36
    axis = axes[0, 0]
    axis.bar(x - width / 2, first_values, width, label=r"$2048\to4096$")
    axis.bar(x + width / 2, second_values, width, label=r"$4096\to8192$")
    axis.set_yscale("log")
    axis.set_xticks(x, labels)
    axis.set_ylabel(r"certified $2$-norm upper")
    axis.set_title("(a) Certified block scaling")
    axis.legend(frameon=False)
    for index, (old, new) in enumerate(zip(first_values, second_values)):
        axis.text(index + width / 2, new * 1.18, f"{new / old:.3f}", ha="center", va="bottom")

    axis = axes[0, 1]
    theta = np.linspace(0.0, 2.0 * np.pi, 600)
    center = complex(pilot["contour_center_real"], pilot["contour_center_imag"])
    radius = float(pilot["contour_radius"])
    circle = center + radius * np.exp(1j * theta)
    axis.plot(circle.real, circle.imag, color="black", linewidth=1.0, label=r"$\Gamma$")
    for key, marker, color, label in (
        ("coarse_eigenvalues", "o", "tab:blue", r"$A_{4096}$"),
        ("fine_eigenvalues", "x", "tab:orange", r"$A_{8192}$"),
    ):
        values = pilot[key]
        axis.scatter(
            [row["real"] for row in values],
            [row["imag"] for row in values],
            s=20,
            marker=marker,
            color=color,
            linewidths=0.9,
            label=label,
        )
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlim(-0.62, 0.16)
    axis.set_ylim(-0.88, 0.52)
    axis.set_xlabel(r"$\Re z$")
    axis.set_ylabel(r"$\Im z$")
    axis.set_title("(b) Floating localization only")
    axis.legend(frameon=False, loc="upper left")

    turns = np.asarray([float(row["theta_midpoint"]) / (2.0 * np.pi) for row in leaves])
    coarse_bounds = np.asarray(
        [float(row["transported_coarse_resolvent_upper"]) for row in leaves]
    )
    fine_bounds = np.asarray([float(row["fine_resolvent_upper"]) for row in leaves])
    order = np.argsort(turns)
    axis = axes[1, 0]
    axis.plot(turns[order], coarse_bounds[order], linewidth=1.0, label=r"$A_{2048}$ transported")
    axis.plot(turns[order], fine_bounds[order], linewidth=1.0, label=r"$A_{4096}$ propagated")
    axis.axhline(
        second["continuation_gate"]["admissible_coarse_resolvent_upper"],
        color="black",
        linestyle="--",
        linewidth=0.9,
        label="second-level threshold",
    )
    axis.set_yscale("log")
    axis.set_xlabel("contour turn")
    axis.set_ylabel(r"resolvent upper bound")
    axis.set_title("(c) Hierarchical resolvent propagation")
    axis.legend(frameon=False, loc="upper right")

    first_products = np.asarray(
        [float(row["first_effective_product_upper"]) for row in leaves]
    )
    second_products = np.asarray(
        [float(row["second_continuation_product_upper"]) for row in leaves]
    )
    axis = axes[1, 1]
    axis.plot(turns[order], first_products[order], linewidth=1.0, label="first effective gate")
    axis.plot(turns[order], second_products[order], linewidth=1.0, label="second Rouch\'e gate")
    axis.axhline(1.0, color="black", linestyle="--", linewidth=0.9)
    axis.set_ylim(0.0, 1.04)
    axis.set_xlabel("contour turn")
    axis.set_ylabel("outward-rounded product")
    axis.set_title("(d) Both continuation gates close")
    axis.legend(frameon=False, loc="upper right")
    axis.text(
        0.02,
        0.04,
        rf"max second $={atlas['maximum_second_continuation_product_upper']:.6f}$",
        transform=axis.transAxes,
    )

    output_dir = ROOT / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_dir / "iterated_dyadic_physical_count.png", dpi=220)
    figure.savefig(output_dir / "iterated_dyadic_physical_count.pdf")
    plt.close(figure)


if __name__ == "__main__":
    main()
