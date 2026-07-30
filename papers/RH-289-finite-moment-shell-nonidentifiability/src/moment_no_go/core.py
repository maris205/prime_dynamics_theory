from __future__ import annotations

import cmath
import numpy as np


def shell(order: int, radius: float) -> np.ndarray:
    if order < 2 or radius <= 0.0:
        raise ValueError("require order >= 2 and positive radius")
    return np.asarray(
        [radius * cmath.exp(2j * cmath.pi * index / order) for index in range(order)],
        dtype=complex,
    )


def shell_moment(shell_order: int, radius: float, power: int) -> complex:
    if power < 1:
        raise ValueError("power must be positive")
    return complex(np.sum(shell(shell_order, radius) ** power))


def shell_factor(shell_order: int, radius: float, z: complex) -> complex:
    roots = shell(shell_order, radius)
    return complex(np.prod((1.0 - z * roots) * np.exp(z * roots)))
