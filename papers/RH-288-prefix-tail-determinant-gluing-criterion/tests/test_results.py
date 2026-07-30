import json
from pathlib import Path


def test_result_missing_leaf():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["three_budget_theorem"] is True
    assert data["noisy_spectral_tail_leaf"] is True
    assert data["target_tail_leaf"] is True
    assert data["direct_weighted_complement_anchor_prefix_leaf"] is False
    assert data["weighted_full_trace_counterloop_anchor_leaf"] is False
    assert data["weighted_head_counterloop_leaf"] is False
    assert data["criterion_activated"] is False
    assert data["gate_A"] is False
