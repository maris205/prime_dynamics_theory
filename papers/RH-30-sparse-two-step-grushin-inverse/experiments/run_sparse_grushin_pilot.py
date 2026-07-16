"""Sparse-LU pilot for the two-step Grushin inverse construction.

All inverse norms produced by this script are floating-point lower
candidates.  They are used to decide whether a later verified-LU bound has
enough room; they are not certificates by themselves.
"""

from __future__ import annotations

import argparse
import csv
import json
import resource
import sys
import time
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import splu


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH29 = PAPERS / "RH-29-deflated-complement-resolvent"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH29 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from sparse_grushin import build_sparse_grushin_system  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def selected_row(sigma: float) -> dict[str, str]:
    rows = read_csv(RH29 / "results" / "deflated_scale_summary.csv")
    return min(rows, key=lambda row: abs(float(row["sigma"]) - float(sigma)))


def triplet_path(row: dict[str, str]) -> Path:
    return RH29 / row["triplet_file"]


def deterministic_vector(dimension: int, phase: float) -> np.ndarray:
    index = np.arange(int(dimension), dtype=np.float64)
    vector = np.sin(np.sqrt(2.0) * (index + 0.5) + phase)
    vector += 0.29 * np.cos(np.sqrt(7.0) * (index + 0.5) - phase)
    vector = vector.astype(np.complex128)
    vector *= np.exp(0.17j * index / max(int(dimension), 1))
    return vector / np.linalg.norm(vector)


def relative_residual(matrix, solution: np.ndarray, source: np.ndarray) -> float:
    residual = np.asarray(matrix @ solution) - np.asarray(source)
    denominator = max(
        float(np.linalg.norm(source)),
        float(np.linalg.norm(matrix @ solution)),
        np.finfo(float).tiny,
    )
    return float(np.linalg.norm(residual) / denominator)


def inverse_block_iteration(
    matrix,
    factor,
    physical_dimension: int,
    *,
    iterations: int,
    full: bool,
    phase: float,
) -> dict[str, object]:
    """Power iteration for either ``G^{-1}`` or its physical leading block."""

    total = int(matrix.shape[0])
    active = total if full else int(physical_dimension)
    vector = deterministic_vector(active, phase)
    history: list[dict[str, float | int]] = []
    maximum_solve_residual = 0.0
    for iteration in range(int(iterations)):
        source = np.zeros(total, dtype=np.complex128)
        source[:active] = vector
        solution = factor.solve(source)
        maximum_solve_residual = max(
            maximum_solve_residual,
            relative_residual(matrix, solution, source),
        )
        image = np.asarray(solution[:active])
        singular = float(np.linalg.norm(image))
        left = image / singular

        dual_source = np.zeros(total, dtype=np.complex128)
        dual_source[:active] = left
        dual_solution = factor.solve(dual_source, trans="H")
        maximum_solve_residual = max(
            maximum_solve_residual,
            relative_residual(matrix.conj().T, dual_solution, dual_source),
        )
        normal_image = np.asarray(dual_solution[:active])
        triplet_residual = float(np.linalg.norm(normal_image - singular * vector))
        vector = normal_image / np.linalg.norm(normal_image)
        history.append(
            {
                "iteration": iteration + 1,
                "inverse_norm_candidate": singular,
                "triplet_residual": triplet_residual,
            }
        )
    return {
        "inverse_norm_candidate": float(history[-1]["inverse_norm_candidate"]),
        "triplet_residual": float(history[-1]["triplet_residual"]),
        "maximum_relative_solve_residual": maximum_solve_residual,
        "history": history,
    }


def matrix_norms(matrix) -> tuple[float, float]:
    absolute = abs(matrix)
    one = float(np.asarray(absolute.sum(axis=0)).max())
    infinity = float(np.asarray(absolute.sum(axis=1)).max())
    return one, infinity


def peak_megabytes() -> float:
    # Linux reports ru_maxrss in KiB.
    return float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)


