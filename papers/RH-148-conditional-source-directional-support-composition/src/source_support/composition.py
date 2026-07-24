from __future__ import annotations

import math
from collections.abc import Iterable


def projector_radius(error: float, approximate_gap: float) -> float:
    eps = float(error)
    gap = float(approximate_gap)
    if not math.isfinite(eps) or eps < 0.0:
        raise ValueError("error must be finite and nonnegative")
    if not math.isfinite(gap) or gap <= 2.0 * eps:
        raise ValueError("approximate gap must exceed twice the error")
    return eps / (gap - eps)


def branch_is_stable(propagated_radius: float, branch_margin: float) -> bool:
    radius = float(propagated_radius)
    margin = float(branch_margin)
    if not math.isfinite(radius) or radius < 0.0:
        raise ValueError("radius must be finite and nonnegative")
    if not math.isfinite(margin) or margin < 0.0:
        raise ValueError("margin must be finite and nonnegative")
    return radius < margin


def support_value(tail_upper: float, base_lower: float) -> float:
    y = float(tail_upper)
    a = float(base_lower)
    if not math.isfinite(y) or y < 0.0 or not math.isfinite(a) or a < 0.0:
        raise ValueError("tail and base bounds must be finite and nonnegative")
    return a * max(0.0, 1.0 - math.sqrt(y)) ** 4


def compose_support_floor(initial_support: float, log_multipliers: Iterable[float]) -> tuple[float, float]:
    initial = float(initial_support)
    if not math.isfinite(initial) or initial < 0.0:
        raise ValueError("initial support must be finite and nonnegative")
    running = 0.0
    minimum = 0.0
    for logarithm in log_multipliers:
        value = float(logarithm)
        if not math.isfinite(value):
            raise ValueError("log multipliers must be finite")
        running += value
        minimum = min(minimum, running)
    return initial * math.exp(minimum), -minimum

