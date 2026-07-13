"""Finite weighted-zeta and postcritical-deflation diagnostics."""

from __future__ import annotations

import numpy as np

from .periodic import LAMBDA_FIXED


def postcritical_model(
    two_step_length: int | np.ndarray,
    *,
    dtype: type = np.longdouble,
) -> np.ndarray:
    """Return ``1-lambda**(-n)+lambda**(-2*n)``.

    This is the coefficient sequence of the Perron pole together with the
    exact postcritical factor ``(1-z/lambda)/(1-z/lambda**2)``.
    """

    length = np.asarray(two_step_length, dtype=np.int64)
    if np.any(length < 1):
        raise ValueError("two_step_length must be positive")
    lam = dtype(LAMBDA_FIXED)
    return np.asarray(
        dtype(1) - lam ** (-length) + lam ** (-2 * length),
        dtype=dtype,
    )


def postcritical_remainder(weighted_traces: np.ndarray) -> np.ndarray:
    """Deflate the Perron and exact postcritical trace coefficients."""

    traces = np.asarray(weighted_traces, dtype=np.longdouble)
    if traces.ndim != 1 or traces.size < 1:
        raise ValueError("weighted_traces must be a nonempty one-dimensional array")
    lengths = np.arange(1, traces.size + 1, dtype=np.int64)
    return traces - postcritical_model(lengths)


def exponential_series(log_coefficients: np.ndarray) -> np.ndarray:
    """Exponentiate a formal power series through its available degree."""

    values = np.asarray(log_coefficients, dtype=np.complex128)
    if values.ndim != 1 or values.size < 1:
        raise ValueError("log_coefficients must be a nonempty one-dimensional array")
    degree = values.size - 1
    result = np.zeros(degree + 1, dtype=np.complex128)
    result[0] = np.exp(values[0])
    for n in range(1, degree + 1):
        result[n] = sum(
            k * values[k] * result[n - k] for k in range(1, n + 1)
        ) / n
    return result


def centered_zeta_series(weighted_traces: np.ndarray) -> np.ndarray:
    """Taylor series of ``H(z)=(1-z) Z(z)`` from periodic traces."""

    traces = np.asarray(weighted_traces, dtype=np.longdouble)
    if traces.ndim != 1 or traces.size < 1:
        raise ValueError("weighted_traces must be a nonempty one-dimensional array")
    log_coefficients = np.zeros(traces.size + 1, dtype=np.complex128)
    for n, value in enumerate(traces, start=1):
        log_coefficients[n] = (float(value) - 1.0) / n
    return exponential_series(log_coefficients)


def deflated_zeta_series(weighted_traces: np.ndarray) -> np.ndarray:
    """Taylor series of the postcritical-deflated remainder ``G(z)``."""

    remainder = postcritical_remainder(weighted_traces)
    log_coefficients = np.zeros(remainder.size + 1, dtype=np.complex128)
    for n, value in enumerate(remainder, start=1):
        log_coefficients[n] = float(value) / n
    return exponential_series(log_coefficients)


def flat_determinant_series(flat_traces: np.ndarray) -> np.ndarray:
    """Taylor series of ``exp(-sum trace_n*z**n/n)``."""

    traces = np.asarray(flat_traces, dtype=np.longdouble)
    if traces.ndim != 1 or traces.size < 1:
        raise ValueError("flat_traces must be a nonempty one-dimensional array")
    log_coefficients = np.zeros(traces.size + 1, dtype=np.complex128)
    for n, value in enumerate(traces, start=1):
        log_coefficients[n] = -float(value) / n
    return exponential_series(log_coefficients)


def smallest_positive_real_root(
    coefficients: np.ndarray,
    *,
    imaginary_tolerance: float = 1.0e-7,
) -> float:
    """Return the smallest positive numerically real polynomial root."""

    values = np.asarray(coefficients, dtype=np.complex128)
    if values.ndim != 1 or values.size < 2:
        raise ValueError("coefficients must contain a nonconstant polynomial")
    roots = np.roots(values[::-1])
    candidates = [
        root.real
        for root in roots
        if root.real > 0.0 and abs(root.imag) <= imaginary_tolerance
    ]
    if not candidates:
        raise RuntimeError("no positive real root found")
    return float(min(candidates))


def partial_log_g(
    weighted_traces: np.ndarray,
    z: float | np.longdouble,
) -> np.longdouble:
    """Evaluate ``sum_{n<=N} e_n z**n/n`` in long-double arithmetic."""

    remainder = postcritical_remainder(weighted_traces)
    argument = np.longdouble(z)
    lengths = np.arange(1, remainder.size + 1, dtype=np.int64)
    terms = remainder * argument**lengths / lengths
    return np.sum(terms, dtype=np.longdouble)
