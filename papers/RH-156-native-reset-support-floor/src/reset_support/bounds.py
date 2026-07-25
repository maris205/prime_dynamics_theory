"""Sharp native reset support composition."""

from __future__ import annotations

import math


def support_tail_factor(relative_tail_upper: float) -> float:
    value = float(relative_tail_upper)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError("invalid relative-tail upper")
    return max(0.0, 1.0 - math.sqrt(value)) ** 4


def native_support_lower(
    full_eigenvalue_lower: float,
    full_eigenvalue_upper: float,
    tail_mass_upper: float,
    overlap_lower: float,
    overlap_upper: float = 1.0,
) -> dict[str, float | bool]:
    lower = float(full_eigenvalue_lower)
    upper = float(full_eigenvalue_upper)
    tail = float(tail_mass_upper)
    alpha = float(overlap_lower)
    beta = float(overlap_upper)
    if not all(math.isfinite(value) for value in (lower, upper, tail, alpha, beta)):
        raise ValueError("non-finite support data")
    if lower <= 0.0 or upper < lower or tail < 0.0 or alpha < 0.0 or beta <= 0.0 or alpha > beta:
        raise ValueError("invalid support data")
    recent_lower = lower - tail
    if recent_lower <= 0.0:
        return {"recent_positive": False, "subunit_tail": False, "recent_base_lower": 0.0, "relative_tail_upper": math.inf, "tail_factor": 0.0, "support_lower": 0.0}
    ratio = tail / recent_lower
    base = alpha / beta * math.sqrt(recent_lower / upper)
    factor = support_tail_factor(ratio)
    return {
        "recent_positive": True,
        "subunit_tail": ratio < 1.0,
        "recent_base_lower": base,
        "relative_tail_upper": ratio,
        "tail_factor": factor,
        "support_lower": base * factor,
    }
