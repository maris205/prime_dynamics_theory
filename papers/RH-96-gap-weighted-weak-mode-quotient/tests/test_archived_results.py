from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("weak_mode_quotient_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_primary_quotient_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["primary_update_count"] == 120
    assert summary["primary_omitted_update_count"] == 5
    assert summary["primary_gap_certificate_count"] == 5
    assert summary["primary_width_three_update_count"] == 5
    assert summary["primary_width_four_update_count"] == 115
    assert summary["primary_maximum_endpoint_to_reference_ratio"] < 1.01
    assert summary["primary_maximum_adaptive_to_full_tail_ratio"] < 1.00001
    assert not summary["threshold_summaries"]["1e-06"]["all_endpoints_green"]
    assert not summary["threshold_summaries"]["1e-04"]["all_endpoints_green"]


def test_boundary() -> None:
    boundary = load("weak_mode_quotient_audit.json")["theorem_boundary"]
    assert boundary["universal_omitted_block_bound"]
    assert boundary["gap_weighted_weak_mode_tail_loss_theorem"]
    assert boundary["adaptive_width_frozen_horizons_validated"]
    assert not boundary["weak_cross_modes_geometrically_identified"]
    assert not boundary["uniform_retained_to_omitted_gap_proved"]
    assert not boundary["repeated_block_contraction_proved"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("weak_mode_quotient_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["primary_update_count"] == 8
