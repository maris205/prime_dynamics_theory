"""Optimal scalar balancing of two directed packet couplings."""

from __future__ import annotations

import math


def balance_data(
    complement_to_packet_upper: float,
    packet_to_complement_upper: float,
) -> dict[str, float | bool]:
    b = float(complement_to_packet_upper)
    c = float(packet_to_complement_upper)
    if not all(math.isfinite(value) for value in (b, c)) or min(b, c) < 0.0:
        raise ValueError("couplings must be finite and nonnegative")
    if b == 0.0 or c == 0.0:
        return {
            "triangular": True,
            "optimal_scale": math.inf if b == 0.0 and c > 0.0 else 0.0,
            "balanced_coupling_infimum": 0.0,
            "similarity_condition": math.inf,
        }
    scale = math.sqrt(c / b)
    return {
        "triangular": False,
        "optimal_scale": scale,
        "balanced_coupling_infimum": math.sqrt(b * c),
        "similarity_condition": max(scale, 1.0 / scale),
    }


def similarity_certificate(
    contour_length: float,
    block_resolvent_upper: float,
    complement_to_packet_upper: float,
    packet_to_complement_upper: float,
    scale: float | None = None,
) -> dict[str, float | bool]:
    length = float(contour_length)
    m = float(block_resolvent_upper)
    b = float(complement_to_packet_upper)
    c = float(packet_to_complement_upper)
    if not all(math.isfinite(value) for value in (length, m, b, c)):
        raise ValueError("inputs must be finite")
    if min(length, m, b, c) < 0.0:
        raise ValueError("inputs must be nonnegative")
    if b == 0.0 or c == 0.0:
        return {
            "triangular": True,
            "rank_certified": True,
            "balanced_neumann_product": 0.0,
            "transformed_projector_error_upper": 0.0 if b == c == 0.0 else math.inf,
            "original_projector_error_upper": 0.0 if b == c == 0.0 else math.inf,
            "graph_certified": b == c == 0.0,
        }
    t = math.sqrt(c / b) if scale is None else float(scale)
    if not math.isfinite(t) or t <= 0.0:
        raise ValueError("scale must be finite and positive")
    coupling = max(t * b, c / t)
    product = m * coupling
    condition = max(t, 1.0 / t)
    if product >= 1.0:
        return {
            "triangular": False,
            "scale": t,
            "balanced_coupling": coupling,
            "similarity_condition": condition,
            "balanced_neumann_product": product,
            "rank_certified": False,
            "transformed_projector_error_upper": math.inf,
            "original_projector_error_upper": math.inf,
            "graph_certified": False,
        }
    transformed = length * m * m * coupling / (2.0 * math.pi * (1.0 - product))
    original = condition * transformed
    return {
        "triangular": False,
        "scale": t,
        "balanced_coupling": coupling,
        "similarity_condition": condition,
        "balanced_neumann_product": product,
        "rank_certified": True,
        "transformed_projector_error_upper": transformed,
        "original_projector_error_upper": original,
        "graph_certified": original < 1.0,
    }
