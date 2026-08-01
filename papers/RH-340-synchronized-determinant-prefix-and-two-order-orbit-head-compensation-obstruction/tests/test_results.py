import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_common_cut_rederives_both_tails_without_claiming_rh288():
    data = _result()
    cut = data["common_cut"]
    assert cut["cut"] == "u=4k"
    assert cut["one_alias_window"] == "2k<u<=4k"
    assert cut["tail_clock_is_rederived_from_mass_bound"] is True
    assert cut["noisy_tail_vanishes"] is True
    assert cut["target_tail_vanishes"] is True
    assert data["three_budget_equivalence"]["rh288_status"] == "OPEN_not_activated"


def test_prefix_identity_and_three_budget_firewall():
    data = _result()
    identity = data["prefix_identity"]
    assert identity["sharp_bound"] == "abs(P_u-E_u)<=D_u"
    assert identity["conditional_equivalence"].startswith("D_u->0")
    condition = data["three_budget_equivalence"]["same_clock_condition"]
    assert "D_u->0" in condition
    assert "E_off->0" in condition
    assert "q_(sigma,k,2k)=o(H_k)" in condition


def test_two_order_compensation_is_necessary_only():
    atoms = _result()["two_order_atoms"]
    assert atoms["critical_compensation"].startswith("C_k^0-d_")
    assert atoms["lower_compensation"].startswith("C_k^--d_")
    assert atoms["critical_relative_precision"] == "o((beta*R)^(-2k))"
    assert atoms["lower_relative_precision"] == "o((beta*R)^(-2(k-1)))"


def test_claim_firewall_and_gates():
    data = _result()
    assert len(data["false_claims"]) == 17
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())
