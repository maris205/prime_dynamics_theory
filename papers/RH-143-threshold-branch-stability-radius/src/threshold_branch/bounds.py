"""Threshold-branch and projected-cross perturbation bounds."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def _singular(values: Iterable[float]) -> np.ndarray:
    singular = np.asarray(tuple(float(value) for value in values), dtype=float)
    if singular.ndim != 1 or singular.size == 0 or np.any(~np.isfinite(singular)) or np.any(singular < 0.0):
        raise ValueError("singular values must be finite and nonnegative")
    if singular[0] <= 0.0 or np.any(singular[:-1] < singular[1:]):
        raise ValueError("positive nonincreasing singular values are required")
    return singular


def selected_width(values: Iterable[float], threshold: float, minimum: int = 1, maximum: int | None = None) -> int:
    singular = _singular(values)
    tau = float(threshold)
    floor = int(minimum)
    ceiling = singular.size if maximum is None else min(int(maximum), singular.size)
    if not math.isfinite(tau) or tau < 0.0 or floor <= 0 or floor > ceiling:
        raise ValueError("invalid threshold policy")
    count = int(np.count_nonzero(singular[:ceiling] / singular[0] >= tau))
    return max(floor, min(ceiling, count))


def branch_radius(values: Iterable[float], threshold: float, minimum: int = 1, maximum: int | None = None) -> dict[str, float | int]:
    """Largest open operator ball preserving the clipped threshold width."""
    singular = _singular(values)
    tau = float(threshold)
    floor = int(minimum)
    ceiling = singular.size if maximum is None else min(int(maximum), singular.size)
    width = selected_width(singular, tau, floor, ceiling)
    margins: list[float] = []
    if width > floor:
        margins.append((singular[width - 1] - tau * singular[0]) / (1.0 + tau))
    if width < ceiling:
        margins.append((tau * singular[0] - singular[width]) / (1.0 + tau))
    radius = min(margins, default=math.inf)
    radius = max(0.0, float(radius))
    return {
        "selected_width": width,
        "absolute_radius": radius,
        "relative_radius": radius / singular[0],
    }


def cross_projector_error_bound(matrix_error: float, reference_norm: float, projector_error: float) -> float:
    """Bound K(A,P)-K(B,Q), K(A,P)=(I-P)AP."""
    delta = float(matrix_error)
    norm = float(reference_norm)
    angle = float(projector_error)
    if not all(math.isfinite(value) for value in (delta, norm, angle)) or min(delta, norm, angle) < 0.0:
        raise ValueError("errors and norm must be finite and nonnegative")
    return delta + 2.0 * norm * angle

