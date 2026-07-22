"""Outward-rounded scalar predictor-corrector bounds."""

from __future__ import annotations

import math


def predictor_coefficient(theta: float, eta: float) -> float:
    memory = float(theta)
    decay = float(eta)
    if memory < 0.0 or not 0.0 <= decay < 1.0:
        raise ValueError("invalid predictor data")
    return math.nextafter(memory + decay, math.inf)


def contraction_factor(reoptimization: float, theta: float, eta: float) -> float:
    gain = float(reoptimization)
    if not 0.0 <= gain <= 1.0:
        raise ValueError("reoptimization factor must lie in [0,1]")
    return math.nextafter(gain * predictor_coefficient(theta, eta), math.inf)


def global_rayleigh_upper(operator_norm: float, full_growth: float) -> float:
    norm = float(operator_norm)
    growth = float(full_growth)
    if norm < 0.0 or growth <= 0.0:
        raise ValueError("invalid Rayleigh data")
    return math.nextafter(norm * norm / growth, math.inf)
