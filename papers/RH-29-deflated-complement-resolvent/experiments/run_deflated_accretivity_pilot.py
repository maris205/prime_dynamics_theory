"""Test whether lifting the smallest singular direction restores accretivity."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh


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
from run_resolvent_pilot import _gmres_solve, tightest_arc  # noqa: E402


def smallest_triplet(operator, tolerance: float, iterations: int):
    dimension = int(operator.shape[0])
    vector = rh25_global.deterministic_start(dimension, 0.413)
    for _ in range(int(iterations)):
        dual, _, _ = _gmres_solve(operator.H, vector, tolerance)
        updated, _, _ = _gmres_solve(operator, dual, tolerance)
        vector = updated / np.linalg.norm(updated)
    image = operator @ vector
    singular = float(np.linalg.norm(image))
    left = image / singular
    residual = float(np.linalg.norm(operator.H @ left - singular * vector))
    return singular, np.asarray(left), np.asarray(vector), residual


def lifted_operator(operator, left, right, singular: float, lift: float):
    coefficient = float(lift) - float(singular)
    return LinearOperator(
        operator.shape,
        matvec=lambda vector: operator @ vector
        + coefficient * left * np.vdot(right, vector),
        rmatvec=lambda vector: operator.H @ vector
        + coefficient * right * np.vdot(left, vector),
        dtype=np.complex128,
    )


def hermitian_part(operator, phase: float):
    rotation = np.exp(-1.0j * float(phase))
    return LinearOperator(
        operator.shape,
        matvec=lambda vector: 0.5
        * (rotation * (operator @ vector) + np.conj(rotation) * (operator.H @ vector)),
        dtype=np.complex128,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--lift", type=float, nargs="*", default=(0.05, 0.1, 0.5, 1.0))
    parser.add_argument("--phases", type=int, default=24)
    parser.add_argument("--tolerance", type=float, default=1.0e-10)
    parser.add_argument("--inverse-iterations", type=int, default=4)
    parser.add_argument("--eigsh-tolerance", type=float, default=1.0e-8)
    parser.add_argument("--eigsh-iterations", type=int, default=1200)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    sigma = float(arguments.sigma)
    setting = rh24.physical_settings()[sigma]
    arc = tightest_arc(sigma)
    point = complex(float(arc["center_real"]), float(arc["center_imag"]))
    environment = rh25_global.add_adjoint_actions(
        rh25_global.build_environment(sigma, setting)
    )
    operator = rh25_global.shifted_operator(environment, point)
    singular, left, right, residual = smallest_triplet(
        operator, float(arguments.tolerance), int(arguments.inverse_iterations)
    )
    phases = 2.0 * np.pi * np.arange(int(arguments.phases)) / int(arguments.phases)
    rows = []
    for lift in arguments.lift:
        lifted = lifted_operator(operator, left, right, singular, float(lift))
        start = right.copy()
        for phase in phases:
            begun = time.time()
            value, vector = eigsh(
                hermitian_part(lifted, float(phase)),
                k=1,
                which="SA",
                v0=start,
                tol=float(arguments.eigsh_tolerance),
                maxiter=int(arguments.eigsh_iterations),
            )
            start = np.asarray(vector[:, 0])
            rows.append(
                {
                    "lift": float(lift),
                    "phase": float(phase),
                    "minimum_hermitian_candidate": float(value[0]),
                    "seconds": time.time() - begun,
                }
            )
            print(
                f"lift={lift:g}, phase/pi={phase / np.pi:.3f}, "
                f"lambda_min={value[0]:.6e}",
                flush=True,
            )
    result = {
        "sigma": sigma,
        "dimension": int(setting["dimension"]),
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
        "singular_candidate": singular,
        "singular_triplet_residual": residual,
        "maximum_minimum_hermitian_candidate": max(
            float(row["minimum_hermitian_candidate"]) for row in rows
        ),
        "rows": rows,
    }
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
