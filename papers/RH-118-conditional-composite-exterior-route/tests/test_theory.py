from __future__ import annotations

import pytest

from conditional_route import (
    conditional_composite_gate,
    directional_route_lower,
    factorized_route_lower,
    outward_degraded_candidates,
    trace_route_lower,
)


def test_factorized_and_trace_routes() -> None:
    assert factorized_route_lower(0.2, 0.5) == pytest.approx(0.4)
    assert trace_route_lower(0.09, 4.0, 0.5) == pytest.approx(0.3)


def test_directional_route() -> None:
    value = directional_route_lower(0.4, 0.25, 0.5)
    assert value == pytest.approx((0.75**4) * 0.8)


def test_composite_and_alternating_selection() -> None:
    gate = conditional_composite_gate({"direct": 0.1, "trace": 0.4, "directional": 0.3}, 0.25)
    assert gate["selected_route"] == "trace"
    assert gate["support_certified"]
    assert gate["margin"] == pytest.approx(0.15)


def test_outward_transport_only_degrades() -> None:
    candidates = {"a": 0.3, "b": 0.1}
    transported = outward_degraded_candidates(candidates, {"a": 0.04, "b": 0.2})
    assert transported == pytest.approx({"a": 0.26, "b": 0.0})


def test_validation() -> None:
    with pytest.raises(ValueError):
        trace_route_lower(-1.0, 2.0, 1.0)
    with pytest.raises(ValueError):
        directional_route_lower(1.0, -0.1, 1.0)
    with pytest.raises(ValueError):
        conditional_composite_gate({}, 1e-4)
    with pytest.raises(ValueError):
        outward_degraded_candidates({"a": 1.0}, {"b": 0.1})
