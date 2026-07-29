"""Exact budget arithmetic for anchored head--tail certificates."""

from __future__ import annotations

import math


def _finite_nonnegative(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def logarithmic_certificate_bound(
    head_error: float,
    quotient_tail_bound: float,
    target_tail_bound: float,
) -> float:
    """Add the three independent logarithmic error budgets."""

    values = (
        _finite_nonnegative(head_error, "head error"),
        _finite_nonnegative(quotient_tail_bound, "quotient tail bound"),
        _finite_nonnegative(target_tail_bound, "target tail bound"),
    )
    return float(math.fsum(values))


def determinant_certificate_bound(
    target_log_budget: float,
    log_difference_bound: float,
) -> float:
    """Convert a logarithmic difference into an absolute determinant bound.

    If ``|L_*| <= B`` and ``|L-L_*| <= E``, then
    ``|exp(L)-exp(L_*)| <= exp(B) * (exp(E)-1)``.
    """

    target = _finite_nonnegative(target_log_budget, "target log budget")
    difference = _finite_nonnegative(
        log_difference_bound, "logarithmic difference bound"
    )
    return float(math.exp(target) * math.expm1(difference))


def cauchy_target_tail_bound(
    boundary_supremum_bound: float,
    disk_radius: float,
    cauchy_radius: float,
    first_omitted_order: int,
) -> float:
    """Return the RH-252 Cauchy target-tail budget from a certified ``M_S``."""

    boundary = _finite_nonnegative(
        boundary_supremum_bound, "boundary supremum bound"
    )
    inner = float(disk_radius)
    outer = float(cauchy_radius)
    order = int(first_omitted_order)
    if not math.isfinite(inner) or not math.isfinite(outer):
        raise ValueError("radii must be finite")
    if inner < 0.0 or outer <= 0.0 or inner >= outer or order < 1:
        raise ValueError("require 0 <= R < S and a positive omitted order")
    ratio = inner / outer
    return float(boundary * ratio**order / (1.0 - ratio))


def complete_certificate_status(
    *,
    legal_anchored_head: bool,
    coefficient_bridge: bool,
    uniform_quotient_tail: bool,
    analytic_target_tail: bool,
    certified_target_boundary_constant: bool,
) -> dict[str, object]:
    """Record the logically independent obligations of a complete certificate."""

    components = {
        "legal_anchored_head": bool(legal_anchored_head),
        "coefficient_bridge": bool(coefficient_bridge),
        "uniform_quotient_tail": bool(uniform_quotient_tail),
        "analytic_target_tail": bool(analytic_target_tail),
        "certified_target_boundary_constant": bool(
            certified_target_boundary_constant
        ),
    }
    return {
        "components": components,
        "required_component_count": len(components),
        "satisfied_component_count": sum(components.values()),
        "complete": all(components.values()),
    }
