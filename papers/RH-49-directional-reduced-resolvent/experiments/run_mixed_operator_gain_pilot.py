"""Floating mixed Schatten/operator directional-gain audit for RH-49."""

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
from scipy.sparse.linalg import gmres


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
sys.path.insert(0, str(ROOT / "experiments"))

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from run_dyadic_identification_pilot import haar_compress_matrix  # noqa: E402
from run_peripheral_factor_pilot import resolve_factors  # noqa: E402
from run_reduced_directional_pilot import (  # noqa: E402
    branch_factor,
    coarse_from_fine,
    coarse_to_fine,
    coupling_actions,
    deflated_shift,
    detail_from_fine,
    detail_to_fine,
    reduced_solve,
)


OUTPUT = ROOT / "results" / "mixed_operator_gain_pilot.json"
FROBENIUS_PILOT = ROOT / "results" / "reduced_directional_pilot.json"
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


def deterministic_start(dimension: int, phase: float) -> np.ndarray:
    index = np.arange(int(dimension), dtype=np.float64)
    vector = np.sin((index + 0.5) * math.sqrt(2.0 + phase))
    vector += 0.31 * np.cos((index + 0.5) * math.sqrt(3.0 + phase))
    return vector / np.linalg.norm(vector)


def reduced_adjoint_solve(
    matrix,
    z: complex,
    eigenvalue: float,
    right: np.ndarray,
    left: np.ndarray,
    source: np.ndarray,
    *,
    tolerance: float,
) -> tuple[np.ndarray, dict[str, float | int]]:
    source_value = np.asarray(source, dtype=np.complex128)
    reduced_source = source_value - left * np.dot(right, source_value)
    operator = deflated_shift(matrix, z, eigenvalue, right, left).H
    history: list[float] = []
    solution, info = gmres(
        operator,
        reduced_source,
        rtol=float(tolerance),
        atol=0.0,
        restart=100,
        maxiter=30,
        callback=lambda value: history.append(float(value)),
        callback_type="pr_norm",
    )
    if int(info) != 0:
        raise RuntimeError(
            f"adjoint deflated GMRES failed: info={info}, iterations={len(history)}"
        )
    residual = np.linalg.norm(operator @ solution - reduced_source)
    denominator = max(np.linalg.norm(reduced_source), np.finfo(float).tiny)
    return np.asarray(solution), {
        "iterations": len(history),
        "relative_residual": float(residual / denominator),
        "branch_leakage": float(abs(np.dot(right, solution))),
    }


def power_singular_candidate(
    matvec,
    rmatvec,
    dimension: int,
    *,
    iterations: int,
    phase: float,
) -> dict[str, object]:
    vector = deterministic_start(dimension, phase).astype(np.complex128)
    history = []
    previous = 0.0
    for index in range(int(iterations)):
        image = np.asarray(matvec(vector))
        singular = float(np.linalg.norm(image))
        if singular == 0.0 or not np.isfinite(singular):
            raise RuntimeError("power iteration encountered an invalid image")
        left = image / singular
        dual = np.asarray(rmatvec(left))
        dual_norm = float(np.linalg.norm(dual))
        if dual_norm == 0.0 or not np.isfinite(dual_norm):
            raise RuntimeError("power iteration encountered an invalid dual image")
        residual = float(np.linalg.norm(dual - singular * vector))
        change = float(abs(singular - previous) / singular)
        history.append(
            {
                "iteration": index + 1,
                "singular_candidate": singular,
                "relative_change": change,
                "triplet_residual": residual,
            }
        )
        vector = dual / dual_norm
        previous = singular
    image = np.asarray(matvec(vector))
    singular = float(np.linalg.norm(image))
    left = image / singular
    residual = float(np.linalg.norm(np.asarray(rmatvec(left)) - singular * vector))
    return {
        "singular_candidate": singular,
        "triplet_residual": residual,
        "relative_triplet_residual": float(
            residual / max(singular, np.finfo(float).tiny)
        ),
        "iterations": int(iterations),
        "history": history,
    }


