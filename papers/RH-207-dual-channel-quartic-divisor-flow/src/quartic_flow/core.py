"""Similarity-invariant scalar data of a finite spectral quartet."""

from __future__ import annotations

import numpy as np


def monic_coefficients(values: np.ndarray) -> np.ndarray:
    packet = np.asarray(values, dtype=complex).reshape(-1)
    if packet.size < 1:
        raise ValueError("a nonempty packet is required")
    return np.poly(packet)


def coefficient_comparison(first: np.ndarray, second: np.ndarray) -> dict[str, float]:
    left = monic_coefficients(first)
    right = monic_coefficients(second)
    if left.shape != right.shape:
        raise ValueError("packets must have equal degree")
    difference = left - right
    return {
        "relative_l2_error": float(np.linalg.norm(difference) / max(np.linalg.norm(left), np.finfo(float).tiny)),
        "maximum_absolute_error": float(np.max(np.abs(difference))),
        "constant_term_relative_error": float(abs(left[-1] - right[-1]) / max(abs(left[-1]), np.finfo(float).tiny)),
    }


def newton_traces(coefficients: np.ndarray, maximum_power: int) -> np.ndarray:
    """Recover power sums from monic polynomial coefficients."""

    coeff = np.asarray(coefficients, dtype=complex).reshape(-1)
    degree = coeff.size - 1
    if degree < 1 or abs(coeff[0] - 1.0) > 1e-12 or maximum_power < 1:
        raise ValueError("monic coefficients and a positive power are required")
    traces = np.zeros(int(maximum_power), dtype=complex)
    for power in range(1, int(maximum_power) + 1):
        total = 0.0j
        for index in range(1, min(power, degree) + 1):
            if index == power:
                total += power * coeff[index]
            else:
                total += coeff[index] * traces[power - index - 1]
        traces[power - 1] = -total
    return traces
