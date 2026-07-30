from __future__ import annotations

import math


Q = 0.5
RADIUS = 1.4
LAMBDA = 1.678573510428322
R_H = 0.85
RHO_STAR = R_H * LAMBDA


def minimal_slope() -> float:
    return 1.0 / math.log(1.0 / (Q * RADIUS))


def critical_gap_constant() -> float:
    return 1.0 / minimal_slope()


def logarithmic_gap(sigma: float, coefficient: float) -> float:
    if not 0.0 < sigma < math.exp(-1.0) or coefficient < 0.0:
        raise ValueError("invalid shrinking-gap parameters")
    length = math.log(1.0 / sigma)
    return coefficient * math.log(length) / length


def critical_tail_scale(sigma: float, coefficient: float) -> float:
    if not 0.0 < sigma < math.exp(-1.0) or coefficient < 0.0:
        raise ValueError("invalid shrinking-gap parameters")
    length = math.log(1.0 / sigma)
    return length ** (minimal_slope() * coefficient - 1.0)


def shrinking_radius(sigma: float, coefficient: float) -> float:
    return RADIUS * math.exp(logarithmic_gap(sigma, coefficient))


def radius_is_certified(sigma: float, coefficient: float) -> bool:
    return shrinking_radius(sigma, coefficient) < RHO_STAR
