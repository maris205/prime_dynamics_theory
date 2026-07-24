import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_backward_viability_audit():
    summary = load("backward_viability_audit.json")["audit_summary"]
    assert summary["chain_count"] == 30
    assert summary["viable_chain_count"] == 28
    assert summary["obstructed_chain_count"] == 2
    assert summary["full_unit_start_radius_count"] == 28
    assert summary["near_boundary_policy_safe_count"] == 28
    assert 0.0017 < summary["minimum_positive_backward_radius"] < 0.0018
    assert summary["minimum_obstruction_minimum_floor"] > 9.4


def test_boundary_and_smoke():
    data = load("backward_viability_audit.json")
    boundary = data["theorem_boundary"]
    assert boundary["controlled_backward_viability_kernel"]
    assert boundary["two_rh137_failures_are_candidate_family_obstructions"]
    assert not boundary["all_level_repeating_block_hypothesis_verified"]
    assert not boundary["normalized_base_liminf"]
    assert not boundary["riemann_hypothesis"]
    assert load("backward_viability_smoke.json")["audit_summary"]["chain_count"] == 2

