from __future__ import annotations

import math


def weighted_prefix(errors: list[complex], radius: float, first_order: int = 2) -> float:
    if radius <= 0.0 or first_order < 1:
        raise ValueError("invalid weighted-prefix parameters")
    return sum(
        abs(error) * radius**order / order
        for order, error in enumerate(errors, start=first_order)
    )


def gluing_relative_error(prefix: float, noisy_tail: float, target_tail: float) -> float:
    if min(prefix, noisy_tail, target_tail) < 0.0:
        raise ValueError("budgets must be nonnegative")
    return math.expm1(prefix + noisy_tail + target_tail)
