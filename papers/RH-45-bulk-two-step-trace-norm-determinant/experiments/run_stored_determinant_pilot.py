"""Floating sparse determinant pilot on the archived dyadic matrices."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
sys.path.insert(0, str(ROOT / "src"))

from bulk_trace import bulk_square_determinant  # noqa: E402


RH36_SNAPSHOT = (
    RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
)
RH37_SNAPSHOT = (
    RH37 / "results" / "second_dyadic_fine_object_sigma_1e-02.npz"
)
OUTPUT = ROOT / "results" / "stored_bulk_square_determinants.json"
DEFAULT_RADII = (1.0e-4, 3.0e-4, 1.0e-3, 3.0e-3, 1.0e-2)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def sparse_from_snapshot(data, prefix: str) -> csr_matrix:
    shape = tuple(int(value) for value in data[f"{prefix}_matrix_shape"])
    return csr_matrix(
        (
            np.asarray(data[f"{prefix}_matrix_data"]),
            np.asarray(data[f"{prefix}_matrix_indices"]),
            np.asarray(data[f"{prefix}_matrix_indptr"]),
        ),
        shape=shape,
    )


def stored_object(path: Path, prefix: str) -> dict[str, object]:
    with np.load(path) as data:
        matrix = sparse_from_snapshot(data, prefix)
        return {
            "matrix": matrix,
            "right": np.asarray(data[f"{prefix}_right_modes"]),
            "left": np.asarray(data[f"{prefix}_left_modes"]),
            "values": np.asarray(data[f"{prefix}_peripheral_values"]),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dimensions",
        nargs="*",
        type=int,
        default=(2048, 4096, 8192),
    )
    parser.add_argument(
        "--radii", nargs="*", type=float, default=DEFAULT_RADII
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    requested = tuple(int(value) for value in arguments.dimensions)
    supported = {
        2048: (RH36_SNAPSHOT, "coarse"),
        4096: (RH36_SNAPSHOT, "fine"),
        8192: (RH37_SNAPSHOT, "fine"),
    }
    if not requested or any(value not in supported for value in requested):
        raise ValueError("dimensions must be selected from 2048, 4096, 8192")
    radii = tuple(sorted(set(float(value) for value in arguments.radii)))
    if not radii or radii[0] < 0.0 or radii[-1] >= 1.0:
        raise ValueError("radii must lie in [0,1)")

    levels: dict[str, object] = {}
    for dimension in requested:
        snapshot, prefix = supported[dimension]
        stored = stored_object(snapshot, prefix)
        matrix = stored["matrix"]
        right = stored["right"]
        left = stored["left"]
        values = stored["values"]
        gram = left.T @ right
        weighted_right = right * values[None, :]
        right_residual = matrix @ right - weighted_right
        left_residual = matrix.T @ left - left * values[None, :]
        rows = {}
        begun = time.perf_counter()
        for radius in radii:
            started = time.perf_counter()
            evaluation = bulk_square_determinant(
                matrix, right, left, values, radius
            )
            row = evaluation.as_dict()
            row["seconds"] = time.perf_counter() - started
            rows[str(radius)] = row
            print(
                f"n={dimension} w={radius:.4g} "
                f"D={evaluation.square_determinant:.16e} "
                f"seconds={row['seconds']:.2f}",
                flush=True,
            )
        levels[str(dimension)] = {
            "dimension": dimension,
            "matrix_nonzeros": int(matrix.nnz),
            "matrix_density": float(matrix.nnz / (dimension * dimension)),
            "peripheral_values": [float(value) for value in values],
            "biorthogonality_error": float(
                np.linalg.norm(gram - np.eye(values.size), ord=2)
            ),
            "maximum_relative_right_residual": float(
                max(
                    np.linalg.norm(right_residual[:, index])
                    / np.linalg.norm(right[:, index])
                    for index in range(values.size)
                )
            ),
            "maximum_relative_left_residual": float(
                max(
                    np.linalg.norm(left_residual[:, index])
                    / np.linalg.norm(left[:, index])
                    for index in range(values.size)
                )
            ),
            "determinants": rows,
            "total_seconds": time.perf_counter() - begun,
            "snapshot": repository_entry(snapshot),
        }

    consecutive = {}
    dimensions = sorted(int(value) for value in levels)
    for lower, upper in zip(dimensions, dimensions[1:]):
        lower_rows = levels[str(lower)]["determinants"]
        upper_rows = levels[str(upper)]["determinants"]
        consecutive[f"{lower}_to_{upper}"] = {
            str(radius): abs(
                float(upper_rows[str(radius)]["square_determinant"])
                - float(lower_rows[str(radius)]["square_determinant"])
            )
            for radius in radii
        }

    maximum_identity_error = max(
        float(row["symmetric_det2_identity_error"])
        for level in levels.values()
        for row in level["determinants"].values()
    )
    payload = {
        "status": "floating_stored_adaptive_bulk_square_determinant_pilot",
        "evidence_level": "binary64_sparse_lu_diagnostic_not_validated",
        "scope": (
            "stored fixed-eight-sigma matrices, which coincide with the "
            "adaptive schedule at dimensions 2048, 4096, and 8192"
        ),
        "sigma": 0.01,
        "square_parameters": list(radii),
        "levels": levels,
        "consecutive_absolute_differences": consecutive,
        "maximum_symmetric_det2_identity_error": maximum_identity_error,
        "limitations": [
            "All determinant values are floating diagnostics, not outward interval enclosures.",
            "The three stored matrices use an eight-sigma cutoff; at these dimensions this equals the declared adaptive schedule.",
            "Observed dyadic stabilization is not used to prove continuum determinant convergence.",
        ],
    }
    output = arguments.output
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
