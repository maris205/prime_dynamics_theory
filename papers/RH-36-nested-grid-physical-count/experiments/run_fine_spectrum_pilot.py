"""Floating sparse spectral localization for the nested-grid pair."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator, eigs


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def two_step_operator(data, prefix: str):
    matrix = sparse_from_snapshot(data, f"{prefix}_matrix")
    right = np.asarray(data[f"{prefix}_right_modes"])
    left = np.asarray(data[f"{prefix}_left_modes"])
    values = np.asarray(data[f"{prefix}_peripheral_values"])
    weighted_right = right * values[None, :]

    def one_step(source):
        array = np.asarray(source)
        coefficients = left.T @ array
        correction = weighted_right @ coefficients
        return matrix @ array - correction

    def two_step(source):
        return one_step(one_step(source))

    dimension = int(matrix.shape[0])
    return LinearOperator(
        (dimension, dimension), matvec=two_step, dtype=np.float64
    ), two_step


def deterministic_start(dimension: int) -> np.ndarray:
    index = np.arange(int(dimension), dtype=np.float64)
    values = np.sin(np.sqrt(2.0) * (index + 0.5))
    values += 0.41 * np.cos(np.sqrt(7.0) * (index + 0.5))
    return values / np.linalg.norm(values)


def solve(operator, action, count: int):
    begun = time.perf_counter()
    values, vectors = eigs(
        operator,
        k=int(count),
        which="LM",
        tol=1.0e-11,
        maxiter=30000,
        v0=deterministic_start(operator.shape[0]),
    )
    residuals = []
    for index, value in enumerate(values):
        vector = vectors[:, index]
        residuals.append(
            float(
                np.linalg.norm(action(vector) - value * vector)
                / np.linalg.norm(vector)
            )
        )
    order = np.argsort(-np.abs(values))
    return values[order], np.asarray(residuals)[order], time.perf_counter() - begun


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=Path("results/nested_grid_snapshot_sigma_1e-02.npz"),
    )
    parser.add_argument("--count", type=int, default=24)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    snapshot = arguments.snapshot
    if not snapshot.is_absolute():
        snapshot = ROOT / snapshot

    scale = next(
        row
        for row in read_csv(RH28 / "results" / "arcwise_scale_summary.csv")
        if float(row["sigma"]) == 1.0e-2
    )
    center = complex(
        float(scale["contour_center_real"]),
        float(scale["contour_center_imag"]),
    )
    radius = float(scale["contour_radius"])
    with np.load(snapshot) as data:
        coarse_operator, coarse_action = two_step_operator(data, "coarse")
        fine_operator, fine_action = two_step_operator(data, "fine")
        coarse_values, coarse_residuals, coarse_seconds = solve(
            coarse_operator, coarse_action, int(arguments.count)
        )
        fine_values, fine_residuals, fine_seconds = solve(
            fine_operator, fine_action, int(arguments.count)
        )

    def rows(values, residuals):
        return [
            {
                "real": float(value.real),
                "imag": float(value.imag),
                "modulus": float(abs(value)),
                "signed_contour_distance": float(abs(value - center) - radius),
                "relative_residual": float(residual),
            }
            for value, residual in zip(values, residuals)
        ]

    coarse_rows = rows(coarse_values, coarse_residuals)
    fine_rows = rows(fine_values, fine_residuals)
    coarse_inside = [row for row in coarse_rows if row["signed_contour_distance"] < 0]
    fine_inside = [row for row in fine_rows if row["signed_contour_distance"] < 0]
    if len(coarse_inside) == 1 and len(fine_inside) == 1:
        displacement = abs(
            complex(coarse_inside[0]["real"], coarse_inside[0]["imag"])
            - complex(fine_inside[0]["real"], fine_inside[0]["imag"])
        )
    else:
        displacement = None
    payload = {
        "status": "floating_nested_grid_sparse_spectrum_pilot",
        "evidence_level": "floating_not_validated",
        "sigma": 1.0e-2,
        "coarse_dimension": int(coarse_operator.shape[0]),
        "fine_dimension": int(fine_operator.shape[0]),
        "requested_eigenvalue_count": int(arguments.count),
        "contour_center_real": center.real,
        "contour_center_imag": center.imag,
        "contour_radius": radius,
        "coarse_resolved_inside_count": len(coarse_inside),
        "fine_resolved_inside_count": len(fine_inside),
        "coarse_inside": coarse_inside,
        "fine_inside": fine_inside,
        "inside_eigenvalue_displacement": (
            None if displacement is None else float(displacement)
        ),
        "maximum_coarse_residual": float(np.max(coarse_residuals)),
        "maximum_fine_residual": float(np.max(fine_residuals)),
        "coarse_seconds": coarse_seconds,
        "fine_seconds": fine_seconds,
        "coarse_eigenvalues": coarse_rows,
        "fine_eigenvalues": fine_rows,
    }
    output = arguments.output
    if output is None:
        output = ROOT / "results" / "fine_spectrum_pilot_sigma_1e-02.json"
    if not output.is_absolute():
        output = ROOT / output
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    np.savez_compressed(
        output.with_suffix(".npz"),
        coarse_eigenvalues=coarse_values,
        fine_eigenvalues=fine_values,
        coarse_residuals=coarse_residuals,
        fine_residuals=fine_residuals,
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
