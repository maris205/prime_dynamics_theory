"""Second-regularized product tails on a zero-free disk."""

from __future__ import annotations

import numpy as np


def det2_log(resonances: np.ndarray, variable: complex) -> complex:
    values = np.asarray(resonances, dtype=complex).reshape(-1)
    z = complex(variable)
    return complex(np.sum(np.log1p(-z * values) + z * values))


def det2_log_tail_bound(resonances: np.ndarray, radius: float) -> dict[str, float]:
    values = np.asarray(resonances, dtype=complex).reshape(-1)
    disk_radius = float(radius)
    if disk_radius < 0.0:
        raise ValueError("radius must be nonnegative")
    if values.size == 0:
        return {"q": 0.0, "squared_mass": 0.0, "log_tail_upper": 0.0}
    q = float(disk_radius * np.max(np.abs(values)))
    if q >= 1.0:
        raise ValueError("the disk crosses an omitted reciprocal zero")
    squared_mass = float(np.sum(np.abs(values) ** 2))
    return {
        "q": q,
        "squared_mass": squared_mass,
        "log_tail_upper": float(disk_radius**2 * squared_mass / (2.0 * (1.0 - q))),
    }


def maximum_grid_log_tail(resonances: np.ndarray, grid: np.ndarray) -> float:
    values = np.asarray(resonances, dtype=complex).reshape(-1)
    points = np.asarray(grid, dtype=complex).reshape(-1)
    return float(max(abs(det2_log(values, point)) for point in points))
