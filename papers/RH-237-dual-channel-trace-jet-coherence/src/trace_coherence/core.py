"""Finite logarithmic trace-jet seminorms."""

from __future__ import annotations

import numpy as np


def trace_jet_distance(
    first: np.ndarray,
    second: np.ndarray,
    *,
    radius: float = 1.0,
    first_order: int = 2,
) -> float:
    left = np.asarray(first, dtype=complex).reshape(-1)
    right = np.asarray(second, dtype=complex).reshape(-1)
    if left.shape != right.shape:
        raise ValueError("trace jets must have the same shape")
    start = int(first_order)
    if start < 1 or start > left.size:
        raise ValueError("invalid first order")
    disk = float(radius)
    if disk < 0.0:
        raise ValueError("radius must be nonnegative")
    orders = np.arange(start, left.size + 1)
    return float(np.sum(np.abs(left[start - 1 :] - right[start - 1 :]) * disk**orders / orders))


def complex_values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])
