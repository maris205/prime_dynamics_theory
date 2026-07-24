import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit_counts():
    data = load("floor_free_audit.json")
    summary = data["audit_summary"]
    assert summary["state_count"] == 120
    assert summary["pair_count"] == 96
    assert summary["chain_count"] == 24
    assert summary["exact_discrete_rank_four_count"] == 120
    assert summary["positive_floor_free_candidate_count"] == 118
    assert summary["positive_transfer_count"] == 67
    assert summary["infinite_tail_factor_count"] == 24
    assert summary["finite_superunit_gamma_transfer_count"] == 5
    assert summary["positive_chain_count"] == 0


def test_boundary_and_smoke():
    data = load("floor_free_audit.json")
    boundary = data["theorem_boundary"]
    assert boundary["artificial_positive_gram_floor_removed"]
    assert not boundary["four_directional_chain_survives_floor_removal"]
    assert not boundary["physical_all_level_recurrence_proved"]
    assert not boundary["riemann_hypothesis"]
    assert load("floor_free_smoke.json")["audit_summary"]["state_count"] == 8
