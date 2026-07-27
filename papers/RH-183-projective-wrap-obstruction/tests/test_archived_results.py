import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_wrap_audit():
    payload = json.loads((ROOT / "results/wrap_obstruction_audit.json").read_text())
    assert payload["formula_case_count"] == 80
    assert payload["formula_failure_count"] == 0
    assert payload["physical_window_count"] == 126
    assert payload["orthogonal_three_gate_success_count"] == 0
