from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_ledger() -> None:
    ledger = load("prefix_observability_power_ledger.json")
    assert len(ledger["rows"]) == 5
    summary = ledger["audit_summary"]
    assert summary["all_finite_anchor_gates_green"]
    assert summary["maximum_clock_rank"] == 7
    assert summary["finite_memory_depth"] == 5
    assert summary["maximum_conditional_zero_power_hardy_upper"] < 1.84
    assert summary["maximum_stopped_primary_endpoint_ratio"] < 1.01
    assert summary["stress_identification_envelope_last"] < summary["stress_identification_envelope_first"]
    assert abs(summary["prefix_counterexample_fitted_power"] - 1.25) < 1e-12
    assert abs(summary["observation_counterexample_fitted_power"] - 0.75) < 1e-12
    assert summary["scenario_count"] == 6
    assert summary["scenario_green_count"] == 4


def test_scenarios_and_independence() -> None:
    ledger = load("prefix_observability_power_ledger.json")
    scenarios = {item["name"]: item for item in ledger["scenarios"]}
    assert scenarios["zero_power_target"]["total_hardy_power"] == 0.0
    assert scenarios["balanced_quarter_boundary"]["rh49_full_strict_mesh_range_green"]
    assert not scenarios["one_sided_observability_leak"]["rh49_full_strict_mesh_range_green"]
    assert not scenarios["two_sided_prefix_leak"]["rh49_full_strict_mesh_range_green"]
    assert scenarios["observation_residual_cancellation"]["total_hardy_power"] == 0.0
    for item in ledger["counterexamples"].values():
        assert item["normalized_packet_gram"] == 1.0
        assert item["packet_relative_tail"] == 0.0


def test_boundary_and_smoke() -> None:
    ledger = load("prefix_observability_power_ledger.json")
    boundary = ledger["theorem_boundary"]
    assert boundary["max_plus_sigma_power_ledger_theorem"]
    assert boundary["normalization_rank_memory_stop_mesh_overheads_power_zero"]
    assert boundary["prefix_independence_counterexample"]
    assert boundary["observation_independence_counterexample"]
    assert not boundary["prefix_observability_gate_closed"]
    assert not boundary["only_uniform_quotient_gate_remains"]
    assert not boundary["uniform_stage_A_closed"]
    assert not boundary["riemann_hypothesis"]
    smoke = load("prefix_observability_power_smoke.json")
    assert len(smoke["rows"]) == 1
