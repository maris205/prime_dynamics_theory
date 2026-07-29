"""Finite deterministic numerator anchor calculations."""

from __future__ import annotations

import numpy as np


def hardy_scaled_anchor(
    flat_trace: float,
    order: int,
    determinant_lambda: float,
    hardy_radius: float = 0.85,
) -> float:
    """Evaluate the exact RH-243 coefficient dictionary at one order."""

    n = int(order)
    lam = float(determinant_lambda)
    radius = float(hardy_radius)
    if n < 2 or lam <= 1.0 or not 0.0 < radius < 1.0:
        raise ValueError("invalid order, multiplier, or Hardy radius")
    centered = float(flat_trace) - 1.0 - (-1.0) ** n
    correction = 2.0 * lam ** (-n / 2.0) if n % 2 == 0 else 0.0
    return float((centered + correction) * radius ** (-n))


def finite_logarithmic_norm(
    orders: np.ndarray,
    coefficients: np.ndarray,
    radius: float = 1.0,
) -> float:
    powers = np.asarray(orders, dtype=float).reshape(-1)
    values = np.asarray(coefficients, dtype=complex).reshape(-1)
    disk = float(radius)
    if powers.size != values.size or np.any(powers <= 0.0) or disk < 0.0:
        raise ValueError("orders and coefficients must match and the radius be nonnegative")
    return float(np.sum(np.abs(values) * disk**powers / powers))


def log_linear_root_rate(orders: np.ndarray, coefficients: np.ndarray) -> float:
    """Return the descriptive exponential rate from a log-linear fit."""

    powers = np.asarray(orders, dtype=float).reshape(-1)
    values = np.abs(np.asarray(coefficients, dtype=complex).reshape(-1))
    if powers.size != values.size or powers.size < 2 or np.any(values <= 0.0):
        raise ValueError("positive coefficients at two or more orders are required")
    slope = np.polyfit(powers, np.log(values), 1)[0]
    return float(np.exp(slope))


def ordinary_coefficients_from_traces(trace_coefficients: np.ndarray) -> np.ndarray:
    """Exponentiate ``-sum a_n z^n/n`` through the available degree."""

    traces = np.asarray(trace_coefficients, dtype=complex).reshape(-1)
    degree = traces.size - 1
    if degree < 0:
        raise ValueError("a coefficient array is required")
    result = np.zeros(degree + 1, dtype=complex)
    result[0] = 1.0
    for n in range(1, degree + 1):
        result[n] = -sum(traces[k] * result[n - k] for k in range(1, n + 1)) / n
    return result
