import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_conditioning_audit():
    payload = json.loads((ROOT / "results/oblique_conditioning_audit.json").read_text())
    assert payload["window_count"] == 126
    assert payload["raw_two_sided_0_10_count"] > 0
    assert payload["conditioned_contraction_success_count"] == 0
