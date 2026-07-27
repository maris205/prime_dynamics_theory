"""Scalar gauge balancing for two directed packet couplings."""

from __future__ import annotations

import math


def scalar_gauge_balance(
    left_coupling: float,
    right_coupling: float,
) -> dict[str, float]:
    left = float(left_coupling)
    right = float(right_coupling)
    if left < 0.0 or right < 0.0:
        raise ValueError("couplings must be nonnegative")
    if left == 0.0 and right == 0.0:
        return {
            "optimal_gauge": 1.0,
            "balanced_left_coupling": 0.0,
            "balanced_right_coupling": 0.0,
            "balanced_maximum_coupling": 0.0,
            "directed_coupling_product": 0.0,
        }
    if left == 0.0 or right == 0.0:
        return {
            "optimal_gauge": math.inf if left > 0.0 else 0.0,
            "balanced_left_coupling": 0.0,
            "balanced_right_coupling": 0.0,
            "balanced_maximum_coupling": 0.0,
            "directed_coupling_product": 0.0,
        }
    gauge = math.sqrt(left / right)
    balanced = math.sqrt(left * right)
    return {
        "optimal_gauge": gauge,
        "balanced_left_coupling": left / gauge,
        "balanced_right_coupling": gauge * right,
        "balanced_maximum_coupling": balanced,
        "directed_coupling_product": left * right,
    }


def directed_schur_feedback(
    packet_resolvent_bound: float,
    complement_resolvent_bound: float,
    left_coupling: float,
    right_coupling: float,
) -> dict[str, float | bool]:
    a = float(packet_resolvent_bound)
    d = float(complement_resolvent_bound)
    b = float(left_coupling)
    c = float(right_coupling)
    if min(a, d, b, c) < 0.0:
        raise ValueError("Schur data must be nonnegative")
    product = a * d * b * c
    return {"directed_schur_product": product, "schur_contraction": product < 1.0}


def weighted_scalar_gauge_balance(
    left_coupling: float,
    right_coupling: float,
    left_weight: float,
    right_weight: float,
) -> dict[str, float]:
    left = float(left_coupling)
    right = float(right_coupling)
    mu = float(left_weight)
    nu = float(right_weight)
    if min(left, right, mu, nu) <= 0.0:
        raise ValueError("weighted balance requires positive data")
    gauge = math.sqrt(mu * left / (nu * right))
    balanced = math.sqrt(mu * nu * left * right)
    return {
        "optimal_gauge": gauge,
        "weighted_left_coupling": mu * left / gauge,
        "weighted_right_coupling": nu * gauge * right,
        "weighted_minimax_coupling": balanced,
        "weighted_product": mu * nu * left * right,
    }
