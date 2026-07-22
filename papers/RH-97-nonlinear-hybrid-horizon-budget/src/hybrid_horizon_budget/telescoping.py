"""Scalar forms of the nonlinear hybrid telescoping identity."""

from __future__ import annotations

import math
from typing import Iterable


def _values(items: Iterable[float]) -> tuple[float, ...]:
    values = tuple(float(item) for item in items)
    if not values or any(not math.isfinite(item) for item in values):
        raise ValueError("a nonempty finite sequence is required")
    return values


def hybrid_contributions(hybrid_endpoint_values: Iterable[float]) -> tuple[float, ...]:
    values = _values(hybrid_endpoint_values)
    if len(values) < 2:
        raise ValueError("at least two hybrid endpoint values are required")
    return tuple(values[index] - values[index - 1] for index in range(1, len(values)))


def signed_horizon_shift(hybrid_endpoint_values: Iterable[float]) -> float:
    values = _values(hybrid_endpoint_values)
    if len(values) < 2:
        raise ValueError("at least two hybrid endpoint values are required")
    return values[-1] - values[0]


def absolute_horizon_budget(contributions: Iterable[float]) -> float:
    values = _values(contributions)
    return math.nextafter(sum(abs(value) for value in values), math.inf)
