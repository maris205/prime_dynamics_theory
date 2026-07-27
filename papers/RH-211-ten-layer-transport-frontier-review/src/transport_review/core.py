"""Claim-boundary logic for the transport-frontier review."""

from __future__ import annotations


def review_coordinate(statuses: dict[str, bool]) -> str:
    required = (
        "naive_haar_transport_rejected",
        "branch_correspondence_supported",
        "dual_channel_divisor_supported",
        "scalar_residue_renormalization_rejected",
        "expanded_cloud_rejected",
    )
    if not all(bool(statuses.get(key)) for key in required):
        return "transport_review_incomplete"
    if statuses.get("all_level_divisor_limit"):
        return "intrinsic_divisor_open_fredholm_assembly"
    return "finite_dual_channel_divisor_flow_open_renormalization"


def strict_gate_vector() -> dict[str, bool]:
    return {
        "gate_A": False,
        "gate_B": False,
        "gate_C": False,
        "gate_D": False,
        "gate_E": False,
        "hilbert_polya_operator": False,
        "zeta_zero_identification": False,
        "riemann_hypothesis": False,
    }
