import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_full_audit_boundary():
    payload = json.loads((ROOT / "results/temporal_clock_audit.json").read_text())
    assert payload["status"] == "rh182_finite_temporal_clock_physical_audit"
    assert payload["window_count"] == 126
    assert payload["formula_failure_count"] == 0
    assert payload["three_gate_success_count"] == 0
