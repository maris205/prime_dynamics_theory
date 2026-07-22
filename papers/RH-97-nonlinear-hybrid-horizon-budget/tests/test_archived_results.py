from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("hybrid_horizon_budget_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_primary_hybrid_budget_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["primary_omission_count"] == 5
    assert summary["primary_telescoping_green_count"] == 10
    assert summary["primary_absolute_budget_green_count"] == 10
    assert summary["primary_maximum_absolute_horizon_budget_to_reference"] < 1.1e-5
    assert summary["threshold_summaries"]["1e-06"]["maximum_absolute_horizon_budget_to_reference"] > 0.02
    assert summary["threshold_summaries"]["1e-04"]["maximum_absolute_horizon_budget_to_reference"] > 0.014
    assert summary["threshold_summaries"]["1e-06"]["absolute_budget_green_count"] == 9
    assert summary["threshold_summaries"]["1e-04"]["absolute_budget_green_count"] == 9


def test_boundary() -> None:
    boundary = load("hybrid_horizon_budget_audit.json")["theorem_boundary"]
    assert boundary["nonlinear_hybrid_telescoping_identity"]
    assert boundary["absolute_propagated_horizon_budget"]
    assert boundary["primary_frozen_hybrid_budget_validated"]
    assert not boundary["a_priori_refresh_lipschitz_law_proved"]
    assert not boundary["uniform_block_propagation_envelope_proved"]
    assert not boundary["repeated_block_contraction_proved"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("hybrid_horizon_budget_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["primary_omission_count"] == 4
