"""Reduce a conjugation-closed quartet to two upper-half-plane branches."""

from __future__ import annotations

import numpy as np


def conjugate_representatives(values: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    """Return upper-half-plane representatives ordered by real part."""

    packet = np.asarray(values, dtype=complex).reshape(-1)
    upper = packet[packet.imag > float(tolerance)]
    if upper.size * 2 != packet.size:
        raise ValueError("packet must consist of nonreal conjugate pairs")
    for value in upper:
        if np.min(np.abs(packet - np.conj(value))) > tolerance:
            raise ValueError("packet is not conjugation closed")
    return upper[np.argsort(upper.real)]


def branch_matching_data(coarse_values: np.ndarray, fine_values: np.ndarray) -> dict[str, object]:
    """Audit the real-order correspondence between two two-branch packets."""

    coarse = conjugate_representatives(coarse_values)
    fine = conjugate_representatives(fine_values)
    if coarse.size != 2 or fine.size != 2:
        raise ValueError("exactly two conjugate branches are required")
    distance = np.abs(coarse[:, None] - fine[None, :])
    direct_cost = float(distance[0, 0] + distance[1, 1])
    swapped_cost = float(distance[0, 1] + distance[1, 0])
    pointwise_margin = float(min(distance[0, 1] - distance[0, 0], distance[1, 0] - distance[1, 1]))
    return {
        "coarse_representatives_real": [float(value.real) for value in coarse],
        "coarse_representatives_imag": [float(value.imag) for value in coarse],
        "fine_representatives_real": [float(value.real) for value in fine],
        "fine_representatives_imag": [float(value.imag) for value in fine],
        "branch_displacements": [float(value) for value in np.diag(distance)],
        "maximum_branch_displacement": float(np.max(np.diag(distance))),
        "direct_total_cost": direct_cost,
        "swapped_total_cost": swapped_cost,
        "assignment_cost_margin": swapped_cost - direct_cost,
        "minimum_pointwise_assignment_margin": pointwise_margin,
        "real_order_assignment_unique": direct_cost < swapped_cost and pointwise_margin > 0.0,
        "coarse_interbranch_separation": float(abs(coarse[1] - coarse[0])),
        "fine_interbranch_separation": float(abs(fine[1] - fine[0])),
    }


def synchronize_branches(first_values: np.ndarray, second_values: np.ndarray) -> dict[str, object]:
    """Compare branch representatives from two physical channels."""

    first = conjugate_representatives(first_values)
    second = conjugate_representatives(second_values)
    mismatch = np.abs(first - second)
    return {
        "branch_mismatches": [float(value) for value in mismatch],
        "maximum_branch_mismatch": float(np.max(mismatch)),
        "mean_branch_mismatch": float(np.mean(mismatch)),
    }
