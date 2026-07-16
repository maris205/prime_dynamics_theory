"""Floating-point reconnaissance for the RH-28 complement-resolvent gate.

This script deliberately produces candidates rather than certificates.  It
locates the small singular directions that a later block-Grushin enclosure
must isolate, and records residuals independently of the singular values
reported by the iterative solver.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import ArpackNoConvergence, gmres, svds


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
sys.path[:0] = [
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def tightest_arc(sigma: float) -> dict[str, str]:
    rows = read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
    selected = [row for row in rows if float(row["sigma"]) == float(sigma)]
    if not selected:
        raise ValueError(f"sigma={sigma:g} is absent from the RH-28 archive")
    return min(selected, key=lambda row: float(row["resolvent_budget_lower"]))


def singular_candidates(
    operator,
    *,
    count: int,
    solver: str,
    tolerance: float,
    maximum_iterations: int,
) -> dict[str, object]:
    dimension = int(operator.shape[0])
    start = rh25_global.deterministic_start(dimension, 0.413)
    begun = time.time()
    try:
        left, singular, right_h = svds(
            operator,
            k=int(count),
            which="SM",
            solver=str(solver),
            tol=float(tolerance),
            maxiter=int(maximum_iterations),
            v0=start,
            return_singular_vectors=True,
            random_state=1729,
        )
    except ArpackNoConvergence as error:
        return {
            "status": "not_converged",
            "seconds": time.time() - begun,
            "message": str(error).replace("\n", " "),
        }
    except Exception as error:
        return {
            "status": f"error:{type(error).__name__}",
            "seconds": time.time() - begun,
            "message": str(error).replace("\n", " "),
        }

    order = np.argsort(singular)
    singular = np.asarray(singular)[order]
    left = np.asarray(left)[:, order]
    right = np.asarray(right_h).conj().T[:, order]
    residuals = []
    for index, value in enumerate(singular):
        first = np.linalg.norm(operator @ right[:, index] - value * left[:, index])
        second = np.linalg.norm(operator.H @ left[:, index] - value * right[:, index])
        residuals.append(float(max(first, second)))
    left_gram = np.linalg.norm(left.conj().T @ left - np.eye(len(singular)), 2)
    right_gram = np.linalg.norm(right.conj().T @ right - np.eye(len(singular)), 2)
    return {
        "status": "converged",
        "seconds": time.time() - begun,
        "singular_candidates": [float(value) for value in singular],
        "resolvent_candidates": [float(1.0 / value) for value in singular],
        "singular_triplet_residuals": residuals,
        "left_orthogonality_defect": float(left_gram),
        "right_orthogonality_defect": float(right_gram),
        "message": "",
    }


def _gmres_solve(operator, source: np.ndarray, tolerance: float) -> tuple[np.ndarray, int, float]:
    history: list[float] = []
    source_norm = float(np.linalg.norm(source))
    solution, info = gmres(
        operator,
        source,
        rtol=0.0,
        atol=float(tolerance) * max(source_norm, np.finfo(float).tiny),
        restart=160,
        maxiter=80,
        callback=lambda value: history.append(float(value)),
        callback_type="pr_norm",
    )
    if int(info) != 0:
        raise RuntimeError(f"GMRES did not converge: info={info}, iterations={len(history)}")
    residual = float(np.linalg.norm(operator @ solution - source) / source_norm)
    return np.asarray(solution), len(history), residual


def inverse_iteration_candidate(
    operator,
    *,
    tolerance: float,
    maximum_iterations: int,
) -> dict[str, object]:
    """Find the smallest singular direction by inverse normal iteration."""

    dimension = int(operator.shape[0])
    vector = rh25_global.deterministic_start(dimension, 0.413)
    previous = np.inf
    rows: list[dict[str, object]] = []
    begun = time.time()
    try:
        for iteration in range(int(maximum_iterations)):
            dual, dual_iterations, dual_residual = _gmres_solve(
                operator.H, vector, tolerance
            )
            updated, primal_iterations, primal_residual = _gmres_solve(
                operator, dual, tolerance
            )
            updated_norm = float(np.linalg.norm(updated))
            if updated_norm == 0.0 or not np.isfinite(updated_norm):
                raise RuntimeError("inverse iteration produced an invalid vector")
            vector = updated / updated_norm
            image = operator @ vector
            singular = float(np.linalg.norm(image))
            left = image / singular
            triplet_residual = float(np.linalg.norm(operator.H @ left - singular * vector))
            change = float(abs(previous - singular) / max(singular, np.finfo(float).tiny))
            rows.append(
                {
                    "iteration": iteration + 1,
                    "singular_candidate": singular,
                    "relative_change": change,
                    "triplet_residual": triplet_residual,
                    "primal_gmres_iterations": primal_iterations,
                    "dual_gmres_iterations": dual_iterations,
                    "primal_relative_residual": primal_residual,
                    "dual_relative_residual": dual_residual,
                }
            )
            print(
                f"  inverse iteration {iteration + 1}: s={singular:.8e}, "
                f"triplet={triplet_residual:.3e}, "
                f"gmres={dual_iterations}+{primal_iterations}",
                flush=True,
            )
            if change <= max(10.0 * tolerance, 1.0e-12) and triplet_residual <= max(
                100.0 * tolerance, 1.0e-10
            ):
                break
            previous = singular
    except Exception as error:
        return {
            "status": f"error:{type(error).__name__}",
            "seconds": time.time() - begun,
            "message": str(error).replace("\n", " "),
            "inverse_iteration_history": rows,
        }
    return {
        "status": "converged",
        "seconds": time.time() - begun,
        "singular_candidates": [float(rows[-1]["singular_candidate"])],
        "resolvent_candidates": [float(1.0 / rows[-1]["singular_candidate"])],
        "singular_triplet_residuals": [float(rows[-1]["triplet_residual"])],
        "inverse_iteration_history": rows,
        "message": "",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, required=True)
    parser.add_argument(
        "--solver",
        choices=("arpack", "propack", "lobpcg", "inverse"),
        default="inverse",
    )
    parser.add_argument("--count", type=int, default=4)
    parser.add_argument("--tolerance", type=float, default=1.0e-10)
    parser.add_argument("--maximum-iterations", type=int, default=4000)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    sigma = float(arguments.sigma)
    setting = rh24.physical_settings()[sigma]
    arc = tightest_arc(sigma)
    spectral_parameter = complex(
        float(arc["center_real"]), float(arc["center_imag"])
    )
    print(
        f"build sigma={sigma:g}, n={setting['dimension']}, z={spectral_parameter}",
        flush=True,
    )
    build_started = time.time()
    environment = rh25_global.add_adjoint_actions(
        rh25_global.build_environment(sigma, setting)
    )
    build_seconds = time.time() - build_started
    operator = rh25_global.shifted_operator(environment, spectral_parameter)
    print(
        f"solve {arguments.solver}, k={arguments.count}, build={build_seconds:.3f}s",
        flush=True,
    )
    if arguments.solver == "inverse":
        candidates = inverse_iteration_candidate(
            operator,
            tolerance=float(arguments.tolerance),
            maximum_iterations=int(arguments.maximum_iterations),
        )
    else:
        candidates = singular_candidates(
            operator,
            count=int(arguments.count),
            solver=str(arguments.solver),
            tolerance=float(arguments.tolerance),
            maximum_iterations=int(arguments.maximum_iterations),
        )
    result = {
        "sigma": sigma,
        "dimension": int(setting["dimension"]),
        "packet_rank": int(environment["analysis"].shape[0]),
        "arc": int(arc["arc"]),
        "spectral_parameter_real": spectral_parameter.real,
        "spectral_parameter_imag": spectral_parameter.imag,
        "arc_disc_radius": float(arc["disc_radius"]),
        "rh28_resolvent_budget_lower": float(arc["resolvent_budget_lower"]),
        "rh28_reciprocal_budget": float(1.0 / float(arc["resolvent_budget_lower"])),
        "solver": str(arguments.solver),
        "requested_count": int(arguments.count),
        "tolerance": float(arguments.tolerance),
        "maximum_iterations": int(arguments.maximum_iterations),
        "build_seconds": build_seconds,
        **candidates,
    }
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
