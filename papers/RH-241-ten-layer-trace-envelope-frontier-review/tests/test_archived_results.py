import json
from pathlib import Path


def test_archived_trace_envelope_review():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/trace_envelope_frontier_review.json").read_text()
    )
    assert payload["paper_numbers"] == list(range(232, 241))
    assert payload["identity_failure_count"] == 0
    assert payload["route_coordinate"] == "projection_free_relative_det2_open_uniform_trace_envelope"
    assert not payload["theorem_boundary"]["uniform_all_order_trace_envelope"]
    assert not any(payload["macro_gates"].values())
