from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("uniform_quotient_audit.json")
    summary = audit["audit_summary"]
    assert len(audit["thresholds"]) == 3
    assert summary["candidate_count"] == 38
    assert summary["accepted_count"] == 35
    assert summary["rejected_count"] == 3
    assert summary["all_local_gap_certificates_green"]
    assert summary["primary_all_candidates_fit_stopped_budget"]
    assert summary["maximum_stopped_endpoint_ratio"] < 1.007
    assert summary["maximum_unrestricted_endpoint_ratio"] > 1.024
    assert summary["maximum_replay_multiplier"] < 1.0
    assert summary["ratio_collapse_good_price_power"] == 1.5
    assert summary["ratio_collapse_bad_price_power"] == 0.0


def test_boundary_scenarios_and_smoke() -> None:
    audit = load("uniform_quotient_audit.json")
    scenarios = {item["name"]: item for item in audit["scenarios"]}
    assert scenarios["gap_collapses_but_price_decays"]["zero_power"]
    assert scenarios["gap_collapses_without_cross_decay"]["zero_power"]
    assert scenarios["propagation_consumes_margin"]["price_growth_power"] > 0.0
    boundary = audit["theorem_boundary"]
    assert boundary["uniform_all_candidates_fit_law"]
    assert boundary["stopped_sparse_supply_safety_law"]
    assert boundary["ratio_not_gap_principle"]
    assert not boundary["uniform_gap_aware_physical_supply_proved"]
    assert not boundary["riemann_hypothesis"]
    smoke = load("uniform_quotient_smoke.json")
    assert len(smoke["thresholds"]) == 3
