"""Closed formulas used by the RH-82 endpoint-to-postblock criterion."""

from __future__ import annotations

import math


LAMBDA_FIXED = 1.6785735104283224


def half_log_clock(sigma: float, *, expansion: float = LAMBDA_FIXED) -> float:
    noise = float(sigma)
    lam = float(expansion)
    if not 0.0 < noise < 1.0 or lam <= 1.0:
        raise ValueError("require 0 < sigma < 1 and expansion > 1")
    return math.log(1.0 / noise) / (2.0 * math.log(lam))


def clock_rank(sigma: float, *, offset: int = 2, expansion: float = LAMBDA_FIXED) -> int:
    shift = int(offset)
    if shift < 0:
        raise ValueError("offset must be nonnegative")
    return int(math.ceil(half_log_clock(sigma, expansion=expansion))) + shift


def excess_rank_tail_bound(
    excess: int,
    *,
    ratio_upper: float,
    quadratic_energy_constant: float,
) -> float:
    """HS tail after J_sigma+excess for F(t)<=C t^2 and delta ratios <=q."""
    ell = int(excess)
    q = float(ratio_upper)
    constant = float(quadratic_energy_constant)
    if ell < 0 or not 0.0 < q < 1.0 or constant < 0.0:
        raise ValueError("invalid tail parameters")
    value = math.sqrt(constant / (1.0 - q * q)) * q**ell
    return math.nextafter(value, math.inf)


def factorized_tail_bound(
    resolution_tail: float,
    left_norm: float,
    right_norm: float,
    remainder_hs: float,
) -> float:
    tail = float(resolution_tail)
    left = float(left_norm)
    right = float(right_norm)
    remainder = float(remainder_hs)
    if min(tail, left, right, remainder) < 0.0:
        raise ValueError("norm bounds must be nonnegative")
    return math.nextafter(left * right * tail + remainder, math.inf)

