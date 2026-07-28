import json
from pathlib import Path


def test_archived_divisor_obstruction():
    payload = json.loads((Path(__file__).parents[1] / "results/divisor_obstruction_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["minimum_tightness_count_slack"] >= 0
    assert payload["all_normalized_roots_inside_certificate_disk"]
    assert payload["all_raw_roots_inside_unit_disk"]
    assert payload["theorem_boundary"]["direct_normalized_cloud_route_rejected"]
    assert not payload["theorem_boundary"]["reciprocal_fredholm_divisor_rejected"]
