import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit():
    data = load("partial_isometry_audit.json")
    summary = data["audit_summary"]
    assert summary["sample_count"] == 4096
    assert summary["equal_rank_procrustes_sample_count"] == 2048
    assert summary["partial_isometry_failure_count"] == 0
    assert summary["procrustes_failure_count"] == 0
    assert summary["forcing_dominance_failure_count"] == 0
    assert summary["unmatched_lower_failure_count"] == 0
    assert summary["rh130_zero_to_zero_count"] == 30
    assert summary["rh130_zero_to_four_count"] == 24
    assert summary["rh130_four_to_four_count"] == 42
    assert summary["rh130_subunit_birth_forcing_count"] == 22


def test_boundary_and_smoke():
    data = load("partial_isometry_audit.json")
    assert data["theorem_boundary"]["minimal_trace_positive_forcing"]
    assert not data["theorem_boundary"]["natural_dynamical_gauge_derived"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    assert load("partial_isometry_smoke.json")["audit_summary"]["sample_count"] == 128
