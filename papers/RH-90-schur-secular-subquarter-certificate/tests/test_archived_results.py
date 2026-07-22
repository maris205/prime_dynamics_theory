from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_schur_audit() -> None:
    audit = load("schur_certificate_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_schur_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["correction_needed_count"] == 9
    assert summary["schur_negative_count"] == 9
    assert summary["minimum_gain_to_required_ratio"] > 1.003
    assert summary["maximum_interval_corrected_contraction"] < 0.24
    assert summary["maximum_linear_solve_dimension"] == 7


def test_boundary() -> None:
    boundary = load("schur_certificate_audit.json")["theorem_boundary"]
    assert boundary["schur_trial_gain_certificate"]
    assert boundary["target_contraction_corollary"]
    assert boundary["ten_channel_subquarter_contraction_validated"]
    assert not boundary["uniform_schur_margin_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("schur_certificate_smoke.json")["rows"]) == 1
