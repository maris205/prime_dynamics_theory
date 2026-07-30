import json
from pathlib import Path


def test_result_keeps_branches_separate():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["spectral_score"] == 4
    assert data["counterloop_score"] == 4
    assert data["coordinatewise_union"] == [True] * 5
    assert data["coordinatewise_union_legal"] is False
    assert data["cross_branch_weighted_glue"] is False
    assert data["direct_weighted_complement_anchor_prefix"] is False
    assert data["weighted_full_trace_counterloop_anchor"] is False
    assert data["weighted_head_counterloop"] is False
    assert data["complete_count"] == 0
    assert not any(data[f"gate_{letter}"] for letter in "ABCDE")
