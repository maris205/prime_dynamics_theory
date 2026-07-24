"""Deterministic low-rank packet bounds used by RH-142."""

from __future__ import annotations

import math

import numpy as np


def factorized_gap_lower(left: np.ndarray, right: np.ndarray) -> float:
    """Lower bound the nonzero normalized Gram gap of H=left@right."""
    l = np.asarray(left, dtype=float)
    r = np.asarray(right, dtype=float)
    if l.ndim != 2 or r.ndim != 2 or l.shape[1] != r.shape[0] or l.shape[1] == 0:
        raise ValueError("incompatible nonempty factors")
    left_low = float(np.linalg.eigvalsh((l.T @ l + (l.T @ l).T) / 2.0)[0])
    right_low = float(np.linalg.eigvalsh((r @ r.T + (r @ r.T).T) / 2.0)[0])
    product = l @ r
    scale = float(np.sum(product * product))
    if left_low <= 0.0 or right_low <= 0.0 or scale <= 0.0:
        return 0.0
    return left_low * right_low / scale


def projector_radius(gap_lower: float, operator_radius_upper: float) -> float | None:
    gap = float(gap_lower)
    radius = float(operator_radius_upper)
    if not all(math.isfinite(value) for value in (gap, radius)) or gap < 0.0 or radius < 0.0:
        raise ValueError("gap and radius must be finite and nonnegative")
    if gap <= 2.0 * radius:
        return None
    return min(1.0, radius / (gap - radius))


def hybrid_packet_gate(gap_lower: float, frobenius_upper: float, eigen_upper: float | None = None) -> dict[str, float | str | bool | None]:
    """Use a Frobenius operator bound, with a validated eigen rescue if needed."""
    gap = float(gap_lower)
    frobenius = float(frobenius_upper)
    if gap < 0.0 or frobenius < 0.0 or not math.isfinite(gap) or not math.isfinite(frobenius):
        raise ValueError("invalid packet data")
    method = "frobenius"
    radius = frobenius
    if gap <= 2.0 * radius and eigen_upper is not None:
        eigen = float(eigen_upper)
        if eigen < 0.0 or not math.isfinite(eigen):
            raise ValueError("invalid eigenvalue enclosure")
        method = "interval_eigen"
        radius = min(radius, eigen)
    packet_radius = projector_radius(gap, radius)
    return {
        "method": method,
        "snapshot_radius": radius,
        "gap_ratio": math.inf if radius == 0.0 and gap > 0.0 else (gap / (2.0 * radius) if radius > 0.0 else 0.0),
        "certified": packet_radius is not None,
        "projector_radius": packet_radius,
    }

