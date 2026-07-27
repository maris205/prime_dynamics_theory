import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_source_cyclic_audit():
    payload = json.loads((ROOT / "results/source_cyclic_identity_audit.json").read_text())
    assert payload["case_count"] == 140
    assert payload["failure_count"] == 0
    assert payload["maximum_relative_moment_error"] < 1e-8
