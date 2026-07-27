"""Route bookkeeping for the RH-192--201 source-channel batch."""

from __future__ import annotations


def route_coordinate(statuses: dict[str, bool]) -> str:
    if statuses.get("edge_quartet_selected") and statuses.get("canonical_packet_exact"):
        if statuses.get("cross_scale_transport"):
            return "transported_source_channel_cloud_open_uniformity"
        return "finite_canonical_edge_quartet_open_transport"
    if statuses.get("source_cyclic_quotient"):
        return "source_cyclic_quotient_open_spectral_selection"
    return "frobenius_type_correction_required"


def macro_boundary() -> dict[str, bool]:
    return {
        "full_frobenius_rank_four_shell": False,
        "finite_source_channel_quartet": True,
        "validated_interval_quartet": False,
        "uniform_edge_gap": False,
        "cross_scale_transport": False,
        "cloud_ledger_Q": False,
        "physical_interface_R_all_levels": False,
        "gate_A": False,
        "gate_B": False,
        "gate_C": False,
        "gate_D": False,
        "gate_E": False,
        "hilbert_polya_operator": False,
        "riemann_hypothesis": False,
    }


def next_frontier(boundary: dict[str, bool]) -> list[str]:
    order = [
        "validated_interval_quartet",
        "uniform_edge_gap",
        "cross_scale_transport",
        "cloud_ledger_Q",
        "physical_interface_R_all_levels",
    ]
    return [name for name in order if not boundary.get(name, False)]
