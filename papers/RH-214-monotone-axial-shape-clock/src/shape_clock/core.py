"""Finite monotone-clock and corridor diagnostics."""

from __future__ import annotations

import numpy as np


def ordered_increments(sigmas: np.ndarray, values: np.ndarray) -> np.ndarray:
    scales = np.asarray(sigmas, dtype=float).reshape(-1)
    data = np.asarray(values, dtype=float).reshape(-1)
    if scales.size != data.size or scales.size < 2:
        raise ValueError("paired scale and value arrays of length at least two are required")
    order = np.argsort(-scales)  # coarse to fine: sigma decreases
    return np.diff(data[order])


def monotone_clock_summary(sigmas: np.ndarray, values: np.ndarray) -> dict[str, float | int | bool]:
    increments = ordered_increments(sigmas, values)
    return {
        "transition_count": int(increments.size),
        "strict_increase_count": int(np.sum(increments > 0.0)),
        "strictly_increasing": bool(np.all(increments > 0.0)),
        "minimum_increment": float(np.min(increments)),
        "maximum_increment": float(np.max(increments)),
        "total_variation": float(np.sum(np.abs(increments))),
        "net_change": float(np.sum(increments)),
    }


def corridor_summary(values: np.ndarray) -> dict[str, float]:
    data = np.asarray(values, dtype=float).reshape(-1)
    if not data.size:
        raise ValueError("a nonempty corridor sample is required")
    return {
        "minimum": float(np.min(data)),
        "maximum": float(np.max(data)),
        "width": float(np.ptp(data)),
        "mean": float(np.mean(data)),
        "rms_about_mean": float(np.sqrt(np.mean((data - np.mean(data)) ** 2))),
        "total_variation": float(np.sum(np.abs(np.diff(data)))),
    }


def paired_channel_summary(left: np.ndarray, right: np.ndarray) -> dict[str, float]:
    first = np.asarray(left, dtype=float).reshape(-1)
    second = np.asarray(right, dtype=float).reshape(-1)
    if first.shape != second.shape or not first.size:
        raise ValueError("paired nonempty channels are required")
    difference = first - second
    return {
        "maximum_absolute_discrepancy": float(np.max(np.abs(difference))),
        "mean_absolute_discrepancy": float(np.mean(np.abs(difference))),
        "rms_discrepancy": float(np.sqrt(np.mean(difference**2))),
        "signed_mean_discrepancy": float(np.mean(difference)),
    }


def piecewise_linear_clock(t: np.ndarray, u: np.ndarray, query: np.ndarray) -> np.ndarray:
    """The unique linear interpolant through a strictly ordered finite clock."""

    times = np.asarray(t, dtype=float).reshape(-1)
    values = np.asarray(u, dtype=float).reshape(-1)
    points = np.asarray(query, dtype=float)
    if times.size != values.size or times.size < 2 or not np.all(np.diff(times) > 0.0):
        raise ValueError("strictly increasing clock times are required")
    if not np.all(np.diff(values) > 0.0):
        raise ValueError("strictly increasing clock values are required")
    return np.interp(points, times, values)
