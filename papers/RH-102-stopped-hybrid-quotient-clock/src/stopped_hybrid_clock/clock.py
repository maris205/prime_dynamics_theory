"""Scalar accounting laws for stopped nonlinear hybrid quotient clocks."""

from __future__ import annotations

import math
from collections.abc import Iterable


def _finite_nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def hybrid_contributions(endpoint_values: Iterable[float]) -> tuple[float, ...]:
    values = tuple(float(value) for value in endpoint_values)
    if len(values) < 2 or any(not math.isfinite(value) for value in values):
        raise ValueError("at least two finite endpoint values are required")
    return tuple(values[index] - values[index - 1] for index in range(1, len(values)))


def absolute_debits(contributions: Iterable[float]) -> tuple[float, ...]:
    values = tuple(float(value) for value in contributions)
    if any(not math.isfinite(value) for value in values):
        raise ValueError("contributions must be finite")
    return tuple(abs(value) for value in values)


def cumulative_budget(debits: Iterable[float]) -> tuple[float, ...]:
    total = 0.0
    output = []
    for debit in debits:
        total += _finite_nonnegative(debit, "debit")
        output.append(math.nextafter(total, math.inf))
    return tuple(output)


def gate_slack(reference_lower: float, baseline_upper: float, gate: float = 1.01) -> float:
    reference = _finite_nonnegative(reference_lower, "reference lower bound")
    baseline = _finite_nonnegative(baseline_upper, "baseline upper bound")
    target = float(gate)
    if not math.isfinite(target) or target <= 0.0:
        raise ValueError("gate must be finite and positive")
    return max(0.0, math.nextafter(target * reference - baseline, -math.inf))


def stopped_allowance(
    reference_lower: float,
    baseline_upper: float,
    *,
    gate: float = 1.01,
    safety_fraction: float = 0.99,
) -> float:
    fraction = float(safety_fraction)
    if not math.isfinite(fraction) or fraction < 0.0 or fraction > 1.0:
        raise ValueError("safety fraction must lie in [0, 1]")
    value = fraction * gate_slack(reference_lower, baseline_upper, gate)
    return 0.0 if value == 0.0 else math.nextafter(value, -math.inf)


def debit_fits(spent: float, debit: float, allowance: float) -> bool:
    used = _finite_nonnegative(spent, "spent budget")
    proposed = _finite_nonnegative(debit, "debit")
    limit = _finite_nonnegative(allowance, "allowance")
    return math.nextafter(used + proposed, math.inf) <= limit


def certified_endpoint_upper(baseline_upper: float, spent: float) -> float:
    baseline = _finite_nonnegative(baseline_upper, "baseline upper bound")
    used = _finite_nonnegative(spent, "spent budget")
    return math.nextafter(baseline + used, math.inf)


def remaining_budget(allowance: float, spent: float) -> float:
    limit = _finite_nonnegative(allowance, "allowance")
    used = _finite_nonnegative(spent, "spent budget")
    return max(0.0, math.nextafter(limit - used, -math.inf))
