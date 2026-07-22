"""Polynomial upper and moment-coherence lower bounds on phase packets."""

from __future__ import annotations

import math


def arc_chord_radius(width: float) -> float:
    arc = float(width)
    if arc < 0.0 or arc > 2.0 * math.pi:
        raise ValueError("arc width must lie in [0,2pi]")
    if arc == 0.0:
        return 0.0
    return math.nextafter(2.0 * math.sin(arc / 4.0), math.inf)


def binomial_arc_remainder(horizon: int, depth: int, width: float) -> float:
    """Bound degree-(depth-1) truncation of z^horizon on one arc."""

    m = int(horizon)
    d = int(depth)
    if m < 0 or d < 0 or d > m + 1:
        raise ValueError("invalid horizon/depth")
    if d == m + 1:
        return 0.0
    delta = arc_chord_radius(width)
    if delta == 0.0:
        return 0.0
    total = 0.0
    for order in range(d, m + 1):
        total = math.nextafter(
            total + math.comb(m, order) * delta**order,
            math.inf,
        )
    return total


def coherence_residual_lower(depth: int, coherence: float) -> float:
    """Lower bound for a phase-moment Krylov residual."""

    d = int(depth)
    mu = float(coherence)
    if d <= 0 or mu < 0.0:
        raise ValueError("invalid coherence inputs")
    denominator = 1.0 - (d - 1) * mu
    if denominator <= 0.0:
        return 0.0
    square = 1.0 - d * mu * mu / denominator
    return math.sqrt(max(0.0, square))
