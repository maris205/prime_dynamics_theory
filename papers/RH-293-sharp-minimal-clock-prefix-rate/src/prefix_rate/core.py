from __future__ import annotations

import math


def minimal_bridge_slope() -> float:
    return 1.0 / math.log(10.0 / 7.0)


def critical_exponent(slope: float, radius: float = 1.4) -> float:
    if slope <= 0.0 or radius <= 1.0:
        raise ValueError("require a positive slope and radius above one")
    return slope * math.log(radius)


def weighted_geometric_sum(order_cut: int, radius: float = 1.4) -> float:
    if order_cut < 3 or radius <= 1.0:
        raise ValueError("invalid weighted-prefix parameters")
    return sum(radius**order / order for order in range(2, order_cut))


def saturated_budget(
    sigma: float,
    beta: float,
    slope: float | None = None,
    radius: float = 1.4,
) -> float:
    if not 0.0 < sigma < 1.0 or beta <= 0.0:
        raise ValueError("invalid rate parameters")
    use_slope = minimal_bridge_slope() if slope is None else slope
    cut = max(3, math.ceil(use_slope * math.log(1.0 / sigma)))
    return sigma**beta * weighted_geometric_sum(cut, radius)
