import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_audit_counts() -> None:
    summary = json.loads((ROOT / "results/congruence_audit.json").read_text())["audit_summary"]
    assert summary["transition_count"] == 120
    assert summary["correlated_positive_base_count"] == 120
    assert summary["minimum_correlated_pulled_base_lower"] > 2e-7
    assert summary["independent_positive_definite_count"] == 68
    assert summary["independent_positive_definite_failure_count"] == 52


def test_boundary() -> None:
    boundary = json.loads((ROOT / "results/congruence_audit.json").read_text())["theorem_boundary"]
    assert boundary["all_frozen_correlated_bases_positive"]
    assert not boundary["independent_ball_route_closes"]
    assert not boundary["native_reset_tail_assembly"]
