"""Telescoping common-contour Riesz projection bounds."""

from __future__ import annotations

import math
from collections.abc import Iterable


def projector_step_bound(
    contour_length: float,
    source_resolvent_upper: float,
    target_resolvent_upper: float,
    operator_defect_upper: float,
) -> dict[str, float | bool]:
    length, source, target, defect = map(
        float,
        (contour_length, source_resolvent_upper, target_resolvent_upper, operator_defect_upper),
    )
    if not all(math.isfinite(value) for value in (length, source, target, defect)):
        raise ValueError("inputs must be finite")
    if min(length, source, target, defect) < 0.0:
        raise ValueError("inputs must be nonnegative")
    bound = length * source * target * defect / (2.0 * math.pi)
    return {
        "projector_step_upper": bound,
        "stable_range_transport": bound < 1.0,
        "range_inverse_upper": 1.0 / (1.0 - bound) if bound < 1.0 else math.inf,
    }


def transport_chain(step_bounds: Iterable[float]) -> dict[str, float | bool]:
    values = tuple(float(value) for value in step_bounds)
    if not all(math.isfinite(value) and value >= 0.0 for value in values):
        raise ValueError("step bounds must be finite and nonnegative")
    total = sum(values)
    return {
        "step_count": len(values),
        "all_local_transports_stable": all(value < 1.0 for value in values),
        "telescoping_upper": total,
        "finite_sum_for_displayed_chain": math.isfinite(total),
    }
