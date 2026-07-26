import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_double_cycle_archive():
    payload = json.loads((ROOT / "results/double_cycle_audit.json").read_text())
    assert payload["determinant_case_count"] == 192
    assert payload["maximum_relative_determinant_error"] < 1e-12
    assert payload["maximum_absolute_trace_error"] < 1e-10
    assert not payload["theorem_boundary"]["actual_noisy_cloud_identification"]
