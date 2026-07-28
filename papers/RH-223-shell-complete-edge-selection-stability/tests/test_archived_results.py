import json
from pathlib import Path


def test_archived_shell_stability():
    payload = json.loads((Path(__file__).parents[1] / "results/shell_stability_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["naive_split_pair_count"] > 0
    assert payload["maximum_shell_completion_overshoot"] == 1
    assert payload["minimum_reference_radial_gap"] > 0.0
    assert payload["all_margin_prefixes_recover_reference"]
    assert not payload["theorem_boundary"]["canonical_rank_schedule"]
