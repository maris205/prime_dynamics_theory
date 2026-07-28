import json
from pathlib import Path


def test_archived_cloud_atlas():
    payload = json.loads((Path(__file__).parents[1] / "results/cloud_atlas.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["minimum_actual_rank"] >= 4
    assert payload["maximum_actual_rank"] >= 34
    assert payload["maximum_conjugacy_error"] < 1e-7
    assert all(payload["strict_rank_growth_by_channel"].values())
    assert payload["theorem_boundary"]["finite_sixteen_scale_rank_growth_audited"]
    assert not payload["theorem_boundary"]["canonical_rank_schedule"]
