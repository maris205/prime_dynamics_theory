"""Universal bounds for a spectral-reset recent/tail memory pair."""

from __future__ import annotations

import math


def geometric_tail_mass(eta: float, depth: int, time: int | None = None) -> float:
    decay = float(eta)
    cutoff = int(depth)
    if not math.isfinite(decay) or decay < 0.0 or decay >= 1.0 or cutoff < 0:
        raise ValueError("invalid geometric-memory data")
    if time is not None:
        endpoint = int(time)
        if endpoint < 0:
            raise ValueError("time must be nonnegative")
        if endpoint < cutoff:
            return 0.0
        return decay**cutoff * (1.0 - decay ** (endpoint - cutoff + 1)) / (1.0 - decay)
    return decay**cutoff / (1.0 - decay)


def full_tail_ratio_upper(packet_eigenvalue_lower: float, tail_mass_upper: float) -> float:
    eigenvalue = float(packet_eigenvalue_lower)
    tail = float(tail_mass_upper)
    if not math.isfinite(eigenvalue) or not math.isfinite(tail) or eigenvalue <= 0.0 or tail < 0.0:
        raise ValueError("invalid packet/tail endpoints")
    return tail / eigenvalue


def recent_tail_ratio_upper(packet_eigenvalue_lower: float, tail_mass_upper: float) -> dict[str, float | bool]:
    eigenvalue = float(packet_eigenvalue_lower)
    tail = float(tail_mass_upper)
    if not math.isfinite(eigenvalue) or not math.isfinite(tail) or eigenvalue <= 0.0 or tail < 0.0:
        raise ValueError("invalid packet/tail endpoints")
    denominator = eigenvalue - tail
    if denominator <= 0.0:
        return {"recent_positive": False, "subunit": False, "ratio_upper": math.inf, "twice_tail_margin": eigenvalue / (2.0 * tail) if tail > 0.0 else math.inf}
    ratio = tail / denominator
    return {
        "recent_positive": True,
        "subunit": ratio < 1.0,
        "ratio_upper": ratio,
        "twice_tail_margin": eigenvalue / (2.0 * tail) if tail > 0.0 else math.inf,
    }
