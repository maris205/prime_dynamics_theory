from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("block_schur_budget_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_block_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["update_count"] == 40
    assert summary["schur_negative_count"] == 40
    assert summary["refresh_dominance_count"] == 40
    assert summary["pointwise_subquarter_failure_count"] == 7
    assert summary["pointwise_positive_definite_obstruction_count"] == 7
    assert summary["maximum_block_budget_product"] < 0.24**4
    assert summary["maximum_block_budget_geometric_mean"] < 0.24
    assert summary["minimum_certified_relative_surplus"] > 1e-4


def test_claim_boundary() -> None:
    boundary = load("block_schur_budget_audit.json")["theorem_boundary"]
    assert boundary["exact_schur_threshold_dichotomy"]
    assert boundary["block_bootstrap_theorem"]
    assert boundary["pointwise_subquarter_law_rejected_on_frozen_window"]
    assert not boundary["uniform_all_level_four_step_law_proved"]
    assert not boundary["reduced_packet_refresh_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("block_schur_budget_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["update_count"] == 8
