from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_late_memory_audit() -> None:
    audit = load("late_memory_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_memory_gates_green"]
    summary = audit["audit_summary"]
    assert summary["maximum_interval_relative_terminal_residual"] < 1.2e-5
    assert summary["minimum_interval_terminal_energy_capture"] > 0.99999999985
    assert summary["minimum_unweighted_improvement_factor"] > 1000.0
    assert summary["minimum_angle_perturbation_gap_ratio"] > 1e6
    assert summary["maximum_past_trace_fraction"] < 0.002


def test_boundary() -> None:
    boundary = load("late_memory_audit.json")["theorem_boundary"]
    assert boundary["normalized_memory_variational_theorem"]
    assert boundary["gap_free_snapshot_energy_transfer"]
    assert boundary["angle_perturbation_route_rejected_at_anchors"]
    assert not boundary["all_level_late_memory_packet_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("late_memory_smoke.json")["rows"]) == 1
