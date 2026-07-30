from __future__ import annotations

import math


R_H = 0.85
C_STAR = 0.105258535936908


def minimal_bridge_slope() -> float:
    return 1.0 / math.log(10.0 / 7.0)


def bulk_leading_coefficient(order: int) -> float:
    if order < 2:
        raise ValueError("order must be at least two")
    return (-1.0) ** order * order * C_STAR * R_H ** (-order)


def growth_exponent(
    slope: float,
    radius: float = 1.4,
    hardy_radius: float = R_H,
) -> float:
    if slope <= 0.0 or radius <= hardy_radius:
        raise ValueError("invalid growth parameters")
    return slope * math.log(radius / hardy_radius) - 0.5


def parity_budget(
    sigma: float,
    slope: float | None = None,
    radius: float = 1.4,
) -> float:
    if not 0.0 < sigma < 1.0:
        raise ValueError("require 0 < sigma < 1")
    use_slope = minimal_bridge_slope() if slope is None else slope
    cut = max(4, math.ceil(use_slope * math.log(1.0 / sigma)))
    delta = C_STAR * math.sqrt(sigma)
    parity = -1.0 + delta
    return sum(
        abs(parity**order - (-1.0) ** order)
        * (radius / R_H) ** order
        / order
        for order in range(3, cut)
        if order % 2 == 1
    )
