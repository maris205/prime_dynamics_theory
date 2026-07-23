from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("observation_residual_audit.json")
    summary = audit["audit_summary"]
    assert len(audit["rows"]) == 5
    assert summary["channel_count"] == 10
    assert summary["maximum_clock_rank"] == 7
    assert summary["maximum_observation_factor"] < 21.26
    assert summary["maximum_sqrt_sigma_observation_factor"] < 2.13
    assert summary["maximum_residual_over_sqrt_sigma"] < 3.08e-9
    assert summary["maximum_weighted_residual"] < 5.05e-9
    assert summary["all_weighted_residuals_below_1e_minus_8"]
    assert summary["maximum_recomposition_discrepancy"] < 1.0e-12
    assert summary["sharp_barrier_weighted_growth_power"] == 0.25


def test_scenarios_boundary_and_smoke() -> None:
    audit = load("observation_residual_audit.json")
    scenarios = {item["name"]: item for item in audit["scenarios"]}
    assert scenarios["matched_square_root"]["zero_power"]
    assert scenarios["strict_overcancellation"]["zero_power"]
    assert not scenarios["undercancellation"]["zero_power"]
    boundary = audit["theorem_boundary"]
    assert boundary["signed_observation_residual_cancellation_theorem"]
    assert boundary["sharp_rate_matching_boundary"]
    assert not boundary["uniform_observation_residual_law_closed"]
    assert not boundary["riemann_hypothesis"]
    smoke = load("observation_residual_smoke.json")
    assert len(smoke["rows"]) == 1
