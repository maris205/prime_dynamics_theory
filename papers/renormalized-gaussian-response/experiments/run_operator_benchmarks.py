#!/usr/bin/env python3
"""Multiresolution sparse-kernel, resonance, and response benchmark."""

from __future__ import annotations

import argparse
import csv
import json
import platform
import resource
import time
from pathlib import Path

import numpy as np
import psutil
from scipy.sparse.linalg import ArpackNoConvergence, eigs

from gaussian_response.operator import FixedSupportGaussianFamily


def max_row_sum_error(matrix, target: float) -> float:
    row_sums = np.asarray(matrix.sum(axis=1)).ravel()
    return float(np.max(np.abs(row_sums - target)))


def sparse_infinity_norm(matrix) -> float:
    return float(np.max(np.asarray(abs(matrix).sum(axis=1)).ravel()))


def sorted_eigensystem(matrix, count: int, tolerance: float):
    try:
        values, vectors = eigs(
            matrix,
            k=count,
            which="LM",
            tol=tolerance,
            maxiter=30_000,
        )
    except ArpackNoConvergence as error:
        values = error.eigenvalues
        vectors = error.eigenvectors
        if values is None or vectors is None or len(values) < 4:
            raise
    order = np.argsort(-np.abs(values))
    return values[order], vectors[:, order]


