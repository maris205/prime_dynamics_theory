from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_scale_law_audit() -> None:
    audit = load("scale_law_audit.json")
    summary = audit["audit_summary"]
    assert (summary["scale_count"], summary["physical_record_count"]) == (5, 120)
    assert summary["alignment_failure_count"] == 0
    assert summary["continuation_anchor_failure_count"] == 0
    assert summary["maximum_observed_certifying_depth"] == 6
    assert summary["maximum_fit_residual_factor"] > 100.0
    assert summary["maximum_leave_one_out_exponent_span"] > 4.0


def test_bounded_barrier_and_boundary() -> None:
    audit = load("scale_law_audit.json")
    barrier = audit["continuation_barrier"]
    assert barrier["all_anchor_errors_below_tolerance"]
    assert barrier["preserved_range"] == [0.0, 1.0]
    probes = barrier["examples"]
    assert probes["vanishing"]["probe_value"] < 2e-6
    assert probes["interior_limit"]["probe_value"] == 0.5
    assert probes["unit_limit"]["probe_value"] > 0.99999
    boundary = audit["theorem_boundary"]
    assert boundary["finite_anchor_asymptotic_nonidentifiability"]
    assert boundary["bounded_interval_anchor_extension"]
    assert not boundary["descriptive_fit_is_asymptotic_law"]
    assert not boundary["uniform_stage_A_closed"]


def test_smoke_exists() -> None:
    smoke = load("scale_law_smoke.json")
    assert smoke["audit_summary"]["scale_count"] == 3
    assert smoke["audit_summary"]["physical_record_count"] == 42
