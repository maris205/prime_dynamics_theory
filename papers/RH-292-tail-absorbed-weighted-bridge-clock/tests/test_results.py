import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["clock_shortening_proved"] is True
    assert data["critical_tail_absorption_proved"] is True
    assert data["direct_weighted_prefix_proved"] is False
    assert data["weighted_full_trace_bridge_proved"] is False
    assert data["weighted_head_transport_proved"] is False
    assert not any(data["gates"].values())
