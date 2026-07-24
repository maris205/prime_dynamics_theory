"""Minimal scalar frontier for the directional candidate architecture."""

from __future__ import annotations

import math


def _nn(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def directional_candidate(tail_squared_upper: float, normalized_base: float) -> float:
    tail = _nn(tail_squared_upper, "tail squared upper")
    base = _nn(normalized_base, "normalized base")
    return max(0.0, 1.0 - math.sqrt(tail)) ** 4 * base


def controlled_support_floor(tail_limsup_upper: float, base_liminf_lower: float) -> float:
    """Return the eventual support floor when the tail tube stays below one."""
    tail = _nn(tail_limsup_upper, "tail limsup upper")
    base = _nn(base_liminf_lower, "base liminf lower")
    if tail >= 1.0:
        return 0.0
    return (1.0 - math.sqrt(tail)) ** 4 * base
