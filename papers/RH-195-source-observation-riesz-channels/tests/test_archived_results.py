import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_channel_audit():
    payload = json.loads((ROOT / "results/riesz_channel_identity_audit.json").read_text())
    assert payload["case_count"] == 160
    assert payload["failure_count"] == 0
    assert max(payload["maxima"].values()) < 1e-9
