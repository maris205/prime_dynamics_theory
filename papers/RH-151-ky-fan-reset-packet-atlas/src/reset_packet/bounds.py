"""Ky--Fan packet-angle and branch-free energy-loss bounds."""

from __future__ import annotations

import math


def _nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def ky_fan_projector_bound(captured_energy_loss: float, spectral_gap: float) -> dict[str, float | bool]:
    """Convert a Ky--Fan trace deficit into projector distances."""
    loss = _nonnegative(captured_energy_loss, "captured-energy loss")
    gap = _nonnegative(spectral_gap, "spectral gap")
    if gap == 0.0:
        return {
            "operator_radius": 1.0,
            "frobenius_radius": math.sqrt(2.0),
            "informative": False,
        }
    ratio = loss / gap
    return {
        "operator_radius": min(1.0, math.sqrt(ratio)),
        "frobenius_radius": min(math.sqrt(2.0), math.sqrt(2.0 * ratio)),
        "informative": ratio < 1.0,
    }


def branch_free_energy_step(
    previous_loss: float,
    previous_gap: float,
    global_packet_drift_loss: float,
    gram_frobenius_drift: float,
) -> float:
    """Propagate captured-energy loss through any monotone Ritz update.

    The update subspace only needs to contain the previous packet.  No
    threshold branch or selected direction coordinates enter the bound.
    """
    loss = _nonnegative(previous_loss, "previous loss")
    gap = _nonnegative(previous_gap, "previous gap")
    drift_loss = _nonnegative(global_packet_drift_loss, "global packet drift loss")
    gram_drift = _nonnegative(gram_frobenius_drift, "Gram drift")
    if loss > 0.0 and gap == 0.0:
        return math.inf
    angle_frobenius = 0.0 if loss == 0.0 else math.sqrt(2.0 * loss / gap)
    return math.nextafter(drift_loss + loss + angle_frobenius * gram_drift, math.inf)


def direct_packet_enclosure(center_gap: float, matrix_radius: float) -> dict[str, float | bool | None]:
    """Davis--Kahan packet enclosure around an independently reset center."""
    gap = _nonnegative(center_gap, "center gap")
    radius = _nonnegative(matrix_radius, "matrix radius")
    stable = gap > 2.0 * radius
    return {
        "stable": stable,
        "projector_radius": radius / (gap - radius) if stable else None,
        "gap_ratio": gap / (2.0 * radius) if radius > 0.0 else math.inf,
    }
