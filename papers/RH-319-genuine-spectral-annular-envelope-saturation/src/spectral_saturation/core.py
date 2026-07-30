from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
Q_STAR = 1.0 / (R_H * LAMBDA)
Q = 0.5
RHO_STAR = 1.0 / Q_STAR
KAPPA_DENOMINATOR = math.log(Q_STAR / Q)


def annular_kappa(radius: float) -> float:
    rho = float(radius)
    if not 0.0 < rho < RHO_STAR:
        raise ValueError("radius must lie below rho_star")
    return math.log(1.0 / (Q_STAR * rho)) / KAPPA_DENOMINATOR


def annular_mass_scale(mass: float, radius: float) -> float:
    if mass <= 1.0:
        raise ValueError("mass must exceed one")
    return mass ** (-annular_kappa(radius)) / math.log(mass)
