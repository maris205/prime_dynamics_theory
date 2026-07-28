"""Elementary projector-growth models and log-log fits."""

from __future__ import annotations

import numpy as np


def triangular_spectral_projector(
    first_eigenvalue: complex,
    second_eigenvalue: complex,
    coupling: complex,
) -> np.ndarray:
    first = complex(first_eigenvalue)
    second = complex(second_eigenvalue)
    if first == second:
        raise ValueError("distinct eigenvalues are required")
    return np.asarray(
        [[1.0, complex(coupling) / (first - second)], [0.0, 0.0]],
        dtype=complex,
    )


def triangular_projector_norm(
    first_eigenvalue: complex,
    second_eigenvalue: complex,
    coupling: complex,
) -> float:
    projector = triangular_spectral_projector(
        first_eigenvalue, second_eigenvalue, coupling
    )
    return float(np.linalg.norm(projector, 2))


def power_growth_fit(scales: np.ndarray, values: np.ndarray) -> dict[str, float]:
    sigma = np.asarray(scales, dtype=float)
    data = np.asarray(values, dtype=float)
    if sigma.shape != data.shape or np.min(sigma) <= 0.0 or np.min(data) <= 0.0:
        raise ValueError("positive paired samples are required")
    slope, intercept = np.polyfit(np.log(sigma), np.log(data), 1)
    residual = np.log(data) - (slope * np.log(sigma) + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(-slope),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
    }
