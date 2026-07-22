"""Scalar forms of the RH-86 energy bounds."""

from __future__ import annotations

import math


def memory_mass(eta: float, horizon: int) -> dict[str, float]:
    """Current and preceding trace mass of a geometric memory."""

    decay = float(eta)
    j = int(horizon)
    if not 0.0 <= decay < 1.0 or j < 0:
        raise ValueError("require 0 <= eta < 1 and nonnegative horizon")
    total = (1.0 - decay ** (j + 1)) / (1.0 - decay)
    return {"total": total, "past": total - 1.0, "past_fraction": (total - 1.0) / total}


def relative_stack_bound(current_tail: float, prefix_leakage: float) -> float:
    """Gap-free normalized-stack residual bound."""

    current = float(current_tail)
    prefix = float(prefix_leakage)
    if current < 0.0 or prefix < 0.0:
        raise ValueError("tail and leakage must be nonnegative")
    return math.nextafter(math.sqrt(current * current + prefix * prefix), math.inf)


def suffix_relative_bound(power_norm: float, snapshot_norm: float, terminal_norm: float, snapshot_relative_tail: float) -> float:
    """Relative terminal residual after suffix propagation."""

    power = float(power_norm)
    snapshot = float(snapshot_norm)
    terminal = float(terminal_norm)
    tail = float(snapshot_relative_tail)
    if min(power, snapshot, tail) < 0.0 or terminal <= 0.0:
        raise ValueError("invalid norm data")
    return math.nextafter(power * snapshot * tail / terminal, math.inf)
