from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("two_direction_refresh_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_two_direction_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["two_direction_update_count"] == 40
    assert summary["trial_frame_negative_count"] == 40
    assert summary["direct_target_contraction_count"] == 40
    assert summary["one_direction_subquarter_failure_count"] == 4
    assert summary["two_direction_subquarter_block_count"] == 10
    assert summary["maximum_two_direction_budget_geometric_mean"] < 0.24
    assert summary["maximum_two_direction_block_geometric_mean"] < 0.229
    assert summary["maximum_primary_compressed_dimension"] == 9
    assert summary["minimum_top_two_cross_energy_fraction"] > 0.963


def test_boundary() -> None:
    boundary = load("two_direction_refresh_audit.json")["theorem_boundary"]
    assert boundary["k_direction_complement_ritz_theorem"]
    assert boundary["generalized_trial_frame_gain_certificate"]
    assert boundary["recursive_reduced_block_theorem"]
    assert boundary["one_direction_recursive_route_rejected_on_four_fine_channels"]
    assert not boundary["uniform_all_level_two_direction_law_proved"]
    assert not boundary["continuum_cross_direction_construction_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("two_direction_refresh_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["two_direction_update_count"] == 8
