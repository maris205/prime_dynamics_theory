"""Counting consequences of tight rank-growing empirical root measures."""

from __future__ import annotations

import math

import numpy as np


def tightness_count_lower(rank: int, epsilon: float) -> int:
    size = int(rank)
    tolerance = float(epsilon)
    if size < 1 or not 0.0 < tolerance < 1.0:
        raise ValueError("invalid rank or epsilon")
    return int(math.ceil((1.0 - tolerance) * size - 1.0e-15))


def disk_count(values: np.ndarray, radius: float) -> int:
    threshold = float(radius)
    if threshold <= 0.0:
        raise ValueError("radius must be positive")
    roots = np.asarray(values, dtype=complex).reshape(-1)
    return int(np.sum(np.abs(roots) <= threshold))


def divisor_mass_diverges(rank_sequence: list[int], epsilon: float) -> bool:
    if not rank_sequence:
        raise ValueError("a rank sequence is required")
    lower = [tightness_count_lower(rank, epsilon) for rank in rank_sequence]
    return all(next_value > value for value, next_value in zip(lower[:-1], lower[1:]))
