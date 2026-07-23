"""Nested Weyl certificates for finite-memory projected crosses."""

from __future__ import annotations

from collections.abc import Iterable
import math

import numpy as np


def _eta(value: float) -> float:
    decay = float(value)
    if not math.isfinite(decay) or decay < 0.0 or decay >= 1.0:
        raise ValueError("eta must lie in [0, 1)")
    return decay


def finite_history_tail_bound(eta: float, depth: int, history_length: int) -> float:
    """Return the geometric operator budget beyond a recent window."""
    decay = _eta(eta)
    memory = int(depth)
    length = int(history_length)
    if memory <= 0 or length <= 0:
        raise ValueError("depth and history length must be positive")
    if memory >= length:
        return 0.0
    dropped = length - memory
    value = decay**memory * (1.0 - decay**dropped) / (1.0 - decay)
    return math.nextafter(value, math.inf)


def weyl_ratio_lower_bound(
    singular_values: Iterable[float],
    tail_bound: float,
    mode: int = 4,
) -> float:
    """Lower-bound ``s_mode(C)/s_1(C)`` from a truncated cross."""
    singular = np.asarray(tuple(singular_values), dtype=float)
    index = int(mode) - 1
    radius = float(tail_bound)
    if singular.ndim != 1 or index < 0 or singular.size <= index:
        raise ValueError("the requested singular mode is unavailable")
    if np.any(~np.isfinite(singular)) or np.any(singular < 0.0):
        raise ValueError("singular values must be finite and nonnegative")
    if not math.isfinite(radius) or radius < 0.0:
        raise ValueError("the tail bound must be finite and nonnegative")
    ordered = np.sort(singular)[::-1]
    numerator = max(0.0, float(ordered[index]) - radius)
    denominator = float(ordered[0]) + radius
    if numerator == 0.0 or denominator == 0.0:
        return 0.0
    return max(0.0, math.nextafter(numerator / denominator, -math.inf))


def first_certifying_depth(
    depth_bounds: Iterable[tuple[int, float]],
    threshold: float,
) -> int | None:
    """Return the first certified depth from a strictly ordered enumeration."""
    cutoff = float(threshold)
    if not math.isfinite(cutoff) or cutoff <= 0.0:
        raise ValueError("threshold must be finite and positive")
    previous = 0
    for raw_depth, raw_bound in depth_bounds:
        depth = int(raw_depth)
        bound = float(raw_bound)
        if depth <= previous:
            raise ValueError("depths must be strictly increasing")
        if not math.isfinite(bound) or bound < 0.0:
            raise ValueError("bounds must be finite and nonnegative")
        if bound >= cutoff:
            return depth
        previous = depth
    return None


def snapshot_action_cost(depth: int, packet_rank: int) -> int:
    """Count snapshot--packet products in a depth-limited action."""
    memory = int(depth)
    rank = int(packet_rank)
    if memory <= 0 or rank <= 0:
        raise ValueError("depth and packet rank must be positive")
    return memory * rank
