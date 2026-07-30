from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
Q = 0.5
RADIUS = 1.4
Q_STAR = 1.0 / (R_H * LAMBDA)


def minimal_slope() -> float:
    return 1.0 / math.log(1.0 / (Q * RADIUS))


def mass_ratio() -> float:
    return Q_STAR / Q


def mass_exponent(slope: float | None = None) -> float:
    use_slope = minimal_slope() if slope is None else slope
    return use_slope * math.log(mass_ratio())


def mass_saturation_slope() -> float:
    return 1.0 / math.log(mass_ratio())


def odd_anchor(order: int) -> float:
    if order < 3 or order % 2 == 0:
        raise ValueError("order must be odd and at least three")
    return Q_STAR**order / (1.0 + LAMBDA ** (-order))


def necessary_mass(order: int, relative_error: float = 0.5) -> float:
    if not 0.0 <= relative_error < 1.0:
        raise ValueError("relative error must lie in [0,1)")
    return (1.0 - relative_error) * Q * Q * mass_ratio() ** order / (
        1.0 + LAMBDA ** (-order)
    )
