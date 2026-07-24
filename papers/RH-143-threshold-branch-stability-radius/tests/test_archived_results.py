import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_threshold_audit():
    summary = load("threshold_branch_audit.json")["audit_summary"]
    assert summary["threshold_count"] == 3
    assert summary["update_record_count"] == 360
    assert summary["selected_width_mismatch_count"] == 0
    assert summary["strict_branch_count"] == 360
    assert summary["fp64_budget_stable_count"] == 360
    assert 4.34e-9 < summary["primary_minimum_relative_branch_radius"] < 4.35e-9
    assert summary["primary_minimum_branch_radius_to_fp64_budget"] > 2300


def test_boundary_and_smoke():
    data = load("threshold_branch_audit.json")
    boundary = data["theorem_boundary"]
    assert boundary["sharp_clipped_relative_threshold_branch_radius"]
    assert boundary["all_archived_branches_have_positive_nominal_margin"]
    assert not boundary["fp64_proxy_is_an_interval_source_to_cross_enclosure"]
    assert not boundary["uniform_all_level_packet_update"]
    assert not boundary["riemann_hypothesis"]
    assert load("threshold_branch_smoke.json")["audit_summary"]["update_record_count"] == 8

