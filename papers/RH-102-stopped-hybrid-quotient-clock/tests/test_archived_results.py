from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("stopped_hybrid_clock_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_stopped_clock_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["all_threshold_chain_count"] == 30
    assert summary["all_threshold_endpoint_green_count"] == 30
    assert summary["primary_accepted_quotient_count"] == 5
    assert summary["primary_stopped_channel_count"] == 0
    coarse = summary["threshold_summary"]["1e-04"]
    medium = summary["threshold_summary"]["1e-06"]
    assert coarse["accepted_quotient_count"] == 20
    assert coarse["rejected_quotient_count"] == 2
    assert coarse["stopped_channel_count"] == 2
    assert coarse["maximum_unrestricted_endpoint_to_reference_ratio"] > 1.014
    assert coarse["maximum_final_endpoint_to_reference_ratio"] < 1.007
    assert medium["accepted_quotient_count"] == 10
    assert medium["rejected_quotient_count"] == 1
    assert medium["maximum_unrestricted_endpoint_to_reference_ratio"] > 1.024
    assert medium["maximum_final_endpoint_to_reference_ratio"] < 1.002


def test_every_chain_certificate() -> None:
    audit = load("stopped_hybrid_clock_audit.json")
    for row in audit["rows"]:
        for channel in row["channels"]:
            for chain in channel["chains"].values():
                assert chain["endpoint_gate_green"]
                assert chain["telescoping_error_contains_zero"]
                assert chain["all_hybrid_continuity_errors_contain_zero"]
                assert chain["all_accepted_local_gap_certificates_green"]
                assert chain["certified_endpoint_to_reference_upper"] < 1.01


def test_boundary_and_smoke() -> None:
    audit = load("stopped_hybrid_clock_audit.json")
    boundary = audit["theorem_boundary"]
    assert boundary["stopped_hybrid_budget_theorem"]
    assert boundary["gap_certificate_and_endpoint_debit_clock_composed"]
    assert boundary["all_frozen_threshold_endpoint_gates_certified"]
    assert not boundary["hybrid_replay_removed"]
    assert not boundary["uniform_gap_aware_quotient_law_proved"]
    assert not boundary["uniform_stage_A_closed"]
    assert not boundary["riemann_hypothesis"]
    smoke = load("stopped_hybrid_clock_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["all_threshold_chain_count"] == 6
