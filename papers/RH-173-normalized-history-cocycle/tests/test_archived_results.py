import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_cocycle_audit():
    payload = json.loads((ROOT / "results/cocycle_identity_audit.json").read_text())
    assert payload["case_count"] == 160
    assert max(payload["maximum_residuals"].values()) < 1e-12
    assert payload["orthogonal_reset_counterexample_distance"] > 0.999999
