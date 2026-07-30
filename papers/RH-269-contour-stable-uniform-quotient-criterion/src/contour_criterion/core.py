"""Quantitative checklist for contour-stable quotient uniformity."""

from __future__ import annotations

import math


def riesz_projection_difference_bound(
    contour_length: float, resolvent_bound: float, operator_difference: float
) -> float:
    """Bound ||P_sigma-P_0|| by the resolvent identity."""

    length = float(contour_length); bound = float(resolvent_bound); delta = float(operator_difference)
    if length <= 0.0 or bound <= 0.0 or delta < 0.0:
        raise ValueError("invalid contour, resolvent, or difference bound")
    return float(length * bound * bound * delta / (2.0 * math.pi))


def criterion_status(
    *,
    hilbert_schmidt_convergence: bool,
    common_finite_rank_isolating_contour: bool,
    uniform_resolvent_bound: bool,
    limit_block_contraction: bool,
) -> dict[str, object]:
    fields = {
        "hilbert_schmidt_convergence": bool(hilbert_schmidt_convergence),
        "common_finite_rank_isolating_contour": bool(
            common_finite_rank_isolating_contour
        ),
        "uniform_resolvent_bound": bool(uniform_resolvent_bound),
        "limit_block_contraction": bool(limit_block_contraction),
    }
    satisfied = sum(fields.values())
    return {
        **fields,
        "satisfied_hypothesis_count": satisfied,
        "required_hypothesis_count": len(fields),
        "criterion_complete": satisfied == len(fields),
    }
