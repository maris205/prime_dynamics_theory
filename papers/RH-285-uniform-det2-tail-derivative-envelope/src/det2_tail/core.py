from __future__ import annotations

import math


def derivative_constant(order: int, x: float, terms: int = 100000) -> float:
    if order < 0 or not 0.0 < x < 1.0 or terms < 1:
        raise ValueError("invalid derivative constant parameters")
    exponent = max(order - 1, 0)
    total = 0.0
    term = 1.0
    for k in range(terms):
        total += (1 + k) ** exponent * term
        term *= x
        if term * (1 + k) ** exponent < 1e-16:
            break
    return total


def derivative_envelope(
    sigma: float,
    derivative_order: int,
    cutoff: float = 0.5,
    radius: float = 1.4,
    slope: float = 4.0,
    alpha: float = 1.0,
) -> float:
    if not 0.0 < sigma < 1.0:
        raise ValueError("sigma must lie in (0,1)")
    m = max(2, derivative_order, math.ceil(slope * math.log(1.0 / sigma)))
    x = cutoff * radius
    return (
        sigma ** (-alpha)
        * cutoff**-2
        * radius ** (-derivative_order)
        * derivative_constant(derivative_order, x)
        * m ** max(derivative_order - 1, 0)
        * x**m
    )


def power_gain(
    alpha: float = 1.0, cutoff: float = 0.5, radius: float = 1.4, slope: float = 4.0
) -> float:
    return slope * math.log(1.0 / (cutoff * radius)) - alpha
