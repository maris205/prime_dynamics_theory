"""Deterministic route labels for the ten-layer review."""

from __future__ import annotations


def macro_gates(statuses: dict[str, bool]) -> dict[str, bool]:
    return {
        gate: bool(statuses.get(f"gate_{gate}", statuses.get(gate, False)))
        for gate in "ABCDE"
    }


def route_coordinate(statuses: dict[str, bool]) -> str:
    if statuses.get("complete_gluing_certificate", False):
        return "anchored_uniform_relative_det2_certificate_pending_gate_A_review"
    return "exact_superloop_quotient_frozen_anchor_class_obstructed_open_new_selector_uniform_tail"
