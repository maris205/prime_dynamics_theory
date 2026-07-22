from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("projector_propagation_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_projector_bounds_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["production_omission_count"] == 38
    assert summary["production_unit_tail_roundoff_count"] == 38
    assert summary["production_maximum_tail_amplification_upper"] < 1.0 + 1e-12
    assert summary["production_maximum_projector_secant_multiplier"] > 8.8
    assert summary["production_all_gap_distance_bounds_green"]
    assert summary["production_all_endpoint_lipschitz_bounds_green"]
    assert summary["production_all_conditional_envelopes_green"]
    assert summary["counterexample_tail_amplification_lower"] > 44.0


def test_counterexample() -> None:
    counter = load("projector_propagation_audit.json")["counterexample"]
    assert counter["unit_tail_propagation_rejected"]
    assert counter["g1_trace"] == 1.0
    assert counter["g2_trace"] == 1.0
    assert counter["g1_minimum_eigenvalue"] > 0.0
    assert counter["g2_minimum_eigenvalue"] > 0.0
    assert counter["endpoint_tail_lipschitz_green"]


def test_boundary() -> None:
    boundary = load("projector_propagation_audit.json")["theorem_boundary"]
    assert boundary["endpoint_tail_projector_lipschitz_theorem"]
    assert boundary["local_gap_loss_to_projector_theorem"]
    assert boundary["conditional_projector_block_envelope"]
    assert not boundary["universal_unit_tail_propagation"]
    assert not boundary["uniform_refresh_projector_lipschitz_constant_proved"]
    assert not boundary["repeated_block_contraction_proved"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("projector_propagation_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["production_omission_count"] == 19
