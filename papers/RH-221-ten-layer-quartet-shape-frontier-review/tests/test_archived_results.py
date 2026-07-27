import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_shape_frontier_review():
    payload = json.loads((ROOT / "results/shape_frontier_review.json").read_text())
    assert payload["route_coordinate"] == "finite_gauge_complete_shape_flow_open_rank_growing_divisor"
    assert payload["aggregate_finite_ledger_item_count"] == 2140
    assert payload["aggregate_identity_failure_count"] == 0
    assert not any(payload["strict_gate_vector"].values())
    assert len(payload["paper_rows"]) == 9
