"""Perturbation bounds for spectral-reset tail coupling."""

from __future__ import annotations

import math


def coupling_radius(tail_norm: float, projector_radius: float, tail_radius: float) -> float:
    norm = float(tail_norm)
    projector = float(projector_radius)
    radius = float(tail_radius)
    if not all(math.isfinite(value) for value in (norm, projector, radius)):
        raise ValueError("non-finite coupling data")
    if norm < 0.0 or projector < 0.0 or projector > 1.0 or radius < 0.0:
        raise ValueError("invalid coupling data")
    return radius + 2.0 * norm * projector


def singular_interval(nominal_singular: float, operator_radius: float) -> tuple[float, float]:
    singular = float(nominal_singular)
    radius = float(operator_radius)
    if not math.isfinite(singular) or not math.isfinite(radius) or singular < 0.0 or radius < 0.0:
        raise ValueError("invalid singular-value data")
    return max(0.0, singular - radius), singular + radius
