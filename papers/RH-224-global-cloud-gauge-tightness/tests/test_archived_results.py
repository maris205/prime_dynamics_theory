import json
from pathlib import Path


def test_archived_tightness_certificate():
    payload = json.loads((Path(__file__).parents[1] / "results/tightness_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["maximum_mean_modulus"] < 1e-12
    assert payload["maximum_second_moment_error"] < 1e-12
    assert payload["minimum_tail_bound_slack"] >= -1e-12
    assert payload["theorem_boundary"]["uniform_empirical_tightness"]
    assert not payload["theorem_boundary"]["unique_weak_limit"]
