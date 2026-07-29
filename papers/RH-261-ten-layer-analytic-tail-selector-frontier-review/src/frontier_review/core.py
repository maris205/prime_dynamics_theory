"""Small deterministic helpers for the RH-252--RH-261 frontier review."""

from __future__ import annotations


def macro_gates(statuses: dict[str, object]) -> dict[str, bool]:
    """Return the five macro-gate flags with a false-by-default firewall."""

    return {
        letter: bool(statuses.get(f"gate_{letter}", statuses.get(letter, False)))
        for letter in "ABCDE"
    }


def obligation_summary(
    *,
    legal_anchored_head: bool,
    coefficient_bridge: bool,
    uniform_quotient_tail: bool,
    analytic_target_tail: bool,
    certified_target_boundary_constant: bool,
) -> dict[str, object]:
    """Count the independent obligations in the gluing interface."""

    components = {
        "legal_anchored_head": bool(legal_anchored_head),
        "coefficient_bridge": bool(coefficient_bridge),
        "uniform_quotient_tail": bool(uniform_quotient_tail),
        "analytic_target_tail": bool(analytic_target_tail),
        "certified_target_boundary_constant": bool(
            certified_target_boundary_constant
        ),
    }
    return {
        "components": components,
        "required_component_count": len(components),
        "satisfied_component_count": sum(components.values()),
        "complete": all(components.values()),
    }


def route_coordinate(ledger: dict[str, object]) -> str:
    """Use the archived RH-260 route unless a future complete ledger says otherwise."""

    if bool(ledger.get("complete_certificate_count", 0)):
        return "complete_head_tail_certificate_ready_for_gate_A_audit"
    return str(
        ledger.get(
            "route_coordinate",
            "legal_heads_obstructed_target_tail_exists_Ms_uncertified_"
            "quotient_finite_nonuniform_complete_certificate_zero",
        )
    )
