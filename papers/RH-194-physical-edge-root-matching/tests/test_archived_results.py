import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_physical_matching():
    payload = json.loads((ROOT / "results/physical_edge_matching.json").read_text())
    assert payload["accepted_window_count"] == 12
    assert payload["root_case_count"] == 48
    assert payload["unique_physical_mode_count"] == 8
    assert payload["base_single_count_contour_count"] == 48
    assert payload["source_observable_root_count"] == 48
    assert payload["maximum_absolute_matching_error"] < 0.0013
