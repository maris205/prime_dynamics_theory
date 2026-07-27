import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_complement_budget():
    payload = json.loads((ROOT / "results/complement_budget_audit.json").read_text())
    assert payload["window_count"] == 126
    assert payload["norm_only_resolvent_success_count"] == 0
    assert payload["full_norm_only_certificate_count"] == 0
