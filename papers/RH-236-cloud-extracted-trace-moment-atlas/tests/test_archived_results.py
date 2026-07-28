import json
from pathlib import Path


def test_archived_trace_moment_atlas():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/trace_moment_atlas.json").read_text()
    )
    assert payload["endpoint_count"] == 32
    assert payload["trace_case_count"] == 384
    assert payload["maximum_order"] == 12
    assert payload["maximum_fine_unit_disk_log_jet_norm"] < 0.02
    assert payload["maximum_observed_root_rate_orders_2_to_12"] < 0.5
    assert not payload["theorem_boundary"]["uniform_all_order_trace_envelope"]
