"""Finite-jet contraction bounds for tolerance-adaptive clouds."""

from __future__ import annotations

import numpy as np


def trace_jet_norm(values: np.ndarray, radius: float = 1.0) -> float:
    data = np.asarray(values, dtype=complex).reshape(-1)
    if data.size < 2:
        raise ValueError("at least two trace orders are required")
    disk = float(radius)
    orders = np.arange(2, data.size + 1)
    return float(np.sum(np.abs(data[1:]) * disk**orders / orders))


def trace_jet_distance(first: np.ndarray, second: np.ndarray, radius: float = 1.0) -> float:
    left = np.asarray(first, dtype=complex).reshape(-1)
    right = np.asarray(second, dtype=complex).reshape(-1)
    if left.shape != right.shape:
        raise ValueError("jets must have the same shape")
    return trace_jet_norm(left - right, radius)


def triangle_tolerance_bound(first_tolerance: float, second_tolerance: float) -> float:
    first = float(first_tolerance)
    second = float(second_tolerance)
    if first < 0.0 or second < 0.0:
        raise ValueError("tolerances must be nonnegative")
    return first + second


def complex_values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])
