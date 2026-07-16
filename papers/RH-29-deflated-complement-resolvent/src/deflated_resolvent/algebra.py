"""Rigorous scalar algebra for one-channel Grushin resolvent reduction."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _up(value: float) -> float:
    result = float(value)
    if result < 0.0 or np.isnan(result):
        raise ValueError("an upper bound must be nonnegative")
    return float(np.nextafter(result, np.inf))


def _down(value: float) -> float:
    result = float(value)
    if result <= 0.0:
        return 0.0
    return float(np.nextafter(result, 0.0))


def _up_add(*values: float) -> float:
    total = 0.0
    for value in values:
        item = float(value)
        if item < 0.0 or np.isnan(item):
            raise ValueError("upper additions require nonnegative values")
        total = _up(total + item)
    return total


def _up_multiply(left: float, right: float) -> float:
    first = float(left)
    second = float(right)
    if first < 0.0 or second < 0.0 or np.isnan(first + second):
        raise ValueError("upper products require nonnegative values")
    return _up(first * second)


def _up_divide(numerator: float, denominator: float) -> float:
    top = float(numerator)
    bottom = float(denominator)
    if top < 0.0 or bottom <= 0.0 or np.isnan(top + bottom):
        raise ValueError("invalid outward division")
    lowered = float(np.nextafter(bottom, 0.0))
    if lowered <= 0.0:
        return float("inf")
    return _up(top / lowered)


def _down_divide(numerator: float, denominator: float) -> float:
    top = float(numerator)
    bottom = float(denominator)
    if top <= 0.0:
        return 0.0
    if bottom <= 0.0 or np.isnan(top + bottom):
        raise ValueError("invalid downward division")
    raised = float(np.nextafter(bottom, np.inf))
    return _down(_down(top) / raised)


@dataclass(frozen=True)
class NormInterval:
    """A positive interval known to contain one Euclidean norm."""

    lower: float
    upper: float

    def __post_init__(self) -> None:
        if self.lower <= 0.0 or self.upper < self.lower:
            raise ValueError("a norm interval must be positive and ordered")


@dataclass(frozen=True)
class NormalizedResidualBounds:
    """Residual bounds after exact normalization of stored trial vectors."""

    right: float
    left: float
    norm_mismatch: float


@dataclass(frozen=True)
class LiftedInverseEvaluation:
    """One conditional full-inverse bound obtained from a lifted inverse."""

    admissible: bool
    denominator_lower: float
    full_inverse_upper: float


def normalized_residual_bounds(
    raw_right_residual_upper: float,
    raw_left_residual_upper: float,
    right_norm: NormInterval,
    left_norm: NormInterval,
    singular_value: float,
) -> NormalizedResidualBounds:
    """Bound residuals for ``v/vnorm`` and ``u/unorm``.

    The raw stored vectors satisfy approximate equations with the same stored
    scalar ``singular_value``.  Exact normalization changes each equation by
    at most ``singular_value * |unorm-vnorm|`` divided by the relevant norm.
    """

    value = float(singular_value)
    if value <= 0.0:
        raise ValueError("the singular value must be positive")
    mismatch = max(
        abs(left_norm.lower - right_norm.upper),
        abs(left_norm.upper - right_norm.lower),
    )
    mismatch = _up(mismatch)
    right_numerator = _up_add(
        float(raw_right_residual_upper), _up_multiply(value, mismatch)
    )
    left_numerator = _up_add(
        float(raw_left_residual_upper), _up_multiply(value, mismatch)
    )
    return NormalizedResidualBounds(
        right=_up_divide(right_numerator, right_norm.lower),
        left=_up_divide(left_numerator, left_norm.lower),
        norm_mismatch=mismatch,
    )


def arc_center_threshold_lower(
    arc_resolvent_budget_lower: float, arc_disc_radius_upper: float
) -> float:
    """Return a sufficient center budget for Neumann transport over an arc."""

    budget = float(arc_resolvent_budget_lower)
    radius = float(arc_disc_radius_upper)
    if budget <= 0.0 or radius < 0.0:
        raise ValueError("the arc budget must be positive and radius nonnegative")
    denominator = _up_add(1.0, _up_multiply(radius, budget))
    return _down_divide(budget, denominator)


def lifted_full_inverse_upper(
    lifted_inverse_upper: float,
    singular_value: float,
    right_residual_upper: float,
    left_residual_upper: float,
    *,
    lift: float = 1.0,
) -> LiftedInverseEvaluation:
    r"""Bound ``||A^{-1}||`` from a rank-one lifted inverse.

    For unit vectors ``u,v``, put

    ``A_tilde = A + (tau-s) u v*``.

    If ``K >= ||A_tilde^{-1}||``, ``r=A v-su``, and
    ``q=A* u-sv``, Sherman--Morrison and the two lifted residual equations
    give

    ``||A^{-1}|| <= K + c(1+Kr)(1+Kq)/(tau(s-cKr))``,

    where ``c=|tau-s|``.  The formula is valid when ``s-cKr>0``.
    """

    inverse = float(lifted_inverse_upper)
    value = float(singular_value)
    tau = float(lift)
    right = float(right_residual_upper)
    left = float(left_residual_upper)
    if inverse < 0.0 or value <= 0.0 or tau <= 0.0:
        raise ValueError("inverse, singular value, and lift are invalid")
    if right < 0.0 or left < 0.0:
        raise ValueError("residual bounds must be nonnegative")
    coefficient = _up(abs(tau - value))
    loss = _up_multiply(coefficient, _up_multiply(inverse, right))
    denominator = _down(value - loss)
    if denominator <= 0.0:
        return LiftedInverseEvaluation(False, 0.0, float("inf"))
    right_factor = _up_add(1.0, _up_multiply(inverse, right))
    left_factor = _up_add(1.0, _up_multiply(inverse, left))
    numerator = _up_multiply(
        coefficient, _up_multiply(right_factor, left_factor)
    )
    correction = _up_divide(numerator, _up_multiply(tau, denominator))
    return LiftedInverseEvaluation(
        True,
        denominator,
        _up_add(inverse, correction),
    )


def lifted_inverse_budget_lower(
    center_inverse_budget_lower: float,
    singular_value: float,
    right_residual_upper: float,
    left_residual_upper: float,
    *,
    lift: float = 1.0,
    bisection_steps: int = 100,
) -> float:
    """Return a downward conditional budget for the lifted inverse norm."""

    target = float(center_inverse_budget_lower)
    if target <= 0.0:
        raise ValueError("the center inverse budget must be positive")
    zero = lifted_full_inverse_upper(
        0.0,
        singular_value,
        right_residual_upper,
        left_residual_upper,
        lift=lift,
    )
    if not zero.admissible or zero.full_inverse_upper >= target:
        return 0.0
    lower = 0.0
    upper = target
    for _ in range(int(bisection_steps)):
        midpoint = 0.5 * (lower + upper)
        evaluation = lifted_full_inverse_upper(
            midpoint,
            singular_value,
            right_residual_upper,
            left_residual_upper,
            lift=lift,
        )
        if evaluation.admissible and evaluation.full_inverse_upper < target:
            lower = midpoint
        else:
            upper = midpoint
    return _down(lower)


def candidate_arc_inverse(
    center_inverse_candidate: float, arc_disc_radius: float
) -> float:
    """Floating diagnostic for center-to-arc Neumann transport."""

    inverse = float(center_inverse_candidate)
    radius = float(arc_disc_radius)
    product = inverse * radius
    if inverse <= 0.0 or radius < 0.0 or product >= 1.0:
        return float("inf")
    return float(inverse / (1.0 - product))
