from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit_is_complete_and_monotone() -> None:
    audit = load("memory_depth_audit.json")
    summary = audit["audit_summary"]
    assert (summary["scale_count"], summary["channel_count"], summary["update_count"]) == (5, 10, 360)
    assert summary["supported_update_count"] == 322
    assert summary["adaptive_certificate_count"] == 322
    assert summary["maximum_certifying_depth"] == 6
    assert summary["tail_enclosure_failure_count"] == 0
    assert summary["dominance_failure_count"] == 0
    assert summary["monotone_failure_count"] == 0
    assert summary["completeness_failure_count"] == 0
    assert summary["aggregate_cost_reduction"] > 0.72


def test_threshold_depths_and_boundary() -> None:
    audit = load("memory_depth_audit.json")
    expected = {"1e-08": (115, 6), "1e-06": (109, 5), "1e-04": (98, 4)}
    for key, pair in expected.items():
        record = audit["threshold_summary"][key]
        assert (record["adaptive_certificate_count"], record["maximum_certifying_depth"]) == pair
        assert record["fine_certificate_count"] == 78
    boundary = audit["theorem_boundary"]
    assert boundary["nested_weyl_lower_monotonicity"]
    assert boundary["first_passage_depth_is_cost_minimal"]
    assert boundary["finite_full_history_search_is_complete"]
    assert not boundary["all_level_uniform_depth_proved"]
    assert not boundary["uniform_stage_A_closed"]


def test_smoke_exists() -> None:
    assert load("memory_depth_smoke.json")["audit_summary"]["update_count"] == 24
