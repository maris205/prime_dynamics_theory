import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_channel_determinant_audit():
    payload = json.loads((ROOT / "results/channel_determinant_audit.json").read_text())
    assert payload["identity_case_count"] == 240
    assert payload["identity_failure_count"] == 0
    assert payload["latest_maximum_relative_determinant_error"] < 1e-4
    assert payload["latest_maximum_relative_trace_power_error"] < 8e-4
