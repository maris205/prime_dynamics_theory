from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
Q = 0.5
TARGET_RADIUS = 1.4
Q_STAR = 1.0 / (R_H * LAMBDA)
RHO_STAR = 1.0 / Q_STAR


def rate_ceiling(rho: float) -> float:
    if not TARGET_RADIUS < rho < RHO_STAR:
        raise ValueError("rho must lie strictly between 1.4 and rho_star")
    return math.log(1.0 / (Q_STAR * rho)) / math.log(Q_STAR / Q)


def odd_anchor(order: int) -> float:
    if order < 3 or order % 2 == 0:
        raise ValueError("order must be odd and at least three")
    return Q_STAR**order / (1.0 + LAMBDA ** (-order))


def forced_odd_order(
    mass: float, relative_mismatch: float = 0.5
) -> int:
    if mass <= 0.0:
        raise ValueError("mass must be positive")
    if not 0.0 < relative_mismatch < 1.0:
        raise ValueError("relative_mismatch must lie in (0,1)")

    order = 3
    log_mass = math.log(mass)
    log_q = math.log(Q)
    log_q_star = math.log(Q_STAR)
    log_allowance = math.log(1.0 - relative_mismatch)
    while True:
        log_trace_cap = log_mass + (order - 2) * log_q
        log_anchor_allowance = (
            log_allowance
            + order * log_q_star
            - math.log1p(LAMBDA ** (-order))
        )
        if log_trace_cap <= log_anchor_allowance:
            return order
        order += 2


def coefficient_norm_lower_bound(
    mass: float, rho: float, relative_mismatch: float = 0.5
) -> float:
    rate_ceiling(rho)
    order = forced_odd_order(mass, relative_mismatch)
    log_value = (
        math.log(relative_mismatch)
        + order * math.log(Q_STAR * rho)
        - math.log1p(LAMBDA ** (-order))
        - math.log(order)
    )
    return math.exp(log_value)


def asymptotic_lower_bound(mass: float, rho: float) -> float:
    """Backward-compatible name for the exact forced-coefficient lower bound."""

    return coefficient_norm_lower_bound(mass, rho)
