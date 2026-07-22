"""Finite singular-list forms of the optimal factorization theorem."""

from __future__ import annotations

import math
from typing import Sequence


def optimal_factor_constant(
    target_singular_values: Sequence[float],
    mediator_singular_values: Sequence[float],
    rank: int,
) -> float:
    target = [float(value) for value in target_singular_values]
    mediator = [float(value) for value in mediator_singular_values]
    r = int(rank)
    if r < 0 or r > min(len(target), len(mediator)):
        raise ValueError("invalid rank")
    if any(value < 0.0 for value in target) or any(value <= 0.0 for value in mediator[:r]):
        raise ValueError("invalid singular values")
    if r == 0:
        return 0.0
    return math.nextafter(max(target[index] / mediator[index] for index in range(r)), math.inf)


def optimal_rank_residual(singular_values: Sequence[float], rank: int) -> float:
    values = [float(value) for value in singular_values]
    r = int(rank)
    if r < 0 or r > len(values) or any(value < 0.0 for value in values):
        raise ValueError("invalid singular values")
    return math.nextafter(math.sqrt(sum(value * value for value in values[r:])), math.inf)

