from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("source_seeded_support_audit.json")
    summary = audit["audit_summary"]
    assert len(audit["thresholds"]) == 3
    assert summary["total_candidate_comparisons"] == 360
    assert summary["total_weak_mode_events"] == 38
    assert summary["all_finite_selector_equivalences_green"]
    assert summary["all_finite_fine_supports_empty"]
    assert summary["primary_fine_support_start_level"] == 2
    assert summary["minimum_fine_support_margin"] > 7.0
    assert summary["maximum_stopped_endpoint_ratio"] < 1.007
    assert summary["maximum_unrestricted_endpoint_ratio"] > 1.024


def test_boundary_and_smoke() -> None:
    audit = load("source_seeded_support_audit.json")
    boundary = audit["theorem_boundary"]
    assert boundary["adaptive_support_equivalence"]
    assert boundary["coarse_support_to_price_reduction"]
    assert boundary["finite_extrapolation_barrier"]
    assert boundary["five_anchor_fine_support_separation_validated"]
    assert not boundary["all_level_fine_support_separation_proved"]
    assert not boundary["riemann_hypothesis"]
    smoke = load("source_seeded_support_smoke.json")
    assert len(smoke["thresholds"]) == 1
