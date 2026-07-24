from __future__ import annotations

import math
from collections.abc import Iterable


def support_factor(tail_bound: float) -> float:
    y = float(tail_bound)
    if not math.isfinite(y) or y < 0.0:
        raise ValueError("tail bound must be finite and nonnegative")
    return max(0.0, 1.0 - math.sqrt(y)) ** 4


def support(tail_bound: float, base_lower: float) -> float:
    a = float(base_lower)
    if not math.isfinite(a) or a < 0.0:
        raise ValueError("base lower must be finite and nonnegative")
    return a * support_factor(tail_bound)


def tube_base_requirement(beta: float, tail_bound: float) -> float:
    target = float(beta)
    if not math.isfinite(target) or target < 0.0:
        raise ValueError("beta must be finite and nonnegative")
    factor = support_factor(tail_bound)
    if target == 0.0:
        return 0.0
    if factor == 0.0:
        return math.inf
    return target / factor


def tube_multiplier(source_tail: float, target_tail: float, base_ratio_lower: float) -> float:
    ratio = float(base_ratio_lower)
    if not math.isfinite(ratio) or ratio < 0.0:
        raise ValueError("base ratio lower must be finite and nonnegative")
    source_factor = support_factor(source_tail)
    if source_factor == 0.0:
        raise ValueError("source tail must be below the support wall")
    return ratio * support_factor(target_tail) / source_factor


def cocycle_lower(initial_support: float, multipliers: Iterable[float]) -> tuple[float, list[float]]:
    value = float(initial_support)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError("initial support must be finite and nonnegative")
    trajectory = [value]
    for multiplier in multipliers:
        factor = float(multiplier)
        if not math.isfinite(factor) or factor < 0.0:
            raise ValueError("multipliers must be finite and nonnegative")
        value *= factor
        trajectory.append(value)
    return min(trajectory), trajectory
