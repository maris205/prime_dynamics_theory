"""Route logic for the RH-232--RH-240 trace-envelope batch."""

from __future__ import annotations


def route_coordinate(statuses: dict[str, bool]) -> str:
    required = (
        "riesz_wall_identified",
        "radial_gap_insufficient",
        "projection_free_factor",
        "trace_hs_separation",
        "trace_moment_atlas",
        "dual_channel_jet_coherence",
        "adaptive_selector",
        "finite_jet_contraction_bound",
        "trace_envelope_criterion",
    )
    if not all(bool(statuses.get(key)) for key in required):
        return "trace_envelope_frontier_incomplete"
    if statuses.get("all_order_trace_envelope") and statuses.get("coefficient_anchor"):
        return "relative_det2_family_open_dynamical_realization"
    return "projection_free_relative_det2_open_uniform_trace_envelope"


def macro_gates(statuses: dict[str, bool]) -> dict[str, bool]:
    return {
        gate: bool(statuses.get(gate, False))
        for gate in ("gate_A", "gate_B", "gate_C", "gate_D", "gate_E")
    }
