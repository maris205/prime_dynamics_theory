from __future__ import annotations

import math


def _ratio(radius: float, outer_radius: float) -> float:
    if radius <= 0.0 or outer_radius <= radius:
        raise ValueError("require 0 < radius < outer_radius")
    return radius / outer_radius


def hinfty_bound(norm: float, radius: float = 1.4, outer_radius: float = 1.41) -> float:
    if norm < 0.0:
        raise ValueError("norm must be nonnegative")
    ratio = _ratio(radius, outer_radius)
    return norm * ratio**2 / (1.0 - ratio)


def hardy_bound(norm: float, radius: float = 1.4, outer_radius: float = 1.41) -> float:
    if norm < 0.0:
        raise ValueError("norm must be nonnegative")
    ratio = _ratio(radius, outer_radius)
    return norm * ratio**2 / math.sqrt(1.0 - ratio**2)


def endpoint_hardy_example(term_count: int) -> tuple[float, float]:
    if term_count < 1:
        raise ValueError("term count must be positive")
    return 1.0 / math.sqrt(term_count), 1.0
