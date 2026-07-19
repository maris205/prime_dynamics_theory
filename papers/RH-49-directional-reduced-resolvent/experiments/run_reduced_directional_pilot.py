"""Floating residue-deflated directional-resolvent audit for RH-49.

For one exactly nested Haar pair ``A_n = E_n A_2n E_n``, this script
estimates the Frobenius directional gains of

    S_circ(z) B,       C R_A,circ(z),

on the Perron and negative-parity circles.  The reduced actions are
evaluated by exact rank-one deflation of the resolved branch followed by
GMRES.  Hutchinson probes avoid forming either dense directional operator.
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
from scipy.sparse.linalg import LinearOperator, gmres


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"
RH48 = PAPERS / "RH-48-intrinsic-riesz-identification"
sys.path.insert(0, str(RH14 / "src"))
sys.path.insert(0, str(RH47 / "src"))
sys.path.insert(0, str(RH47 / "experiments"))
sys.path.insert(0, str(RH48 / "experiments"))

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from run_dyadic_identification_pilot import (  # noqa: E402
    haar_compress_matrix,
)
from run_peripheral_factor_pilot import resolve_factors  # noqa: E402


OUTPUT = ROOT / "results" / "reduced_directional_pilot.json"
FULL_SIGMAS = (0.01, 0.004, 0.002, 0.001, 0.0005)
SMOKE_SIGMAS = (0.01, 0.004)
FINE_RESOLUTION = 20.48
CONTOUR_RADIUS = 0.05


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def coarse_to_fine(vector: np.ndarray) -> np.ndarray:
    return np.repeat(np.asarray(vector), 2) / math.sqrt(2.0)


def detail_to_fine(vector: np.ndarray) -> np.ndarray:
    value = np.asarray(vector)
    result = np.empty(2 * value.size, dtype=value.dtype)
    result[0::2] = value / math.sqrt(2.0)
    result[1::2] = -value / math.sqrt(2.0)
    return result


def coarse_from_fine(vector: np.ndarray) -> np.ndarray:
    value = np.asarray(vector)
    return (value[0::2] + value[1::2]) / math.sqrt(2.0)


def detail_from_fine(vector: np.ndarray) -> np.ndarray:
    value = np.asarray(vector)
    return (value[0::2] - value[1::2]) / math.sqrt(2.0)


def coupling_actions(matrix: csr_matrix):
    """Return matrix-free B, B*, C, and C* for the Haar split."""

    def b(vector: np.ndarray) -> np.ndarray:
        return coarse_from_fine(matrix @ detail_to_fine(vector))

    def bt(vector: np.ndarray) -> np.ndarray:
        return detail_from_fine(matrix.T @ coarse_to_fine(vector))

    def c(vector: np.ndarray) -> np.ndarray:
        return detail_from_fine(matrix @ coarse_to_fine(vector))

    def ct(vector: np.ndarray) -> np.ndarray:
        return coarse_from_fine(matrix.T @ detail_to_fine(vector))

    return b, bt, c, ct


def branch_factor(
    factors: dict[str, object], branch: str
) -> tuple[float, np.ndarray, np.ndarray]:
    dimension = np.asarray(factors["perron_mass"]).size
    if branch == "perron":
        return (
            1.0,
            np.ones(dimension, dtype=np.float64),
            np.asarray(factors["perron_mass"], dtype=np.float64),
        )
    if branch == "parity":
        return (
            float(factors["parity_eigenvalue"]),
            np.asarray(factors["parity_right"], dtype=np.float64),
            np.asarray(factors["parity_mass"], dtype=np.float64),
        )
    raise ValueError(f"unknown branch: {branch}")


def deflated_shift(
    matrix: csr_matrix,
    z: complex,
    eigenvalue: float,
    right: np.ndarray,
    left: np.ndarray,
) -> LinearOperator:
    dimension = matrix.shape[0]
    dtype = np.dtype(np.complex128)

    def matvec(vector: np.ndarray) -> np.ndarray:
        value = np.asarray(vector, dtype=np.complex128)
        return (
            z * value
            - matrix @ value
            + eigenvalue * right * np.dot(left, value)
        )

    def rmatvec(vector: np.ndarray) -> np.ndarray:
        value = np.asarray(vector, dtype=np.complex128)
        return (
            np.conjugate(z) * value
            - matrix.T @ value
            + eigenvalue * left * np.dot(right, value)
        )

    return LinearOperator(
        (dimension, dimension),
        matvec=matvec,
        rmatvec=rmatvec,
        dtype=dtype,
    )


def reduced_solve(
    matrix: csr_matrix,
    z: complex,
    eigenvalue: float,
    right: np.ndarray,
    left: np.ndarray,
    source: np.ndarray,
    *,
    tolerance: float,
    restart: int,
    maximum_cycles: int,
) -> tuple[np.ndarray, dict[str, float | int]]:
    """Apply the branch-reduced resolvent using exact rank-one deflation."""

    source_value = np.asarray(source, dtype=np.complex128)
    reduced_source = source_value - right * np.dot(left, source_value)
    operator = deflated_shift(matrix, z, eigenvalue, right, left)
    history: list[float] = []
    solution, info = gmres(
        operator,
        reduced_source,
        rtol=float(tolerance),
        atol=0.0,
        restart=int(restart),
        maxiter=int(maximum_cycles),
        callback=lambda value: history.append(float(value)),
        callback_type="pr_norm",
    )
    if int(info) != 0:
        raise RuntimeError(
            f"deflated GMRES failed: info={info}, iterations={len(history)}"
        )
    residual = np.linalg.norm(operator @ solution - reduced_source)
    denominator = max(np.linalg.norm(reduced_source), np.finfo(float).tiny)
    branch_leakage = abs(np.dot(left, solution))
    return np.asarray(solution), {
        "iterations": len(history),
        "relative_residual": float(residual / denominator),
        "branch_leakage": float(branch_leakage),
    }


def rademacher_probes(
    dimension: int, count: int, seed: int
) -> list[np.ndarray]:
    rng = np.random.default_rng(int(seed))
    return [
        rng.choice(np.asarray((-1.0, 1.0)), size=int(dimension))
        for _ in range(int(count))
    ]


def circle_nodes(center: float, radius: float, count: int) -> list[complex]:
    return [
        complex(center) + radius * np.exp(2j * np.pi * index / count)
        for index in range(int(count))
    ]


def branch_audit(
    *,
    branch: str,
    sigma: float,
    fine: csr_matrix,
    coarse: csr_matrix,
    fine_factors: dict[str, object],
    coarse_factors: dict[str, object],
    probes: int,
    nodes: int,
    tolerance: float,
) -> dict[str, object]:
    fine_lambda, fine_right, fine_left = branch_factor(
        fine_factors, branch
    )
    coarse_lambda, coarse_right, coarse_left = branch_factor(
        coarse_factors, branch
    )
    center = 1.0 if branch == "perron" else fine_lambda
    b, _, c, _ = coupling_actions(fine)
    dimension = coarse.shape[0]
    detail_probes = rademacher_probes(
        dimension, probes, 4900 + int(round(1.0e6 * sigma))
    )
    coarse_probes = rademacher_probes(
        dimension, probes, 5900 + int(round(1.0e6 * sigma))
    )

    b_images = [b(vector) for vector in detail_probes]
    c_images = [c(vector) for vector in coarse_probes]
    b_square = float(sum(np.vdot(value, value).real for value in b_images))
    c_square = float(sum(np.vdot(value, value).real for value in c_images))
    if b_square <= 0.0 or c_square <= 0.0:
        raise RuntimeError("a Haar coupling vanished unexpectedly")

    fine_coarse_right = coarse_from_fine(fine_right)
    fine_coarse_left = coarse_from_fine(fine_left)
    node_rows = []
    all_iterations: list[int] = []
    all_residuals: list[float] = []
    all_leakage: list[float] = []
    started = time.perf_counter()
    for node_index, z in enumerate(circle_nodes(center, CONTOUR_RADIUS, nodes)):
        left_reduced_square = 0.0
        left_full_square = 0.0
        right_reduced_square = 0.0
        right_full_square = 0.0

        for vector, b_image in zip(detail_probes, b_images):
            del vector
            source = coarse_to_fine(b_image)
            solved, ledger = reduced_solve(
                fine,
                z,
                fine_lambda,
                fine_right,
                fine_left,
                source,
                tolerance=tolerance,
                restart=100,
                maximum_cycles=30,
            )
            reduced = coarse_from_fine(solved)
            residue = (
                fine_coarse_right
                * np.dot(fine_coarse_left, b_image)
                / (z - fine_lambda)
            )
            full = reduced + residue
            left_reduced_square += float(np.vdot(reduced, reduced).real)
            left_full_square += float(np.vdot(full, full).real)
            all_iterations.append(int(ledger["iterations"]))
            all_residuals.append(float(ledger["relative_residual"]))
            all_leakage.append(float(ledger["branch_leakage"]))

        for vector, c_image in zip(coarse_probes, c_images):
            solved, ledger = reduced_solve(
                coarse,
                z,
                coarse_lambda,
                coarse_right,
                coarse_left,
                vector,
                tolerance=tolerance,
                restart=100,
                maximum_cycles=30,
            )
            reduced = c(solved)
            residue_state = (
                coarse_right
                * np.dot(coarse_left, vector)
                / (z - coarse_lambda)
            )
            full = reduced + c(residue_state)
            right_reduced_square += float(np.vdot(reduced, reduced).real)
            right_full_square += float(np.vdot(full, full).real)
            all_iterations.append(int(ledger["iterations"]))
            all_residuals.append(float(ledger["relative_residual"]))
            all_leakage.append(float(ledger["branch_leakage"]))

        left_reduced_gain = math.sqrt(left_reduced_square / b_square)
        left_full_gain = math.sqrt(left_full_square / b_square)
        right_reduced_gain = math.sqrt(right_reduced_square / c_square)
        right_full_gain = math.sqrt(right_full_square / c_square)
        node_rows.append(
            {
                "node": node_index,
                "z_real": float(z.real),
                "z_imag": float(z.imag),
                "left_reduced_frobenius_gain": left_reduced_gain,
                "left_full_frobenius_gain": left_full_gain,
                "right_reduced_frobenius_gain": right_reduced_gain,
                "right_full_frobenius_gain": right_full_gain,
                "reduced_gain_product": left_reduced_gain
                * right_reduced_gain,
                "full_gain_product": left_full_gain * right_full_gain,
            }
        )

    return {
        "branch": branch,
        "fine_eigenvalue": fine_lambda,
        "coarse_eigenvalue": coarse_lambda,
        "contour_center": center,
        "contour_radius": CONTOUR_RADIUS,
        "probe_count": probes,
        "node_count": nodes,
        "nodes": node_rows,
        "maximum_left_reduced_frobenius_gain": max(
            row["left_reduced_frobenius_gain"] for row in node_rows
        ),
        "maximum_left_full_frobenius_gain": max(
            row["left_full_frobenius_gain"] for row in node_rows
        ),
        "maximum_right_reduced_frobenius_gain": max(
            row["right_reduced_frobenius_gain"] for row in node_rows
        ),
        "maximum_right_full_frobenius_gain": max(
            row["right_full_frobenius_gain"] for row in node_rows
        ),
        "maximum_reduced_gain_product": max(
            row["reduced_gain_product"] for row in node_rows
        ),
        "maximum_full_gain_product": max(
            row["full_gain_product"] for row in node_rows
        ),
        "maximum_gmres_iterations": max(all_iterations),
        "median_gmres_iterations": float(np.median(all_iterations)),
        "maximum_relative_residual": max(all_residuals),
        "maximum_branch_leakage": max(all_leakage),
        "elapsed_seconds": time.perf_counter() - started,
    }


def run_sigma(
    sigma: float,
    fine_resolution: float,
    probes: int,
    nodes: int,
    tolerance: float,
) -> dict[str, object]:
    fine_dimension = int(round(float(fine_resolution) / float(sigma)))
    fine_dimension = max(128, 2 * int(round(fine_dimension / 2)))
    build_started = time.perf_counter()
    fine = sparse_folded_gaussian_matrix(fine_dimension, sigma)
    coarse = haar_compress_matrix(fine)
    fine_factors = resolve_factors(fine, sigma)
    coarse_factors = resolve_factors(coarse, sigma)
    build_seconds = time.perf_counter() - build_started
    branches = {
        branch: branch_audit(
            branch=branch,
            sigma=sigma,
            fine=fine,
            coarse=coarse,
            fine_factors=fine_factors,
            coarse_factors=coarse_factors,
            probes=probes,
            nodes=nodes,
            tolerance=tolerance,
        )
        for branch in ("perron", "parity")
    }
    result = {
        "sigma": float(sigma),
        "fine_dimension": fine_dimension,
        "coarse_dimension": fine_dimension // 2,
        "fine_dimension_times_sigma": fine_dimension * sigma,
        "coarse_dimension_times_sigma": fine_dimension * sigma / 2.0,
        "fine_nonzeros": int(fine.nnz),
        "coarse_nonzeros": int(coarse.nnz),
        "build_and_eigenfactor_seconds": build_seconds,
        "branches": branches,
        "maximum_reduced_gain_product": max(
            branch["maximum_reduced_gain_product"]
            for branch in branches.values()
        ),
        "maximum_full_gain_product": max(
            branch["maximum_full_gain_product"]
            for branch in branches.values()
        ),
    }
    del fine, coarse, fine_factors, coarse_factors
    gc.collect()
    return result


def fit_power(rows: list[dict[str, object]], field: str) -> dict[str, float]:
    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(np.asarray([float(row[field]) for row in rows]))
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent_gamma": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--fine-resolution", type=float, default=FINE_RESOLUTION)
    parser.add_argument("--probes", type=int, default=4)
    parser.add_argument("--nodes", type=int, default=8)
    parser.add_argument("--tolerance", type=float, default=2.0e-10)
    args = parser.parse_args()
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    rows = []
    for sigma in sigmas:
        row = run_sigma(
            sigma,
            args.fine_resolution,
            args.probes,
            args.nodes,
            args.tolerance,
        )
        rows.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)

    source_path = RH14 / "src" / "parity_boundary" / "operators.py"
    payload = {
        "status": "floating_residue_deflated_directional_resolvent_audit",
        "evidence_level": (
            "binary64 sparse exact-Haar Hutchinson-GMRES diagnostic not validated"
        ),
        "fine_resolution_target": float(args.fine_resolution),
        "probe_count": int(args.probes),
        "contour_node_count": int(args.nodes),
        "gmres_tolerance": float(args.tolerance),
        "source": {
            "path": str(source_path.relative_to(REPOSITORY)),
            "sha256": sha256_file(source_path),
        },
        "rows": rows,
        "reduced_product_fit": fit_power(
            rows, "maximum_reduced_gain_product"
        ),
        "full_product_fit": fit_power(rows, "maximum_full_gain_product"),
        "limitations": [
            "The gains are Hutchinson estimates of Frobenius ratios, not certified operator-norm uppers for the RH-48 directional condition.",
            "Branch reduction uses floating eigenfactors and GMRES solves with archived residual diagnostics.",
            "The sparse matrices use an eight-sigma cutoff and exact row renormalization.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "reduced_directional_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
