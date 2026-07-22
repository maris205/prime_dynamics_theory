from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("finite_memory_gram_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_action_bounds_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["update_count"] == 120
    assert summary["minimum_successful_uniform_depth"] == 5
    assert summary["depth_summary"]["4"]["endpoint_green_count"] == 9
    assert summary["depth_summary"]["5"]["endpoint_green_count"] == 10
    assert summary["depth_summary"]["4"]["maximum_endpoint_to_reference_ratio"] > 1.05
    assert summary["depth_summary"]["5"]["maximum_endpoint_to_reference_ratio"] < 1.01
    assert summary["maximum_full_history_to_assembled_action_error"] < 1e-14
    assert summary["maximum_direct_to_structured_projector_distance"] > 1e-4


def test_boundary() -> None:
    boundary = load("finite_memory_gram_audit.json")["theorem_boundary"]
    assert boundary["exact_finite_history_packet_action"]
    assert boundary["uniform_geometric_tail_bound"]
    assert boundary["ambient_gram_assembly_removed"]
    assert boundary["fixed_depth_frozen_prefix_validated"]
    assert not boundary["state_packet_multiplication_removed"]
    assert not boundary["uniform_all_level_ritz_stability_proved"]
    assert not boundary["uniform_stage_A_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("finite_memory_gram_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["update_count"] == 8
