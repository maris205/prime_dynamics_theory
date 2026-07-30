from __future__ import annotations

import numpy as np


def modulus_head(values: np.ndarray, cutoff: float) -> tuple[np.ndarray, np.ndarray]:
    roots = np.asarray(values, dtype=complex).reshape(-1)
    if cutoff <= 0.0:
        raise ValueError("cutoff must be positive")
    mask = np.abs(roots) > cutoff
    return roots[mask], roots[~mask]


def complementary_radius(values: np.ndarray, cutoff: float) -> float:
    _, tail = modulus_head(values, cutoff)
    return 0.0 if tail.size == 0 else float(np.max(np.abs(tail)))


def rank_bound(squared_mass: float, cutoff: float) -> float:
    if squared_mass < 0.0 or cutoff <= 0.0:
        raise ValueError("invalid mass or cutoff")
    return squared_mass / cutoff**2
