"""Differential norm bounds for the invariant projected-cross Ritz map."""

from __future__ import annotations

import math


def spectral_projector_derivative_bound(operator_derivative_norm: float, spectral_gap: float) -> float:
    derivative = float(operator_derivative_norm)
    gap = float(spectral_gap)
    if not math.isfinite(derivative) or not math.isfinite(gap) or derivative < 0.0 or gap <= 0.0:
        raise ValueError("nonnegative derivative and positive gap are required")
    return math.nextafter(2.0 * derivative / gap, math.inf)


def cross_covariance_derivative_bound(gram_operator_norm: float, projector_derivative_norm: float) -> float:
    gram = float(gram_operator_norm)
    derivative = float(projector_derivative_norm)
    if not math.isfinite(gram) or not math.isfinite(derivative) or gram < 0.0 or derivative < 0.0:
        raise ValueError("nonnegative finite norms are required")
    return math.nextafter(3.0 * gram * gram * derivative, math.inf)


def two_gap_refresh_derivative_bound(gram_operator_norm: float, cross_squared_gap: float, ritz_gap: float) -> float:
    gram = float(gram_operator_norm)
    cross_gap = float(cross_squared_gap)
    output_gap = float(ritz_gap)
    if not all(math.isfinite(value) for value in (gram, cross_gap, output_gap)) or gram < 0.0 or cross_gap <= 0.0 or output_gap <= 0.0:
        raise ValueError("positive cross and Ritz gaps are required")
    value = 4.0 * gram / output_gap * (1.0 + 6.0 * gram * gram / cross_gap)
    return math.nextafter(value, math.inf)
