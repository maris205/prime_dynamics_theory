import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_edge_quartet_audit():
    payload = json.loads((ROOT / "results/edge_quartet_audit.json").read_text())
    assert payload["physical_case_count"] == 6
    assert payload["physical_quartet_conjugate_closed_count"] == 6
    assert payload["physical_quartet_all_nonreal_count"] == 6
    assert payload["physical_quartet_all_visible_count"] == 6
    assert payload["minimum_radial_gap_after_quartet"] > 0.05
