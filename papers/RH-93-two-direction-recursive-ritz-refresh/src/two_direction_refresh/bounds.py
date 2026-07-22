"""Finite-dimensional forms of the RH-93 refresh theorems."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def _values(items: Iterable[float]) -> tuple[float, ...]:
    values = tuple(float(item) for item in items)
    if not values or any(not math.isfinite(item) or item < 0.0 for item in values):
        raise ValueError("a nonempty finite nonnegative sequence is required")
    return values


def block_budget_product(factors: Iterable[float]) -> float:
    product = math.prod(_values(factors))
    return math.nextafter(product, math.inf)


def block_geometric_mean(factors: Iterable[float]) -> float:
    values = _values(factors)
    return math.nextafter(math.prod(values) ** (1.0 / len(values)), math.inf)


def recursive_tail_bound(initial_tail: float, factors: Iterable[float]) -> float:
    initial = float(initial_tail)
    if initial < 0.0:
        raise ValueError("initial tail must be nonnegative")
    return math.nextafter(initial * math.prod(_values(factors)), math.inf)


def cross_energy_fraction(singular_values: Iterable[float], width: int) -> float:
    singular = np.asarray(tuple(float(value) for value in singular_values), dtype=float)
    rank = int(width)
    if singular.ndim != 1 or singular.size == 0 or rank <= 0 or rank > singular.size or np.any(singular < 0.0):
        raise ValueError("invalid singular-value data")
    energy = float(singular @ singular)
    if energy == 0.0:
        return 1.0
    value = float(singular[:rank] @ singular[:rank] / energy)
    return math.nextafter(value, -math.inf)


def ky_fan_gain(new_block_trace: float, bottom_eigenvalues: Iterable[float]) -> float:
    trace_value = float(new_block_trace)
    bottom = _values(bottom_eigenvalues)
    gain = trace_value - sum(bottom)
    return math.nextafter(gain, -math.inf)


def generalized_frame_trace(matrix: np.ndarray, frame: np.ndarray) -> float:
    """Trace((W*W)^(-1) W*H W) for a full-column-rank frame W."""
    hermitian = np.asarray(matrix, dtype=float)
    trial = np.asarray(frame, dtype=float)
    if hermitian.ndim != 2 or hermitian.shape[0] != hermitian.shape[1] or trial.ndim != 2 or trial.shape[0] != hermitian.shape[0]:
        raise ValueError("incompatible frame data")
    metric = trial.T @ trial
    if np.linalg.eigvalsh((metric + metric.T) / 2.0)[0] <= 0.0:
        raise ValueError("trial frame must have full column rank")
    compressed = trial.T @ hermitian @ trial
    return float(np.trace(np.linalg.solve(metric, compressed)))


def trial_frame_form(matrix: np.ndarray, frame: np.ndarray, new_block_trace: float, delta: float) -> float:
    gain = float(delta)
    if gain < 0.0:
        raise ValueError("delta must be nonnegative")
    value = generalized_frame_trace(matrix, frame) + gain - float(new_block_trace)
    return math.nextafter(value, math.inf)
