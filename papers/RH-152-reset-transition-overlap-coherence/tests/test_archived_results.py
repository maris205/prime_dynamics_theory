import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_audit() -> None:
    summary = json.loads((ROOT / "results/overlap_audit.json").read_text())["audit_summary"]
    assert summary["transition_count"] == 120
    assert summary["invertible_transition_count"] == 120
    assert summary["minimum_robust_overlap_lower"] > 8e-5
    assert summary["maximum_inverse_overlap_upper"] < 1.2e4
    assert summary["polar_stability_failure_count"] == 0
    assert summary["below_1e_3_count"] == 2


def test_boundary() -> None:
    boundary = json.loads((ROOT / "results/overlap_audit.json").read_text())["theorem_boundary"]
    assert boundary["all_frozen_reset_transitions_invertible"]
    assert not boundary["uniform_overlap_lower"]
    assert not boundary["outward_assembly_closed"]
