from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
Q = 0.5
Q_STAR = 1.0 / (R_H * LAMBDA)


def envelope_mass(order: int, constant: float = 48.0) -> float:
    if order < 2 or constant <= 0.0:
        raise ValueError("invalid envelope parameters")
    return constant * Q * Q * (Q_STAR / Q) ** order


def model_hardy_tail_bounds(
    order: int, rho: float, constant: float = 48.0
) -> tuple[float, float]:
    if order < 2 or constant <= 0.0 or not 0.0 < Q_STAR * rho < 1.0:
        raise ValueError("invalid tail parameters")
    x = Q_STAR * rho
    first = constant * x ** (order + 1) / (order + 1)
    return first, first / math.sqrt(1.0 - x * x)


def model_sup_tail_bounds(
    order: int, rho: float, constant: float = 48.0
) -> tuple[float, float]:
    if order < 2 or constant <= 0.0 or not 0.0 < Q_STAR * rho < 1.0:
        raise ValueError("invalid tail parameters")
    x = Q_STAR * rho
    first = constant * x ** (order + 1) / (order + 1)
    return first, first / (1.0 - x)


def saturation_identity_ratio(order: int, constant: float = 48.0) -> float:
    return envelope_mass(order, constant) * Q ** (order - 2) / (
        constant * Q_STAR**order
    )
