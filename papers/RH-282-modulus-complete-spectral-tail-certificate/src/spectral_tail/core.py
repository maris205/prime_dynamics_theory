from __future__ import annotations

import math


def block_clock(sigma: float, slope: float = 4.0) -> int:
    if not 0.0 < sigma < 1.0 or slope <= 0.0:
        raise ValueError("require 0 < sigma < 1 and positive slope")
    return max(2, math.ceil(slope * math.log(1.0 / sigma)))


def trace_power_bound(order: int, sigma: float, cutoff: float = 0.5) -> float:
    if order < 2 or not 0.0 < sigma < 1.0 or not 0.0 < cutoff < 1.0:
        raise ValueError("invalid trace-tail parameters")
    return sigma**-1 * cutoff ** (order - 2)


def logarithmic_tail_bound(
    sigma: float, radius: float = 1.4, cutoff: float = 0.5, slope: float = 4.0
) -> float:
    m = block_clock(sigma, slope)
    x = cutoff * radius
    if not x < 1.0:
        raise ValueError("cutoff times radius must be below one")
    return sigma**-1 * cutoff**-2 * x**m / (m * (1.0 - x))


def root_rate_limit(
    radius: float = 1.4, cutoff: float = 0.5, slope: float = 4.0
) -> float:
    if slope <= 0.0:
        raise ValueError("slope must be positive")
    return cutoff * radius * math.exp(1.0 / slope)


def head_rank_bound(sigma: float, cutoff: float = 0.5) -> float:
    if not 0.0 < sigma < 1.0 or cutoff <= 0.0:
        raise ValueError("invalid head parameters")
    return sigma**-1 / cutoff**2
