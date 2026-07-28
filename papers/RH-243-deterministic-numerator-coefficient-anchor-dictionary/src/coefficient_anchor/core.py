"""One-step, two-step, and Hardy-scaled numerator coefficient dictionaries."""

from __future__ import annotations

import numpy as np


HARDY_RADIUS = 0.85


def centered_deterministic_trace(flat_trace: float, order: int) -> float:
    """Return ``P_n - 1 - (-1)^n``."""

    n = int(order)
    if n < 2:
        raise ValueError("the regularized trace order must be at least two")
    return float(flat_trace) - 1.0 - (-1.0) ** n


def one_step_numerator_trace_coefficient(
    flat_trace: float,
    order: int,
    determinant_lambda: float,
    *,
    hardy_radius: float = HARDY_RADIUS,
) -> float:
    """Return the Hardy-scaled trace-style coefficient of the numerator G."""

    n = int(order)
    lam = float(determinant_lambda)
    radius = float(hardy_radius)
    if n < 2 or lam <= 1.0 or not 0.0 < radius < 1.0:
        raise ValueError("valid order, pole parameter, and Hardy radius are required")
    centered = centered_deterministic_trace(flat_trace, n)
    pole_correction = 2.0 * lam ** (-n / 2.0) if n % 2 == 0 else 0.0
    return float((centered + pole_correction) * radius ** (-n))


def one_step_anchor_array(
    flat_traces: np.ndarray,
    first_order: int,
    determinant_lambda: float,
    *,
    hardy_radius: float = HARDY_RADIUS,
) -> np.ndarray:
    """Convert consecutive deterministic flat traces to numerator coefficients."""

    traces = np.asarray(flat_traces, dtype=float).reshape(-1)
    first = int(first_order)
    return np.asarray([
        one_step_numerator_trace_coefficient(
            trace,
            first + index,
            determinant_lambda,
            hardy_radius=hardy_radius,
        )
        for index, trace in enumerate(traces)
    ])


def two_step_anchor_from_one_step(
    one_step_orders: np.ndarray,
    one_step_coefficients: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return ``b_k=a_(2k)`` for the symmetric two-step numerator."""

    orders = np.asarray(one_step_orders, dtype=int).reshape(-1)
    values = np.asarray(one_step_coefficients, dtype=complex).reshape(-1)
    if orders.shape != values.shape:
        raise ValueError("orders and coefficients must have matching shapes")
    mask = orders % 2 == 0
    return orders[mask] // 2, values[mask]


def trace_log_jet(
    orders: np.ndarray,
    coefficients: np.ndarray,
    variable: complex,
) -> complex:
    """Evaluate ``-sum a_n z^n/n`` for a finite trace-style jet."""

    n = np.asarray(orders, dtype=int).reshape(-1)
    values = np.asarray(coefficients, dtype=complex).reshape(-1)
    if n.shape != values.shape or np.min(n, initial=1) < 1:
        raise ValueError("valid paired orders and coefficients are required")
    z = complex(variable)
    return complex(-np.sum(values * z**n / n))


def exponential_coefficients_from_trace(
    trace_coefficients: np.ndarray,
    maximum_degree: int,
) -> np.ndarray:
    """Return Taylor coefficients of ``exp(-sum a_n z^n/n)`` through a degree."""

    degree = int(maximum_degree)
    traces = np.asarray(trace_coefficients, dtype=complex).reshape(-1)
    if degree < 0 or traces.size < degree + 1:
        raise ValueError("trace_coefficients must include indices zero through degree")
    logarithm = np.zeros(degree + 1, dtype=complex)
    for n in range(1, degree + 1):
        logarithm[n] = -traces[n] / n
    coefficients = np.zeros(degree + 1, dtype=complex)
    coefficients[0] = 1.0
    for n in range(1, degree + 1):
        coefficients[n] = sum(
            k * logarithm[k] * coefficients[n - k] for k in range(1, n + 1)
        ) / n
    return coefficients


def anchored_jet_distance(
    residual: np.ndarray,
    anchor: np.ndarray,
    *,
    first_order: int = 2,
    radius: float = 1.0,
) -> float:
    """Return the finite logarithmic distance from a prescribed anchor."""

    values = np.asarray(residual, dtype=complex).reshape(-1)
    target = np.asarray(anchor, dtype=complex).reshape(-1)
    if values.shape != target.shape:
        raise ValueError("residual and anchor arrays must match")
    first = int(first_order)
    disk = float(radius)
    if first < 1 or first > values.size or disk < 0.0:
        raise ValueError("invalid first order or radius")
    orders = np.arange(first, values.size + 1)
    return float(np.sum(np.abs(values[first - 1 :] - target[first - 1 :]) * disk**orders / orders))
