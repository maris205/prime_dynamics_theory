#!/usr/bin/env python3
"""Second-order extrapolation of fixed-width resonance data from the prior layer."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    paper_dir = Path(__file__).resolve().parents[1]
    default_source = (
        paper_dir.parent
        / "renormalized-gaussian-response"
        / "results"
        / "operator_benchmarks.json"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=default_source)
    parser.add_argument("--minimum-fit-d", type=int, default=5000)
    parser.add_argument("--csv", type=Path, default=Path("results/spectral_extrapolation.csv"))
    parser.add_argument("--json", type=Path, default=Path("results/spectral_extrapolation.json"))
    parser.add_argument("--figure", type=Path, default=Path("figures/spectral_extrapolation.pdf"))
    args = parser.parse_args()

    with args.source.open() as handle:
        source = json.load(handle)["dimensions"]
    dimensions = np.array(sorted(int(value) for value in source), dtype=float)
    h = 2.0 / dimensions
    eigenvalues = np.array(
        [complex(*source[str(int(d))]["response"]["eigenvalue"]) for d in dimensions]
    )
    phase_derivatives = np.array(
        [source[str(int(d))]["response"]["analytic_phase_derivative"] for d in dimensions]
    )
    fit = dimensions >= args.minimum_fit_d
    design = np.column_stack((np.ones(np.count_nonzero(fit)), h[fit] ** 2))

    coefficients = {}
    for name, values in (
        ("real", eigenvalues.real),
        ("imag", eigenvalues.imag),
        ("phase_derivative", phase_derivatives),
    ):
        coefficients[name] = np.linalg.lstsq(design, values[fit], rcond=None)[0]
    continuum_eigenvalue = complex(coefficients["real"][0], coefficients["imag"][0])
    continuum_phase_derivative = float(coefficients["phase_derivative"][0])
    eigenvalue_errors = np.abs(eigenvalues - continuum_eigenvalue)
    phase_errors = np.abs(phase_derivatives - continuum_phase_derivative)

    rows = []
    for index, d in enumerate(dimensions.astype(int)):
        rows.append(
            {
                "d": d,
                "h": h[index],
                "eigenvalue_real": eigenvalues[index].real,
                "eigenvalue_imag": eigenvalues[index].imag,
                "phase_derivative": phase_derivatives[index],
                "eigenvalue_error_to_extrapolation": eigenvalue_errors[index],
                "phase_error_to_extrapolation": phase_errors[index],
            }
        )
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    try:
        source_label = str(args.source.resolve().relative_to(paper_dir.parent))
    except ValueError:
        source_label = str(args.source)
    metadata = {
        "source": source_label,
        "minimum_fit_dimension": args.minimum_fit_d,
        "continuum_eigenvalue": [continuum_eigenvalue.real, continuum_eigenvalue.imag],
        "continuum_phase_derivative": continuum_phase_derivative,
        "fit_coefficients_in_1_h2": {
            name: [float(value) for value in coefficient]
            for name, coefficient in coefficients.items()
        },
    }
    with args.json.open("w") as handle:
        json.dump(metadata, handle, indent=2)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.35))
    axes[0].loglog(dimensions, eigenvalue_errors, "o-", label="resonance error")
    axes[0].loglog(
        dimensions,
        eigenvalue_errors[0] * (dimensions / dimensions[0]) ** (-2),
        "--",
        label=r"$d^{-2}$ guide",
    )
    axes[0].set_xlabel(r"dimension $d$")
    axes[0].set_ylabel(r"$|\lambda_d-\lambda_\infty^{\rm fit}|$")
    axes[0].set_title("Isolated resonance")
    axes[0].legend(frameon=False)

    axes[1].loglog(dimensions, phase_errors, "s-", label="phase-response error")
    axes[1].loglog(
        dimensions,
        phase_errors[0] * (dimensions / dimensions[0]) ** (-2),
        "--",
        label=r"$d^{-2}$ guide",
    )
    axes[1].set_xlabel(r"dimension $d$")
    axes[1].set_ylabel(r"$|\theta'_d-(\theta')_\infty^{\rm fit}|$")
    axes[1].set_title("Derivative of eigenphase")
    axes[1].legend(frameon=False)
    for axis in axes:
        axis.grid(alpha=0.25, which="both")
    fig.tight_layout()
    args.figure.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.figure)
    fig.savefig(args.figure.with_suffix(".png"), dpi=180)

    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
