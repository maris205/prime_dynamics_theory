import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_review():
    payload = json.loads((ROOT / "results/source_channel_review.json").read_text())
    assert payload["layer_count"] == 9
    assert payload["finite_item_count"] == 1352
    assert payload["identity_failure_count"] == 0
    assert payload["matched_root_count"] == 48
    assert payload["route_coordinate"] == "finite_canonical_edge_quartet_open_transport"
    assert not payload["macro_boundary"]["gate_A"]
