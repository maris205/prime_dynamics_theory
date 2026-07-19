"""Render the validated rank-two peripheral-complement summary figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
CERTIFICATE = (
    ROOT / "results" / "validated_rank_two_peripheral_complement.json"
)
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
        right = np.asarray(data["fine_right_modes"][:, :2])
        left = np.asarray(data["fine_left_modes"][:, :2])
        eigenvalues = np.asarray(data["fine_peripheral_values"][:2])
    dimension = right.shape[0]
    indices = np.linspace(0, dimension - 1, 256, dtype=int)
    center_kernel = (
        right[indices]
        @ np.diag(eigenvalues)
        @ (dimension * left[indices]).T
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
    axis.set_title("(a) Archived 4096 center for the rank-two kernel")

    axis = axes[0, 1]
    levels = ("2048", "4096", "8192")
    perron = certificate["stored_perron_factor_validation"]["levels"]
    parity_path = (
        PAPERS
        / "RH-43-validated-weighted-riesz-parity-kernel"
        / "results"
        / "validated_weighted_parity_kernel.json"
    )
    parity = load(parity_path)["stored_factor_validation"]["levels"]
    perron_errors = [perron[level]["weighted_term_error_upper"] for level in levels]
    parity_errors = [parity[level]["weighted_term_error_upper"] for level in levels]
    combined_errors = [
        certificate["stored_rank_two_haar_law"]["combined_factor_errors"][
            level
        ]
        for level in levels
    ]
    xvalues = np.arange(len(levels))
    axis.semilogy(
        xvalues,
        perron_errors,
        marker="o",
        linewidth=2.0,
        label="Perron spectral factor",
    )
    axis.semilogy(
        xvalues,
        parity_errors,
        marker="s",
        linewidth=2.0,
        label="parity spectral factor",
    )
    axis.semilogy(
        xvalues,
        combined_errors,
        marker="^",
        linewidth=2.0,
        label="rank-two sum",
    )
    axis.set_xticks(xvalues, levels)
    axis.set_ylabel("rigorous weighted-term error upper")
    axis.set_title("(b) Both stored peripheral factors are spectral")
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
    ratios = certificate["stored_rank_two_haar_law"][
        "actual_spectral_ratios"
    ]
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
        label="validated rank-two spectral ratio",
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
    axis.set_title("(c) The rank-two quarter--half law is spectral")
    axis.grid(True, axis="y", alpha=0.3)
    axis.legend(frameon=False, loc="center right")

    axis = axes[1, 1]
    perron_continuum = certificate["perron_continuum_contour"]
    family = certificate["uniform_perron_and_rank_two_families"]
    parity_certificate = load(parity_path)
    parity_family = parity_certificate["improved_uniform_matrix_family"]
    perron_values = np.array(
        [
            perron_continuum["continuum_L2_resolvent_upper"],
            family["uniform_perron_full_resolvent_upper"],
            family[
                "uniform_perron_fixed_and_adaptive_sparse_resolvent_upper"
            ],
        ]
    )
    parity_values = np.array(
        [
            parity_certificate["continuum_complement_schur"][
                "improved_continuum_L2_resolvent_upper"
            ],
            parity_family["uniform_full_resolvent_upper"],
            parity_family["uniform_fixed_and_adaptive_sparse_resolvent_upper"],
        ]
    )
    positions = np.arange(3)
    width = 0.36
    axis.bar(positions - width / 2, perron_values, width, label="Perron contour")
    axis.bar(positions + width / 2, parity_values, width, label="parity contour")
    axis.set_xticks(positions, ("continuum", "full", "sparse"))
    axis.set_ylabel("uniform Euclidean resolvent upper")
    axis.set_title("(d) The union contour inherits the parity threshold")
    axis.set_ylim(0.0, 320.0)
    axis.text(
        0.98,
        0.95,
        "$n_0=65536$\nrank-two cutoff $<9.28\\times10^{-10}$",
        transform=axis.transAxes,
        ha="right",
        va="top",
        fontsize=11,
        bbox={"facecolor": "white", "alpha": 0.88, "edgecolor": "none"},
    )
    axis.grid(True, axis="y", alpha=0.3)
    axis.legend(frameon=False)

    figure.tight_layout()
    output = ROOT / "figures" / "validated_rank_two_peripheral_complement"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output.with_suffix(".png"), dpi=220)
    figure.savefig(output.with_suffix(".pdf"))
    plt.close(figure)


if __name__ == "__main__":
    main()
