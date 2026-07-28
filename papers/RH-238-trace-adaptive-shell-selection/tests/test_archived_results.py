import json
from pathlib import Path


def test_archived_adaptive_selection():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/adaptive_shell_selection.json").read_text()
    )
    assert payload["endpoint_count"] == 32
    assert payload["selection_pass_count"] == 32
    assert payload["minimum_adaptive_rank"] >= 4
    assert payload["maximum_adaptive_rank"] < 40
    assert payload["minimum_tolerance_slack"] >= -1e-12
    assert not payload["theorem_boundary"]["all_order_trace_control"]
