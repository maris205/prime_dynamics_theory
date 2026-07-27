import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_feshbach_audit():
    payload = json.loads((ROOT / "results/feshbach_identity_audit.json").read_text())
    assert payload["case_count"] == 240
    assert payload["failure_count"] == 0
