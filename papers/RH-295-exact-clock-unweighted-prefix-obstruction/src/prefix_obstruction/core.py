from __future__ import annotations

import math


def minimal_clock(sigma: float) -> int:
    if not 0.0 < sigma < 1.0:
        raise ValueError("require 0 < sigma < 1")
    slope = 1.0 / math.log(10.0 / 7.0)
    return max(3, math.ceil(slope * math.log(1.0 / sigma)))


def escaping_spike(order_cut: int, radius: float = 1.4) -> tuple[float, float]:
    if order_cut < 3 or radius <= 1.0:
        raise ValueError("invalid spike parameters")
    order = order_cut - 1
    amplitude = radius ** (-order / 2.0)
    weighted_budget = amplitude * radius**order / order
    return amplitude, weighted_budget
