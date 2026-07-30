from __future__ import annotations

import math


def critical_slope(alpha: float, cutoff: float, radius: float) -> float:
    x = cutoff * radius
    if alpha <= 0.0 or not 0.0 < x < 1.0:
        raise ValueError("require alpha > 0 and 0 < cutoff*radius < 1")
    return alpha / math.log(1.0 / x)


def decay_exponent(alpha: float, slope: float, cutoff: float, radius: float) -> float:
    if slope <= 0.0:
        raise ValueError("slope must be positive")
    return slope * math.log(1.0 / (cutoff * radius)) - alpha


def root_rate_limit(alpha: float, slope: float, cutoff: float, radius: float) -> float:
    if slope <= 0.0:
        raise ValueError("slope must be positive")
    return cutoff * radius * math.exp(alpha / slope)


def saturation_lower(
    sigma: float,
    alpha: float,
    slope: float,
    cutoff: float,
    radius: float,
    mass_constant: float = 1.0,
) -> float:
    if not 0.0 < sigma < 1.0:
        raise ValueError("sigma must lie in (0,1)")
    m = max(2, math.ceil(slope * math.log(1.0 / sigma)))
    multiplicity = math.floor(mass_constant * sigma ** (-alpha) / cutoff**2)
    return multiplicity * (cutoff * radius) ** m / m
