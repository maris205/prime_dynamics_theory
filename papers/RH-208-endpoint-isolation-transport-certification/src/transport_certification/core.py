"""Local numerical budgets used before an interval certification attempt."""

from __future__ import annotations

import numpy as np


def eigenpair_condition(right: np.ndarray, left: np.ndarray) -> float:
    vector = np.asarray(right, dtype=complex).reshape(-1)
    dual = np.asarray(left, dtype=complex).reshape(-1)
    overlap = abs(np.vdot(dual, vector))
    if overlap <= np.finfo(float).tiny:
        raise ValueError("left and right eigenvectors must pair nontrivially")
    return float(np.linalg.norm(vector) * np.linalg.norm(dual) / overlap)


def isolation_budget(
    residual_norm: float, eigenpair_condition_number: float, spectral_separation: float
) -> float:
    """Return kappa*residual/(separation/2), a feasibility ratio."""

    residual = float(residual_norm)
    condition = float(eigenpair_condition_number)
    separation = float(spectral_separation)
    if residual < 0.0 or condition < 1.0 or separation <= 0.0:
        raise ValueError("invalid isolation budget data")
    return 2.0 * condition * residual / separation


def transport_residual(
    fine_operator: np.ndarray,
    embedding: np.ndarray,
    coarse_vector: np.ndarray,
    coarse_eigenvalue: complex,
) -> float:
    fine = np.asarray(fine_operator, dtype=complex)
    lift = np.asarray(embedding, dtype=complex)
    vector = np.asarray(coarse_vector, dtype=complex).reshape(-1)
    lifted = lift @ vector
    return float(np.linalg.norm(fine @ lifted - complex(coarse_eigenvalue) * lifted))
