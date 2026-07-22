from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("source_seeded_horizon_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_source_seeded_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["primary_update_count"] == 120
    assert summary["source_seed_equivalence_count"] == 10
    assert summary["width_four_endpoint_green_count"] == 10
    assert summary["maximum_width_two_endpoint_to_reference_ratio"] > 11.0
    assert summary["maximum_width_three_endpoint_to_reference_ratio"] > 1.4
    assert summary["maximum_width_four_endpoint_to_reference_ratio"] < 1.01
    assert summary["minimum_width_four_cross_energy_fraction"] > 0.975
    assert summary["maximum_primary_compressed_dimension"] == 11


def test_boundary() -> None:
    boundary = load("source_seeded_horizon_audit.json")["theorem_boundary"]
    assert boundary["source_seed_equivalence_theorem"]
    assert boundary["source_seeded_recursive_horizon_theorem"]
    assert boundary["late_ambient_eigenspace_seed_removed"]
    assert not boundary["source_coordinate_svd_removed"]
    assert not boundary["ambient_gram_packet_action_removed"]
    assert not boundary["uniform_all_level_four_direction_law_proved"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("source_seeded_horizon_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["primary_update_count"] == 8
