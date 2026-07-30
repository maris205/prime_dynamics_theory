"""Exact bookkeeping helpers for the RH-270 certificate ledger."""

from __future__ import annotations

import math
from typing import Mapping


OBLIGATION_ORDER = (
    "legal_anchored_head",
    "coefficient_bridge",
    "uniform_quotient_tail",
    "analytic_target_tail",
    "certified_target_boundary_constant",
)


def _finite_nonnegative(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def geometric_log_tail_bound(
    envelope_constant: float, base: float, radius: float, first_omitted_order: int
) -> float:
    """Bound ``sum_{n>=N} |a_n| R^n/n`` from ``|a_n| < C q^n``.

    Since ``1/n <= 1/N`` for ``n >= N``, the geometric sum is
    ``C (qR)^N / (N (1-qR))``.  The strict input ``qR < 1`` is checked
    explicitly because this is an analytic tail interface, not a finite fit.
    """

    constant = _finite_nonnegative(envelope_constant, "envelope constant")
    q = float(base)
    radius = float(radius)
    order = int(first_omitted_order)
    if not math.isfinite(q) or not math.isfinite(radius):
        raise ValueError("base and radius must be finite")
    if q < 0.0 or radius < 0.0 or order < 1:
        raise ValueError("require nonnegative base/radius and positive order")
    ratio = q * radius
    if ratio >= 1.0:
        raise ValueError("require base times radius < 1")
    if ratio == 0.0:
        return 0.0
    return float(constant * ratio**order / (order * (1.0 - ratio)))


def safe_ratio(numerator: float, denominator: float) -> float:
    """Return a finite nonnegative comparison ratio."""

    top = _finite_nonnegative(numerator, "numerator")
    bottom = _finite_nonnegative(denominator, "denominator")
    if bottom == 0.0:
        raise ValueError("denominator must be positive")
    return float(top / bottom)


def obligation_status(**values: bool) -> dict[str, object]:
    """Normalize the five logically independent certificate obligations."""

    missing = set(values) - set(OBLIGATION_ORDER)
    if missing:
        raise ValueError(f"unknown obligations: {sorted(missing)}")
    if set(values) != set(OBLIGATION_ORDER):
        raise ValueError("all five obligations are required")
    components: Mapping[str, bool] = {
        name: bool(values[name]) for name in OBLIGATION_ORDER
    }
    vector = [components[name] for name in OBLIGATION_ORDER]
    satisfied = sum(vector)
    return {
        "order": list(OBLIGATION_ORDER),
        "components": dict(components),
        "obligation_vector": vector,
        "required_component_count": len(vector),
        "satisfied_component_count": satisfied,
        "complete": satisfied == len(vector),
    }
