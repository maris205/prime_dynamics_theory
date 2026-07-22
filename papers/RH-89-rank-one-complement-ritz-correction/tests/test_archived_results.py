from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_ritz_audit() -> None:
    audit = load("ritz_correction_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_ritz_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["minimum_interval_reference_dividend_fraction"] > 0.96
    assert summary["maximum_interval_corrected_contraction"] < 0.24
    assert summary["maximum_binary64_corrected_reference_tail_ratio"] < 3.28
    assert summary["maximum_enriched_dimension"] == 8


def test_boundary() -> None:
    boundary = load("ritz_correction_audit.json")["theorem_boundary"]
    assert boundary["rank_one_complement_ritz_theorem"]
    assert boundary["cross_block_maximal_coupling_direction"]
    assert boundary["ten_channel_corrected_contraction_validated"]
    assert not boundary["uniform_cross_block_enrichment_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("ritz_correction_smoke.json")["rows"]) == 1
