"""Route logic for the RH-222--RH-230 determinant-frontier batch."""

from __future__ import annotations


def route_coordinate(statuses: dict[str, bool]) -> str:
    required = (
        "rank_growing_cloud",
        "shell_complete_selection",
        "empirical_tightness",
        "direct_divisor_rejected",
        "reciprocal_dictionary",
        "resolved_tail_control",
        "dual_channel_coherence",
    )
    if not all(bool(statuses.get(key)) for key in required):
        return "rank_growing_determinant_frontier_incomplete"
    if statuses.get("uniform_complement_ideal_control") and statuses.get("local_count_stability"):
        return "relative_det2_family_open_dynamical_limit"
    return "rank_growing_reciprocal_cloud_open_uniform_complement_ideal_limit"


def macro_gates(statuses: dict[str, bool]) -> dict[str, bool]:
    return {gate: bool(statuses.get(gate, False)) for gate in ("gate_A", "gate_B", "gate_C", "gate_D", "gate_E")}
