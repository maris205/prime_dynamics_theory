from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
RADIUS = 1.4


def localization_slope() -> float:
    return 1.0 / math.log(LAMBDA)


def beta_limit() -> float:
    return 1.0 / (R_H * math.sqrt(LAMBDA))


def alias_growth_exponent() -> float:
    return math.log(beta_limit() * RADIUS) / math.log(LAMBDA)


def parity_alias_exponent() -> float:
    return math.log(RADIUS / R_H) / math.log(LAMBDA) - 0.5


def absolute_matching_exponent() -> float:
    return math.log(RADIUS) / math.log(LAMBDA)


def first_alias_clearance_exponent() -> float:
    return localization_slope() * math.log(LAMBDA) - 1.0


def minimal_clearance_exponent() -> float:
    minimal = 1.0 / math.log(10.0 / 7.0)
    return minimal * math.log(LAMBDA) - 1.0
