from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_ten_layer_audit() -> None:
    audit = load("ten_layer_review_audit.json")
    summary = audit["audit_summary"]
    assert summary["layer_count"] == 10
    assert summary["upstream_archive_count"] == 9
    assert (summary["constructive_layer_count"], summary["negative_layer_count"], summary["synthesis_layer_count"]) == (6, 2, 2)
    assert summary["theorem_check_failure_count"] == 0
    assert summary["closed_route_count"] == 4
    assert summary["frontier_packet_count"] == 3
    assert summary["proved_frontier_packet_count"] == 0
    assert not summary["eventual_support_reachable"]
    assert summary["finite_archive_support_reachable"]
    assert summary["each_physical_packet_individually_completes_conditional_graph"]
    assert summary["finite_actual_support_count"] == summary["finite_adaptive_support_count"] == 322


def test_frontier_and_overclaim_guard() -> None:
    audit = load("ten_layer_review_audit.json")
    mathematical = audit["proof_graph"]["mathematical_minimal_missing_sets"]
    assert mathematical == [
        ["direct_margin_packet"],
        ["directional_rayleigh_packet"],
        ["trace_concentration_packet"],
    ]
    assert all(len(values) == 2 and "all_level_outward_admissibility" in values for values in audit["proof_graph"]["validated_minimal_missing_sets"])
    boundary = audit["theorem_boundary"]
    assert boundary["ten_layer_factor_ledger_verified"]
    assert boundary["proof_frontier_antichain_identified"]
    assert boundary["finite_archive_support_complete"]
    assert not boundary["eventual_fourth_mode_support_proved"]
    assert not boundary["hilbert_polya_operator"]
    assert not boundary["zeta_zero_identification"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("ten_layer_review_smoke.json")
    assert smoke["audit_summary"]["layer_count"] == 3
    assert smoke["audit_summary"]["theorem_check_failure_count"] == 0
