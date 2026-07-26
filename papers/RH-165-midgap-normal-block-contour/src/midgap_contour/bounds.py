"""Closed-form normal-block midpoint circle bounds."""

from __future__ import annotations

import math


def _matrix_norm_2(x11: float, x12: float, x21: float, x22: float) -> float:
    square_sum = x11 * x11 + x12 * x12 + x21 * x21 + x22 * x22
    determinant = x11 * x22 - x12 * x21
    disc = max(0.0, square_sum * square_sum - 4.0 * determinant * determinant)
    return math.sqrt(0.5 * (square_sum + math.sqrt(disc)))


def centered_circle_certificate(
    packet_radius: float,
    complement_inner_radius: float,
    complement_to_packet_upper: float,
    packet_to_complement_upper: float,
) -> dict[str, float | bool]:
    rho, outer, b, c = map(
        float,
        (
            packet_radius,
            complement_inner_radius,
            complement_to_packet_upper,
            packet_to_complement_upper,
        ),
    )
    if not all(math.isfinite(value) for value in (rho, outer, b, c)):
        raise ValueError("inputs must be finite")
    if min(rho, b, c) < 0.0 or outer <= rho:
        raise ValueError("invalid disk separation data")
    gap = outer - rho
    radius = 0.5 * (rho + outer)
    a = d = 2.0 / gap
    kappa = 4.0 * b * c / (gap * gap)
    result: dict[str, float | bool] = {
        "gap": gap,
        "midpoint_radius": radius,
        "packet_resolvent_upper": a,
        "complement_resolvent_upper": d,
        "feedback_product": kappa,
        "rank_certified": kappa < 1.0,
        "gap_gate_margin": gap - 2.0 * math.sqrt(b * c),
    }
    if kappa >= 1.0:
        result.update({"projector_error_upper": math.inf, "graph_certified": False})
        return result
    scalar = _matrix_norm_2(
        a * kappa,
        a * b * d,
        a * c * d,
        d * kappa,
    ) / (1.0 - kappa)
    delta = radius * scalar  # |Gamma|/(2 pi) = radius.
    result.update({"projector_error_upper": delta, "graph_certified": delta < 1.0})
    return result
