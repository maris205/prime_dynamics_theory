"""Trace-power quantities that separate spectral and nonnormal mass."""

from __future__ import annotations

import numpy as np


def nilpotent_shift(dimension: int, weight: float = 1.0) -> np.ndarray:
    size = int(dimension)
    if size < 2:
        raise ValueError("dimension must be at least two")
    matrix = np.zeros((size, size), dtype=float)
    matrix[np.arange(size - 1), np.arange(1, size)] = float(weight)
    return matrix


def complement_trace_power(
    full_trace: complex,
    perron: complex,
    parity: complex,
    cloud: np.ndarray,
    order: int,
) -> complex:
    n = int(order)
    if n < 1:
        raise ValueError("a positive order is required")
    roots = np.asarray(cloud, dtype=complex).reshape(-1)
    return complex(full_trace - complex(perron) ** n - complex(parity) ** n - np.sum(roots**n))


def sparse_trace_square(matrix) -> complex:
    return complex(matrix.multiply(matrix.T).sum())
