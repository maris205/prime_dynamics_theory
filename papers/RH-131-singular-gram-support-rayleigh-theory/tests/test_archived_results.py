import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit():
    data = load("support_rayleigh_audit.json")
    summary = data["audit_summary"]
    assert summary["compatible_sample_count"] == 4096
    assert summary["kernel_leakage_sample_count"] == 1024
    assert summary["compatible_failure_count"] == 0
    assert summary["leakage_detection_failure_count"] == 0
    assert summary["outward_failure_count"] == 0
    assert summary["rh130_zero_tail_state_count"] == 54
    assert summary["rh130_full_tail_state_count"] == 66
    assert summary["rh130_rank_creation_pair_count"] == 24
    assert data["rh130_application"]["rank_creation_matches_infinite_factors"]


def test_boundary_and_smoke():
    data = load("support_rayleigh_audit.json")
    assert data["theorem_boundary"]["sharp_supported_pseudovolume_bound"]
    assert not data["theorem_boundary"]["physical_all_level_support_projector_proved"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    assert load("support_rayleigh_smoke.json")["audit_summary"]["compatible_sample_count"] == 128
