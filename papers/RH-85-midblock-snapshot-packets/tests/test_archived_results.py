from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_snapshot_audit() -> None:
    audit = load("snapshot_packet_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_packet_gates_green"]
    summary = audit["audit_summary"]
    assert summary["maximum_clock_rank"] == 7
    assert summary["maximum_interval_relative_terminal_residual"] < 4.5e-6
    assert summary["minimum_interval_terminal_energy_capture"] > 0.99999999997
    assert summary["maximum_source_packet_relative_residual"] > 0.8
    assert summary["maximum_prefix_gram_relative_residual"] > 0.3


def test_boundary() -> None:
    boundary = load("snapshot_packet_audit.json")["theorem_boundary"]
    assert boundary["snapshot_packet_transfer"]
    assert boundary["unweighted_prefix_gram_no_go"]
    assert not boundary["all_level_packet_decay_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("snapshot_packet_smoke.json")["rows"]) == 1
