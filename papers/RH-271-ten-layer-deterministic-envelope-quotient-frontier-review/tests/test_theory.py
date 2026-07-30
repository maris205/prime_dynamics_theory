import pytest

from frontier_review import (
    macro_gates,
    obligation_summary,
    root_of_unity_shell_trace,
    route_coordinate,
)


def test_root_of_unity_shell_hides_any_fixed_head():
    assert all(root_of_unity_shell_trace(29, order) == 0 for order in range(1, 29))
    assert root_of_unity_shell_trace(29, 29) == 29


def test_root_of_unity_shell_validates_inputs():
    with pytest.raises(ValueError):
        root_of_unity_shell_trace(0, 1)
    with pytest.raises(ValueError):
        root_of_unity_shell_trace(3, 0)


def test_obligation_and_gate_firewalls():
    summary = obligation_summary(
        legal_anchored_head=False,
        coefficient_bridge=False,
        uniform_quotient_tail=False,
        analytic_target_tail=True,
        certified_target_boundary_constant=True,
    )
    assert summary["obligation_vector"] == [False, False, False, True, True]
    assert summary["satisfied_component_count"] == 2
    assert summary["complete"] is False
    assert macro_gates({}) == {letter: False for letter in "ABCDE"}


def test_route_uses_ledger_coordinate():
    coordinate = "deterministic_target_envelope_sharp_open"
    assert route_coordinate({"route_coordinate": coordinate}) == coordinate
    assert route_coordinate({"complete_certificate_count": 1}) == (
        "complete_certificate_ready_for_gate_A_audit"
    )
