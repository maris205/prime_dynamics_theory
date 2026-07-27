"""Separate scalar spectral divisors from raw state transport."""

from __future__ import annotations

import math

import numpy as np


def rotating_similarity_example(angle: float) -> dict[str, np.ndarray | float]:
    """Keep a divisor fixed while rotating its spectral projector."""

    theta = float(angle)
    if not math.isfinite(theta):
        raise ValueError("angle must be finite")
    rotation = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
    diagonal = np.diag([0.7, -0.2])
    operator = rotation @ diagonal @ rotation.T
    projector = rotation @ np.diag([1.0, 0.0]) @ rotation.T
    reference_projector = np.diag([1.0, 0.0])
    return {
        "operator": operator,
        "projector": projector,
        "characteristic_coefficients": np.poly(np.linalg.eigvals(operator)),
        "projector_distance": float(np.linalg.norm(projector - reference_projector, 2)),
    }


def route_coordinate(statuses: dict[str, bool]) -> str:
    required = (
        "finite_branch_correspondence",
        "finite_dual_channel_divisor",
        "naive_state_transport_rejected",
        "scalar_residue_renormalization_rejected",
    )
    if not all(bool(statuses.get(key)) for key in required):
        return "transport_frontier_incomplete"
    if statuses.get("all_level_divisor_limit"):
        return "intrinsic_divisor_open_fredholm_assembly"
    return "finite_dual_channel_divisor_flow_open_renormalization"
