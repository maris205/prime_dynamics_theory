import json
from pathlib import Path


def test_scope_flags():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["single_fixed_rank_contour_compatible"] is False
    assert data["rank_growing_selector_excluded"] is False
    assert data["gate_A"] is False
