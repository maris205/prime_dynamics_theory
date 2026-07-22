from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_injection_audit() -> None:
    audit = load("injection_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_injection_gates_green"]
    summary = audit["audit_summary"]
    assert summary["maximum_interval_last_injection_relative_norm"] < 5e-4
    assert summary["minimum_interval_last_injection_capture"] > 0.99999975
    assert summary["maximum_last_injection_energy_ratio"] < 0.18
    assert summary["maximum_interval_lagged_terminal_relative_residual"] < 0.0012
    assert summary["maximum_final_recursion_utilization"] < 0.53


def test_boundary() -> None:
    boundary = load("injection_audit.json")["theorem_boundary"]
    assert boundary["rank_staircase_injection_recursion"]
    assert boundary["scalar_convolution_corollary"]
    assert boundary["five_scale_last_injection_validated"]
    assert not boundary["all_level_injection_law_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("injection_smoke.json")["rows"]) == 1
