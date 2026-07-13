"""Chunked statistics for logarithmic and endpoint-anchored schedules."""

from __future__ import annotations

import numpy as np


def power_weighted_schedule_means(
    T: int,
    exponents: tuple[float, ...],
    *,
    kappa: float = 0.02,
    p: float = 2.0,
    c: float = 10.0,
    anchored: bool = False,
    chunk_size: int = 1_000_000,
) -> dict[float, float]:
    """Return means weighted by ``(n/T)**a`` without storing a long schedule."""
    if T < 1 or p <= 0.0 or c <= 0.0 or chunk_size < 1:
        raise ValueError("invalid schedule parameters")
    exponents = tuple(float(value) for value in exponents)
    numerator = np.zeros(len(exponents), dtype=np.float64)
    denominator = np.zeros(len(exponents), dtype=np.float64)
    endpoint = np.log(T + c) ** (-p) if anchored else 0.0

    for first in range(1, T + 1, chunk_size):
        last = min(T + 1, first + chunk_size)
        n = np.arange(first, last, dtype=np.float64)
        delta = kappa * (np.log(n + c) ** (-p) - endpoint)
        x = n / T
        for index, exponent in enumerate(exponents):
            weights = np.power(x, exponent)
            numerator[index] += np.dot(weights, delta)
            denominator[index] += np.sum(weights)
    return {
        exponent: numerator[index] / denominator[index]
        for index, exponent in enumerate(exponents)
    }
