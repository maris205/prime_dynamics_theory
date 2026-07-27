import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_gauge_reconstruction():
    payload = json.loads((ROOT / "results/gauge_reconstruction_audit.json").read_text())
    assert payload["route_coordinate"] == "finite_gauge_complete_shape_flow_open_rank_growing_divisor"
    assert payload["maximum_coefficient_reconstruction_error"] < 1e-12
    assert payload["maximum_root_reconstruction_error"] < 1e-12
    assert payload["gauge_dominant_transition_count"] + payload["shape_dominant_transition_count"] == 30
    assert not payload["theorem_boundary"]["rank_growing_divisor_constructed"]
