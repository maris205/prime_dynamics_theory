"""Exact geometric-cloud identities and trace-class determinant bounds."""

from __future__ import annotations

import cmath
import math


def ideal_cloud_factor(q: complex, degree: int) -> complex:
    """Return Pi_N(q)^2, with the removable value at q=1."""
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    value = complex(q)
    if value == 1:
        return complex((degree + 1) ** 2)
    return ((1.0 - value ** (degree + 1)) / (1.0 - value)) ** 2


def fixed_pole_cancellation(q: complex, degree: int) -> complex:
    """Return (1-q)^2 Pi_N(q)^2 = (1-q^(N+1))^2."""
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    value = complex(q)
    return (1.0 - value ** (degree + 1)) ** 2


def interior_cancellation_error_bound(radius_ratio: float, degree: int) -> float:
    """Uniform error for fixed pole cancellation on |q| <= radius_ratio < 1."""
    radius = float(radius_ratio)
    if not 0.0 <= radius < 1.0:
        raise ValueError("radius_ratio must lie in [0,1)")
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    power = radius ** (degree + 1)
    return math.nextafter(2.0 * power + power * power, math.inf)


def complement_normal_bound(radius: float, trace_norm_upper: float) -> float:
    """Bound |det(I-wT)| on |w|<=radius from ||T||_1."""
    disk = float(radius)
    trace = float(trace_norm_upper)
    if min(disk, trace) < 0.0:
        raise ValueError("bounds must be nonnegative")
    return math.nextafter(math.exp(disk * trace), math.inf)


def determinant_continuity_bound(
    radius: float,
    trace_error: float,
    left_trace_norm: float,
    right_trace_norm: float,
) -> float:
    """Standard trace-class determinant continuity bound on a disk."""
    disk = float(radius)
    error = float(trace_error)
    left = float(left_trace_norm)
    right = float(right_trace_norm)
    if min(disk, error, left, right) < 0.0:
        raise ValueError("bounds must be nonnegative")
    value = disk * error * math.exp(1.0 + disk * (left + right))
    return math.nextafter(value, math.inf)

