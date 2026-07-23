"""Finite-memory bounds for the relative second/third singular capacity."""

from __future__ import annotations

import math

import numpy as np


def _spectrum(values: list[float] | tuple[float, ...] | np.ndarray) -> np.ndarray:
    singular = np.asarray(values, dtype=float)
    if singular.ndim != 1 or singular.size < 4:
        raise ValueError("at least four singular values are required")
    if np.any(~np.isfinite(singular)) or np.any(singular < 0.0):
        raise ValueError("singular values must be finite and nonnegative")
    return np.sort(singular)[::-1]


def _radius(value: float) -> float:
    radius = float(value)
    if not math.isfinite(radius) or radius < 0.0:
        raise ValueError("the perturbation radius must be finite and nonnegative")
    return radius


def three_mode_capacity(values: list[float] | tuple[float, ...] | np.ndarray) -> float:
    """Return Lambda_23=(s2/s1)(s3/s1)."""
    singular = _spectrum(values)
    if singular[0] == 0.0:
        return 0.0
    return float(singular[1] * singular[2] / singular[0] ** 2)


def normalized_spectral_four_volume(
    values: list[float] | tuple[float, ...] | np.ndarray,
) -> float:
    singular = _spectrum(values)
    if singular[0] == 0.0:
        return 0.0
    return float(np.prod(singular[:4], dtype=float) / singular[0] ** 4)


def finite_memory_capacity_interval(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    tail_operator_bound: float,
) -> dict[str, float]:
    """Enclose Lambda_23 of a perturbed cross using singular-value Weyl bounds."""
    singular = _spectrum(recent_singular_values)
    delta = _radius(tail_operator_bound)
    lower = np.maximum(singular - delta, 0.0)
    upper = singular + delta
    lower_capacity = float(lower[1] * lower[2] / upper[0] ** 2) if upper[0] else 0.0
    upper_capacity = float(upper[1] * upper[2] / lower[0] ** 2) if lower[0] else math.inf
    return {
        "lower": lower_capacity,
        "upper": upper_capacity,
        "recent": three_mode_capacity(singular),
        "tail_operator_bound": delta,
    }


def capacity_aware_ratio_lower_bound(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    tail_operator_bound: float,
) -> dict[str, float]:
    """Recover q4 from a spectral-volume lower bound and a capacity upper bound."""
    singular = _spectrum(recent_singular_values)
    delta = _radius(tail_operator_bound)
    lower = np.maximum(singular - delta, 0.0)
    upper = singular + delta
    denominator = upper[0] ** 4
    volume_lower = float(np.prod(lower[:4], dtype=float) / denominator) if denominator else 0.0
    capacity = finite_memory_capacity_interval(singular, delta)
    capacity_upper = float(capacity["upper"])
    if not math.isfinite(capacity_upper) or capacity_upper <= 0.0:
        recovered = 0.0
    else:
        recovered = volume_lower / capacity_upper
    direct = float(lower[3] / upper[0]) if upper[0] else 0.0
    return {
        "spectral_volume_lower": volume_lower,
        "capacity_upper": capacity_upper,
        "recovered_ratio_lower": recovered,
        "direct_weyl_ratio_lower": direct,
        "recovery_efficiency": recovered / direct if direct > 0.0 else 0.0,
    }


def sharp_capacity_interval(normalized_volume: float) -> tuple[float, float]:
    """Sharp capacity interval at fixed normalized spectral four-volume."""
    volume = float(normalized_volume)
    if not math.isfinite(volume) or volume < 0.0 or volume > 1.0:
        raise ValueError("normalized volume must lie in [0, 1]")
    return volume ** (2.0 / 3.0), 1.0
