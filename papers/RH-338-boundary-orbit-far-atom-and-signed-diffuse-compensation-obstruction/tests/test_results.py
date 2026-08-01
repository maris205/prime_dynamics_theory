import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_containment_and_atom_theorems_are_typed_exactly():
    data = _result()
    assert data["analytic_containment"]["Omega_subset_F_eventually"] is True
    theorem = data["far_atom_theorem"]
    assert theorem["noisy_localized_trace_on_Omega"].startswith("0_exactly")
    assert theorem["D_orb_over_alias_limit"] == "1"
    assert theorem["D_orb_over_H_limit"] == "+infinity"
    assert theorem["certified_far_counts"] == {
        "2": 3,
        "4": 7,
        "8": 15,
        "16": 31,
        "32": 63,
    }


def test_signed_compensation_is_necessary_but_not_supplied():
    barrier = _result()["signed_compensation_barrier"]
    assert barrier["necessary_condition_for_R_o_H"] == "R_rest_k=D_orb_k+o(H_k)"
    assert barrier["separate_absolute_atom_rest_bound_sufficient"] is False
    assert barrier["aggregate_verdict"].startswith("NOT_TESTABLE")


def test_finite_rows_are_diagnostics_only():
    data = _result()
    assert len(data["finite_rows"]) == 5
    assert data["finite_rows_are_reproduction_checks_only"] is True
    for row in data["finite_rows"]:
        assert row["certified_subset_count"] == 2 * row["k"] - 1
        assert row["certified_subset_far_count"] == 2 * row["k"] - 1


def test_claim_firewall_and_gates_remain_false():
    data = _result()
    assert len(data["false_claims"]) == 18
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())
