from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("exterior_fourth_support_audit.json")
    summary = audit["audit_summary"]
    assert len(audit["rows"]) == 5
    assert summary["channel_count"] == 10
    assert summary["update_count"] == 360
    assert summary["fine_update_count"] == 234
    assert summary["spectral_certificate_implication_violation_count"] == 0
    assert summary["trace_certificate_implication_violation_count"] == 0
    assert summary["volume_ordering_violation_count"] == 0
    assert summary["observed_cross_error_bound_failure_count"] == 0
    assert audit["threshold_summary"]["1e-08"]["fine_spectral_certificate_green"]
    assert not audit["threshold_summary"]["1e-06"]["fine_spectral_certificate_green"]
    assert not audit["threshold_summary"]["1e-04"]["fine_spectral_certificate_green"]


def test_barrier_and_claim_boundary() -> None:
    audit = load("exterior_fourth_support_audit.json")
    barrier = audit["barrier"]
    assert barrier["all_trace_clocks_constant"]
    assert barrier["all_diagonal_blocks_constant"]
    assert barrier["maximum_volume_formula_error"] < 1e-13
    assert barrier["maximum_endpoint_ratio_error"] < 1e-13
    boundary = audit["theorem_boundary"]
    assert boundary["finite_memory_spectral_exterior_certificate"]
    assert boundary["finite_memory_trace_exterior_certificate"]
    assert boundary["sharp_scalar_volume_interval"]
    assert boundary["reduced_moment_spectral_trace_distinction"]
    assert not boundary["all_level_physical_exterior_lower_bound_proved"]
    assert not boundary["uniform_stage_A_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("exterior_fourth_support_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["update_count"] == 24
