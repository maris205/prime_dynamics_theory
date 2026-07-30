from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
Q_STAR = 1.0 / (R_H * LAMBDA)
Q = 0.5
BASE = Q_STAR / Q
LOG_BASE = math.log(BASE)


def proper_divisors(order: int) -> tuple[int, ...]:
    n = int(order)
    if n < 2:
        return ()
    return tuple(divisor for divisor in range(1, n) if n % divisor == 0)


def normalized_divisor_feedback(order: int, base: float = BASE) -> float:
    n = int(order)
    if n < 2 or base <= 1.0:
        raise ValueError("invalid divisor-feedback data")
    return float(sum(base**divisor for divisor in proper_divisors(n)) / base**n)


def rank_lower_bound(order: int, anchor_abs: float, radius_cap: float = Q) -> float:
    n = int(order)
    if n < 1 or anchor_abs < 0.0 or radius_cap <= 0.0:
        raise ValueError("invalid rank lower-bound data")
    return anchor_abs / radius_cap**n


def mass_lower_bound(order: int, anchor_abs: float, radius_cap: float = Q) -> float:
    n = int(order)
    if n < 2 or anchor_abs < 0.0 or radius_cap <= 0.0:
        raise ValueError("invalid mass lower-bound data")
    return anchor_abs * radius_cap ** (2 - n)
