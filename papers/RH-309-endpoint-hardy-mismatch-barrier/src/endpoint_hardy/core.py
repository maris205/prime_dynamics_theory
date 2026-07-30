from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
Q = 0.5
RADIUS = 1.4
Q_STAR = 1.0 / (R_H * LAMBDA)
RHO_STAR = 1.0 / Q_STAR


def endpoint_conversion_constant(radius: float = RADIUS) -> float:
    x = radius / RHO_STAR
    if not 0.0 < x < 1.0:
        raise ValueError("radius must lie below the endpoint")
    return x * x / math.sqrt(1.0 - x * x)


def complement_endpoint_product() -> float:
    return Q * RHO_STAR


def endpoint_odd_cutoff(mass: float) -> int:
    if mass <= 0.0:
        raise ValueError("mass must be positive")
    order = 3
    log_mass = math.log(mass)
    while (
        log_mass
        + (order - 2) * math.log(Q)
        > math.log(0.25) + order * math.log(Q_STAR)
    ):
        order += 2
    return order


def endpoint_h2_lower_bound(mass: float) -> tuple[int, float]:
    order = endpoint_odd_cutoff(mass)
    return order, 1.0 / math.sqrt(32.0 * order)


def normalized_logarithmic_scale(mass: float) -> float:
    if mass <= 0.0:
        raise ValueError("mass must be positive")
    return 1.0 / math.sqrt(math.log(math.e + mass))


def model_target_hardy_tail_bounds(order: int) -> tuple[float, float]:
    if order < 1:
        raise ValueError("order must be positive")
    return 1.0 / math.sqrt(order + 1.0), 1.0 / math.sqrt(order)
