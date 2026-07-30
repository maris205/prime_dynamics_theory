from __future__ import annotations

import math


def hardy_constant(radius: float, rho: float) -> float:
    if not 0.0 < radius < rho:
        raise ValueError("require radius < rho")
    x = radius / rho
    return x * x / math.sqrt(1.0 - x * x)


def cauchy_constant(radius: float, rho: float) -> float:
    if not 0.0 < radius < rho:
        raise ValueError("require radius < rho")
    x = radius / rho
    return x * x / (1.0 - x)


def shrinking_hardy_scale(eta: float) -> float:
    if eta <= 0.0:
        raise ValueError("eta must be positive")
    x = math.exp(-eta)
    return x * x / math.sqrt(1.0 - x * x)


def rudin_shapiro_block_lower(eta: float, length: int) -> float:
    if eta <= 0.0 or length < 1 or length & (length - 1):
        raise ValueError("invalid block parameters")
    x = math.exp(-eta)
    return x * x * (1.0 - x**length) / (
        math.sqrt(2.0 * length) * (1.0 - x)
    )