def frobenius_node(
    frobenius: dict[str, object], sigma: float, branch: str
) -> dict[str, object]:
    row = min(
        frobenius["rows"],
        key=lambda item: abs(float(item["sigma"]) - sigma),
    )
    nodes = row["branches"][branch]["nodes"]
    if branch == "perron":
        return min(nodes, key=lambda item: float(item["z_real"]))
    return max(nodes, key=lambda item: float(item["z_real"]))


def run_branch(
    *,
    sigma: float,
    branch: str,
    fine,
    coarse,
    fine_factors: dict[str, object],
    coarse_factors: dict[str, object],
    frobenius: dict[str, object],
    iterations: int,
    tolerance: float,
) -> dict[str, object]:
    fine_lambda, fine_right, fine_left = branch_factor(fine_factors, branch)
    coarse_lambda, coarse_right, coarse_left = branch_factor(
        coarse_factors, branch
    )
    z = complex(0.95 if branch == "perron" else fine_lambda + CONTOUR_RADIUS)
    b, bt, c, ct = coupling_actions(fine)
    dimension = coarse.shape[0]
    solve_ledgers: list[dict[str, float | int]] = []

    def left_matvec(vector: np.ndarray) -> np.ndarray:
        source = coarse_to_fine(b(vector))
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
        solve_ledgers.append(ledger)
        return coarse_from_fine(solved)

    def left_rmatvec(vector: np.ndarray) -> np.ndarray:
        source = coarse_to_fine(vector)
        solved, ledger = reduced_adjoint_solve(
            fine,
            z,
            fine_lambda,
            fine_right,
            fine_left,
            source,
            tolerance=tolerance,
        )
        solve_ledgers.append(ledger)
        return bt(coarse_from_fine(solved))

    def right_matvec(vector: np.ndarray) -> np.ndarray:
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
        solve_ledgers.append(ledger)
        return c(solved)

    def right_rmatvec(vector: np.ndarray) -> np.ndarray:
        source = ct(vector)
        solved, ledger = reduced_adjoint_solve(
            coarse,
            z,
            coarse_lambda,
            coarse_right,
            coarse_left,
            source,
            tolerance=tolerance,
        )
        solve_ledgers.append(ledger)
        return solved

    begun = time.perf_counter()
    coupling_iterations = max(60, 3 * iterations)
    b_operator = power_singular_candidate(
        b, bt, dimension, iterations=coupling_iterations, phase=0.11
    )
    c_operator = power_singular_candidate(
        c, ct, dimension, iterations=coupling_iterations, phase=0.23
    )
    left_operator = power_singular_candidate(
        left_matvec,
        left_rmatvec,
        dimension,
        iterations=iterations,
        phase=0.37,
    )
    right_operator = power_singular_candidate(
        right_matvec,
        right_rmatvec,
        dimension,
        iterations=iterations,
        phase=0.53,
    )
    elapsed = time.perf_counter() - begun
    left_operator_gain = float(left_operator["singular_candidate"]) / float(
        b_operator["singular_candidate"]
    )
    right_operator_gain = float(right_operator["singular_candidate"]) / float(
        c_operator["singular_candidate"]
    )
    frobenius_row = frobenius_node(frobenius, sigma, branch)
    left_frobenius_gain = float(
        frobenius_row["left_reduced_frobenius_gain"]
    )
    right_frobenius_gain = float(
        frobenius_row["right_reduced_frobenius_gain"]
    )
    mixed_first = left_frobenius_gain * right_operator_gain
    mixed_second = left_operator_gain * right_frobenius_gain
    return {
        "branch": branch,
        "z_real": float(z.real),
        "z_imag": float(z.imag),
        "fine_eigenvalue": fine_lambda,
        "coarse_eigenvalue": coarse_lambda,
        "B_operator_candidate": b_operator,
        "C_operator_candidate": c_operator,
        "left_reduced_operator_candidate": left_operator,
        "right_reduced_operator_candidate": right_operator,
        "left_operator_gain": left_operator_gain,
        "right_operator_gain": right_operator_gain,
        "left_frobenius_gain": left_frobenius_gain,
        "right_frobenius_gain": right_frobenius_gain,
        "left_frobenius_right_operator_product": mixed_first,
        "left_operator_right_frobenius_product": mixed_second,
        "mixed_directional_product_candidate": min(mixed_first, mixed_second),
        "maximum_gmres_iterations": max(
            int(item["iterations"]) for item in solve_ledgers
        ),
        "maximum_gmres_relative_residual": max(
            float(item["relative_residual"]) for item in solve_ledgers
        ),
        "maximum_branch_leakage": max(
            float(item["branch_leakage"]) for item in solve_ledgers
        ),
        "elapsed_seconds": elapsed,
    }


