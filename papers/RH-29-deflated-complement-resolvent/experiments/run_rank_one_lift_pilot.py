"""Measure the bulk singular gap after lifting one dangerous direction."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
sys.path[:0] = [
    str(ROOT / "experiments"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from run_deflated_accretivity_pilot import (  # noqa: E402
    lifted_operator,
    smallest_triplet,
)
from run_resolvent_pilot import _gmres_solve, tightest_arc  # noqa: E402


def inverse_triplet(operator, tolerance: float, iterations: int, phase: float):
    dimension = int(operator.shape[0])
    vector = rh25_global.deterministic_start(dimension, phase)
    history = []
    for iteration in range(int(iterations)):
        begun = time.time()
        dual, dual_iterations, dual_residual = _gmres_solve(
            operator.H, vector, tolerance
        )
        updated, primal_iterations, primal_residual = _gmres_solve(
            operator, dual, tolerance
        )
        vector = updated / np.linalg.norm(updated)
        image = operator @ vector
        singular = float(np.linalg.norm(image))
        left = image / singular
        triplet = float(np.linalg.norm(operator.H @ left - singular * vector))
        history.append(
            {
                "iteration": iteration + 1,
                "singular_candidate": singular,
                "triplet_residual": triplet,
                "dual_gmres_iterations": dual_iterations,
                "primal_gmres_iterations": primal_iterations,
                "dual_relative_residual": dual_residual,
                "primal_relative_residual": primal_residual,
                "seconds": time.time() - begun,
            }
        )
        print(
            f"  lifted iteration {iteration + 1}: s={singular:.8e}, "
            f"triplet={triplet:.3e}, gmres={dual_iterations}+{primal_iterations}",
            flush=True,
        )
    return singular, triplet, history


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, required=True)
    parser.add_argument("--lift", type=float, default=1.0)
    parser.add_argument("--tolerance", type=float, default=1.0e-9)
    parser.add_argument("--first-iterations", type=int, default=3)
    parser.add_argument("--lifted-iterations", type=int, default=5)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    sigma = float(arguments.sigma)
    setting = rh24.physical_settings()[sigma]
    arc = tightest_arc(sigma)
    point = complex(float(arc["center_real"]), float(arc["center_imag"]))
    build_started = time.time()
    environment = rh25_global.add_adjoint_actions(
        rh25_global.build_environment(sigma, setting)
    )
    operator = rh25_global.shifted_operator(environment, point)
    build_seconds = time.time() - build_started
    print(f"first direction sigma={sigma:g}, n={setting['dimension']}", flush=True)
    first, left, right, first_residual = smallest_triplet(
        operator, float(arguments.tolerance), int(arguments.first_iterations)
    )
    lifted = lifted_operator(operator, left, right, first, float(arguments.lift))
    second, second_residual, history = inverse_triplet(
        lifted,
        float(arguments.tolerance),
        int(arguments.lifted_iterations),
        0.827,
    )
    result = {
        "sigma": sigma,
        "dimension": int(setting["dimension"]),
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
        "build_seconds": build_seconds,
        "first_singular_candidate": first,
        "first_triplet_residual": first_residual,
        "lift": float(arguments.lift),
        "lifted_smallest_singular_candidate": second,
        "lifted_triplet_residual": second_residual,
        "candidate_gap_ratio": float(second / first),
        "history": history,
    }
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
