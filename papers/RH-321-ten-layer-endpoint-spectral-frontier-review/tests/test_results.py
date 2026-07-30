import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["paper_numbers"] == list(range(312, 322))
    assert data["actual_endpoint_h2_convergence_proved"] is False
    assert data["complete_count"] == 0
    assert data["hilbert_polya_constructed"] is False
    assert data["riemann_zeros_identified"] is False
    assert data["riemann_hypothesis_proved"] is False
    assert data["reopening_trigger_supplied"] is False
    assert data["scoped_spectral_route_stop"] is True
    assert not any(data["gates"].values())
