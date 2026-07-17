"""Floating 4096-to-8192 nested-grid pilot for RH-37."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator, svds


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
sys.path[:0] = [str(RH24 / "src"), str(RH24 / "experiments")]

import run_contour_feshbach_audit as rh24  # noqa: E402


def sparse_from_snapshot(data, prefix: str) -> csr_matrix:
    shape = tuple(int(value) for value in data[f"{prefix}_shape"])
    return csr_matrix(
        (
            np.asarray(data[f"{prefix}_data"]),
            np.asarray(data[f"{prefix}_indices"]),
            np.asarray(data[f"{prefix}_indptr"]),
        ),
        shape=shape,
    )


def spectrum_from_snapshot(data, prefix: str) -> dict[str, np.ndarray]:
    return {
        "right_modes": np.asarray(data[f"{prefix}_right_modes"]),
        "left_modes": np.asarray(data[f"{prefix}_left_modes"]),
        "peripheral_values": np.asarray(data[f"{prefix}_peripheral_values"]),
    }


def bulk_actions(matrix, spectrum):
    right = np.asarray(spectrum["right_modes"])
    left = np.asarray(spectrum["left_modes"])
    values = np.asarray(spectrum["peripheral_values"])
    weighted_right = right * values[None, :]

    def one_step(source):
        array = np.asarray(source)
        return matrix @ array - weighted_right @ (left.T @ array)

    def one_step_adjoint(source):
        array = np.asarray(source)
        return matrix.T @ array - left @ (weighted_right.T @ array)

    return (
        lambda source: one_step(one_step(source)),
        lambda source: one_step_adjoint(one_step_adjoint(source)),
    )


def prolong(source):
    return np.repeat(np.asarray(source), 2, axis=0)


def detail_injection(source):
    array = np.asarray(source)
    result = np.empty((2 * array.shape[0],) + array.shape[1:], dtype=array.dtype)
    result[0::2] = array
    result[1::2] = -array
    return result


def restrict(source):
    array = np.asarray(source)
    return 0.5 * (array[0::2] + array[1::2])


def detail_restriction(source):
    array = np.asarray(source)
    return 0.5 * (array[0::2] - array[1::2])


def block_actions(name, coarse, coarse_adjoint, fine, fine_adjoint):
    if name == "coarse_consistency":
        return (
            lambda x: restrict(fine(prolong(x))) - coarse(x),
            lambda x: restrict(fine_adjoint(prolong(x))) - coarse_adjoint(x),
        )
    if name == "coarse_to_detail":
        return (
            lambda x: detail_restriction(fine(prolong(x))),
            lambda x: restrict(fine_adjoint(detail_injection(x))),
        )
    if name == "detail_to_coarse":
        return (
            lambda x: restrict(fine(detail_injection(x))),
            lambda x: detail_restriction(fine_adjoint(prolong(x))),
        )
    if name == "detail_block":
        return (
            lambda x: detail_restriction(fine(detail_injection(x))),
            lambda x: detail_restriction(fine_adjoint(detail_injection(x))),
        )
    raise ValueError(name)


def materialized_norms(dimension: int, action, chunk_size: int):
    total = 0.0
    row_sums = np.zeros(dimension, dtype=np.float64)
    maximum_column_sum = 0.0
    begun = time.perf_counter()
    for start in range(0, dimension, int(chunk_size)):
        stop = min(start + int(chunk_size), dimension)
        source = np.zeros((dimension, stop - start), dtype=np.float64)
        source[np.arange(start, stop), np.arange(stop - start)] = 1.0
        values = np.abs(np.asarray(action(source)))
        total += float(np.sum(values**2))
        row_sums += np.sum(values, axis=1)
        maximum_column_sum = max(
            maximum_column_sum, float(np.max(np.sum(values, axis=0)))
        )
    infinity = float(np.max(row_sums))
    return {
        "frobenius_norm_candidate": float(np.sqrt(total)),
        "one_norm_candidate": maximum_column_sum,
        "infinity_norm_candidate": infinity,
        "schur_two_norm_upper_candidate": float(
            np.sqrt(maximum_column_sum * infinity)
        ),
        "materialization_seconds": time.perf_counter() - begun,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank", type=int, default=96)
    parser.add_argument("--chunk-size", type=int, default=128)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    inherited_snapshot = (
        RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
    )
    with np.load(inherited_snapshot) as data:
        sigma = float(data["sigma"])
        coarse_matrix = sparse_from_snapshot(data, "fine_matrix").copy()
        coarse_spectrum = {
            key: value.copy()
            for key, value in spectrum_from_snapshot(data, "fine").items()
        }
    coarse_dimension = int(coarse_matrix.shape[0])
    fine_dimension = 2 * coarse_dimension
    constants = rh24.critical_constants(130)
    begun = time.perf_counter()
    fine_matrix = rh24.sparse_folded_gaussian_matrix(
        fine_dimension, sigma, u=float(constants.u)
    )
    fine_spectrum = rh24.resolve_peripheral_modes(fine_matrix)
    fine_build_seconds = time.perf_counter() - begun

    coarse, coarse_adjoint = bulk_actions(coarse_matrix, coarse_spectrum)
    fine, fine_adjoint = bulk_actions(fine_matrix, fine_spectrum)
    results = {}
    for name in (
        "coarse_consistency",
        "coarse_to_detail",
        "detail_to_coarse",
        "detail_block",
    ):
        action, adjoint = block_actions(
            name, coarse, coarse_adjoint, fine, fine_adjoint
        )
        operator = LinearOperator(
            (coarse_dimension, coarse_dimension),
            matvec=action,
            rmatvec=adjoint,
            dtype=np.float64,
        )
        begun = time.perf_counter()
        singular_values = svds(
            operator,
            k=int(arguments.rank),
            which="LM",
            return_singular_vectors=False,
            tol=1.0e-11,
            maxiter=10000,
            random_state=161803,
        )
        singular_values = np.sort(singular_values)[::-1]
        svd_seconds = time.perf_counter() - begun
        materialized = materialized_norms(
            coarse_dimension, action, int(arguments.chunk_size)
        )
        tail = float(
            np.sqrt(
                max(
                    materialized["frobenius_norm_candidate"] ** 2
                    - float(np.sum(singular_values**2)),
                    0.0,
                )
            )
        )
        results[name] = {
            **materialized,
            "leading_singular_values": [
                float(value) for value in singular_values
            ],
            "largest_singular_value_candidate": float(singular_values[0]),
            "post_rank_frobenius_tail_candidate": tail,
            "svd_seconds": svd_seconds,
        }
        print(
            f"{name}: s1={singular_values[0]:.16e}, "
            f"tail={tail:.3e}",
            flush=True,
        )

    payload = {
        "status": "floating_second_dyadic_nested_grid_pilot",
        "evidence_level": "floating_not_validated",
        "sigma": sigma,
        "coarse_dimension": coarse_dimension,
        "fine_dimension": fine_dimension,
        "approximation_rank": int(arguments.rank),
        "fine_build_seconds": fine_build_seconds,
        "coarse_peripheral_values": [
            float(value) for value in coarse_spectrum["peripheral_values"]
        ],
        "fine_peripheral_values": [
            float(value) for value in fine_spectrum["peripheral_values"]
        ],
        "blocks": results,
    }
    output = arguments.output
    if output is None:
        output = ROOT / "results" / "second_dyadic_pilot_sigma_1e-02.json"
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
