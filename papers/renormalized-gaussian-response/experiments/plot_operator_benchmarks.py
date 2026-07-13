#!/usr/bin/env python3
"""Plot cost scaling and fixed-sigma resonance convergence."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=Path("results/operator_benchmarks.csv"))
    parser.add_argument("--json", type=Path, default=Path("results/operator_benchmarks.json"))
    parser.add_argument("--figure", type=Path, default=Path("figures/operator_scaling.pdf"))
    args = parser.parse_args()

    with args.csv.open() as handle:
        rows = list(csv.DictReader(handle))
    with args.json.open() as handle:
        details = json.load(handle)["dimensions"]

    d = np.array([int(row["d"]) for row in rows], dtype=float)
    memory_mib = np.array([float(row["bytes_per_matrix"]) for row in rows]) / 2.0**20
    build = np.array([float(row["build_seconds_three_matrices"]) for row in rows])
    matvec = np.array([float(row["median_matvec_seconds"]) for row in rows])
    eigen = np.array([float(row["eigs_seconds"]) for row in rows])

    eigenvalues = np.array(
        [complex(*details[str(int(value))]["response"]["eigenvalue"]) for value in d]
    )
    phase_derivatives = np.array(
        [details[str(int(value))]["response"]["analytic_phase_derivative"] for value in d]
    )
    eigen_error = np.abs(eigenvalues[:-1] - eigenvalues[-1])
    phase_error = np.abs(phase_derivatives[:-1] - phase_derivatives[-1])

    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.35))

    axes[0].loglog(d, memory_mib, "o-", label="measured CSR")
    axes[0].loglog(d, memory_mib[0] * (d / d[0]) ** 2, "--", label=r"$d^2$ guide")
    axes[0].set_xlabel(r"grid dimension $d$")
    axes[0].set_ylabel("MiB per matrix")
    axes[0].set_title("Fixed-width storage")
    axes[0].legend(frameon=False)

    axes[1].loglog(d, build, "o-", label=r"build $K,K',K''$")
    axes[1].loglog(d, eigen, "s-", label="12 ARPACK modes")
    axes[1].loglog(d, matvec, "^-", label="one matvec")
    axes[1].set_xlabel(r"grid dimension $d$")
    axes[1].set_ylabel("seconds")
    axes[1].set_title("Measured runtime")
    axes[1].legend(frameon=False)

    axes[2].loglog(d[:-1], eigen_error, "o-", label=r"$|\lambda_d-\lambda_{50000}|$")
    axes[2].loglog(d[:-1], phase_error, "s-", label=r"$|\theta'_d-\theta'_{50000}|$")
    guide = eigen_error[0] * (d[:-1] / d[0]) ** (-2)
    axes[2].loglog(d[:-1], guide, "--", label=r"$d^{-2}$ guide")
    axes[2].set_xlabel(r"grid dimension $d$")
    axes[2].set_ylabel("difference from finest grid")
    axes[2].set_title("Resonance response convergence")
    axes[2].legend(frameon=False, fontsize=8)

    for axis in axes:
        axis.grid(alpha=0.25, which="both")
    fig.tight_layout()
    args.figure.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.figure)
    fig.savefig(args.figure.with_suffix(".png"), dpi=180)


if __name__ == "__main__":
    main()