def run_sigma(
    sigma: float,
    fine_resolution: float,
    frobenius: dict[str, object],
    iterations: int,
    tolerance: float,
) -> dict[str, object]:
    fine_dimension = max(
        128, 2 * int(round(float(fine_resolution) / sigma / 2.0))
    )
    build_started = time.perf_counter()
    fine = sparse_folded_gaussian_matrix(fine_dimension, sigma)
    coarse = haar_compress_matrix(fine)
    fine_factors = resolve_factors(fine, sigma)
    coarse_factors = resolve_factors(coarse, sigma)
    build_seconds = time.perf_counter() - build_started
    branches = {
        branch: run_branch(
            sigma=sigma,
            branch=branch,
            fine=fine,
            coarse=coarse,
            fine_factors=fine_factors,
            coarse_factors=coarse_factors,
            frobenius=frobenius,
            iterations=iterations,
            tolerance=tolerance,
        )
        for branch in ("perron", "parity")
    }
    result = {
        "sigma": float(sigma),
        "fine_dimension": fine_dimension,
        "coarse_dimension": fine_dimension // 2,
        "fine_dimension_times_sigma": fine_dimension * sigma,
        "build_and_eigenfactor_seconds": build_seconds,
        "branches": branches,
        "maximum_mixed_directional_product_candidate": max(
            item["mixed_directional_product_candidate"]
            for item in branches.values()
        ),
    }
    del fine, coarse, fine_factors, coarse_factors
    gc.collect()
    return result


def fit_power(rows: list[dict[str, object]]) -> dict[str, float]:
    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(
        np.asarray(
            [
                float(row["maximum_mixed_directional_product_candidate"])
                for row in rows
            ]
        )
    )
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
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--tolerance", type=float, default=2.0e-10)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    frobenius = json.loads(FROBENIUS_PILOT.read_text(encoding="utf-8"))
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    rows = []
    for sigma in sigmas:
        row = run_sigma(
            sigma,
            args.fine_resolution,
            frobenius,
            args.iterations,
            args.tolerance,
        )
        rows.append(row)
        if args.verbose:
            print(json.dumps(row, sort_keys=True), flush=True)
        else:
            print(
                json.dumps(
                    {
                        "sigma": row["sigma"],
                        "fine_dimension": row["fine_dimension"],
                        "maximum_mixed_directional_product_candidate": row[
                            "maximum_mixed_directional_product_candidate"
                        ],
                        "maximum_gmres_iterations": max(
                            branch_row["maximum_gmres_iterations"]
                            for branch_row in row["branches"].values()
                        ),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    source_path = RH14 / "src" / "parity_boundary" / "operators.py"
    payload = {
        "status": "floating_mixed_directional_operator_gain_audit",
        "evidence_level": (
            "binary64 sparse power-GMRES singular candidates not validated uppers"
        ),
        "fine_resolution_target": float(args.fine_resolution),
        "power_iterations": int(args.iterations),
        "gmres_tolerance": float(args.tolerance),
        "source": {
            "path": str(source_path.relative_to(REPOSITORY)),
            "sha256": sha256_file(source_path),
        },
        "frobenius_pilot": {
            "path": str(FROBENIUS_PILOT.relative_to(ROOT)),
            "sha256": sha256_file(FROBENIUS_PILOT),
        },
        "rows": rows,
        "mixed_product_fit": fit_power(rows),
        "limitations": [
            "Power iteration gives floating lower candidates for operator norms, not validated upper bounds.",
            "The mixed product combines those candidates with Hutchinson Frobenius estimates from the companion audit.",
            "Only the empirically worst real contour node is evaluated for each branch.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "mixed_operator_gain_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "mixed_product_fit": payload["mixed_product_fit"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
