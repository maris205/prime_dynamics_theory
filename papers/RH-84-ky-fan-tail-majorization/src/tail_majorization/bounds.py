"""Scalar forms of the tail-majorization theorems."""

from __future__ import annotations

import math
from typing import Sequence


def ky_fan_tail(singular_values: Sequence[float], rank: int) -> float:
    values = [float(value) for value in singular_values]
    r = int(rank)
    if r < 0 or r > len(values) or any(value < 0.0 for value in values):
        raise ValueError("invalid singular values or rank")
    return math.nextafter(math.sqrt(sum(value * value for value in values[r:])), math.inf)


def tail_transfer_bound(mediator_tail: float, dilation: float, remainder: float) -> float:
    tail = float(mediator_tail)
    factor = float(dilation)
    error = float(remainder)
    if min(tail, factor, error) < 0.0:
        raise ValueError("bounds must be nonnegative")
    return math.nextafter(factor * tail + error, math.inf)

