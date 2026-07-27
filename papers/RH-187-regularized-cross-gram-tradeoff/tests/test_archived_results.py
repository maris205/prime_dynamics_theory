import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_regularization_audit():
    payload = json.loads((ROOT / "results/regularization_audit.json").read_text())
    assert payload["window_count"] == 126
    assert payload["sweep_case_count"] == 1638
    assert payload["strict_regularized_contraction_count"] == 0
