"""Exact algebra for the resolution-clocked monodromy counterloop."""

from __future__ import annotations

import cmath
import math

LAMBDA = 1.678573510428322
R_H = 0.85
BETA = 1.0 / (R_H * math.sqrt(LAMBDA))


def counterloop_roots(k: int, rho: float = 1.0 / LAMBDA) -> list[complex]:
    if k < 2:
        raise ValueError("k must be at least two")
    radius = math.sqrt(rho) / R_H
    return [radius * cmath.exp(1j * j * math.pi / k) for j in range(1, k)] + [
        radius * cmath.exp(-1j * j * math.pi / k) for j in range(1, k)
    ]


def counterloop_moment(k: int, n: int, rho: float = 1.0 / LAMBDA) -> complex:
    beta = math.sqrt(rho) / R_H
    return beta**n * (2 * k * (1 if (2 * k) and n % (2 * k) == 0 else 0) - 1 - (-1) ** n)


def factor(k: int, z: complex, rho: float = 1.0 / LAMBDA) -> complex:
    q = rho * (z / R_H) ** 2
    return sum(q**j for j in range(k))


def bridge_error(k: int, radius: float) -> float:
    t = BETA * abs(radius)
    if t >= 1:
        raise ValueError("radius must lie inside the pole circle")
    return t ** (2 * k) / (1 - t ** (2 * k))
