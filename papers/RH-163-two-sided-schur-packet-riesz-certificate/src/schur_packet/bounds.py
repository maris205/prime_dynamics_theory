"""Quantitative two-sided Schur bounds."""

from __future__ import annotations

import math


def scalar_block_norm(x11: float, x12: float, x21: float, x22: float) -> float:
    """Spectral norm of a real 2-by-2 scalar matrix."""

    values = tuple(float(value) for value in (x11, x12, x21, x22))
    if not all(math.isfinite(value) for value in values):
        raise ValueError("entries must be finite")
    square_sum = sum(value * value for value in values)
    determinant = values[0] * values[3] - values[1] * values[2]
    discriminant = max(0.0, square_sum * square_sum - 4.0 * determinant * determinant)
    return math.sqrt(0.5 * (square_sum + math.sqrt(discriminant)))


def schur_certificate(
    contour_length: float,
    packet_resolvent_upper: float,
    complement_resolvent_upper: float,
    complement_to_packet_upper: float,
    packet_to_complement_upper: float,
) -> dict[str, float | bool]:
    """Return the directed Schur rank and projector certificates."""

    length, a, d, b, c = map(
        float,
        (
            contour_length,
            packet_resolvent_upper,
            complement_resolvent_upper,
            complement_to_packet_upper,
            packet_to_complement_upper,
        ),
    )
    if not all(math.isfinite(value) for value in (length, a, d, b, c)):
        raise ValueError("certificate inputs must be finite")
    if min(length, a, d, b, c) < 0.0:
        raise ValueError("certificate inputs must be nonnegative")
    kappa = a * d * b * c
    symmetric_product = max(a, d) * max(b, c)
    if kappa >= 1.0:
        return {
            "feedback_product": kappa,
            "symmetric_neumann_product": symmetric_product,
            "rank_certified": False,
            "projector_error_upper": math.inf,
            "graph_certified": False,
        }
    denominator = 1.0 - kappa
    block_norm = scalar_block_norm(
        a * kappa,
        a * b * d,
        d * c * a,
        d * kappa,
    ) / denominator
    delta = length * block_norm / (2.0 * math.pi)
    return {
        "feedback_product": kappa,
        "symmetric_neumann_product": symmetric_product,
        "rank_certified": True,
        "resolvent_difference_upper": block_norm,
        "projector_error_upper": delta,
        "graph_certified": delta < 1.0,
        "graph_slope_upper": delta / (1.0 - delta) if delta < 1.0 else math.inf,
    }
