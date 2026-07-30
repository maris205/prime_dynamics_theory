"""Exact helpers for the RH-262--RH-271 frontier review."""

from __future__ import annotations


def macro_gates(statuses: dict[str, object]) -> dict[str, bool]:
    """Return Gate A--E with a false-by-default firewall."""

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
    """Normalize and count the five independent certificate obligations."""

    components = {
        "legal_anchored_head": bool(legal_anchored_head),
        "coefficient_bridge": bool(coefficient_bridge),
        "uniform_quotient_tail": bool(uniform_quotient_tail),
        "analytic_target_tail": bool(analytic_target_tail),
        "certified_target_boundary_constant": bool(
            certified_target_boundary_constant
        ),
    }
    vector = list(components.values())
    return {
        "components": components,
        "obligation_vector": vector,
        "required_component_count": len(vector),
        "satisfied_component_count": sum(vector),
        "complete": all(vector),
    }


def root_of_unity_shell_trace(
    shell_size: int, order: int, amplitude_power: complex = 1.0
) -> complex:
    """Return the exact trace formula for a complete root-of-unity shell.

    If the shell eigenvalues are ``alpha*zeta^j`` for ``j=0,...,m-1``, then
    its order-``n`` trace is zero unless ``m`` divides ``n``.  In the divisible
    case ``amplitude_power`` represents ``alpha**n``.
    """

    size = int(shell_size)
    degree = int(order)
    if size < 1 or degree < 1:
        raise ValueError("shell size and order must be positive")
    return 0.0 if degree % size else size * amplitude_power


def route_coordinate(ledger: dict[str, object]) -> str:
    """Preserve the RH-270 route unless all five obligations are complete."""

    if bool(ledger.get("complete_certificate_count", 0)):
        return "complete_certificate_ready_for_gate_A_audit"
    return str(
        ledger.get(
            "route_coordinate",
            "deterministic_target_envelope_sharp_legal_head_bridge_"
            "uniform_quotient_open_complete_zero",
        )
    )
