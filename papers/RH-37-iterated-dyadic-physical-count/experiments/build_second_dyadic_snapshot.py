"""Build the exact 4096-to-8192 factor snapshot and low-rank centers."""

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
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator, svds


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
sys.path[:0] = [str(RH24 / "src"), str(RH24 / "experiments")]

import run_contour_feshbach_audit as rh24  # noqa: E402


def sha256_array(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).view(np.uint8)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        maxiter=10000,
        random_state=161803,
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
    parser.add_argument("--rank", type=int, default=96)
    parser.add_argument(
        "--reuse-snapshot",
        type=Path,
        help="repackage an existing monolithic snapshot without recomputing",
    )
    arguments = parser.parse_args()

    inherited_snapshot = (
        RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
    )
    begun = time.perf_counter()
    with np.load(inherited_snapshot) as inherited:
        sigma = float(inherited["sigma"])
        critical_u = float(inherited["critical_u"])
        coarse_matrix = sparse_from_snapshot(inherited, "fine_matrix").copy()
        coarse_spectrum = {
            key: value.copy()
            for key, value in spectrum_from_snapshot(inherited, "fine").items()
        }
        inherited_arrays = {
            "matrix_data": sha256_array(np.asarray(inherited["fine_matrix_data"])),
            "matrix_indices": sha256_array(
                np.asarray(inherited["fine_matrix_indices"])
            ),
            "matrix_indptr": sha256_array(
                np.asarray(inherited["fine_matrix_indptr"])
            ),
            "right_modes": sha256_array(
                np.asarray(inherited["fine_right_modes"])
            ),
            "left_modes": sha256_array(np.asarray(inherited["fine_left_modes"])),
            "peripheral_values": sha256_array(
                np.asarray(inherited["fine_peripheral_values"])
            ),
        }
    names = (
        "coarse_consistency",
        "coarse_to_detail",
        "detail_to_coarse",
        "detail_block",
    )
    construction_record = None
    if arguments.reuse_snapshot is not None:
        source = arguments.reuse_snapshot
        if not source.is_absolute():
            source = ROOT / source
        sidecar = source.with_suffix(".json")
        if sidecar.exists():
            construction_record = json.loads(sidecar.read_text(encoding="utf-8"))
        with np.load(source) as reused:
            arrays = {key: np.asarray(reused[key]).copy() for key in reused.files}
        coarse_dimension = int(arrays["coarse_dimension"])
        fine_dimension = int(arrays["fine_dimension"])
        if int(arrays["approximation_rank"]) != int(arguments.rank):
            raise ValueError("reused snapshot rank does not match --rank")
        build_seconds = float(
            0.0 if construction_record is None else construction_record["build_seconds"]
        )
        svd_seconds = dict(
            {} if construction_record is None else construction_record["svd_seconds"]
        )
    else:
        coarse_dimension = int(coarse_matrix.shape[0])
        fine_dimension = 2 * coarse_dimension
        fine_matrix = rh24.sparse_folded_gaussian_matrix(
            fine_dimension, sigma, u=critical_u
        )
        fine_spectrum = rh24.resolve_peripheral_modes(fine_matrix)
        build_seconds = time.perf_counter() - begun

        coarse, coarse_adjoint = bulk_actions(coarse_matrix, coarse_spectrum)
        fine, fine_adjoint = bulk_actions(fine_matrix, fine_spectrum)
        arrays = {
            "sigma": np.asarray(sigma, dtype=np.float64),
            "critical_u": np.asarray(critical_u, dtype=np.float64),
            "coarse_dimension": np.asarray(coarse_dimension, dtype=np.int64),
            "fine_dimension": np.asarray(fine_dimension, dtype=np.int64),
            "approximation_rank": np.asarray(int(arguments.rank), dtype=np.int64),
            "fine_right_modes": np.asarray(fine_spectrum["right_modes"]),
            "fine_left_modes": np.asarray(fine_spectrum["left_modes"]),
            "fine_peripheral_values": np.asarray(
                fine_spectrum["peripheral_values"]
            ),
        }
        add_sparse(arrays, "fine_matrix", fine_matrix)

        svd_seconds = {}
        for name in names:
            action, adjoint = block_actions(
                name, coarse, coarse_adjoint, fine, fine_adjoint
            )
            operator = LinearOperator(
                (coarse_dimension, coarse_dimension),
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

    results = ROOT / "results"
    results.mkdir(parents=True, exist_ok=True)
    object_keys = [
        "sigma",
        "critical_u",
        "coarse_dimension",
        "fine_dimension",
        "approximation_rank",
        "fine_right_modes",
        "fine_left_modes",
        "fine_peripheral_values",
        "fine_matrix_data",
        "fine_matrix_indices",
        "fine_matrix_indptr",
        "fine_matrix_shape",
    ]
    object_path = results / "second_dyadic_fine_object_sigma_1e-02.npz"
    np.savez_compressed(object_path, **{key: arrays[key] for key in object_keys})
    part_paths: dict[str, Path] = {"fine_object": object_path}
    for name in names:
        part = results / f"second_dyadic_center_{name}_sigma_1e-02.npz"
        np.savez_compressed(
            part,
            left=arrays[f"{name}_left"],
            singular_values=arrays[f"{name}_singular_values"],
            right_adjoint=arrays[f"{name}_right_adjoint"],
        )
        part_paths[name] = part

    local_keys = [
        *object_keys,
        *[
            f"{name}_{suffix}"
            for name in names
            for suffix in ("left", "singular_values", "right_adjoint")
        ],
    ]

    metadata = {
        "status": "stored_split_second_dyadic_factor_snapshot",
        "evidence_level": "exact_binary64_inputs_and_floating_low_rank_centers",
        "sigma": sigma,
        "coarse_dimension": coarse_dimension,
        "fine_dimension": fine_dimension,
        "approximation_rank": int(arguments.rank),
        "build_seconds": build_seconds,
        "svd_seconds": svd_seconds,
        "snapshot_parts": {
            name: str(path.relative_to(ROOT)) for name, path in part_paths.items()
        },
        "snapshot_part_sha256": {
            name: sha256_file(path) for name, path in part_paths.items()
        },
        "local_array_sha256": {
            key: sha256_array(arrays[key]) for key in local_keys
        },
        "inherited_snapshot": str(inherited_snapshot),
        "inherited_snapshot_sha256": sha256_file(inherited_snapshot),
        "inherited_coarse_object_array_sha256": inherited_arrays,
        "construction_monolithic_snapshot_sha256": (
            None
            if construction_record is None
            else construction_record.get("snapshot_sha256")
        ),
        "construction_array_sha256": (
            None
            if construction_record is None
            else construction_record.get("array_sha256")
        ),
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
    }
    metadata_path = results / "second_dyadic_snapshot_sigma_1e-02.json"
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
