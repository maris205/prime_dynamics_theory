"""Exact scalar optimization for a Young-split affine recurrence."""

from __future__ import annotations

import math
from collections.abc import Iterable


def _nonnegative(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def optimal_young_step(metric_base: float, frame_base: float, birth: float, source: float) -> dict[str, float | None]:
    """Minimize A(1+tau)x + q + B(1+1/tau) over tau > 0."""
    a = _nonnegative(metric_base, "metric base")
    b = _nonnegative(frame_base, "frame base")
    q = _nonnegative(birth, "birth")
    x = _nonnegative(source, "source")
    envelope = q + (math.sqrt(a * x) + math.sqrt(b)) ** 2
    tau = math.sqrt(b / (a * x)) if a * x > 0.0 and b > 0.0 else None
    return {"envelope": envelope, "tau": tau}


def safety_radius(metric_base: float, frame_base: float, birth: float, threshold: float = 1.0) -> float:
    """Largest source x whose optimized next envelope is strictly below threshold."""
    a = _nonnegative(metric_base, "metric base")
    b = _nonnegative(frame_base, "frame base")
    q = _nonnegative(birth, "birth")
    level = _nonnegative(threshold, "threshold")
    if q + b >= level:
        return 0.0
    if a == 0.0:
        return math.inf
    return (math.sqrt(level - q) - math.sqrt(b)) ** 2 / a


def fixed_point(metric_base: float, frame_base: float, birth: float) -> float:
    """Return the unique nonnegative fixed point of the optimized map when A < 1."""
    a = _nonnegative(metric_base, "metric base")
    b = _nonnegative(frame_base, "frame base")
    q = _nonnegative(birth, "birth")
    if a >= 1.0:
        return math.inf
    root = (math.sqrt(a * b) + math.sqrt(b + (1.0 - a) * q)) / (1.0 - a)
    return root**2


def greedy_step(candidates: Iterable[tuple[float, float, float]], source: float) -> dict[str, float | int | None]:
    """Choose the candidate with the smallest pointwise-optimal envelope."""
    values = list(candidates)
    if not values:
        raise ValueError("at least one candidate is required")
    evaluated = [optimal_young_step(a, b, q, source) for a, b, q in values]
    index = min(range(len(evaluated)), key=lambda item: evaluated[item]["envelope"])
    return {"index": index, **evaluated[index]}
