"""Outward-rounded scalar Rayleigh-injection bounds."""

from __future__ import annotations

import math
from typing import Sequence


def one_step_tail_bound(injection: float, eta: float, previous_tail: float) -> float:
    current = float(injection)
    decay = float(eta)
    previous = float(previous_tail)
    if current < 0.0 or previous < 0.0 or not 0.0 <= decay < 1.0:
        raise ValueError("invalid recursion data")
    return math.nextafter(current + decay * previous, math.inf)


def injection_convolution(initial_tail: float, eta: float, injections: Sequence[float]) -> float:
    tail = float(initial_tail)
    decay = float(eta)
    if tail < 0.0 or not 0.0 <= decay < 1.0:
        raise ValueError("invalid recursion data")
    for injection in injections:
        tail = one_step_tail_bound(float(injection), decay, tail)
    return tail


def geometric_injection_bound(initial_tail: float, eta: float, amplitude: float, rho: float, steps: int) -> float:
    """Bound a recursion with injections amplitude*rho^j, j=1,...,steps."""

    count = int(steps)
    amp = float(amplitude)
    rate = float(rho)
    if count < 0 or amp < 0.0 or not 0.0 <= rate < 1.0:
        raise ValueError("invalid geometric injection data")
    return injection_convolution(initial_tail, eta, [amp * rate**j for j in range(1, count + 1)])
