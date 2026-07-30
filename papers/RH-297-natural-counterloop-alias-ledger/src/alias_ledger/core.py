from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85


def beta_limit() -> float:
    return 1.0 / (R_H * math.sqrt(LAMBDA))


def minimal_bridge_slope() -> float:
    return 1.0 / math.log(10.0 / 7.0)


def alias_order_slope(alias_index: int) -> float:
    if alias_index < 1:
        raise ValueError("alias index must be positive")
    return alias_index / math.log(LAMBDA)


def alias_count(cut_slope: float) -> int:
    if cut_slope <= 0.0:
        raise ValueError("cut slope must be positive")
    estimate = max(0, math.ceil(cut_slope * math.log(LAMBDA)) - 1)
    if estimate > 0 and alias_order_slope(estimate) >= cut_slope:
        return estimate - 1
    if alias_order_slope(estimate + 1) < cut_slope:
        return estimate + 1
    return estimate


def alias_growth_exponent(alias_index: int, radius: float = 1.4) -> float:
    product = beta_limit() * radius
    if product <= 1.0:
        raise ValueError("alias does not amplify on this radius")
    return alias_index * math.log(product) / math.log(LAMBDA)


def alias_weight(
    period: int,
    alias_index: int,
    radius: float = 1.4,
    beta: float | None = None,
) -> float:
    if period < 2 or alias_index < 1:
        raise ValueError("invalid alias parameters")
    use_beta = beta_limit() if beta is None else beta
    return (1.0 - 1.0 / period) * (use_beta * radius) ** (
        2 * alias_index * period
    ) / alias_index
