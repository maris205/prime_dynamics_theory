import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["paper_numbers"] == list(range(292, 302))
    assert data["tail_absorbed_clock_shortening"] is True
    assert data["natural_clock_minimal_alias_count"] == 1
    assert data["natural_clock_slope_four_alias_count"] == 2
    assert data["direct_weighted_prefix_leaf"] is False
    assert data["determinant_gluing_activated"] is False
    assert data["complete_count"] == 0
    assert not any(data["gates"].values())
    assert data["hilbert_polya_constructed"] is False
    assert data["riemann_hypothesis_proved"] is False