def run_scale(
    environment: dict[str, object],
    row: dict[str, str],
    triplet: dict[str, np.ndarray],
    auxiliary_scale: float,
    iterations: int,
    permutation: str,
) -> dict[str, object]:
    spectrum = environment["spectrum"]
    point = complex(
        float(row["spectral_parameter_real"]),
        float(row["spectral_parameter_imag"]),
    )
    build_started = time.time()
    system = build_sparse_grushin_system(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
        triplet["left"],
        triplet["right"],
        float(triplet["singular_value"][0]),
        point,
        auxiliary_scale=float(auxiliary_scale),
    )
    build_seconds = time.time() - build_started
    one_norm, infinity_norm = matrix_norms(system.matrix)
    before_factor_memory = peak_megabytes()
    factor_started = time.time()
    factor = splu(
        system.matrix,
        permc_spec=str(permutation),
        diag_pivot_thresh=1.0,
        options={"Equil": True, "IterRefine": "DOUBLE"},
    )
    factor_seconds = time.time() - factor_started
    after_factor_memory = peak_megabytes()
    factor_nnz = int(factor.L.nnz + factor.U.nnz)

    physical = inverse_block_iteration(
        system.matrix,
        factor,
        system.physical_dimension,
        iterations=iterations,
        full=False,
        phase=0.413,
    )
    full = inverse_block_iteration(
        system.matrix,
        factor,
        system.physical_dimension,
        iterations=iterations,
        full=True,
        phase=0.827,
    )
    budget = float(row["lifted_inverse_budget_lower"])
    return {
        "auxiliary_scale": float(auxiliary_scale),
        "physical_dimension": int(system.physical_dimension),
        "linearized_dimension": int(system.linearized_dimension),
        "border_rank": int(system.update.rank),
        "bordered_dimension": int(system.bordered_dimension),
        "matrix_nnz": int(system.matrix.nnz),
        "matrix_density": float(
            system.matrix.nnz
            / (system.bordered_dimension * system.bordered_dimension)
        ),
        "matrix_one_norm": one_norm,
        "matrix_infinity_norm": infinity_norm,
        "build_seconds": build_seconds,
        "permutation": str(permutation),
        "factor_seconds": factor_seconds,
        "factor_nnz": factor_nnz,
        "factor_fill_ratio": float(factor_nnz / system.matrix.nnz),
        "peak_memory_before_factor_mb": before_factor_memory,
        "peak_memory_after_factor_mb": after_factor_memory,
        "physical_inverse": physical,
        "full_inverse": full,
        "lifted_inverse_budget_lower": budget,
        "physical_budget_margin": float(
            budget / float(physical["inverse_norm_candidate"])
        ),
        "full_budget_margin": float(budget / float(full["inverse_norm_candidate"])),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument(
        "--auxiliary-scales",
        type=float,
        nargs="+",
        default=(0.25, 0.5, 1.0, 2.0, 4.0),
    )
    parser.add_argument("--iterations", type=int, default=8)
    parser.add_argument("--permutation", default="COLAMD")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    sigma = float(arguments.sigma)
    row = selected_row(sigma)
    if abs(float(row["sigma"]) - sigma) > 1.0e-14:
        raise ValueError(f"sigma={sigma:g} is not an archived RH-29 scale")
    setting = rh24.physical_settings()[sigma]
    print(f"building physical environment sigma={sigma:g}", flush=True)
    environment_started = time.time()
    environment = rh25_global.build_environment(sigma, setting)
    environment_seconds = time.time() - environment_started
    with np.load(triplet_path(row)) as archive:
        triplet = {name: np.asarray(archive[name]) for name in archive.files}

    scale_rows = []
    for scale in arguments.auxiliary_scales:
        print(f"factoring auxiliary scale t={scale:g}", flush=True)
        result = run_scale(
            environment,
            row,
            triplet,
            float(scale),
            int(arguments.iterations),
            str(arguments.permutation),
        )
        scale_rows.append(result)
        print(
            "  physical={:.6e}, full={:.6e}, fill={:.2f}, memory={:.1f} MiB".format(
                result["physical_inverse"]["inverse_norm_candidate"],
                result["full_inverse"]["inverse_norm_candidate"],
                result["factor_fill_ratio"],
                result["peak_memory_after_factor_mb"],
            ),
            flush=True,
        )

    payload = {
        "status": "floating_pilot_only",
        "sigma": sigma,
        "environment_seconds": environment_seconds,
        "rh29_lifted_bulk_inverse_candidate": float(
            row["lifted_bulk_inverse_candidate"]
        ),
        "rh29_lifted_inverse_budget_lower": float(
            row["lifted_inverse_budget_lower"]
        ),
        "scales": scale_rows,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    print(rendered, flush=True)
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
