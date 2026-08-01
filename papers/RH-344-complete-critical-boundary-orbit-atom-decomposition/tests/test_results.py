import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_complete_orbit_theorem_is_typed_exactly():
    theorem = _result()["complete_orbit_theorem"]
    assert theorem["cardinality"] == "2k_distinct"
    assert theorem["noisy_trace_on_finite_orbit"] == "0_exactly"
    assert theorem["signed_raw_atom"] == "-F_orb_k"


def test_cellwise_refinement_retains_phase_ambiguity():
    cellwise = _result()["cellwise_refinement"]
    assert cellwise["eventual_counts_Jminus_Jplus_F"] == "(epsilon_k,0,2k-epsilon_k)"
    assert cellwise["threshold_equality_stabilization"].startswith("NOT_DETERMINED")


def test_typed_identity_keeps_head_defect_separate():
    identity = _result()["typed_identity"]
    assert identity["full_trace"] == "q=T_rest+P_parity-A_alias-F_orb"
    assert identity["direct"] == "p=T_rest+P_parity-d_head-A_alias-F_orb"


def test_scale_theorem_records_super_target_missing_point():
    scale = _result()["scale_theorem"]
    assert scale["missing_point"] == "F_orb_k-D_orb_k=G_k"
    assert scale["missing_point_over_H"].endswith("->infinity")
    assert scale["alias_plus_full_over_alias_limit"] == "2"
    assert scale["full_equals_far_plus_o_H"] is False


def test_finite_rows_are_formula_checks_only():
    data = _result()
    assert len(data["finite_rows"]) == 5
    assert data["finite_rows_are_reproduction_checks_only"] is True
    for row in data["finite_rows"]:
        assert row["complete_count"] == 2 * row["k"]
        assert row["cell_count_identity"] == 2 * row["k"]


def test_claim_firewall_and_gates_remain_false():
    data = _result()
    assert len(data["false_claims"]) == 21
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())


def test_route_stops_at_the_actual_orbit_free_rest():
    boundary = _result()["route_boundary"]
    assert boundary["orbit_free_rest_minus_head_estimate"].startswith("NOT_TESTABLE")
    assert boundary["determinant_gluing"] == "OPEN_not_activated"
