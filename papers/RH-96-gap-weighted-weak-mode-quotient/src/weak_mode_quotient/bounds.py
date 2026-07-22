"""Weak-mode quotient selection and finite-dimensional tail-loss bounds."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def adaptive_width(singular_values: Iterable[float], relative_threshold: float, minimum: int = 1, maximum: int | None = None) -> int:
    singular = np.asarray(tuple(float(value) for value in singular_values), dtype=float)
    threshold = float(relative_threshold)
    floor = int(minimum)
    ceiling = singular.size if maximum is None else min(int(maximum), singular.size)
    if singular.ndim != 1 or singular.size == 0 or np.any(singular < 0.0) or singular[0] <= 0.0:
        raise ValueError("positive leading singular data are required")
    if not math.isfinite(threshold) or threshold < 0.0 or floor <= 0 or floor > ceiling:
        raise ValueError("invalid adaptive-width parameters")
    retained = int(np.count_nonzero(singular[:ceiling] / singular[0] >= threshold))
    return max(floor, min(ceiling, retained))


def gap_weighted_tail_loss_bound(cross_frobenius_norm: float, retained_cutoff: float, omitted_spectral_upper: float) -> float:
    cross = float(cross_frobenius_norm)
    alpha = float(retained_cutoff)
    beta = float(omitted_spectral_upper)
    if not all(math.isfinite(value) for value in (cross, alpha, beta)) or cross < 0.0 or alpha <= beta:
        raise ValueError("a positive retained-to-omitted gap is required")
    return math.nextafter(cross * cross / (alpha - beta), math.inf)


def universal_omitted_block_bound(cross_nuclear_norm: float, omitted_trace: float) -> float:
    cross = float(cross_nuclear_norm)
    trace = float(omitted_trace)
    if not math.isfinite(cross) or not math.isfinite(trace) or cross < 0.0 or trace < 0.0:
        raise ValueError("nonnegative finite block data are required")
    return math.nextafter(2.0 * cross + trace, math.inf)
