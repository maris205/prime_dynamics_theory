import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_canonical_packet_audit():
    payload = json.loads((ROOT / "results/canonical_packet_identity_audit.json").read_text())
    assert payload["case_count"] == 140
    assert payload["failure_count"] == 0
    assert max(payload["maxima"].values()) < 1e-8
