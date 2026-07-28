"""Local reciprocal-zero count diagnostics for a small-noise family."""

from __future__ import annotations

import numpy as np


def disk_count(values: np.ndarray, radius: float) -> int:
    roots = np.asarray(values, dtype=complex).reshape(-1)
    threshold = float(radius)
    if threshold <= 0.0:
        raise ValueError("radius must be positive")
    return int(np.sum(np.abs(roots) < threshold))


def contour_clearance(values: np.ndarray, radius: float) -> float:
    roots = np.asarray(values, dtype=complex).reshape(-1)
    threshold = float(radius)
    if threshold <= 0.0:
        raise ValueError("radius must be positive")
    return float(np.min(np.abs(np.abs(roots) - threshold)))


def tail_is_constant(sequence: list[int], width: int) -> bool:
    count = int(width)
    if count < 2 or len(sequence) < count:
        raise ValueError("invalid tail width")
    return len(set(sequence[-count:])) == 1
