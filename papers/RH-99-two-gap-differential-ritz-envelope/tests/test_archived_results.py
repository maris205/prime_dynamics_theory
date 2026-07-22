from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str): return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("two_gap_differential_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_available_two_gap_probe_bounds_green"]
    assert not audit["all_executed_two_gap_certificates_available"]
    summary = audit["audit_summary"]
    assert summary["update_count"] == 120
    assert summary["probe_count"] == 720
    assert summary["differential_certificate_available_count"] == 115
    assert summary["differential_certificate_unavailable_count"] == 5
    assert summary["ritz_gap_nonpositive_count"] == 5
    assert summary["cross_gap_nonpositive_count"] == 0
    assert summary["probe_green_update_count"] == 115
    assert summary["quotient_update_count"] == 5
    assert summary["quotient_inside_linearized_radius_count"] == 0
    assert summary["maximum_two_gap_derivative_bound"] > 1e40
    assert summary["maximum_full_to_adaptive_bound_ratio_on_quotients"] > 1e9


def test_boundary() -> None:
    boundary = load("two_gap_differential_audit.json")["theorem_boundary"]
    assert boundary["cross_covariance_derivative_formula"]
    assert boundary["spectral_projector_sylvester_bound"]
    assert boundary["two_gap_refresh_derivative_theorem"]
    assert boundary["finite_tangent_probe_bounds_validated_where_available"]
    assert not boundary["all_frozen_output_ritz_gaps_certified"]
    assert not boundary["finite_neighborhood_lipschitz_tube_proved"]
    assert not boundary["replay_free_block_envelope_proved"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("two_gap_differential_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["update_count"] == 8
