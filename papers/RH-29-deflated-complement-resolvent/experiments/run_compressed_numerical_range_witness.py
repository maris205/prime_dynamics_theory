"""Find a finite witness obstructing accretivity after rank-one lifting."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import eigsh


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
    hermitian_part,
    lifted_operator,
    smallest_triplet,
)
from run_resolvent_pilot import tightest_arc  # noqa: E402


def barycentric_origin(points: np.ndarray) -> np.ndarray:
    matrix = np.vstack(
        [np.asarray(points).real, np.asarray(points).imag, np.ones(3)]
    )
    return np.linalg.solve(matrix, np.array([0.0, 0.0, 1.0]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--lift", type=float, default=1.0)
    parser.add_argument("--tolerance", type=float, default=1.0e-11)
    parser.add_argument("--inverse-iterations", type=int, default=4)
    parser.add_argument("--eigsh-tolerance", type=float, default=1.0e-10)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--vectors", type=Path)
    arguments = parser.parse_args()

    sigma = float(arguments.sigma)
    setting = rh24.physical_settings()[sigma]
    arc = tightest_arc(sigma)
    point = complex(float(arc["center_real"]), float(arc["center_imag"]))
    environment = rh25_global.add_adjoint_actions(
        rh25_global.build_environment(sigma, setting)
    )
    operator = rh25_global.shifted_operator(environment, point)
    singular, left, right, triplet_residual = smallest_triplet(
        operator, float(arguments.tolerance), int(arguments.inverse_iterations)
    )
    lifted = lifted_operator(operator, left, right, singular, float(arguments.lift))
    phases = 2.0 * np.pi * np.arange(3) / 3.0
    vectors = []
    points = []
    minima = []
    orthogonality = []
    start = right.copy()
    for phase in phases:
        value, vector = eigsh(
            hermitian_part(lifted, float(phase)),
            k=1,
            which="SA",
            v0=start,
            tol=float(arguments.eigsh_tolerance),
            maxiter=2000,
        )
        candidate = np.asarray(vector[:, 0])
        candidate = candidate - right * np.vdot(right, candidate)
        candidate /= np.linalg.norm(candidate)
        start = candidate
        vectors.append(candidate)
        points.append(complex(np.vdot(candidate, operator @ candidate)))
        minima.append(float(value[0]))
        orthogonality.append(float(abs(np.vdot(right, candidate))))
    points_array = np.asarray(points)
    weights = barycentric_origin(points_array)
    reconstruction = complex(np.dot(weights, points_array))
    result = {
        "sigma": sigma,
        "dimension": int(setting["dimension"]),
        "lift": float(arguments.lift),
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
        "singular_candidate": singular,
        "singular_triplet_residual": triplet_residual,
        "phases": [float(value) for value in phases],
        "minimum_hermitian_candidates": minima,
        "rayleigh_points_real": [float(value.real) for value in points],
        "rayleigh_points_imag": [float(value.imag) for value in points],
        "barycentric_weights": [float(value) for value in weights],
        "minimum_barycentric_weight": float(np.min(weights)),
        "origin_reconstruction_absolute": float(abs(reconstruction)),
        "maximum_right_orthogonality_defect": max(orthogonality),
    }
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if arguments.vectors is not None:
        arguments.vectors.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            arguments.vectors,
            right=right,
            witnesses=np.column_stack(vectors),
            points=points_array,
            weights=weights,
        )


if __name__ == "__main__":
    main()
