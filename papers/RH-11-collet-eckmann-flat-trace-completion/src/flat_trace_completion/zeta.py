"""Finite power-series diagnostics for the centered component zeta function."""

from __future__ import annotations

import numpy as np

from .periodic import LAMBDA_FIXED, component_weighted_traces


def exponential_series(log_coefficients: np.ndarray) -> np.ndarray:
    """Exponentiate a power series through its available degree."""

    coefficients = np.asarray(log_coefficients, dtype=np.complex128)
    if coefficients.ndim != 1 or coefficients.size < 1:
        raise ValueError("log_coefficients must be a nonempty one-dimensional array")
    degree = coefficients.size - 1
    result = np.zeros(degree + 1, dtype=np.complex128)
    result[0] = np.exp(coefficients[0])
    for n in range(1, degree + 1):
        result[n] = sum(
            k * coefficients[k] * result[n - k] for k in range(1, n + 1)
        ) / n
    return result


def component_weighted_coefficients(maximum_two_step_length: int) -> np.ndarray:
    if maximum_two_step_length < 1:
        raise ValueError("maximum_two_step_length must be positive")
    values = []
    for two_step_length in range(1, maximum_two_step_length + 1):
        central, high = component_weighted_traces(2 * two_step_length)
        if abs(central - high) > 2.0e-8:
            raise RuntimeError("component weighted traces failed to match")
        values.append(0.5 * (central + high))
    return np.asarray(values, dtype=np.float64)


def centered_component_zeta_series(weighted_coefficients: np.ndarray) -> np.ndarray:
    """Series of ``(1-z) Z(z)`` from component periodic weights."""

    weighted = np.asarray(weighted_coefficients, dtype=np.float64)
    log_series = np.zeros(weighted.size + 1, dtype=np.complex128)
    for n, value in enumerate(weighted, start=1):
        log_series[n] = (value - 1.0) / n
    return exponential_series(log_series)


def smallest_positive_real_root(coefficients: np.ndarray, tolerance: float = 1.0e-7) -> float:
    values = np.asarray(coefficients, dtype=np.complex128)
    roots = np.roots(values[::-1])
    candidates = [root.real for root in roots if abs(root.imag) < tolerance and root.real > 0.0]
    if not candidates:
        raise RuntimeError("no positive real root found")
    return float(min(candidates))


def critical_zero_deflated_coefficients(weighted_coefficients: np.ndarray) -> np.ndarray:
    """Return ``q_n - 1 + lambda^{-n}``, which removes the observed first zero."""

    weighted = np.asarray(weighted_coefficients, dtype=np.float64)
    lengths = np.arange(1, weighted.size + 1, dtype=np.float64)
    return weighted - 1.0 + LAMBDA_FIXED ** (-lengths)
