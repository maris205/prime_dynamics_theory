from frontier_review import macro_gates, obligation_summary, route_coordinate


def test_obligation_summary_keeps_target_tail_separate_from_Ms():
    summary = obligation_summary(
        legal_anchored_head=False,
        coefficient_bridge=False,
        uniform_quotient_tail=False,
        analytic_target_tail=True,
        certified_target_boundary_constant=False,
    )
    assert summary["required_component_count"] == 5
    assert summary["satisfied_component_count"] == 1
    assert summary["complete"] is False


def test_macro_gate_firewall_defaults_false():
    assert macro_gates({}) == {letter: False for letter in "ABCDE"}
    assert macro_gates({"gate_A": True})["A"] is True


def test_route_uses_archived_ledger_coordinate():
    coordinate = "legal_heads_obstructed_target_tail_exists_Ms_uncertified_quotient_finite_nonuniform_complete_certificate_zero"
    assert route_coordinate({"route_coordinate": coordinate}) == coordinate
    assert route_coordinate({"complete_certificate_count": 1}) == (
        "complete_head_tail_certificate_ready_for_gate_A_audit"
    )
