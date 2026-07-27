"""Frontier bookkeeping for the RH-182--191 biorthogonal batch."""

from __future__ import annotations


def route_status(statuses: dict[str, str]) -> str:
    if statuses.get("validated_physical_D") == "proved":
        return "physical_D_candidate_open_KH"
    if statuses.get("biorthogonal_local_candidate") == "local_floating_candidate":
        return "local_biorthogonal_candidate_with_open_DKH"
    return "orthogonal_clock_rejected_biorthogonal_route_open"


def current_frontier(statuses: dict[str, str]) -> list[str]:
    return sorted(name for name, value in statuses.items() if value in {"open", "local_floating_candidate"})


def macro_boundary() -> dict[str, bool]:
    return {
        "physical_interface_R": False,
        "cloud_ledger_Q": False,
        "complement_limit_U": False,
        "canonicity_Z": False,
        "directed_limit_T": False,
        "gate_A": False,
        "gate_B": False,
        "gate_C": False,
        "gate_D": False,
        "gate_E": False,
        "hilbert_polya_operator": False,
        "riemann_hypothesis": False,
    }
