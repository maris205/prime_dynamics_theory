import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_orientation_archive():
    payload = json.loads((ROOT / "results/orientation_mark_audit.json").read_text())
    assert payload["stability_case_count"] == 120
    assert abs(payload["minimum_exact_orientation_gap"] - 1.0) < 1e-12
    assert payload["maximum_ordinary_trace_difference"] < 1e-12
    assert payload["stability_failure_count"] == 0
