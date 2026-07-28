"""Schur-Frobenius eigenvalue-tail budgets for det2 products."""

from __future__ import annotations

import numpy as np


def eigenvalue_squared_tail_budget(
    frobenius_squared: float, selected_eigenvalues: np.ndarray
) -> float:
    total = float(frobenius_squared)
    if total < 0.0:
        raise ValueError("the Frobenius square must be nonnegative")
    selected = np.asarray(selected_eigenvalues, dtype=complex).reshape(-1)
    return float(max(0.0, total - np.sum(np.abs(selected) ** 2)))


def det2_log_tail_upper(squared_tail_budget: float, modulus_upper: float, radius: float) -> float:
    mass = float(squared_tail_budget)
    bound = float(modulus_upper)
    disk = float(radius)
    if mass < 0.0 or bound < 0.0 or disk < 0.0:
        raise ValueError("budgets must be nonnegative")
    q = disk * bound
    if q >= 1.0:
        raise ValueError("the disk reaches the tail reciprocal radius")
    return float(disk**2 * mass / (2.0 * (1.0 - q)))


def power_growth_fit(scales: np.ndarray, values: np.ndarray) -> dict[str, float]:
    sigma = np.asarray(scales, dtype=float)
    data = np.asarray(values, dtype=float)
    if np.min(sigma) <= 0.0 or np.min(data) <= 0.0 or sigma.size != data.size:
        raise ValueError("positive paired samples are required")
    slope, intercept = np.polyfit(np.log(sigma), np.log(data), 1)
    residual = np.log(data) - (slope * np.log(sigma) + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(-slope),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
    }
