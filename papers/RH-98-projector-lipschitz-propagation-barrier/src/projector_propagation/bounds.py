"""Projector-metric bounds for local Ritz loss and endpoint propagation."""

from __future__ import annotations

import math


def endpoint_tail_lipschitz_bound(gram_frobenius_norm: float, projector_distance: float) -> float:
    gram = float(gram_frobenius_norm)
    distance = float(projector_distance)
    if not math.isfinite(gram) or not math.isfinite(distance) or gram < 0.0 or distance < 0.0:
        raise ValueError("nonnegative finite data are required")
    return math.nextafter(gram * distance, math.inf)


def local_gap_distance_bound(capture_loss: float, compressed_gap: float) -> float:
    loss = float(capture_loss)
    gap = float(compressed_gap)
    if not math.isfinite(loss) or not math.isfinite(gap) or loss < 0.0 or gap <= 0.0:
        raise ValueError("nonnegative loss and positive gap are required")
    return math.nextafter(math.sqrt(2.0 * loss / gap), math.inf)


def projector_secant_multiplier(local_distance: float, endpoint_distance: float) -> float:
    local = float(local_distance)
    endpoint = float(endpoint_distance)
    if not math.isfinite(local) or not math.isfinite(endpoint) or local <= 0.0 or endpoint < 0.0:
        raise ValueError("positive local and nonnegative endpoint distances are required")
    return math.nextafter(endpoint / local, math.inf)
