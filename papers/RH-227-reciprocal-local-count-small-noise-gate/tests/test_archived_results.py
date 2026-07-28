import json
from pathlib import Path


def test_archived_local_count_gate():
    payload = json.loads((Path(__file__).parents[1] / "results/local_count_gate.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["minimum_finite_contour_clearance"] > 0.0
    assert payload["maximum_first_to_last_count_growth"] > 0
    assert not payload["all_channel_radius_counts_stable_in_frozen_tail"]
    assert not payload["theorem_boundary"]["finite_reciprocal_count_gate_passed"]
    assert not payload["theorem_boundary"]["small_noise_determinant_limit_disproved"]
