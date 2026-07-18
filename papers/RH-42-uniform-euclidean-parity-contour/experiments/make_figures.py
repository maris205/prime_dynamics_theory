"""Render the uniform Euclidean parity-contour certificate."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from euclidean_contour import (  # noqa: E402
    adaptive_multiple,
    relaxed_cutoff_defect,
)


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    certificate = load(
        ROOT / "results" / "uniform_euclidean_parity_certificate.json"
    )
    pilot = load(ROOT / "results" / "hilbert_constants_pilot.json")
    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "figure.dpi": 160,
        }
    )
    figure, axes = plt.subplots(
        2, 2, figsize=(10.5, 7.4), constrained_layout=True
    )

    axis = axes[0, 0]
    labels = ["stored", "midpoint", "G4096"]
    values = [
        certificate["stored_euclidean_theorem"][
            "contour_resolvent_upper"
        ],
        certificate["stored_to_exact_midpoint_4096"][
            "neumann_transfer"
        ]["transferred_resolvent_upper"],
        certificate["midpoint_to_galerkin_4096"][
            "neumann_transfer"
        ]["transferred_resolvent_upper"],
    ]
    steps = certificate["dyadic_hilbert_galerkin_steps"]
    for key in sorted(
        steps, key=lambda value: int(value.split("_to_")[0])
    ):
        fine = key.split("_to_")[1]
        labels.append(f"G{fine}")
        values.append(
            steps[key]["resolvent_step"]["fine_resolvent_upper"]
        )
    labels.extend(
        [
            "$L^2$ cont.",
            "mid. family",
            "full Markov",
            "adaptive",
        ]
    )
    family = certificate["uniform_matrix_family"]
    values.extend(
        [
            certificate["continuum_L2_conclusion"][
                "contour_resolvent_upper"
            ],
            family["exact_midpoint_transfer"][
                "transferred_resolvent_upper"
            ],
            family["uniform_full_matrix_resolvent_upper"],
            family["uniform_adaptive_sparse_resolvent_upper"],
        ]
    )
    positions = np.arange(len(values))
    axis.plot(positions, values, marker="o", color="tab:purple")
    axis.fill_between(
        positions, 0.0, values, color="tab:purple", alpha=0.08
    )
    axis.set_xticks(positions, labels, rotation=42, ha="right")
    axis.tick_params(axis="x", labelsize=7)
    axis.set_ylabel(r"rigorous Euclidean/$L^2$ resolvent upper")
    axis.set_title("(a) Resolvent control survives every Hilbert-space lift")
    axis.grid(axis="y", color="0.9", linewidth=0.7)

    axis = axes[0, 1]
    gates = certificate["gate_summary"]
    gate_labels = [
        "stored→\nmidpoint",
        "midpoint→\nGalerkin",
        "max Schur",
        "Galerkin→\ncontinuum",
        "continuum→\nfamily",
        "normalizer",
        "cutoff",
    ]
    products = np.asarray(
        [
            gates["stored_to_midpoint_product_upper"],
            gates["midpoint_to_galerkin_product_upper"],
            gates["maximum_dyadic_schur_product_upper"],
            gates["continuum_product_upper"],
            gates["midpoint_family_product_upper"],
            gates["normalization_product_upper"],
            gates["cutoff_product_upper"],
        ]
    )
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(products)))
    bars = axis.bar(
        np.arange(len(products)), products, color=colors, alpha=0.88
    )
    axis.set_yscale("log")
    axis.set_ylim(products.min() / 5.0, 2.0)
    axis.axhline(
        1.0,
        color="black",
        linestyle="--",
        linewidth=1.0,
        label="Neumann/Schur threshold",
    )
    axis.set_xticks(
        np.arange(len(products)), gate_labels, rotation=32, ha="right"
    )
    axis.tick_params(axis="x", labelsize=7)
    axis.set_ylabel("rigorous product upper")
    axis.set_title("(b) All seven nonnormal transfer gates close")
    axis.legend(frameon=False, loc="lower left")
    for bar, value in zip(bars, products, strict=True):
        inside = value > 1.0e-2
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            value / 2.2 if inside else value * 1.45,
            f"{value:.2e}",
            ha="center",
            va="center" if inside else "bottom",
            fontsize=7,
            rotation=0 if inside else 22,
            color="white" if inside else "black",
        )

    axis = axes[1, 0]
    names = [
        "kernel",
        "source\nfirst",
        "target\nfirst",
        "source\nsecond",
        "mixed",
        "target\nsecond",
        "$xxyy$\ncoarse",
    ]
    envelope = certificate["hilbert_schmidt_envelope"]
    constants = np.asarray(
        [
            envelope["kernel"],
            envelope["source_first"],
            envelope["target_first"],
            envelope["source_second"],
            envelope["source_target"],
            envelope["target_second"],
            envelope["source_second_target_second"],
        ]
    )
    pilot_values = pilot["hilbert_schmidt_norms"]
    pilot_constants = np.asarray(
        [
            pilot_values["kernel"],
            pilot_values["source_first"],
            pilot_values["target_first"],
            pilot_values["source_second"],
            pilot_values["source_target"],
            pilot_values["target_second"],
            np.nan,
        ]
    )
    axis.bar(
        np.arange(len(constants)),
        constants,
        color="tab:blue",
        alpha=0.75,
        label="rigorous Arb upper",
    )
    axis.scatter(
        np.arange(len(constants)),
        pilot_constants,
        marker="x",
        s=34,
        color="black",
        label="floating quadrature",
        zorder=3,
    )
    axis.set_yscale("log")
    axis.set_xticks(np.arange(len(constants)), names)
    axis.set_ylabel("Hilbert--Schmidt norm")
    axis.set_title("(c) Closed target integrals reduce validation to one dimension")
    axis.legend(frameon=False)

    axis = axes[1, 1]
    dimensions = np.asarray([2**power for power in range(17, 35)])
    fixed = np.asarray(
        [
            relaxed_cutoff_defect(int(n), 0.01, 8.0).spectral_norm_upper
            for n in dimensions
        ]
    )
    adaptive = np.asarray(
        [
            relaxed_cutoff_defect(
                int(n), 0.01, adaptive_multiple(int(n), 8.0)
            ).spectral_norm_upper
            for n in dimensions
        ]
    )
    axis.loglog(
        dimensions,
        fixed,
        marker="o",
        markersize=3,
        label="fixed eight-sigma upper",
    )
    axis.loglog(
        dimensions,
        adaptive,
        marker="s",
        markersize=3,
        label=r"$\max\{8,2\sqrt{\log n}\}$",
    )
    axis.axvline(
        np.exp(16.0),
        color="0.45",
        linestyle=":",
        linewidth=1.0,
        label="growth crossover",
    )
    axis.set_xlabel("dimension $n$")
    axis.set_ylabel("Euclidean cutoff defect upper")
    axis.set_title("(d) Fixed width is uniformly tiny; adaptive growth restores decay")
    axis.grid(which="both", color="0.92", linewidth=0.6)
    axis.legend(frameon=False)

    output_dir = ROOT / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output_dir / "uniform_euclidean_parity_contour.png", dpi=220
    )
    figure.savefig(
        output_dir / "uniform_euclidean_parity_contour.pdf"
    )
    plt.close(figure)


if __name__ == "__main__":
    main()
