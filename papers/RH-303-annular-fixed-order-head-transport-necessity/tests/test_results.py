import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["fixed_order_head_transport_necessity_proved"] is True
    assert data["annular_route_bypasses_head_moments"] is False
    assert data["actual_head_transport"] is False
    assert not any(data["gates"].values())
