import json
from pathlib import Path


def test_result_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["finite_prefix_identifies_cloud"] is False
    assert data["weighted_or_contour_routes_excluded"] is False
    assert data["scoped_negative_result"] is True
    assert data["gate_A"] is False
