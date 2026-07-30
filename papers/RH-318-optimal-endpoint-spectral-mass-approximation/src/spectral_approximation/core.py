from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
Q_STAR = 1.0 / (R_H * LAMBDA)
Q = 0.5
BASE = Q_STAR / Q
LOG_BASE = math.log(BASE)
SQRT_LOG_BASE = math.sqrt(LOG_BASE)


def logarithmic_degree_clock(mass: float) -> float:
    if mass <= 1.0:
        raise ValueError("mass must exceed one")
    return math.log(mass) / LOG_BASE


def asymptotic_endpoint_energy(mass: float) -> float:
    if mass <= 1.0:
        raise ValueError("mass must exceed one")
    return LOG_BASE / math.log(mass)


def asymptotic_endpoint_norm(mass: float) -> float:
    return math.sqrt(asymptotic_endpoint_energy(mass))
