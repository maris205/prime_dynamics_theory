"""Uniform native and directional floors for the reset-route dichotomy."""

from __future__ import annotations

import math


def native_interface_floor(
    overlap_ratio_lower: float,
    recent_full_ratio_lower: float,
    relative_tail_upper: float,
) -> float:
    """Uniform native floor from the three logically independent interfaces."""

    overlap = float(overlap_ratio_lower)
    spread = float(recent_full_ratio_lower)
    tail = float(relative_tail_upper)
    if not all(math.isfinite(value) for value in (overlap, spread, tail)):
        raise ValueError("non-finite native interface ratio")
    if overlap < 0.0 or overlap > 1.0 or spread < 0.0 or spread > 1.0 or tail < 0.0:
        raise ValueError("invalid native interface ratio")
    return overlap * math.sqrt(spread) * max(0.0, 1.0 - math.sqrt(tail)) ** 4


def native_uniform_floor(
    selected_lower: float,
    selected_upper: float,
    tail_upper: float,
    overlap_lower: float,
    overlap_upper: float = 1.0,
) -> dict[str, float | bool]:
    lower = float(selected_lower)
    upper = float(selected_upper)
    tail = float(tail_upper)
    alpha = float(overlap_lower)
    beta = float(overlap_upper)
    if not all(math.isfinite(value) for value in (lower, upper, tail, alpha, beta)):
        raise ValueError("non-finite native interface data")
    if lower <= 0.0 or upper < lower or tail < 0.0 or alpha < 0.0 or beta <= 0.0 or alpha > beta:
        raise ValueError("invalid native interface data")
    recent = lower - tail
    if recent <= 0.0:
        return {
            "recent_positive": False,
            "subunit_tail": False,
            "relative_tail_upper": math.inf,
            "normalized_recent_base_lower": 0.0,
            "tail_factor": 0.0,
            "support_floor": 0.0,
        }
    ratio = tail / recent
    base = alpha / beta * math.sqrt(recent / upper)
    factor = max(0.0, 1.0 - math.sqrt(ratio)) ** 4
    return {
        "recent_positive": True,
        "subunit_tail": ratio < 1.0,
        "relative_tail_upper": ratio,
        "normalized_recent_base_lower": base,
        "tail_factor": factor,
        "support_floor": native_interface_floor(alpha / beta, recent / upper, ratio),
    }


def directional_uniform_floor(
    overlap_lower: float,
    maximum_lag: int,
    fourth_cross_lower: float,
    first_cross_upper: float,
) -> float:
    alpha = float(overlap_lower)
    lag = int(maximum_lag)
    fourth = float(fourth_cross_lower)
    first = float(first_cross_upper)
    if not all(math.isfinite(value) for value in (alpha, fourth, first)):
        raise ValueError("non-finite directional interface data")
    if alpha < 0.0 or alpha > 1.0 or lag < 1 or fourth < 0.0 or first <= 0.0 or fourth > first:
        raise ValueError("invalid directional interface data")
    return alpha**lag * fourth / first


def directional_path_floor(
    path_overlap_lower: float,
    fourth_cross_lower: float,
    first_cross_upper: float,
) -> float:
    path = float(path_overlap_lower)
    fourth = float(fourth_cross_lower)
    first = float(first_cross_upper)
    if not all(math.isfinite(value) for value in (path, fourth, first)):
        raise ValueError("non-finite path interface data")
    if path < 0.0 or path > 1.0 or fourth < 0.0 or first <= 0.0 or fourth > first:
        raise ValueError("invalid path interface data")
    return path * fourth / first


def outward_cross_lowers(
    nominal_first: float,
    nominal_fourth: float,
    operator_radius: float,
) -> tuple[float, float]:
    first = float(nominal_first)
    fourth = float(nominal_fourth)
    radius = float(operator_radius)
    if not all(math.isfinite(value) for value in (first, fourth, radius)):
        raise ValueError("non-finite cross certificate data")
    if first < fourth or fourth < 0.0 or radius < 0.0:
        raise ValueError("invalid cross certificate data")
    return max(0.0, fourth - radius), first + radius
