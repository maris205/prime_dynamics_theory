"""Typed packet anchors and outward recursive transport bounds."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def _nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def packet_transfer_radius(
    center_distance: float,
    inherited_radius: float,
    inherited_rank: int,
    target_rank: int,
) -> dict[str, float | int | bool]:
    """Transfer a projector ball between temporal centers.

    Orthogonal projectors of different finite ranks are exactly unit distance
    apart in operator norm.  Equal-rank balls transfer by the triangle
    inequality, capped at the diameter one of the projector metric.
    """
    distance = _nonnegative(center_distance, "center distance")
    radius = _nonnegative(inherited_radius, "inherited radius")
    source = int(inherited_rank)
    target = int(target_rank)
    if source <= 0 or target <= 0 or distance > 1.0 + 1e-12 or radius > 1.0 + 1e-12:
        raise ValueError("invalid projector data")
    rank_compatible = source == target
    transferred = 1.0 if not rank_compatible else min(1.0, distance + radius)
    return {
        "inherited_rank": source,
        "target_rank": target,
        "rank_compatible": rank_compatible,
        "transferred_radius": transferred,
        "informative": transferred < 1.0,
    }


def cross_operator_radius(matrix_radius: float, matrix_norm: float, packet_radius: float) -> float:
    """Bound ``K(A,P)-K(B,Q)`` for ``K(A,P)=(I-P)AP``."""
    delta = _nonnegative(matrix_radius, "matrix radius")
    norm = _nonnegative(matrix_norm, "matrix norm")
    angle = _nonnegative(packet_radius, "packet radius")
    if angle > 1.0 + 1e-12:
        raise ValueError("packet radius cannot exceed one")
    return delta + 2.0 * norm * min(1.0, angle)


def singular_direction_enclosure(
    singular_values: Iterable[float],
    width: int,
    cross_radius: float,
) -> dict[str, float | int | bool | None]:
    """Wedin enclosure for the selected left singular subspace.

    The first unlisted singular value is zero.  The strict ``gap > 2*eta``
    gate is the universal non-crossing condition when both selected and
    omitted singular values may move by ``eta``.
    """
    singular = np.asarray(tuple(float(value) for value in singular_values), dtype=float)
    selected = int(width)
    eta = _nonnegative(cross_radius, "cross radius")
    if (
        singular.ndim != 1
        or singular.size == 0
        or np.any(~np.isfinite(singular))
        or np.any(singular < 0.0)
        or np.any(singular[:-1] < singular[1:])
        or selected <= 0
        or selected > singular.size
    ):
        raise ValueError("invalid singular-value packet")
    omitted = float(singular[selected]) if selected < singular.size else 0.0
    gap = float(singular[selected - 1] - omitted)
    stable = gap > 2.0 * eta
    radius = min(1.0, eta / (gap - eta)) if stable else None
    return {
        "selected_width": selected,
        "selected_singular_value": float(singular[selected - 1]),
        "first_omitted_singular_value": omitted,
        "singular_gap": gap,
        "stable": stable,
        "projector_radius": radius,
    }


def enriched_projector_radius(packet_radius: float, direction_radius: float) -> float:
    """Projector radius for an orthogonal packet-plus-direction enrichment."""
    packet = _nonnegative(packet_radius, "packet radius")
    direction = _nonnegative(direction_radius, "direction radius")
    if packet > 1.0 + 1e-12 or direction > 1.0 + 1e-12:
        raise ValueError("projector radii cannot exceed one")
    return min(1.0, packet + direction)


def ritz_operator_radius(matrix_radius: float, matrix_norm: float, enriched_radius: float) -> float:
    """Bound ``EAE-FBF`` for nearby matrices and enriched projectors."""
    return cross_operator_radius(matrix_radius, matrix_norm, enriched_radius)


def spectral_packet_enclosure(gap: float, operator_radius: float) -> dict[str, float | bool | None]:
    """Davis--Kahan enclosure with an approximate spectral-gap gate."""
    separation = _nonnegative(gap, "spectral gap")
    radius = _nonnegative(operator_radius, "operator radius")
    stable = separation > 2.0 * radius
    projector = min(1.0, radius / (separation - radius)) if stable else None
    return {
        "gap": separation,
        "operator_radius": radius,
        "stable": stable,
        "projector_radius": projector,
    }


def ideal_truncation_packet_gate(singular_values: Iterable[float], rank: int) -> dict[str, float | int | bool]:
    """Exact normalized-Gram diagnostic for an ideal SVD truncation.

    This is a diagnostic of the supplied singular spectrum, not an interval
    certificate for a numerically computed SVD.
    """
    singular = np.asarray(tuple(float(value) for value in singular_values), dtype=float)
    width = int(rank)
    if (
        singular.ndim != 1
        or singular.size <= width
        or width <= 0
        or np.any(~np.isfinite(singular))
        or np.any(singular < 0.0)
        or np.any(singular[:-1] < singular[1:])
        or singular[0] <= 0.0
    ):
        raise ValueError("a nonincreasing spectrum with an omitted mode is required")
    energy = singular * singular
    probability = energy / float(energy.sum())
    tail = float(probability[width:].sum())
    capture = 1.0 - tail
    candidate_gap = float(probability[width - 1] / capture)
    retained_shift = float(tail * probability[0] / capture)
    omitted_peak = float(probability[width])
    operator_radius = max(retained_shift, omitted_peak)
    gap_ratio = candidate_gap / (2.0 * operator_radius)
    return {
        "rank": width,
        "tail_energy_fraction": tail,
        "candidate_gap": candidate_gap,
        "normalized_snapshot_operator_radius": operator_radius,
        "gap_ratio": gap_ratio,
        "packet_gate": gap_ratio > 1.0,
    }
