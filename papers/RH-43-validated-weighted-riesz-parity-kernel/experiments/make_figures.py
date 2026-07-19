"""Render the validated intrinsic parity-kernel summary figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
CERTIFICATE = ROOT / "results" / "validated_weighted_parity_kernel.json"
SNAPSHOT = (
    PAPERS
    / "RH-36-nested-grid-physical-count"
    / "results"
    / "nested_grid_snapshot_sigma_1e-02.npz"
)


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    certificate = load(CERTIFICATE)
    with np.load(SNAPSHOT) as data:
        right = np.asarray(data["fine_right_modes"][:, 1])
        left = np.asarray(data["fine_left_modes"][:, 1])
        eigenvalue = float(data["fine_peripheral_values"][1])
    dimension = right.size
    indices = np.linspace(0, dimension - 1, 256, dtype=int)
    center_kernel = eigenvalue * np.outer(
        right[indices], dimension * left[indices]
    )

    figure, axes = plt.subplots(2, 2, figsize=(13.5, 10.0))
    axis = axes[0, 0]
    maximum = float(np.max(np.abs(center_kernel)))
    image = axis.imshow(
        center_kernel,
        origin="lower",
        extent=(0.0, 1.0, 0.0, 1.0),
        cmap="coolwarm",
        norm=TwoSlopeNorm(vmin=-maximum, vcenter=0.0, vmax=maximum),
        aspect="auto",
    )
    figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    axis.set_xlabel("target $y$")
    axis.set_ylabel("source $x$")
    axis.set_title("(a) Archived 4096 center for the intrinsic parity kernel")

    axis = axes[0, 1]
    levels = ("2048", "4096", "8192")
    correction = certificate["stored_factor_validation"]["levels"]
    weighted_errors = [
        correction[level]["weighted_term_error_upper"] for level in levels
    ]
    matrix_corrections = [
        correction[level]["correction_norm_upper"] for level in levels
    ]
    xvalues = np.arange(len(levels))
    axis.semilogy(
        xvalues,
        weighted_errors,
        marker="o",
        linewidth=2.0,
        label="actual $Q$ vs stored factor",
    )
    axis.semilogy(
        xvalues,
        matrix_corrections,
        marker="s",
        linewidth=2.0,
        label="block-diagonalizing correction",
    )
    axis.set_xticks(xvalues, levels)
    axis.set_ylabel("rigorous Euclidean upper")
    axis.set_title("(b) Three stored parity factors are genuine spectral terms")
    axis.grid(True, which="both", alpha=0.3)
    axis.legend(frameon=False)

    axis = axes[1, 0]
    order = (
        "coarse_consistency",
        "coarse_to_detail",
        "detail_to_coarse",
        "detail_block",
    )
    labels = ("$E$", "$C$", "$B$", "$D$")
    ratios = certificate["stored_parity_haar_law"]["actual_spectral_ratios"]
    centers = np.array(
        [(ratios[name]["lower"] + ratios[name]["upper"]) / 2 for name in order]
    )
    lower = np.array([ratios[name]["lower"] for name in order])
    upper = np.array([ratios[name]["upper"] for name in order])
    axis.errorbar(
        np.arange(4),
        centers,
        yerr=np.vstack((centers - lower, upper - centers)),
        fmt="o",
        capsize=5,
        linewidth=2.0,
        color="#4c72b0",
        label="validated actual spectral ratio",
    )
    targets = np.array([0.25, 0.5, 0.5, 0.25])
    axis.scatter(
        np.arange(4),
        targets,
        marker="x",
        s=90,
        linewidths=2.0,
        color="#dd8452",
        label="smooth-kernel target",
    )
    axis.set_xticks(np.arange(4), labels)
    axis.set_ylim(0.22, 0.53)
    axis.set_ylabel("second transition / first transition")
    axis.set_title("(c) The quarter--half Haar law is now spectral")
    axis.grid(True, axis="y", alpha=0.3)
    axis.legend(frameon=False, loc="center right")

    axis = axes[1, 1]
    old_values = np.array([266.6496824500989, 838.2106715223996, 838.2106716588748])
    new_family = certificate["improved_uniform_matrix_family"]
    new_values = np.array(
        [
            certificate["continuum_complement_schur"][
                "improved_continuum_L2_resolvent_upper"
            ],
            new_family["uniform_full_resolvent_upper"],
            new_family["uniform_fixed_and_adaptive_sparse_resolvent_upper"],
        ]
    )
    positions = np.arange(3)
    width = 0.36
    axis.bar(positions - width / 2, old_values, width, label="RH-42")
    axis.bar(positions + width / 2, new_values, width, label="RH-43")
    axis.set_xticks(positions, ("continuum", "full", "sparse"))
    axis.set_ylabel("uniform Euclidean resolvent upper")
    axis.set_title("(d) Complement Schur halves the stable all-grid threshold")
    axis.text(
        0.98,
        0.95,
        "$n_0: 131072 \\to 65536$",
        transform=axis.transAxes,
        ha="right",
        va="top",
        fontsize=12,
        bbox={
            "facecolor": "white",
            "alpha": 0.85,
            "edgecolor": "none",
        },
    )
    axis.grid(True, axis="y", alpha=0.3)
    axis.legend(frameon=False)

    figure.tight_layout()
    output = ROOT / "figures" / "validated_weighted_parity_kernel"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output.with_suffix(".png"), dpi=220)
    figure.savefig(output.with_suffix(".pdf"))
    plt.close(figure)


if __name__ == "__main__":
    main()
