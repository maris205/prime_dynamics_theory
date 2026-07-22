from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_predictor_corrector_audit() -> None:
    audit = load("predictor_corrector_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_factorization_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["global_norm_failure_count"] == 10
    assert summary["point_predictor_contraction_count"] == 6
    assert summary["memory_predictor_contraction_count"] == 9
    assert summary["actual_memory_contraction_count"] == 10
    assert summary["maximum_actual_memory_contraction"] < 0.235
    assert summary["minimum_interval_global_coefficient_lower"] > 2.6


def test_boundary() -> None:
    boundary = load("predictor_corrector_audit.json")["theorem_boundary"]
    assert boundary["residual_rayleigh_factorization"]
    assert boundary["predictor_corrector_contraction_identity"]
    assert boundary["global_norm_route_rejected_at_anchors"]
    assert not boundary["uniform_reoptimization_gain_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("predictor_corrector_smoke.json")["rows"]) == 1
