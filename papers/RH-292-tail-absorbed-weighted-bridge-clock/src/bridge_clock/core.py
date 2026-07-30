from __future__ import annotations

import math


def critical_slope(cutoff: float = 0.5, radius: float = 1.4) -> float:
    product = cutoff * radius
    if not 0.0 < product < 1.0:
        raise ValueError("require 0 < cutoff*radius < 1")
    return 1.0 / math.log(1.0 / product)


def block_clock(sigma: float, slope: float) -> int:
    if not 0.0 < sigma < 1.0 or slope <= 0.0:
        raise ValueError("invalid clock parameters")
    return max(3, math.ceil(slope * math.log(1.0 / sigma)))


def complement_tail_bound(
    sigma: float,
    slope: float | None = None,
    cutoff: float = 0.5,
    radius: float = 1.4,
) -> float:
    use_slope = critical_slope(cutoff, radius) if slope is None else slope
    m = block_clock(sigma, use_slope)
    product = cutoff * radius
    return sigma**-1 * cutoff**-2 * product**m / (m * (1.0 - product))


def target_tail_bound(
    sigma: float,
    slope: float | None = None,
    target_base: float = 0.7008752258547757,
    radius: float = 1.4,
    constant: float = 48.0,
) -> float:
    use_slope = critical_slope() if slope is None else slope
    m = block_clock(sigma, use_slope)
    product = target_base * radius
    if not product < 1.0:
        raise ValueError("target series must be inside its radius")
    return constant * product**m / (m * (1.0 - product))
