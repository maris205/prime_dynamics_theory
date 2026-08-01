import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_cut_lemma_and_sideband_atom_are_locked():
    data = _result()
    assert data["cut_lemma"]["included_for_every_admissible_cut"] is True
    assert data["cut_lemma"]["mandatory_sideband"] == "n_minus=2k-2"
    assert data["physical_orbit_atom"]["far_subset_cardinality"] == "2k-3"
    assert data["physical_orbit_atom"]["atom_over_H_(k-1)_limit"] == "+infinity"


def test_only_necessary_compensation_not_E_off_verdict_is_claimed():
    data = _result()
    compensation = data["necessary_compensation"]
    assert compensation["E_off_to_zero_implies"].endswith("+o(H_(k-1))")
    assert compensation["aggregate_verdict"].startswith("NOT_TESTABLE")
    assert compensation["separate_absolute_atom_complement_bound_sufficient"] is False


def test_counterloop_sideband_sign_is_not_promoted_from_a_decimal():
    identity = _result()["counterloop_sideband_identity"]
    assert identity["sign_claimed_from_current_sources"] is False
    assert identity["reason"] == (
        "source_proves_only_C_M_positive_and_rounded_decimal_is_not_interval_certificate"
    )


def test_finite_rows_and_claim_firewall():
    data = _result()
    assert len(data["finite_rows"]) == 5
    assert data["finite_rows_are_reproduction_checks_only"] is True
    assert len(data["false_claims"]) == 17
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())
