"""Conditional all-level gates for relative fourth-mode support."""

from __future__ import annotations

import math


def _nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def factorized_route_lower(volume_lower: float, capacity_upper: float) -> float:
    """Return ``volume_lower/capacity_upper`` with a safe zero convention."""
    volume = _nonnegative(volume_lower, "volume lower")
    capacity = float(capacity_upper)
    if not math.isfinite(capacity) or capacity <= 0.0:
        return 0.0
    return volume / capacity


def trace_route_lower(theta_lower: float, concentration_upper: float, capacity_upper: float) -> float:
    """Convert normalized exterior trace and concentration into a q4 lower."""
    theta = _nonnegative(theta_lower, "normalized exterior trace lower")
    concentration = float(concentration_upper)
    if not math.isfinite(concentration) or concentration <= 0.0:
        return 0.0
    volume = math.sqrt(theta / concentration)
    return factorized_route_lower(volume, capacity_upper)


def directional_route_lower(frame_volume_lower: float, gamma_upper: float, capacity_upper: float) -> float:
    """Apply the four-dimensional relative-Rayleigh factor and capacity gate."""
    frame = _nonnegative(frame_volume_lower, "frame volume lower")
    gamma = float(gamma_upper)
    if not math.isfinite(gamma) or gamma < 0.0:
        raise ValueError("gamma upper must be finite and nonnegative")
    volume = max(0.0, 1.0 - gamma) ** 4 * frame
    return factorized_route_lower(volume, capacity_upper)


def conditional_composite_gate(candidates: dict[str, float], threshold: float) -> dict[str, float | str | bool]:
    """Take the information-optimal maximum of admitted route lowers."""
    if not candidates:
        raise ValueError("at least one route candidate is required")
    cleaned = {name: _nonnegative(value, name) for name, value in candidates.items()}
    cutoff = float(threshold)
    if not math.isfinite(cutoff) or cutoff <= 0.0:
        raise ValueError("threshold must be finite and positive")
    selected = max(cleaned, key=cleaned.get)
    lower = cleaned[selected]
    return {
        "lower": lower,
        "selected_route": selected,
        "threshold": cutoff,
        "support_certified": lower >= cutoff,
        "margin": lower - cutoff,
    }


def outward_degraded_candidates(
    candidates: dict[str, float],
    transport_losses: dict[str, float],
) -> dict[str, float]:
    """Subtract route-specific outward transport losses before admission."""
    if set(candidates) != set(transport_losses):
        raise ValueError("candidate and transport-loss labels must agree")
    return {
        name: max(0.0, _nonnegative(candidates[name], name) - _nonnegative(transport_losses[name], name))
        for name in candidates
    }
