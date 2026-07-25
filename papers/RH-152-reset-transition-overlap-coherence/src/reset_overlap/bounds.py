"""Robust overlap and polar-transition bounds for reset packet frames."""

from __future__ import annotations

import math


def aligned_frame_radius(projector_radius: float) -> float:
    value = float(projector_radius)
    if not math.isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError("projector radius must lie in [0,1]")
    return math.sqrt(max(0.0, 2.0 - 2.0 * math.sqrt(max(0.0, 1.0 - value * value))))


def robust_overlap_lower(nominal_smin: float, left_radius: float, right_radius: float) -> dict[str, float | bool]:
    """Lower the smallest exact frame overlap singular value."""
    alpha = float(nominal_smin)
    left = float(left_radius)
    right = float(right_radius)
    if not all(math.isfinite(x) for x in (alpha, left, right)) or alpha < 0.0 or alpha > 1.0 or min(left, right) < 0.0 or max(left, right) > 1.0:
        raise ValueError("invalid overlap data")
    frame_error = aligned_frame_radius(left) + aligned_frame_radius(right)
    linear = max(0.0, alpha - frame_error)
    angle = math.acos(min(1.0, max(-1.0, alpha))) + math.asin(left) + math.asin(right)
    angular = max(0.0, math.cos(angle)) if angle < math.pi / 2.0 else 0.0
    lower = max(linear, angular)
    return {
        "nominal_smin": alpha,
        "frame_error": frame_error,
        "angular_sum": angle,
        "linear_lower": linear,
        "angular_lower": angular,
        "robust_lower": lower,
        "invertible": lower > 0.0,
    }


def overlap_inverse_upper(overlap_lower: float) -> float:
    lower = float(overlap_lower)
    if not math.isfinite(lower) or lower <= 0.0:
        return math.inf
    return 1.0 / lower


def polar_transition_radius(overlap_smin: float, overlap_error: float) -> dict[str, float | bool]:
    """Perturbation bound for the polar factor of a square overlap map."""
    alpha = float(overlap_smin)
    error = float(overlap_error)
    if not math.isfinite(alpha) or not math.isfinite(error) or alpha < 0.0 or error < 0.0:
        raise ValueError("invalid polar data")
    stable = alpha > error
    radius = min(2.0, 2.0 * error / (2.0 * alpha - error)) if stable else 2.0
    return {"stable": stable, "radius": radius}
