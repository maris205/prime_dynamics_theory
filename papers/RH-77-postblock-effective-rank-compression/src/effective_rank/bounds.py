"""Singular-value and observability compression bounds."""

from __future__ import annotations

import math
from typing import Sequence


def optimal_rank_residual(singular_values: Sequence[float], rank: int) -> float:
    values = [float(value) for value in singular_values]
    r = int(rank)
    if r < 0 or r > len(values) or any(value < 0.0 for value in values):
        raise ValueError("invalid singular-value inputs")
    return math.nextafter(math.sqrt(sum(value * value for value in values[r:])), math.inf)


def participation_rank(energies: Sequence[float]) -> float:
    values = [float(value) for value in energies]
    if not values or any(value < 0.0 for value in values):
        raise ValueError("invalid energies")
    total = sum(values)
    if total <= 0.0:
        raise ValueError("energy sum must be positive")
    probabilities = [value / total for value in values]
    return math.nextafter(1.0 / sum(value * value for value in probabilities), math.inf)


def tail_compression_error(observability_norm_upper: float, residual_norm: float) -> float:
    gram = float(observability_norm_upper)
    residual = float(residual_norm)
    if gram < 0.0 or residual < 0.0:
        raise ValueError("norm bounds must be nonnegative")
    return math.nextafter(math.sqrt(gram) * residual, math.inf)
