from __future__ import annotations

import math
from scipy.integrate import quad
from scipy.special import erf

U_C = 1.5436890126920753
R_H = 0.85
ASYMPTOTIC_CONSTANT = 1.0 / (2 * math.sqrt(math.pi) * R_H**2)


def row_squared(x: float, sigma: float) -> float:
    a = 1.0 - U_C * x * x
    raw_l2 = sigma * math.sqrt(math.pi) / 2 * (
        erf((1 - a) / sigma) + erf((1 + a) / sigma)
        + 2 * math.exp(-(a / sigma) ** 2) * erf(1 / sigma)
    )
    raw_mass = sigma * math.sqrt(math.pi / 2) * (
        erf((1 - a) / (math.sqrt(2) * sigma))
        + erf((1 + a) / (math.sqrt(2) * sigma))
    )
    return raw_l2 / (raw_mass * raw_mass)


def hs_squared(sigma: float, hardy_scaled: bool = True) -> float:
    critical = math.sqrt(1 / U_C)
    value, _ = quad(lambda x: row_squared(x, sigma), 0.0, 1.0, points=[critical], epsabs=1e-10, epsrel=3e-11, limit=500)
    return value / R_H**2 if hardy_scaled else value


def explicit_lower_constant() -> float:
    return ((math.sqrt(3) - 1) / (4 * math.pi * math.sqrt(U_C))) * math.sqrt(math.pi) * erf(1)
