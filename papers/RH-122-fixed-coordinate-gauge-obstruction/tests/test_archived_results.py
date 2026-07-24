import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text())


def test_audit() -> None:
    summary = load("fixed_coordinate_audit.json")["audit_summary"]
    assert summary["sample_count"] == 512
    assert summary["formula_failure_count"] == 0
    assert summary["gamma_invariance_failure_count"] == 0
    assert summary["gauged_recovery_failure_count"] == 0
    assert abs(summary["log_log_slope"] + 1.0) < 1e-12


def test_smoke_boundary() -> None:
    assert load("fixed_coordinate_smoke.json")["audit_summary"]["sample_count"] == 64
    boundary = load("fixed_coordinate_audit.json")["theorem_boundary"]
    assert boundary["fixed_coordinate_unboundedness"]
    assert boundary["exact_gauge_removes_obstruction"]
    assert not boundary["uniform_physical_gauge_proved"]

