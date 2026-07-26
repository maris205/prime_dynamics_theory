"""Continuous resolvent bounds from a finite contour mesh."""

from __future__ import annotations

import math
from collections.abc import Iterable


def circle_covering_radius(radius: float, node_count: int) -> float:
    value = float(radius)
    count = int(node_count)
    if not math.isfinite(value) or value <= 0.0 or count < 3:
        raise ValueError("positive radius and at least three nodes required")
    return 2.0 * value * math.sin(math.pi / (2.0 * count))


def sampled_resolvent_envelope(
    sample_resolvent_uppers: Iterable[float],
    covering_radii: float | Iterable[float],
) -> dict[str, float | bool]:
    samples = tuple(float(value) for value in sample_resolvent_uppers)
    if not samples or not all(math.isfinite(value) and value >= 0.0 for value in samples):
        raise ValueError("nonempty finite sample bounds required")
    if isinstance(covering_radii, (int, float)):
        radii = (float(covering_radii),) * len(samples)
    else:
        radii = tuple(float(value) for value in covering_radii)
    if len(radii) != len(samples) or not all(math.isfinite(value) and value >= 0.0 for value in radii):
        raise ValueError("covering radii must match sample bounds")
    products = tuple(m * h for m, h in zip(samples, radii, strict=True))
    if any(product >= 1.0 for product in products):
        return {
            "mesh_certified": False,
            "maximum_mesh_product": max(products),
            "continuous_resolvent_upper": math.inf,
        }
    envelopes = tuple(m / (1.0 - product) for m, product in zip(samples, products, strict=True))
    return {
        "mesh_certified": True,
        "maximum_mesh_product": max(products),
        "continuous_resolvent_upper": max(envelopes),
    }


def sampled_schur_gate(
    packet_sample_uppers: Iterable[float],
    complement_sample_uppers: Iterable[float],
    covering_radius: float,
    complement_to_packet_upper: float,
    packet_to_complement_upper: float,
) -> dict[str, float | bool]:
    packet = sampled_resolvent_envelope(packet_sample_uppers, covering_radius)
    complement = sampled_resolvent_envelope(complement_sample_uppers, covering_radius)
    b = float(complement_to_packet_upper)
    c = float(packet_to_complement_upper)
    if not all(math.isfinite(value) and value >= 0.0 for value in (b, c)):
        raise ValueError("couplings must be finite and nonnegative")
    if not packet["mesh_certified"] or not complement["mesh_certified"]:
        return {
            "mesh_certified": False,
            "feedback_product": math.inf,
            "rank_certified": False,
        }
    a = float(packet["continuous_resolvent_upper"])
    d = float(complement["continuous_resolvent_upper"])
    kappa = a * d * b * c
    return {
        "mesh_certified": True,
        "packet_resolvent_upper": a,
        "complement_resolvent_upper": d,
        "feedback_product": kappa,
        "rank_certified": kappa < 1.0,
    }
