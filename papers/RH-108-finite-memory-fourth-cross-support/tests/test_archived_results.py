from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("fourth_cross_support_audit.json")
    summary = audit["audit_summary"]
    assert len(audit["rows"]) == 5
    assert summary["channel_count"] == 10
    assert summary["update_count"] == 360
    assert summary["fine_update_count"] == 234
    assert summary["minimum_fine_certificate_margin_ratio"] > 7.3
    assert summary["certificate_implication_violation_count"] == 0
    assert summary["selector_equivalence_failure_count"] == 0
    assert summary["observed_cross_error_bound_failure_count"] == 0
    assert all(record["fine_certificate_green"] for record in audit["threshold_summary"].values())


def test_barrier_and_boundary() -> None:
    audit = load("fourth_cross_support_audit.json")
    barrier = audit["barrier"]
    assert barrier["trace_clock_constant"]
    assert barrier["diagonal_blocks_constant"]
    assert barrier["maximum_ratio_formula_error"] < 1e-14
    assert barrier["rows"][-1]["ratio"] == 0.0
    boundary = audit["theorem_boundary"]
    assert boundary["finite_memory_weyl_support_certificate"]
    assert boundary["reduced_first_two_moment_realization"]
    assert boundary["exact_normalized_memory_nondegeneracy_barrier"]
    assert not boundary["all_level_fourth_cross_lower_bound_proved"]
    assert not boundary["uniform_stage_A_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("fourth_cross_support_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["update_count"] == 24
