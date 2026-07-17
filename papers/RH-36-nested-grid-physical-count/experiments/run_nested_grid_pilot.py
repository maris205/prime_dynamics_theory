"""Floating nested-grid perturbation pilot for RH-36.

The pilot compares the stored physical two-step operator on a coarse
midpoint grid with the corresponding operator on an integer refinement.
The coarse operator is lifted isometrically by piecewise-constant
prolongation and extended by zero on the fine-grid detail space.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse.linalg import LinearOperator, svds


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
sys.path.insert(0, str(RH24 / "experiments"))

import run_contour_feshbach_audit as rh24  # noqa: E402


def bulk_actions(matrix, spectrum):
    """Return the stored Perron/parity-extracted two-step action and adjoint."""

    right = np.asarray(spectrum["right_modes"])
    left = np.asarray(spectrum["left_modes"])
    values = np.asarray(spectrum["peripheral_values"])

    def one_step(source: np.ndarray) -> np.ndarray:
        array = np.asarray(source)
        coefficients = left.T @ array
        if array.ndim == 1:
            correction = right @ (values * coefficients)
        else:
            correction = right @ (values[:, None] * coefficients)
        return matrix @ array - correction

    def one_step_adjoint(source: np.ndarray) -> np.ndarray:
        array = np.asarray(source)
        coefficients = right.T @ array
        if array.ndim == 1:
            correction = left @ (values * coefficients)
        else:
            correction = left @ (values[:, None] * coefficients)
        return matrix.T @ array - correction

    def two_step(source: np.ndarray) -> np.ndarray:
        return one_step(one_step(source))

    def two_step_adjoint(source: np.ndarray) -> np.ndarray:
        return one_step_adjoint(one_step_adjoint(source))

    return two_step, two_step_adjoint


def prolong(source: np.ndarray, factor: int) -> np.ndarray:
    array = np.asarray(source)
    scale = np.sqrt(float(factor))
    if array.ndim == 1:
        return np.repeat(array, factor) / scale
    return np.repeat(array, factor, axis=0) / scale


def restrict(source: np.ndarray, factor: int) -> np.ndarray:
    array = np.asarray(source)
    scale = np.sqrt(float(factor))
    if array.ndim == 1:
        return array.reshape(-1, factor).sum(axis=1) / scale
    return array.reshape(-1, factor, array.shape[1]).sum(axis=1) / scale


def detail(source: np.ndarray, factor: int) -> np.ndarray:
    array = np.asarray(source)
    return array - prolong(restrict(array, factor), factor)


def largest_singular_value(
    shape: tuple[int, int],
    action,
    adjoint,
    *,
    tolerance: float,
    maxiter: int,
) -> tuple[float, float]:
    operator = LinearOperator(
        shape,
        matvec=action,
        rmatvec=adjoint,
        dtype=np.float64,
    )
    begun = time.perf_counter()
    values = svds(
        operator,
        k=1,
        which="LM",
        return_singular_vectors=False,
        tol=float(tolerance),
        maxiter=int(maxiter),
        random_state=1729,
    )
    return float(values[-1]), time.perf_counter() - begun


def leading_singular_values(
    shape: tuple[int, int],
    action,
    adjoint,
    *,
    rank: int,
    tolerance: float,
    maxiter: int,
) -> tuple[np.ndarray, float]:
    operator = LinearOperator(
        shape,
        matvec=action,
        rmatvec=adjoint,
        dtype=np.float64,
    )
    selected = min(int(rank), min(shape) - 1)
    begun = time.perf_counter()
    values = svds(
        operator,
        k=selected,
        which="LM",
        return_singular_vectors=False,
        tol=float(tolerance),
        maxiter=int(maxiter),
        random_state=2718,
    )
    return np.sort(np.asarray(values))[::-1], time.perf_counter() - begun


def materialized_norm_candidates(
    shape: tuple[int, int], action, *, chunk_size: int
) -> tuple[dict[str, float], float]:
    """Accumulate Frobenius, one, infinity, and Schur norm candidates."""

    rows, columns = shape
    total = 0.0
    maximum_column_sum = 0.0
    row_sums = np.zeros(rows, dtype=np.float64)
    begun = time.perf_counter()
    for start in range(0, columns, int(chunk_size)):
        stop = min(start + int(chunk_size), columns)
        source = np.zeros((columns, stop - start), dtype=np.float64)
        source[np.arange(start, stop), np.arange(stop - start)] = 1.0
        image = np.asarray(action(source))
        if image.shape != (rows, stop - start):
            raise RuntimeError("block action returned an incompatible shape")
        absolute = np.abs(image)
        total += float(np.sum(absolute**2))
        maximum_column_sum = max(
            maximum_column_sum, float(np.max(np.sum(absolute, axis=0)))
        )
        row_sums += np.sum(absolute, axis=1)
    infinity_norm = float(np.max(row_sums))
    return (
        {
            "frobenius_norm_candidate": float(np.sqrt(total)),
            "one_norm_candidate": maximum_column_sum,
            "infinity_norm_candidate": infinity_norm,
            "schur_two_norm_upper_candidate": float(
                np.sqrt(maximum_column_sum * infinity_norm)
            ),
        },
        time.perf_counter() - begun,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--coarse-dimension", type=int, default=2048)
    parser.add_argument("--factor", type=int, default=2)
    parser.add_argument("--tolerance", type=float, default=1.0e-10)
    parser.add_argument("--maxiter", type=int, default=4000)
    parser.add_argument("--frobenius-chunk-size", type=int, default=256)
    parser.add_argument("--singular-rank", type=int, default=24)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    sigma = float(arguments.sigma)
    coarse_dimension = int(arguments.coarse_dimension)
    factor = int(arguments.factor)
    fine_dimension = factor * coarse_dimension
    constants = rh24.critical_constants(130)

    begun = time.perf_counter()
    coarse_matrix = rh24.sparse_folded_gaussian_matrix(
        coarse_dimension, sigma, u=float(constants.u)
    )
    coarse_spectrum = rh24.resolve_peripheral_modes(coarse_matrix)
    coarse_build_seconds = time.perf_counter() - begun

    begun = time.perf_counter()
    fine_matrix = rh24.sparse_folded_gaussian_matrix(
        fine_dimension, sigma, u=float(constants.u)
    )
    fine_spectrum = rh24.resolve_peripheral_modes(fine_matrix)
    fine_build_seconds = time.perf_counter() - begun

    coarse, coarse_adjoint = bulk_actions(coarse_matrix, coarse_spectrum)
    fine, fine_adjoint = bulk_actions(fine_matrix, fine_spectrum)

    def lifted_coarse(source: np.ndarray) -> np.ndarray:
        return prolong(coarse(restrict(source, factor)), factor)

    def lifted_coarse_adjoint(source: np.ndarray) -> np.ndarray:
        return prolong(coarse_adjoint(restrict(source, factor)), factor)

    def difference(source: np.ndarray) -> np.ndarray:
        return fine(source) - lifted_coarse(source)

    def difference_adjoint(source: np.ndarray) -> np.ndarray:
        return fine_adjoint(source) - lifted_coarse_adjoint(source)

    def coarse_consistency(source: np.ndarray) -> np.ndarray:
        return restrict(fine(prolong(source, factor)), factor) - coarse(source)

    def coarse_consistency_adjoint(source: np.ndarray) -> np.ndarray:
        return (
            restrict(fine_adjoint(prolong(source, factor)), factor)
            - coarse_adjoint(source)
        )

    def coarse_to_detail(source: np.ndarray) -> np.ndarray:
        return detail(fine(prolong(source, factor)), factor)

    def coarse_to_detail_adjoint(source: np.ndarray) -> np.ndarray:
        return restrict(fine_adjoint(detail(source, factor)), factor)

    def detail_to_coarse(source: np.ndarray) -> np.ndarray:
        return restrict(fine(detail(source, factor)), factor)

    def detail_to_coarse_adjoint(source: np.ndarray) -> np.ndarray:
        return detail(fine_adjoint(prolong(source, factor)), factor)

    def detail_block(source: np.ndarray) -> np.ndarray:
        return detail(fine(detail(source, factor)), factor)

    def detail_block_adjoint(source: np.ndarray) -> np.ndarray:
        return detail(fine_adjoint(detail(source, factor)), factor)

    tolerance = float(arguments.tolerance)
    maxiter = int(arguments.maxiter)
    estimates = {}
    for name, shape, action, adjoint in (
        (
            "full_lift_difference",
            (fine_dimension, fine_dimension),
            difference,
            difference_adjoint,
        ),
        (
            "coarse_consistency",
            (coarse_dimension, coarse_dimension),
            coarse_consistency,
            coarse_consistency_adjoint,
        ),
        (
            "coarse_to_detail",
            (fine_dimension, coarse_dimension),
            coarse_to_detail,
            coarse_to_detail_adjoint,
        ),
        (
            "detail_to_coarse",
            (coarse_dimension, fine_dimension),
            detail_to_coarse,
            detail_to_coarse_adjoint,
        ),
        (
            "detail_block",
            (fine_dimension, fine_dimension),
            detail_block,
            detail_block_adjoint,
        ),
    ):
        value, seconds = largest_singular_value(
            shape,
            action,
            adjoint,
            tolerance=tolerance,
            maxiter=maxiter,
        )
        estimates[name] = {
            "largest_singular_value_candidate": value,
            "seconds": seconds,
        }
        print(f"{name}: {value:.16e} ({seconds:.2f} s)", flush=True)

    for name, shape, action in (
        ("full_lift_difference", (fine_dimension, fine_dimension), difference),
        (
            "coarse_consistency",
            (coarse_dimension, coarse_dimension),
            coarse_consistency,
        ),
        (
            "coarse_to_detail",
            (fine_dimension, coarse_dimension),
            coarse_to_detail,
        ),
        (
            "detail_to_coarse",
            (coarse_dimension, fine_dimension),
            detail_to_coarse,
        ),
        ("detail_block", (fine_dimension, fine_dimension), detail_block),
    ):
        norms, seconds = materialized_norm_candidates(
            shape,
            action,
            chunk_size=int(arguments.frobenius_chunk_size),
        )
        estimates[name].update(norms)
        estimates[name]["materialization_seconds"] = seconds
        print(
            f"{name} Frobenius/Schur: "
            f"{norms['frobenius_norm_candidate']:.16e} / "
            f"{norms['schur_two_norm_upper_candidate']:.16e} "
            f"({seconds:.2f} s)",
            flush=True,
        )

    action_ledger = {
        "coarse_consistency": (
            (coarse_dimension, coarse_dimension),
            coarse_consistency,
            coarse_consistency_adjoint,
        ),
        "coarse_to_detail": (
            (fine_dimension, coarse_dimension),
            coarse_to_detail,
            coarse_to_detail_adjoint,
        ),
        "detail_to_coarse": (
            (coarse_dimension, fine_dimension),
            detail_to_coarse,
            detail_to_coarse_adjoint,
        ),
        "detail_block": (
            (fine_dimension, fine_dimension),
            detail_block,
            detail_block_adjoint,
        ),
    }
    for name, (shape, action, adjoint) in action_ledger.items():
        values, seconds = leading_singular_values(
            shape,
            action,
            adjoint,
            rank=int(arguments.singular_rank),
            tolerance=tolerance,
            maxiter=maxiter,
        )
        frobenius = estimates[name]["frobenius_norm_candidate"]
        tail = float(
            np.sqrt(max(frobenius**2 - float(np.sum(values**2)), 0.0))
        )
        estimates[name]["leading_singular_values"] = [
            float(value) for value in values
        ]
        estimates[name]["post_rank_frobenius_tail_candidate"] = tail
        estimates[name]["leading_singular_seconds"] = seconds
        print(
            f"{name} rank-{values.size} tail: {tail:.16e} "
            f"({seconds:.2f} s)",
            flush=True,
        )

    payload = {
        "status": "floating_nested_grid_physical_count_pilot",
        "evidence_level": "floating_not_validated",
        "sigma": sigma,
        "coarse_dimension": coarse_dimension,
        "fine_dimension": fine_dimension,
        "refinement_factor": factor,
        "coarse_peripheral_values": [
            float(value) for value in coarse_spectrum["peripheral_values"]
        ],
        "fine_peripheral_values": [
            float(value) for value in fine_spectrum["peripheral_values"]
        ],
        "coarse_build_seconds": coarse_build_seconds,
        "fine_build_seconds": fine_build_seconds,
        "svds_tolerance": tolerance,
        "svds_maxiter": maxiter,
        "estimates": estimates,
    }
    output = arguments.output
    if output is None:
        output = ROOT / "results" / "nested_grid_pilot_sigma_1e-02.json"
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
