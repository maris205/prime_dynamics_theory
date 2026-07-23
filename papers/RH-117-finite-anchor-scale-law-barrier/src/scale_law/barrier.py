"""Positive smooth continuations through finitely many scale anchors."""

from __future__ import annotations

from collections.abc import Callable, Iterable
import math

import numpy as np


def _anchors(scales: Iterable[float], values: Iterable[float]) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(tuple(scales), dtype=float)
    y = np.asarray(tuple(values), dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size == 0 or x.size != y.size:
        raise ValueError("scales and values must be nonempty vectors of equal length")
    if np.any(~np.isfinite(x)) or np.any(x <= 0.0) or np.unique(x).size != x.size:
        raise ValueError("scales must be distinct, finite, and positive")
    if np.any(~np.isfinite(y)) or np.any(y <= 0.0):
        raise ValueError("anchor values must be finite and positive")
    order = np.argsort(x)
    return x[order], y[order]


def smooth_cutoff(points: Iterable[float], lower: float, upper: float) -> np.ndarray:
    """A C-infinity step equal to zero below ``lower`` and one above ``upper``."""
    x = np.asarray(tuple(points), dtype=float)
    left = float(lower)
    right = float(upper)
    if not math.isfinite(left) or not math.isfinite(right) or left < 0.0 or right <= left:
        raise ValueError("cutoff endpoints must satisfy 0 <= lower < upper")
    if np.any(~np.isfinite(x)) or np.any(x <= 0.0):
        raise ValueError("evaluation points must be finite and positive")
    output = np.zeros_like(x)
    output[x >= right] = 1.0
    middle = (x > left) & (x < right)
    if np.any(middle):
        coordinate = (x[middle] - left) / (right - left)
        rising = np.exp(-1.0 / coordinate)
        falling = np.exp(-1.0 / (1.0 - coordinate))
        output[middle] = rising / (rising + falling)
    return output


def log_lagrange_interpolant(
    scales: Iterable[float],
    values: Iterable[float],
    points: Iterable[float],
) -> np.ndarray:
    """Evaluate the polynomial interpolating the logarithms of positive anchors."""
    anchors, heights = _anchors(scales, values)
    x = np.asarray(tuple(points), dtype=float)
    if np.any(~np.isfinite(x)) or np.any(x <= 0.0):
        raise ValueError("evaluation points must be finite and positive")
    return _lagrange_interpolant(np.log(anchors), np.log(heights), np.log(x))


def _lagrange_interpolant(anchors: np.ndarray, heights: np.ndarray, points: np.ndarray) -> np.ndarray:
    output = np.zeros_like(points)
    for index, anchor in enumerate(anchors):
        basis = np.ones_like(points)
        for other_index, other in enumerate(anchors):
            if other_index != index:
                basis *= (points - other) / (anchor - other)
        output += heights[index] * basis
    return output


def anchor_matching_extension(
    scales: Iterable[float],
    values: Iterable[float],
    points: Iterable[float],
    germ: Callable[[np.ndarray], np.ndarray],
    *,
    lower_fraction: float = 0.4,
    upper_fraction: float = 0.8,
) -> np.ndarray:
    """Blend a prescribed positive germ into an exact positive anchor interpolant."""
    anchors, heights = _anchors(scales, values)
    x = np.asarray(tuple(points), dtype=float)
    if np.any(~np.isfinite(x)) or np.any(x <= 0.0):
        raise ValueError("evaluation points must be finite and positive")
    lower = float(lower_fraction) * anchors[0]
    upper = float(upper_fraction) * anchors[0]
    cutoff = smooth_cutoff(x, lower, upper)
    germ_values = np.asarray(germ(x), dtype=float)
    if germ_values.shape != x.shape or np.any(~np.isfinite(germ_values)) or np.any(germ_values <= 0.0):
        raise ValueError("the germ must return finite positive values")
    anchor_log = log_lagrange_interpolant(anchors, heights, x)
    return np.exp(cutoff * anchor_log + (1.0 - cutoff) * np.log(germ_values))


def bounded_anchor_matching_extension(
    scales: Iterable[float],
    values: Iterable[float],
    points: Iterable[float],
    germ: Callable[[np.ndarray], np.ndarray],
    *,
    lower: float = 0.0,
    upper: float = 1.0,
    lower_fraction: float = 0.4,
    upper_fraction: float = 0.8,
) -> np.ndarray:
    """Match anchors while keeping the extension strictly inside ``(lower, upper)``."""
    anchors, heights = _anchors(scales, values)
    floor = float(lower)
    ceiling = float(upper)
    if not math.isfinite(floor) or not math.isfinite(ceiling) or ceiling <= floor:
        raise ValueError("the target interval must be finite and nonempty")
    if np.any(heights <= floor) or np.any(heights >= ceiling):
        raise ValueError("anchor values must lie strictly inside the target interval")
    x = np.asarray(tuple(points), dtype=float)
    if np.any(~np.isfinite(x)) or np.any(x <= 0.0):
        raise ValueError("evaluation points must be finite and positive")
    lower_cutoff = float(lower_fraction) * anchors[0]
    upper_cutoff = float(upper_fraction) * anchors[0]
    cutoff = smooth_cutoff(x, lower_cutoff, upper_cutoff)
    germ_values = np.asarray(germ(x), dtype=float)
    if germ_values.shape != x.shape or np.any(~np.isfinite(germ_values)):
        raise ValueError("the germ must return finite values")
    if np.any(germ_values <= floor) or np.any(germ_values >= ceiling):
        raise ValueError("the germ must lie strictly inside the target interval")
    anchor_coordinates = np.log((heights - floor) / (ceiling - heights))
    germ_coordinates = np.log((germ_values - floor) / (ceiling - germ_values))
    interpolated = _lagrange_interpolant(np.log(anchors), anchor_coordinates, np.log(x))
    coordinate = cutoff * interpolated + (1.0 - cutoff) * germ_coordinates
    logistic = 1.0 / (1.0 + np.exp(-np.clip(coordinate, -700.0, 700.0)))
    return floor + (ceiling - floor) * logistic


def loglog_fit(scales: Iterable[float], values: Iterable[float]) -> dict[str, float | list[float]]:
    """Return a descriptive power-law fit and leave-one-out slope range."""
    x, y = _anchors(scales, values)
    if x.size < 3:
        raise ValueError("at least three anchors are required")
    log_x = np.log(x)
    log_y = np.log(y)
    exponent, intercept = np.polyfit(log_x, log_y, 1)
    predicted = intercept + exponent * log_x
    residual = log_y - predicted
    total = float(np.sum((log_y - np.mean(log_y)) ** 2))
    r_squared = 1.0 - float(np.sum(residual**2)) / total if total > 0.0 else 1.0
    leave_one_out = []
    for index in range(x.size):
        keep = np.arange(x.size) != index
        slope, _ = np.polyfit(log_x[keep], log_y[keep], 1)
        leave_one_out.append(float(slope))
    return {
        "exponent": float(exponent),
        "coefficient": float(math.exp(intercept)),
        "r_squared": r_squared,
        "maximum_multiplicative_residual": float(math.exp(np.max(np.abs(residual)))),
        "leave_one_out_exponents": leave_one_out,
        "leave_one_out_exponent_minimum": min(leave_one_out),
        "leave_one_out_exponent_maximum": max(leave_one_out),
    }
