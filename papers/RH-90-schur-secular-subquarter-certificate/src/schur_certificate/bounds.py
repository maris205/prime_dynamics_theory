"""Scalar bookkeeping for Schur-secular contraction certificates."""

from __future__ import annotations

import math
from typing import Sequence


def required_gain(candidate_tail: float, previous_tail: float, target: float) -> float:
    candidate = float(candidate_tail)
    previous = float(previous_tail)
    rho = float(target)
    if candidate < 0.0 or previous < 0.0 or not 0.0 <= rho < 1.0:
        raise ValueError("invalid contraction data")
    return max(0.0, candidate - rho * previous)


def schur_trial_form(quadratic: float, linear: float, delta: float) -> float:
    q = float(quadratic)
    ell = float(linear)
    gain = float(delta)
    if gain < 0.0:
        raise ValueError("delta must be nonnegative")
    return math.nextafter(q - 2.0 * ell + gain, math.inf)


def corrected_contraction_bound(candidate_tail: float, certified_gain: float, previous_tail: float) -> float:
    candidate = float(candidate_tail)
    gain = float(certified_gain)
    previous = float(previous_tail)
    if candidate < 0.0 or gain < 0.0 or previous <= 0.0 or gain > candidate:
        raise ValueError("invalid tail data")
    return math.nextafter((candidate - gain) / previous, math.inf)
