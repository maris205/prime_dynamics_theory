import math

import pytest

from typed_assembly import (
    assembly_frontier,
    det2_error_bound,
    determinant_error_bound,
    marked_trace_error_bound,
    neumann_packet_riesz_bound,
    packet_riesz_bound,
)


def test_packet_riesz_threshold() -> None:
    result = packet_riesz_bound(2.0 * math.pi, 2.0, 2.5, 0.05)
    assert result["projector_error_upper"] == pytest.approx(0.25)
    assert result["equal_rank_by_closeness_certified"]
    assert result["packet_bridge_certified"]
    assert result["margin"] == pytest.approx(0.75)


def test_packet_riesz_rank_gate_can_fail() -> None:
    result = packet_riesz_bound(2.0 * math.pi, 4.0, 4.0, 0.1)
    assert result["projector_error_upper"] == pytest.approx(1.6)
    assert not result["packet_bridge_certified"]


def test_neumann_packet_riesz_bound() -> None:
    result = neumann_packet_riesz_bound(2.0 * math.pi, 2.0, 0.05)
    assert result["resolvent_certified"]
    assert result["spectral_rank_certified"]
    assert result["full_resolvent_upper"] == pytest.approx(2.0 / 0.9)
    assert result["projector_error_upper"] == pytest.approx(2.0 * (2.0 / 0.9) * 0.05)
    failed = neumann_packet_riesz_bound(2.0 * math.pi, 2.0, 0.5)
    assert not failed["resolvent_certified"]
    assert not failed["spectral_rank_certified"]
    assert not failed["packet_bridge_certified"]


def test_determinant_continuity_formula() -> None:
    result = determinant_error_bound(0.5, 1.0, 1.2, 0.01)
    assert result == pytest.approx(0.005 * math.exp(2.1))


def test_regularized_determinant_continuity_formula() -> None:
    result = det2_error_bound(0.5, 1.0, 1.2, 0.01)
    assert result == pytest.approx(0.005 * math.exp(0.5 * 2.1**2))


def test_marked_trace_telescoping_formula() -> None:
    assert marked_trace_error_bound(3, 2.0, 0.01, 4.0) == pytest.approx(0.48)
    assert marked_trace_error_bound(6, 1.0, 0.02, 0.5) == pytest.approx(0.06)


def test_typed_frontier_has_two_seed_alternatives() -> None:
    statuses = {
        "S_native": "conditional",
        "S_lagged": "conditional",
        "R": "open",
        "Q": "open",
        "U": "open",
        "Z": "open",
        "T": "open",
    }
    assert assembly_frontier(statuses) == (
        frozenset({"Q", "R", "S_lagged", "T", "U", "Z"}),
        frozenset({"Q", "R", "S_native", "T", "U", "Z"}),
    )


def test_proved_gate_drops_and_no_go_kills_only_seed_branch() -> None:
    statuses = {
        "S_native": "no_go",
        "S_lagged": "conditional",
        "R": "proved",
        "Q": "open",
        "U": "open",
        "Z": "open",
        "T": "open",
    }
    assert assembly_frontier(statuses) == (
        frozenset({"Q", "S_lagged", "T", "U", "Z"}),
    )


def test_invalid_bounds_and_statuses() -> None:
    with pytest.raises(ValueError):
        packet_riesz_bound(-1.0, 1.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        determinant_error_bound(1.0, 1.0, 1.0, -0.1)
    with pytest.raises(ValueError):
        det2_error_bound(1.0, 1.0, 1.0, -0.1)
    with pytest.raises(ValueError):
        marked_trace_error_bound(0, 1.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        assembly_frontier({
            "S_native": "guessed", "S_lagged": "open", "R": "open",
            "Q": "open", "U": "open", "Z": "open", "T": "open",
        })
