from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_capacity_audit() -> None:
    audit = load("three_mode_capacity_audit.json")
    summary = audit["audit_summary"]
    assert summary["scale_count"] == 5
    assert summary["channel_count"] == 10
    assert summary["update_count"] == 360
    assert summary["fine_update_count"] == 234
    assert summary["capacity_enclosure_failure_count"] == 0
    assert summary["recovery_implication_failure_count"] == 0
    assert summary["selector_equivalence_failure_count"] == 0
    assert summary["all_threshold_counts_match_direct_weyl"]
    assert summary["minimum_fine_recovery_efficiency"] > 0.998
    assert summary["maximum_fine_capacity_relative_width"] < 0.0018


def test_threshold_counts_and_boundary() -> None:
    audit = load("three_mode_capacity_audit.json")
    expected = {"1e-08": 113, "1e-06": 109, "1e-04": 98}
    for key, count in expected.items():
        record = audit["threshold_summary"][key]
        assert record["recovery_support_count"] == count
        assert record["direct_support_count"] == count
        assert record["fine_recovery_support_count"] == 78
    assert audit["barrier"]["maximum_endpoint_error"] < 1e-14
    boundary = audit["theorem_boundary"]
    assert boundary["finite_memory_capacity_interval"]
    assert boundary["capacity_aware_volume_recovery"]
    assert not boundary["all_level_capacity_upper_law_proved"]
    assert not boundary["uniform_stage_A_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("three_mode_capacity_smoke.json")
    assert smoke["audit_summary"]["update_count"] == 24
