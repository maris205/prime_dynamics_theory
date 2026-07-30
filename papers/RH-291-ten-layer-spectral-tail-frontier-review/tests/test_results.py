import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["paper_numbers"] == list(range(282, 292))
    assert data["rh279_projection_free_tail_activated"] is True
    assert data["physical_riesz_quotient_activated"] is False
    assert data["weighted_prefix_leaf"] is False
    assert data["direct_weighted_complement_anchor_prefix"] is False
    assert data["weighted_full_trace_counterloop_anchor"] is False
    assert data["weighted_head_counterloop"] is False
    assert data["complete_count"] == 0
    assert not any(data["gates"].values())
    assert data["hilbert_polya_constructed"] is False
    assert data["riemann_hypothesis_proved"] is False
