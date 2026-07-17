"""Build the exact stored factor snapshot and low-rank proof centers."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy
from scipy.sparse.linalg import LinearOperator, svds


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
sys.path[:0] = [
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402


def sha256_array(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).view(np.uint8)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bulk_actions(matrix, spectrum):
    right = np.asarray(spectrum["right_modes"])
    left = np.asarray(spectrum["left_modes"])
    values = np.asarray(spectrum["peripheral_values"])

    def one_step(source):
        array = np.asarray(source)
        coefficients = left.T @ array
        correction = right @ (
            values * coefficients
            if array.ndim == 1
            else values[:, None] * coefficients
        )
        return matrix @ array - correction

    def one_step_adjoint(source):
        array = np.asarray(source)
        coefficients = right.T @ array
        correction = left @ (
            values * coefficients
            if array.ndim == 1
            else values[:, None] * coefficients
        )
        return matrix.T @ array - correction

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


def sorted_svd(operator, rank: int):
    left, values, right_h = svds(
        operator,
        k=int(rank),
        which="LM",
        tol=1.0e-11,
        maxiter=8000,
        random_state=314159,
    )
    order = np.argsort(values)[::-1]
    return left[:, order], values[order], right_h[order, :]


def add_sparse(payload: dict[str, np.ndarray], prefix: str, matrix) -> None:
    csr = matrix.tocsr(copy=False)
    payload[f"{prefix}_data"] = np.asarray(csr.data)
    payload[f"{prefix}_indices"] = np.asarray(csr.indices)
    payload[f"{prefix}_indptr"] = np.asarray(csr.indptr)
    payload[f"{prefix}_shape"] = np.asarray(csr.shape, dtype=np.int64)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--coarse-dimension", type=int, default=2048)
    parser.add_argument("--rank", type=int, default=96)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    sigma = float(arguments.sigma)
    dimension = int(arguments.coarse_dimension)
    fine_dimension = 2 * dimension
    settings = rh24.physical_settings()[sigma]
    if int(settings["dimension"]) != dimension:
        raise ValueError("the coarse dimension must match the RH-35 stored scale")

    begun = time.perf_counter()
    coarse_environment = rh25_global.build_environment(sigma, settings)
    constants = rh24.critical_constants(130)
    fine_matrix = rh24.sparse_folded_gaussian_matrix(
        fine_dimension, sigma, u=float(constants.u)
    )
    fine_spectrum = rh24.resolve_peripheral_modes(fine_matrix)
    build_seconds = time.perf_counter() - begun

    coarse_spectrum = coarse_environment["spectrum"]
    coarse, coarse_adjoint = bulk_actions(
        coarse_environment["matrix"], coarse_spectrum
    )
    fine, fine_adjoint = bulk_actions(fine_matrix, fine_spectrum)
    arrays: dict[str, np.ndarray] = {
        "sigma": np.asarray(sigma, dtype=np.float64),
        "critical_u": np.asarray(float(constants.u), dtype=np.float64),
        "coarse_dimension": np.asarray(dimension, dtype=np.int64),
        "fine_dimension": np.asarray(fine_dimension, dtype=np.int64),
        "approximation_rank": np.asarray(int(arguments.rank), dtype=np.int64),
        "coarse_right_modes": np.asarray(coarse_spectrum["right_modes"]),
        "coarse_left_modes": np.asarray(coarse_spectrum["left_modes"]),
        "coarse_peripheral_values": np.asarray(
            coarse_spectrum["peripheral_values"]
        ),
        "coarse_synthesis": np.asarray(coarse_environment["synthesis"]),
        "coarse_analysis": np.asarray(coarse_environment["analysis"]),
        "fine_right_modes": np.asarray(fine_spectrum["right_modes"]),
        "fine_left_modes": np.asarray(fine_spectrum["left_modes"]),
        "fine_peripheral_values": np.asarray(
            fine_spectrum["peripheral_values"]
        ),
    }
    add_sparse(arrays, "coarse_matrix", coarse_environment["matrix"])
    add_sparse(arrays, "fine_matrix", fine_matrix)

    svd_seconds = {}
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
            (dimension, dimension),
            matvec=action,
            rmatvec=adjoint,
            dtype=np.float64,
        )
        started = time.perf_counter()
        left, values, right_h = sorted_svd(operator, int(arguments.rank))
        svd_seconds[name] = time.perf_counter() - started
        arrays[f"{name}_left"] = left
        arrays[f"{name}_singular_values"] = values
        arrays[f"{name}_right_adjoint"] = right_h
        print(
            f"{name}: s1={values[0]:.16e}, s{values.size}={values[-1]:.3e}",
            flush=True,
        )

    output = arguments.output
    if output is None:
        output = ROOT / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output, **arrays)

    array_hashes = {key: sha256_array(value) for key, value in arrays.items()}
    metadata = {
        "status": "stored_nested_grid_factor_snapshot",
        "evidence_level": "exact_binary64_inputs_and_floating_low_rank_centers",
        "sigma": sigma,
        "coarse_dimension": dimension,
        "fine_dimension": fine_dimension,
        "approximation_rank": int(arguments.rank),
        "build_seconds": build_seconds,
        "svd_seconds": svd_seconds,
        "snapshot": str(output.relative_to(ROOT)),
        "snapshot_sha256": sha256_file(output),
        "array_sha256": array_hashes,
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
    }
    metadata_path = output.with_suffix(".json")
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
