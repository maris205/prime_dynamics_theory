import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_anchor_audit():
    data = load("snapshot_enclosure_audit.json")
    summary = data["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["rank_record_count"] == 30
    assert summary["arb_bound_failure_count"] == 0
    assert summary["rank4_radius_below_1e_3_count"] == 10
    assert summary["rank4_radius_below_1e_5_count"] == 8
    assert summary["maximum_rank4_certified_operator_radius"] < 2.83e-4


def test_sharp_boundary_and_smoke_archive():
    data = load("snapshot_enclosure_audit.json")
    boundary = data["theorem_boundary"]
    assert boundary["sharp_normalized_snapshot_perturbation_theorem"]
    assert boundary["orthogonal_svd_quadratic_improvement_theorem"]
    assert not boundary["computed_svd_is_itself_interval_validated"]
    assert not boundary["uniform_all_level_source_enclosure"]
    assert not boundary["riemann_hypothesis"]
    assert load("snapshot_enclosure_smoke.json")["audit_summary"]["channel_count"] == 2

