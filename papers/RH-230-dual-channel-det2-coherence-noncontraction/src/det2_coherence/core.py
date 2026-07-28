"""Branch-free finite det2 comparisons on a common zero-free disk."""

from __future__ import annotations

import numpy as np


def det2_log(resonances: np.ndarray, variable: complex) -> complex:
    values = np.asarray(resonances, dtype=complex).reshape(-1)
    z = complex(variable)
    return complex(np.sum(np.log1p(-z * values) + z * values))


def grid_sup_log_difference(first: np.ndarray, second: np.ndarray, grid: np.ndarray) -> float:
    left = np.asarray(first, dtype=complex).reshape(-1)
    right = np.asarray(second, dtype=complex).reshape(-1)
    points = np.asarray(grid, dtype=complex).reshape(-1)
    return float(max(abs(det2_log(left, point) - det2_log(right, point)) for point in points))


def strict_tail_contraction(values: list[float], width: int) -> bool:
    count = int(width)
    if count < 2 or len(values) < count:
        raise ValueError("invalid contraction window")
    tail = values[-count:]
    return all(next_value < value for value, next_value in zip(tail[:-1], tail[1:]))
