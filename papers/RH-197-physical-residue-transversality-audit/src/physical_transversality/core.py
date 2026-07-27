"""Finite residue and cross-angle diagnostics for physical spectral packets."""

from __future__ import annotations

import numpy as np


def summarize(values) -> dict[str, float]:
    array = np.asarray(list(values), dtype=float)
    if array.size == 0:
        raise ValueError("cannot summarize an empty collection")
    return {
        "minimum": float(np.min(array)),
        "median": float(np.median(array)),
        "maximum": float(np.max(array)),
    }


def optimal_packet_condition(minimum_cross_singular_value: float) -> float:
    value = float(minimum_cross_singular_value)
    if value <= 0.0:
        raise ValueError("minimum cross singular value must be positive")
    return 1.0 / value


def conditioning_ratio(temporal_condition: float, canonical_condition: float) -> float:
    temporal = float(temporal_condition)
    canonical = float(canonical_condition)
    if min(temporal, canonical) <= 0.0:
        raise ValueError("conditions must be positive")
    return temporal / canonical


def normalized_residue_condition(normalized_overlap: float) -> float:
    value = float(normalized_overlap)
    if value <= 0.0:
        raise ValueError("normalized overlap must be positive")
    return 1.0 / value
