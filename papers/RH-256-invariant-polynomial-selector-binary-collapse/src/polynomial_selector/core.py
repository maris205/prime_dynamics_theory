"""Polynomial coordinates for invariant spectral selectors."""

from __future__ import annotations

import numpy as np


def interpolation_coefficients(eigenvalues: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Return monomial coefficients of the simple-spectrum selector polynomial."""

    roots = np.asarray(eigenvalues, dtype=complex).reshape(-1)
    values = np.asarray(mask, dtype=complex).reshape(-1)
    if roots.size == 0 or roots.size != values.size:
        raise ValueError("eigenvalues and mask must be nonempty and have equal size")
    if np.min(np.abs(roots[:, None] - roots[None, :] + np.eye(roots.size))) == 0.0:
        raise ValueError("distinct eigenvalues are required")
    vandermonde = np.vander(roots, N=roots.size, increasing=True)
    return np.linalg.solve(vandermonde, values)


def polynomial_values(coefficients: np.ndarray, points: np.ndarray) -> np.ndarray:
    return np.polynomial.polynomial.polyval(
        np.asarray(points, dtype=complex), np.asarray(coefficients, dtype=complex)
    )


def nodal_idempotence_error(coefficients: np.ndarray, eigenvalues: np.ndarray) -> float:
    values = polynomial_values(coefficients, eigenvalues)
    return float(np.max(np.abs(values * values - values)))


def selected_power_traces(eigenvalues: np.ndarray, mask: np.ndarray, orders: np.ndarray) -> np.ndarray:
    roots = np.asarray(eigenvalues, dtype=complex).reshape(-1)
    weights = np.asarray(mask, dtype=complex).reshape(-1)
    powers = np.asarray(orders, dtype=int).reshape(-1)
    if roots.size != weights.size or np.any(powers < 1):
        raise ValueError("mask and spectrum must match and orders be positive")
    return np.asarray([np.sum(weights * roots**order) for order in powers])
