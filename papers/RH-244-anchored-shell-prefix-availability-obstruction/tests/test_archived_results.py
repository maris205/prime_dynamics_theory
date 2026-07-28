import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_anchored_scan_is_scoped_negative():
    payload = json.loads((ROOT / "results/anchored_prefix_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["anchored_selection_pass_count"] == 0
    assert payload["anchored_selection_failure_count"] == 32
    assert payload["all_archived_endpoints_fail"] is True
    assert payload["minimum_best_anchored_jet_distance"] > 0.39
    assert payload["minimum_best_distance_over_tolerance"] > 10.0
    boundary = payload["theorem_boundary"]
    assert boundary["alternative_cloud_classes_excluded"] is False
    assert boundary["uniform_all_order_trace_envelope"] is False
    assert boundary["gate_A"] is False
