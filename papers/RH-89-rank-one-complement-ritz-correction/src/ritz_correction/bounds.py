"""Scalar bookkeeping for rank-one Ritz correction."""

from __future__ import annotations

import math


def residual_energy(total_energy: float, captured_energy: float) -> float:
    total = float(total_energy)
    captured = float(captured_energy)
    if total < 0.0 or captured < 0.0 or captured > total:
        raise ValueError("invalid energy data")
    return math.nextafter(total - captured, math.inf)


def corrected_tail(candidate_tail: float, certified_gain: float) -> float:
    candidate = float(candidate_tail)
    gain = float(certified_gain)
    if candidate < 0.0 or gain < 0.0 or gain > candidate:
        raise ValueError("invalid correction data")
    return math.nextafter(candidate - gain, math.inf)


def correction_fraction(candidate_tail: float, corrected: float, reference: float) -> float:
    candidate = float(candidate_tail)
    trial = float(corrected)
    target = float(reference)
    if not 0.0 <= target < candidate or not target <= trial <= candidate:
        raise ValueError("invalid tail ordering")
    return math.nextafter((candidate - trial) / (candidate - target), -math.inf)
