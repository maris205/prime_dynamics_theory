from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_tail_audit() -> None:
    audit = load("tail_majorization_audit.json")
    assert len(audit["rows"]) == 7
    assert audit["all_executed_tail_gates_green"]
    summary = audit["audit_summary"]
    assert summary["interval_scale_count"] == 5
    assert summary["extended_stress_scale_count"] == 2
    assert summary["maximum_clock_rank"] == 8
    assert summary["maximum_tail_majorization_ratio"] < 0.015
    assert summary["maximum_extended_relative_tail"] < 2e-15


def test_boundary() -> None:
    boundary = load("tail_majorization_audit.json")["theorem_boundary"]
    assert boundary["ky_fan_candidate_upper"]
    assert boundary["tail_majorization_transfer"]
    assert not boundary["all_level_tail_majorization_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("tail_majorization_smoke.json")["rows"]) == 1

