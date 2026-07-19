"""Floating dyadic audit of the intrinsic peripheral Riesz defect.

The experiment builds one fine row-stochastic folded-Gaussian matrix and
then obtains every coarser matrix by exact orthogonal Haar compression.  For
an adjacent pair ``A_n = E_n A_{2n} E_n`` it compares

    Q_per(A_n)  and  E_n Q_per(A_{2n}) E_n.

Unlike a comparison of independently sampled midpoint matrices, this is an
exact finite-dimensional analogue of the intrinsic identification defect.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"
sys.path.insert(0, str(RH14 / "src"))
sys.path.insert(0, str(RH47 / "src"))
sys.path.insert(0, str(RH47 / "experiments"))
sys.path.insert(0, str(ROOT / "src"))

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from intrinsic_identification import (  # noqa: E402
    compress_factors,
    low_rank_difference_frobenius,
    low_rank_frobenius,
)
from run_peripheral_factor_pilot import resolve_factors  # noqa: E402


OUTPUT = ROOT / "results" / "dyadic_identification_pilot.json"
FULL_SIGMAS = (0.01, 0.004, 0.002, 0.001, 0.0005, 0.0002)
SMOKE_SIGMAS = (0.004, 0.001)
FINE_RESOLUTION = 40.96
LEVELS = 4


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def haar_compress_matrix(matrix: csr_matrix) -> csr_matrix:
    """Return the exact top-left Haar block of an even-dimensional matrix."""

    dimension = int(matrix.shape[0])
    if matrix.shape[1] != dimension or dimension % 2:
        raise ValueError("matrix must be square with even dimension")
    coarse_dimension = dimension // 2
    fine_indices = np.arange(dimension, dtype=np.int64)
    coarse_indices = fine_indices // 2
    restriction = csr_matrix(
        (
            np.full(dimension, 0.5, dtype=np.float64),
            (coarse_indices, fine_indices),
        ),
        shape=(coarse_dimension, dimension),
    )
    prolongation = csr_matrix(
        (
            np.ones(dimension, dtype=np.float64),
            (fine_indices, coarse_indices),
        ),
        shape=(dimension, coarse_dimension),
    )
    coarse = (restriction @ matrix @ prolongation).tocsr()
    coarse.sum_duplicates()
    coarse.eliminate_zeros()
    return coarse


def weighted_factors(data: dict[str, object]) -> tuple[np.ndarray, np.ndarray]:
    """Return factors for the Perron-plus-weighted-parity Riesz term."""

    dimension = np.asarray(data["perron_mass"]).size
    left = np.column_stack(
        (
            np.ones(dimension, dtype=np.float64),
            np.asarray(data["parity_right"], dtype=np.float64),
        )
    )
    right = np.column_stack(
        (
            np.asarray(data["perron_mass"], dtype=np.float64),
            float(data["parity_eigenvalue"])
            * np.asarray(data["parity_mass"], dtype=np.float64),
        )
    )
    return left, right


def branch_factors(
    data: dict[str, object], branch: str
) -> tuple[np.ndarray, np.ndarray]:
    dimension = np.asarray(data["perron_mass"]).size
    if branch == "perron":
        return (
            np.ones((dimension, 1), dtype=np.float64),
            np.asarray(data["perron_mass"], dtype=np.float64)[:, None],
        )
    if branch == "parity":
        return (
            np.asarray(data["parity_right"], dtype=np.float64)[:, None],
            (
                float(data["parity_eigenvalue"])
                * np.asarray(data["parity_mass"], dtype=np.float64)
            )[:, None],
        )
    raise ValueError(f"unknown branch: {branch}")


def defect(
    coarse: dict[str, object], fine: dict[str, object], branch: str
) -> dict[str, float]:
    if branch == "weighted_rank_two":
        coarse_left, coarse_right = weighted_factors(coarse)
        fine_left, fine_right = weighted_factors(fine)
    else:
        coarse_left, coarse_right = branch_factors(coarse, branch)
        fine_left, fine_right = branch_factors(fine, branch)
    ratio = fine_left.shape[0] // coarse_left.shape[0]
    lifted_left, lifted_right = compress_factors(
        fine_left, fine_right, ratio
    )
    value = low_rank_difference_frobenius(
        coarse_left,
        coarse_right,
        lifted_left,
        lifted_right,
    )
    coarse_norm = low_rank_frobenius(coarse_left, coarse_right)
    compressed_fine_norm = low_rank_frobenius(lifted_left, lifted_right)
    return {
        "defect_frobenius": value,
        "coarse_term_frobenius": coarse_norm,
        "compressed_fine_term_frobenius": compressed_fine_norm,
        "relative_to_coarse_term": value / coarse_norm,
    }


def level_record(
    sigma: float,
    matrix: csr_matrix,
    factors: dict[str, object],
    elapsed_seconds: float,
) -> dict[str, object]:
    dimension = int(matrix.shape[0])
    row_sums = np.asarray(matrix.sum(axis=1)).ravel()
    return {
        "sigma": float(sigma),
        "dimension": dimension,
        "dimension_times_sigma": dimension * float(sigma),
        "nonzeros": int(matrix.nnz),
        "maximum_row_sum_error": float(np.max(np.abs(row_sums - 1.0))),
        "parity_eigenvalue": float(factors["parity_eigenvalue"]),
        "bulk_radius_observed": float(factors["bulk_radius"]),
        "elapsed_seconds": float(elapsed_seconds),
    }


def fit_mesh_power(rows: list[dict[str, object]], field: str) -> dict[str, float]:
    x = np.log(
        np.asarray([float(row["coarse_dimension"]) for row in rows])
    )
    y = np.log(
        np.asarray([float(row[field]) for row in rows])
    )
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "power": float(slope),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


def run_sigma(sigma: float, fine_resolution: float, levels: int) -> dict[str, object]:
    fine_dimension = int(round(float(fine_resolution) / float(sigma)))
    divisor = 2 ** (int(levels) - 1)
    fine_dimension = max(divisor * 16, divisor * int(round(fine_dimension / divisor)))
    started = time.perf_counter()
    matrices = [sparse_folded_gaussian_matrix(fine_dimension, sigma)]
    for _ in range(1, levels):
        matrices.append(haar_compress_matrix(matrices[-1]))
    build_seconds = time.perf_counter() - started

    eigendata: list[dict[str, object]] = []
    level_rows: list[dict[str, object]] = []
    for matrix in matrices:
        level_started = time.perf_counter()
        factors = resolve_factors(matrix, sigma)
        elapsed = time.perf_counter() - level_started
        eigendata.append(factors)
        level_rows.append(level_record(sigma, matrix, factors, elapsed))

    adjacent_rows = []
    for fine_index in range(len(matrices) - 1):
        fine = eigendata[fine_index]
        coarse = eigendata[fine_index + 1]
        coarse_dimension = int(matrices[fine_index + 1].shape[0])
        epsilon = coarse_dimension ** -1 * sigma ** -1.5
        logarithm = math.log(1.0 / sigma)
        branches = {
            name: defect(coarse, fine, name)
            for name in ("perron", "parity", "weighted_rank_two")
        }
        weighted = float(branches["weighted_rank_two"]["defect_frobenius"])
        adjacent_rows.append(
            {
                "fine_dimension": int(matrices[fine_index].shape[0]),
                "coarse_dimension": coarse_dimension,
                "coarse_dimension_times_sigma": coarse_dimension * sigma,
                "raw_one_step_clock": epsilon,
                "quadratic_clock": epsilon**2,
                "quadratic_log_clock": epsilon**2 * logarithm,
                "weighted_defect_over_raw_clock": weighted / epsilon,
                "weighted_defect_over_quadratic_clock": weighted / epsilon**2,
                "weighted_defect_over_quadratic_log_clock": weighted
                / (epsilon**2 * logarithm),
                "branches": branches,
                "weighted_defect_frobenius": weighted,
            }
        )

    fits = {
        "weighted_rank_two": fit_mesh_power(
            adjacent_rows, "weighted_defect_frobenius"
        ),
        "perron": fit_mesh_power(
            [
                {
                    **row,
                    "branch_defect": row["branches"]["perron"][
                        "defect_frobenius"
                    ],
                }
                for row in adjacent_rows
            ],
            "branch_defect",
        ),
        "parity": fit_mesh_power(
            [
                {
                    **row,
                    "branch_defect": row["branches"]["parity"][
                        "defect_frobenius"
                    ],
                }
                for row in adjacent_rows
            ],
            "branch_defect",
        ),
    }
    result = {
        "sigma": float(sigma),
        "fine_resolution": fine_dimension * sigma,
        "matrix_build_and_compression_seconds": build_seconds,
        "levels": level_rows,
        "adjacent_identification_defects": adjacent_rows,
        "mesh_power_fits": fits,
    }
    del matrices, eigendata
    gc.collect()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--fine-resolution", type=float, default=FINE_RESOLUTION)
    parser.add_argument("--levels", type=int, default=LEVELS)
    args = parser.parse_args()
    if args.levels < 3:
        raise ValueError("at least three nested levels are required")
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    rows = []
    for sigma in sigmas:
        row = run_sigma(sigma, args.fine_resolution, args.levels)
        rows.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)

    source_path = RH14 / "src" / "parity_boundary" / "operators.py"
    payload = {
        "status": "floating_exact_dyadic_intrinsic_identification_audit",
        "evidence_level": "binary64_sparse_exact_Haar_compression_not_validated",
        "fine_resolution_target": float(args.fine_resolution),
        "nested_levels": int(args.levels),
        "source": {
            "path": str(source_path.relative_to(REPOSITORY)),
            "sha256": sha256_file(source_path),
        },
        "rows": rows,
        "limitations": [
            "Every adjacent defect is exact for the displayed finite fine matrix and its orthogonal Haar top-left block, up to binary64 eigensolver error.",
            "The finest sparse matrix uses an eight-sigma cutoff and exact row renormalization.",
            "The audit is not an interval enclosure and does not upper-bound an infinite-dimensional reduced resolvent.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "dyadic_identification_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
