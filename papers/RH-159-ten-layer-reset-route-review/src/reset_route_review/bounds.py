"""Typed route and positive-block bounds for the reset-route review."""

from __future__ import annotations

import math
from collections.abc import Iterable


ALLOWED_GATE_STATES = {"certified", "open", "obstruction"}


def directional_to_native_lower(cross_singular_lower: float, complement_upper: float) -> float:
    """Lower for a native compression eigenvalue from a cross singular lower.

    For a positive block matrix with cross block ``B`` and complementary
    diagonal block bounded by ``U``, ``B*B <= U A``.
    """

    cross = float(cross_singular_lower)
    complement = float(complement_upper)
    if not math.isfinite(cross) or not math.isfinite(complement) or cross < 0.0 or complement < 0.0:
        raise ValueError("invalid positive-block data")
    if complement == 0.0:
        if cross > 0.0:
            raise ValueError("positive cross is incompatible with a zero positive complement")
        return 0.0
    return cross * cross / complement


def classify_route(required_gate_states: Iterable[str]) -> str:
    """Classify a typed route at a fixed destination."""

    states = list(required_gate_states)
    if not states:
        raise ValueError("a route must contain at least one required gate")
    if any(state not in ALLOWED_GATE_STATES for state in states):
        raise ValueError("unknown gate state")
    if "obstruction" in states:
        return "rejected"
    if "open" in states:
        return "open"
    return "finite_closed"


def first_unresolved_gate(gates: Iterable[tuple[str, str]]) -> str | None:
    """Return the first open or obstructed gate in route order."""

    records = list(gates)
    for name, state in records:
        if state not in ALLOWED_GATE_STATES:
            raise ValueError("unknown gate state")
        if state != "certified":
            return name
    return None
