"""Exact finite suffix-retention quantities."""

from __future__ import annotations

import math
from collections.abc import Sequence


def suffix_length(chain_length: int, retained_fraction: float) -> int:
    length = int(chain_length)
    fraction = float(retained_fraction)
    if length <= 0 or not math.isfinite(fraction) or fraction <= 0.0 or fraction > 1.0:
        raise ValueError("invalid suffix request")
    return int(math.ceil(fraction * length))


def common_suffix_floor(chains: Sequence[Sequence[float]], retained_fraction: float) -> float:
    """Largest common floor among terminal suffixes retaining the requested fraction."""
    if not chains:
        raise ValueError("at least one chain is required")
    floors = []
    for chain in chains:
        values = [float(value) for value in chain]
        if not values or any(not math.isfinite(value) or value <= 0.0 for value in values):
            raise ValueError("chains must contain positive finite values")
        length = suffix_length(len(values), retained_fraction)
        floors.append(min(values[-length:]))
    return min(floors)


def suffix_log_drawdown(chain: Sequence[float], retained_fraction: float) -> float:
    values = [float(value) for value in chain]
    if not values or any(not math.isfinite(value) or value <= 0.0 for value in values):
        raise ValueError("chain must contain positive finite values")
    length = suffix_length(len(values), retained_fraction)
    return sum(-math.log(value) for value in values[-length:])
