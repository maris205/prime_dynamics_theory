"""Quantitative bounds for the RH-161 typed assembly theorem."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from math import exp, inf, pi


def packet_riesz_bound(
    contour_length: float,
    packet_resolvent_upper: float,
    full_resolvent_upper: float,
    coupling_upper: float,
) -> dict[str, float | bool]:
    """Bound the Riesz-projector error from a packet resolvent identity.

    If A is the full operator, P is the packet projection, and
    A0 = PAP + (I-P)A(I-P), then coupling_upper bounds ||A-A0||.
    The returned projector bound is the contour integral of the resolvent
    identity.  A value below one guarantees equal finite rank.
    """

    values = (contour_length, packet_resolvent_upper, full_resolvent_upper, coupling_upper)
    if any(value < 0 for value in values):
        raise ValueError("all bounds must be nonnegative")
    projector_error = (
        contour_length
        * packet_resolvent_upper
        * full_resolvent_upper
        * coupling_upper
        / (2.0 * pi)
    )
    return {
        "projector_error_upper": projector_error,
        "equal_rank_by_closeness_certified": projector_error < 1.0,
        "packet_bridge_certified": projector_error < 1.0,
        "margin": 1.0 - projector_error,
    }


def neumann_packet_riesz_bound(
    contour_length: float,
    block_resolvent_upper: float,
    coupling_upper: float,
) -> dict[str, float | bool]:
    """Derive the full resolvent and projector bounds by a Neumann argument."""

    if min(contour_length, block_resolvent_upper, coupling_upper) < 0:
        raise ValueError("all bounds must be nonnegative")
    neumann_product = block_resolvent_upper * coupling_upper
    if neumann_product >= 1.0:
        return {
            "neumann_product": neumann_product,
            "full_resolvent_upper": inf,
            "projector_error_upper": inf,
            "resolvent_certified": False,
            "spectral_rank_certified": False,
            "equal_rank_by_closeness_certified": False,
            "packet_bridge_certified": False,
            "margin": -inf,
        }
    full_resolvent = block_resolvent_upper / (1.0 - neumann_product)
    result = packet_riesz_bound(
        contour_length,
        block_resolvent_upper,
        full_resolvent,
        coupling_upper,
    )
    return {
        "neumann_product": neumann_product,
        "full_resolvent_upper": full_resolvent,
        "resolvent_certified": True,
        "spectral_rank_certified": True,
        **result,
    }


def determinant_error_bound(
    radius: float,
    source_trace_norm_upper: float,
    target_trace_norm_upper: float,
    trace_norm_error_upper: float,
) -> float:
    """Standard trace-class Fredholm determinant continuity bound."""

    values = (radius, source_trace_norm_upper, target_trace_norm_upper, trace_norm_error_upper)
    if any(value < 0 for value in values):
        raise ValueError("all bounds must be nonnegative")
    return (
        radius
        * trace_norm_error_upper
        * exp(1.0 + radius * (source_trace_norm_upper + target_trace_norm_upper))
    )


def det2_error_bound(
    radius: float,
    source_hs_norm_upper: float,
    target_hs_norm_upper: float,
    hs_error_upper: float,
) -> float:
    """Standard second-regularized determinant continuity bound.

    For A and B in S_2, Simon's bound gives
    |det_2(I-zA)-det_2(I-zB)| <= |z| ||A-B||_2
    exp((|z| ||A||_2 + |z| ||B||_2 + 1)^2 / 2).
    """

    values = (radius, source_hs_norm_upper, target_hs_norm_upper, hs_error_upper)
    if any(value < 0 for value in values):
        raise ValueError("all bounds must be nonnegative")
    return (
        radius
        * hs_error_upper
        * exp(0.5 * (radius * (source_hs_norm_upper + target_hs_norm_upper) + 1.0) ** 2)
    )


def marked_trace_error_bound(
    word_length: int,
    operator_norm_upper: float,
    operator_error_upper: float,
    marker_trace_norm_upper: float,
) -> float:
    """Uniform telescoping bound for a marked noncommutative word.

    Every source and target factor is bounded by operator_norm_upper, every
    paired factor error by operator_error_upper, and J is trace class.
    """

    if word_length < 1:
        raise ValueError("word_length must be positive")
    if min(operator_norm_upper, operator_error_upper, marker_trace_norm_upper) < 0:
        raise ValueError("all bounds must be nonnegative")
    return (
        marker_trace_norm_upper
        * word_length
        * operator_norm_upper ** (word_length - 1)
        * operator_error_upper
    )


def _antichain(families: Iterable[frozenset[str]]) -> tuple[frozenset[str], ...]:
    unique = set(families)
    minimal = [family for family in unique if not any(other < family for other in unique)]
    return tuple(sorted(minimal, key=lambda family: (len(family), tuple(sorted(family)))))


def assembly_frontier(
    statuses: Mapping[str, str],
    seed_alternatives: Iterable[str] = ("S_native", "S_lagged"),
) -> tuple[frozenset[str], ...]:
    """Return minimal missing bundles for (native OR lagged) AND R,Q,U,Z,T."""

    allowed = {"proved", "conditional", "finite", "open", "no_go"}
    required = ("R", "Q", "U", "Z", "T")

    def debt(gate: str) -> tuple[frozenset[str], ...]:
        status = statuses[gate]
        if status not in allowed:
            raise ValueError(f"unknown status for {gate}: {status}")
        if status == "proved":
            return (frozenset(),)
        if status == "no_go":
            return ()
        return (frozenset({gate}),)

    seed_bundles = _antichain(bundle for gate in seed_alternatives for bundle in debt(gate))
    if not seed_bundles:
        return ()
    frontier = seed_bundles
    for gate in required:
        gate_debt = debt(gate)
        if not gate_debt:
            return ()
        frontier = _antichain(left | right for left in frontier for right in gate_debt)
    return frontier
