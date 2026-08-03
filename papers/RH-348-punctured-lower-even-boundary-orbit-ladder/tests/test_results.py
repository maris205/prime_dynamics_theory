import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_index_set_is_the_punctured_lower_even_subprefix():
    index = _result()["index_set"]
    assert index["punctured_lower_even_orders"].endswith("m<=k-2")
    assert index["excluded_selected_orders"] == "2k_and_2k-2"
    assert index["orders_are_in_strict_one_alias_prefix"] is True


def test_coefficient_ladder_keeps_full_trace_and_direct_types_separate():
    ladder = _result()["coefficient_ladder"]
    assert ladder["full_trace"].startswith("q_")
    assert ladder["direct"].startswith("p_")
    assert "-d_" in ladder["Y"]


def test_aggregate_theorem_records_exact_scope():
    aggregate = _result()["aggregate_theorem"]
    assert aggregate["x"] == "x=(beta*R)^2>1"
    assert aggregate["absolute_radial_over_orbit"].endswith("->0")
    assert aggregate["combined_demand_diverges"] is True


def test_compensation_is_necessary_not_observed():
    compensation = _result()["necessary_compensation"]
    assert compensation["reverse_triangle"].startswith("sum_abs_Z>=")
    assert compensation["closure_requires_supply_mass_asymptotic_at_least_orbit_ladder"] is True
    assert compensation["actual_supply_bound_available"] is False


def test_finite_rows_are_diagnostics_only():
    data = _result()
    assert len(data["finite_rows"]) == 4
    assert data["finite_rows_are_reproduction_checks_only"] is True


def test_claim_firewall_and_gates_remain_false():
    data = _result()
    assert len(data["false_claims"]) == 18
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())


def test_route_moves_to_two_sideband_phase_incompatibility():
    route = _result()["route_boundary"]
    assert route["lower_even_punctured_demand"].startswith("PROVED")
    assert route["actual_signed_compensation"].startswith("NOT_TESTABLE")
    assert route["remaining_E_off"].startswith("NOT_TESTABLE")
    assert route["next_route"].startswith("RH-349")
