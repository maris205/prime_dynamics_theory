import json
from pathlib import Path


def test_archived_resolved_tail_control():
    payload = json.loads((Path(__file__).parents[1] / "results/resolved_tail_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["minimum_resolved_omitted_root_count"] > 0
    assert payload["maximum_q_on_unit_disk"] < 1.0
    assert payload["minimum_bound_slack"] >= -1e-12
    assert payload["theorem_boundary"]["resolved_omitted_shells_controlled_on_unit_disk"]
    assert not payload["theorem_boundary"]["unresolved_operator_tail_controlled"]
