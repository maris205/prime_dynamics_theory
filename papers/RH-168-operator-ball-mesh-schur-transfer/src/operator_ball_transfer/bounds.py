"""Validated formulas for mesh and operator-ball perturbations."""

from __future__ import annotations

import math
from collections.abc import Iterable


def inverse_defect_bound(approximate_inverse_norm: float, residual_norm: float) -> dict[str, float | bool]:
    inverse = float(approximate_inverse_norm)
    residual = float(residual_norm)
    if not all(math.isfinite(value) for value in (inverse, residual)) or min(inverse, residual) < 0.0:
        raise ValueError("inverse and residual bounds must be finite and nonnegative")
    if residual >= 1.0:
        return {"inverse_certified": False, "exact_inverse_upper": math.inf}
    return {"inverse_certified": True, "exact_inverse_upper": inverse / (1.0 - residual)}


def robust_resolvent_envelope(
    nominal_sample_uppers: Iterable[float],
    covering_radii: float | Iterable[float],
    operator_radius: float,
) -> dict[str, float | bool]:
    samples = tuple(float(value) for value in nominal_sample_uppers)
    eta = float(operator_radius)
    if not samples or not all(math.isfinite(value) and value >= 0.0 for value in samples):
        raise ValueError("nonempty nominal sample bounds required")
    if not math.isfinite(eta) or eta < 0.0:
        raise ValueError("operator radius must be finite and nonnegative")
    if isinstance(covering_radii, (int, float)):
        radii = (float(covering_radii),) * len(samples)
    else:
        radii = tuple(float(value) for value in covering_radii)
    if len(radii) != len(samples) or not all(math.isfinite(value) and value >= 0.0 for value in radii):
        raise ValueError("covering radii must match samples")
    products = tuple(m * (h + eta) for m, h in zip(samples, radii, strict=True))
    if any(product >= 1.0 for product in products):
        return {
            "transfer_certified": False,
            "maximum_transfer_product": max(products),
            "exact_continuous_resolvent_upper": math.inf,
        }
    envelopes = tuple(m / (1.0 - product) for m, product in zip(samples, products, strict=True))
    return {
        "transfer_certified": True,
        "maximum_transfer_product": max(products),
        "exact_continuous_resolvent_upper": max(envelopes),
    }


def robust_schur_gate(
    packet_sample_uppers: Iterable[float],
    complement_sample_uppers: Iterable[float],
    covering_radius: float,
    packet_block_radius: float,
    complement_block_radius: float,
    nominal_complement_to_packet: float,
    nominal_packet_to_complement: float,
    offdiagonal_radius: float,
) -> dict[str, float | bool]:
    packet = robust_resolvent_envelope(packet_sample_uppers, covering_radius, packet_block_radius)
    complement = robust_resolvent_envelope(complement_sample_uppers, covering_radius, complement_block_radius)
    b0, c0, eta = map(float, (nominal_complement_to_packet, nominal_packet_to_complement, offdiagonal_radius))
    if not all(math.isfinite(value) and value >= 0.0 for value in (b0, c0, eta)):
        raise ValueError("coupling data must be finite and nonnegative")
    if not packet["transfer_certified"] or not complement["transfer_certified"]:
        return {"transfer_certified": False, "feedback_product": math.inf, "rank_certified": False}
    a = float(packet["exact_continuous_resolvent_upper"])
    d = float(complement["exact_continuous_resolvent_upper"])
    b = b0 + eta
    c = c0 + eta
    kappa = a * d * b * c
    return {
        "transfer_certified": True,
        "packet_resolvent_upper": a,
        "complement_resolvent_upper": d,
        "complement_to_packet_upper": b,
        "packet_to_complement_upper": c,
        "feedback_product": kappa,
        "rank_certified": kappa < 1.0,
    }
