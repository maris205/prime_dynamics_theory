"""Certified bounds for adaptive lagged spectral-reset cross actions."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from typing import Any


def centered_action_radius(
    matrix_radius: float,
    spectral_spread: float,
    projector_radius: float,
) -> float:
    """Radius for ``(I-Q) A Q`` around a nominal projected cross.

    The scalar-centered projector perturbation costs
    ``spectral_spread * projector_radius`` rather than the cruder
    ``2 * operator_norm * projector_radius``.
    """

    radius = float(matrix_radius)
    spread = float(spectral_spread)
    projector = float(projector_radius)
    if not all(math.isfinite(value) for value in (radius, spread, projector)):
        raise ValueError("non-finite action-radius data")
    if radius < 0.0 or spread < 0.0 or projector < 0.0 or projector > 1.0:
        raise ValueError("invalid action-radius data")
    return radius + spread * projector


def singular_interval(nominal_singular: float, operator_radius: float) -> tuple[float, float]:
    singular = float(nominal_singular)
    radius = float(operator_radius)
    if not math.isfinite(singular) or not math.isfinite(radius) or singular < 0.0 or radius < 0.0:
        raise ValueError("invalid singular-value data")
    return max(0.0, singular - radius), singular + radius


def path_overlap_lower(overlap_lowers: Iterable[float]) -> float:
    """Multiplicative lower for a product of invertible frame overlaps."""

    product = 1.0
    for value in overlap_lowers:
        lower = float(value)
        if not math.isfinite(lower) or lower < 0.0 or lower > 1.0:
            raise ValueError("invalid overlap lower")
        product *= lower
    return product


def choose_adaptive_candidate(candidates: Iterable[Mapping[str, Any]]) -> Mapping[str, Any]:
    """Choose maximal certified normalized base, breaking ties by short lag."""

    records = list(candidates)
    if not records:
        raise ValueError("at least one lag candidate is required")
    for record in records:
        base = float(record["normalized_base_lower"])
        lag = int(record["lag"])
        if not math.isfinite(base) or base < 0.0 or lag < 1:
            raise ValueError("invalid lag candidate")
    return max(records, key=lambda item: (float(item["normalized_base_lower"]), -int(item["lag"])))