def complex_pair(value: complex) -> list[float]:
    return [float(np.real(value)), float(np.imag(value))]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimensions", nargs="+", type=int, default=[2000, 5000, 10000])
    parser.add_argument("--sigma", type=float, default=0.00785)
    parser.add_argument("--u-critical", type=float, default=1.5437)
    parser.add_argument("--cutoff", type=float, default=6.0)
    parser.add_argument("--eigenvalues", type=int, default=12)
    parser.add_argument("--eigen-tolerance", type=float, default=1.0e-9)
    parser.add_argument("--response-step", type=float, default=2.0e-6)
    parser.add_argument("--matvec-repetitions", type=int, default=7)
    parser.add_argument("--output", type=Path, default=Path("results/operator_benchmarks.csv"))
    parser.add_argument("--details", type=Path, default=Path("results/operator_benchmarks.json"))
    args = parser.parse_args()

    process = psutil.Process()
    rng = np.random.default_rng(20260713)
    rows: list[dict[str, float | int | str]] = []
    details: dict[str, object] = {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "logical_cpus": psutil.cpu_count(logical=True),
        "physical_cpus": psutil.cpu_count(logical=False),
        "total_memory_bytes": psutil.virtual_memory().total,
        "parameters": vars(args) | {"output": str(args.output), "details": str(args.details)},
        "dimensions": {},
    }

    for d in args.dimensions:
        rss_before = process.memory_info().rss
        family = FixedSupportGaussianFamily(
            d=d,
            sigma=args.sigma,
            u_ref=args.u_critical,
            cutoff=args.cutoff,
            parameter_radius=2.0 * args.response_step,
        )
        (kernel, first, second), stats = family.build_with_stats(args.u_critical)
        rss_after_build = process.memory_info().rss

        tail = family.tail_mass_diagnostic(args.u_critical)
        vector = rng.standard_normal(d)
        kernel @ vector
        matvec_times = []
        for _ in range(args.matvec_repetitions):
            start = time.perf_counter()
            kernel @ vector
            matvec_times.append(time.perf_counter() - start)

        eigen_start = time.perf_counter()
        values, right_vectors = sorted_eigensystem(
            kernel, args.eigenvalues, args.eigen_tolerance
        )
        eigen_seconds = time.perf_counter() - eigen_start
        residuals = [
            np.linalg.norm(kernel @ right_vectors[:, index] - values[index] * right_vectors[:, index])
            for index in range(len(values))
        ]

        left_start = time.perf_counter()
        left_values, left_vectors = sorted_eigensystem(
            kernel.transpose().tocsr(), args.eigenvalues, args.eigen_tolerance
        )
        left_seconds = time.perf_counter() - left_start

        candidates = [
            index for index, value in enumerate(values)
            if value.imag > 1.0e-7 and abs(value) < 0.9999999
        ]
        response: dict[str, object] = {}
        if candidates:
            branch_index = candidates[0]
            eigenvalue = values[branch_index]
            right = right_vectors[:, branch_index]
            left_index = int(np.argmin(np.abs(left_values - np.conj(eigenvalue))))
            left = left_vectors[:, left_index]
            pairing_error = abs(left_values[left_index] - np.conj(eigenvalue))
            overlap = np.vdot(left, right)
            analytic = np.vdot(left, first @ right) / overlap

            plus = family.matrix(args.u_critical + args.response_step)
            minus = family.matrix(args.u_critical - args.response_step)
            plus_values, _ = sorted_eigensystem(plus, args.eigenvalues, args.eigen_tolerance)
            minus_values, _ = sorted_eigensystem(minus, args.eigenvalues, args.eigen_tolerance)
            plus_value = plus_values[int(np.argmin(np.abs(plus_values - eigenvalue)))]
            minus_value = minus_values[int(np.argmin(np.abs(minus_values - eigenvalue)))]
            finite = (plus_value - minus_value) / (2.0 * args.response_step)
            analytic_phase = float(np.imag(analytic / eigenvalue))
            finite_phase = float(
                np.angle(plus_value / minus_value) / (2.0 * args.response_step)
            )
            response = {
                "eigenvalue": complex_pair(eigenvalue),
                "left_pairing_error": float(pairing_error),
                "left_right_overlap_abs": float(abs(overlap)),
                "analytic_eigenvalue_derivative": complex_pair(analytic),
                "finite_difference_eigenvalue_derivative": complex_pair(finite),
                "relative_eigenvalue_response_error": float(
                    abs(analytic - finite) / max(abs(analytic), np.finfo(float).eps)
                ),
                "analytic_phase_derivative": analytic_phase,
                "finite_difference_phase_derivative": finite_phase,
                "relative_phase_response_error": float(
                    abs(analytic_phase - finite_phase)
                    / max(abs(analytic_phase), np.finfo(float).eps)
                ),
            }

        row = {
            "d": d,
            "nnz": stats.nnz,
            "density": stats.density,
            "bytes_per_matrix": stats.bytes_per_matrix,
            "build_seconds_three_matrices": stats.elapsed_seconds,
            "median_matvec_seconds": float(np.median(matvec_times)),
            "eigs_seconds": eigen_seconds,
            "left_eigs_seconds": left_seconds,
            "rss_increment_bytes": rss_after_build - rss_before,
            "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024),
            "K_row_sum_error": max_row_sum_error(kernel, 1.0),
            "K1_row_sum_error": max_row_sum_error(first, 0.0),
            "K2_row_sum_error": max_row_sum_error(second, 0.0),
            "K1_infinity_norm": sparse_infinity_norm(first),
            "K2_infinity_norm": sparse_infinity_norm(second),
            "maximum_omitted_mass": tail["maximum_omitted_mass"],
            "maximum_truncation_l1_error": tail["maximum_l1_error"],
            "maximum_eigen_residual": float(max(residuals)),
            "response_relative_error": response.get("relative_eigenvalue_response_error", ""),
            "phase_response_relative_error": response.get("relative_phase_response_error", ""),
        }
        rows.append(row)
        details["dimensions"][str(d)] = {
            "summary": row,
            "eigenvalues": [complex_pair(value) for value in values],
            "eigen_residuals": [float(value) for value in residuals],
            "response": response,
        }
        print(json.dumps(row, indent=2))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    args.details.parent.mkdir(parents=True, exist_ok=True)
    with args.details.open("w") as handle:
        json.dump(details, handle, indent=2)


if __name__ == "__main__":
    main()
