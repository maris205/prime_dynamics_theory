"""Directional primal and dual graph bounds."""

from __future__ import annotations

import math


def directional_graph_certificate(
    contour_length: float,
    packet_resolvent_upper: float,
    complement_resolvent_upper: float,
    left_ritz_residual_upper: float,
    right_ritz_residual_upper: float,
) -> dict[str, float | bool]:
    length, a, d, b, c = map(
        float,
        (
            contour_length,
            packet_resolvent_upper,
            complement_resolvent_upper,
            left_ritz_residual_upper,
            right_ritz_residual_upper,
        ),
    )
    if not all(math.isfinite(value) for value in (length, a, d, b, c)):
        raise ValueError("inputs must be finite")
    if min(length, a, d, b, c) < 0.0:
        raise ValueError("inputs must be nonnegative")
    kappa = a * d * b * c
    if kappa >= 1.0:
        return {
            "feedback_product": kappa,
            "rank_certified": False,
            "packet_diagonal_error_upper": math.inf,
            "primal_graph_slope_upper": math.inf,
            "dual_graph_slope_upper": math.inf,
            "primal_graph_certified": False,
            "dual_graph_certified": False,
        }
    scale = length / (2.0 * math.pi * (1.0 - kappa))
    diagonal = scale * a * kappa
    primal_cross = scale * a * d * c
    dual_cross = scale * a * d * b
    invertible = diagonal < 1.0
    return {
        "feedback_product": kappa,
        "rank_certified": True,
        "packet_diagonal_error_upper": diagonal,
        "primal_cross_upper": primal_cross,
        "dual_cross_upper": dual_cross,
        "primal_graph_slope_upper": primal_cross / (1.0 - diagonal) if invertible else math.inf,
        "dual_graph_slope_upper": dual_cross / (1.0 - diagonal) if invertible else math.inf,
        "primal_graph_certified": invertible,
        "dual_graph_certified": invertible,
    }
