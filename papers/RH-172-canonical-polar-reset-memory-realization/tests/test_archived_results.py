import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_polar_audit():
    payload = json.loads((ROOT / "results/polar_identity_audit.json").read_text())
    assert payload["case_count"] == 192
    assert max(payload["maximum_residuals"].values()) < 2e-12
    assert not payload["theorem_boundary"]["physical_transfer_space_identification"]
