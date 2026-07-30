from __future__ import annotations

import math


Q = 0.5
RADIUS = 1.4
LAMBDA = 1.678573510428322
R_H = 0.85
Q_STAR = 1.0 / (R_H * LAMBDA)
RHO_STAR = 1.0 / Q_STAR


def block_clock(sigma: float, slope: float = 4.0) -> int:
    if not 0.0 < sigma < 1.0 or slope <= 0.0:
        raise ValueError("invalid clock parameters")
    return max(3, math.ceil(slope * math.log(1.0 / sigma)))


def annular_exponents(rho: float) -> tuple[float, float]:
    if not RADIUS < rho < RHO_STAR:
        raise ValueError("rho must lie in the certified annulus")
    return 4.0 * math.log(2.0 / rho) - 1.0, 4.0 * math.log(RHO_STAR / rho)


def tail_bounds(sigma: float, rho: float, hardy: bool = False) -> tuple[float, float]:
    m = block_clock(sigma)
    x = Q * rho
    y = Q_STAR * rho
    if hardy:
        noisy = 4.0 * sigma**-1 * x**m / (m * math.sqrt(1.0 - x * x))
        target = 48.0 * y**m / (m * math.sqrt(1.0 - y * y))
    else:
        noisy = 4.0 * sigma**-1 * x**m / (m * (1.0 - x))
        target = 48.0 * y**m / (m * (1.0 - y))
    return noisy, target
