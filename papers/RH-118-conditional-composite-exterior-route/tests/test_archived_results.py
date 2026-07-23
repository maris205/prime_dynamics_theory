from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_route_audit() -> None:
    audit = load("conditional_route_audit.json")
    summary = audit["audit_summary"]
    assert (summary["scale_count"], summary["update_count"], summary["fine_update_count"]) == (5, 360, 234)
    assert summary["actual_support_count"] == 322
    assert summary["composite_support_count"] == 321
    assert summary["adaptive_support_count"] == 322
    assert summary["composite_missed_supported_count"] == 1
    assert summary["adaptive_missed_supported_count"] == 0
    assert summary["composite_false_positive_count"] == 0
    assert summary["adaptive_false_positive_count"] == 0
    assert summary["support_label_disagreement_count"] == 0


def test_threshold_counts_and_packets() -> None:
    audit = load("conditional_route_audit.json")
    expected = {"1e-08": (115, 114, 115), "1e-06": (109, 109, 109), "1e-04": (98, 98, 98)}
    for key, counts in expected.items():
        record = audit["threshold_summary"][key]
        assert (record["actual_support_count"], record["composite_support_count"], record["adaptive_support_count"]) == counts
        assert record["fine_composite_support_count"] == record["fine_adaptive_support_count"] == 78
    assert len(audit["minimal_physical_packets"]) == 3
    assert all(not packet["all_level_condition_proved"] for packet in audit["minimal_physical_packets"].values())
    boundary = audit["theorem_boundary"]
    assert boundary["conditional_composite_liminf_theorem"]
    assert boundary["alternating_route_closure"]
    assert not boundary["any_all_level_physical_packet_proved"]


def test_smoke_exists() -> None:
    assert load("conditional_route_smoke.json")["audit_summary"]["update_count"] == 24
