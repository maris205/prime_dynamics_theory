"""Render the RH-45 trace-ideal and determinant summary figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "bulk_trace_norm_determinant_certificate.json"
PILOT = ROOT / "results" / "stored_bulk_square_determinants.json"
FIGURES = ROOT / "figures"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    certificate = load(CERTIFICATE)
    pilot = load(PILOT)
    ledgers = [
        certificate["dimension_ledgers"][key]
        for key in sorted(
            certificate["dimension_ledgers"], key=lambda value: int(value)
        )
    ]
    dimensions = np.asarray(
        [float(row["dimension"]) for row in ledgers], dtype=np.float64
    )
    full_hs = np.asarray(
        [row["full_bulk"]["bulk_hilbert_schmidt_error_upper"] for row in ledgers]
    )
    adaptive_hs = np.asarray(
        [
            row["adaptive_bulk"]["bulk_hilbert_schmidt_error_upper"]
            for row in ledgers
        ]
    )
    full_trace = np.asarray(
        [row["full_bulk"]["square_trace_norm_error_upper"] for row in ledgers]
    )
    adaptive_trace = np.asarray(
        [
            row["adaptive_bulk"]["square_trace_norm_error_upper"]
            for row in ledgers
        ]
    )

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "legend.fontsize": 9,
        }
    )
    figure, axes = plt.subplots(2, 2, figsize=(13.5, 9.8))

    axis = axes[0, 0]
    axis.loglog(dimensions, full_hs, "o-", label="full")
    axis.loglog(dimensions, adaptive_hs, "s--", label="adaptive")
    reference = full_hs[-1] * dimensions[-1] / dimensions
    axis.loglog(dimensions, reference, color="0.35", linestyle=":", label=r"$n^{-1}$")
    axis.set_xlabel(r"dimension $n$")
    axis.set_ylabel(r"upper bound for $\|B_n-B\|_{\mathrm{HS}}$")
    axis.set_title("(a) One-step Hilbert--Schmidt convergence")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()

    axis = axes[0, 1]
    axis.loglog(dimensions, full_trace, "o-", label="full")
    axis.loglog(dimensions, adaptive_trace, "s--", label="adaptive")
    reference = full_trace[-1] * dimensions[-1] / dimensions
    axis.loglog(dimensions, reference, color="0.35", linestyle=":", label=r"$n^{-1}$")
    axis.set_xlabel(r"dimension $n$")
    axis.set_ylabel(r"upper bound for $\|B_n^2-B^2\|_1$")
    axis.set_title("(b) Two-step trace-norm convergence")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()

    axis = axes[1, 0]
    styles = (("0.0001", "o-"), ("0.001", "s-"), ("0.01", "^-"))
    for radius, style in styles:
        values = np.asarray(
            [
                row["determinant_disk_bounds"][radius][
                    "full_fredholm_determinant_error_upper"
                ]
                for row in ledgers
            ]
        )
        axis.loglog(dimensions, values, style, label=rf"$|w|\leq {float(radius):g}$")
    axis.set_xlabel(r"dimension $n$")
    axis.set_ylabel("uniform determinant error upper")
    axis.set_title("(c) Rigorous Fredholm determinant disks")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()

    axis = axes[1, 1]
    radii = np.asarray(pilot["square_parameters"], dtype=np.float64)
    first = pilot["consecutive_absolute_differences"]["2048_to_4096"]
    second = pilot["consecutive_absolute_differences"]["4096_to_8192"]
    first_values = np.asarray([first[str(value)] for value in radii])
    second_values = np.asarray([second[str(value)] for value in radii])
    axis.loglog(radii, first_values, "o-", label=r"$2048\to4096$")
    axis.loglog(radii, second_values, "s-", label=r"$4096\to8192$")
    ratio = second_values / first_values
    axis.text(
        0.04,
        0.94,
        rf"mean ratio $={np.mean(ratio):.4f}$",
        transform=axis.transAxes,
        va="top",
        bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "0.7"},
    )
    axis.set_xlabel(r"square parameter $w$")
    axis.set_ylabel("consecutive absolute difference")
    axis.set_title("(d) Stored determinant pilot (floating)")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()

    figure.suptitle(
        "Bulk two-step trace ideals and determinant convergence at $\\sigma=10^{-2}$",
        fontsize=14,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    FIGURES.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        FIGURES / "bulk_two_step_trace_norm_determinant.png",
        dpi=220,
        bbox_inches="tight",
    )
    figure.savefig(
        FIGURES / "bulk_two_step_trace_norm_determinant.pdf",
        bbox_inches="tight",
    )
    plt.close(figure)


if __name__ == "__main__":
    main()
