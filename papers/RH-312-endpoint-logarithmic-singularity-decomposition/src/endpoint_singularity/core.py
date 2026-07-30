from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
Q_STAR = 1.0 / (R_H * LAMBDA)
RHO_STAR = 1.0 / Q_STAR
TRACE_BLOCK = 0.801254


def odd_normalized_anchor(order: int, lam: float = LAMBDA) -> float:
    n = int(order)
    if n < 3 or n % 2 == 0 or lam <= 1.0:
        raise ValueError("require odd order at least three and lambda > one")
    return 1.0 / (1.0 + lam ** (-n))


def even_endpoint_normalized_anchor(iterate: int, lam: float = LAMBDA) -> float:
    m = int(iterate)
    if m < 1 or lam <= 1.0:
        raise ValueError("require positive iterate and lambda > one")
    x = lam ** (-m)
    return (1.0 - 2.0 * x) / (1.0 - x * x)


def regularity_radius_lower_bound(
    lam: float = LAMBDA, trace_block: float = TRACE_BLOCK
) -> float:
    if lam <= 1.0 or not 0.0 < trace_block < 1.0:
        raise ValueError("invalid regularity data")
    return min(lam, math.sqrt(lam), trace_block ** (-1.0 / 6.0))
