import json
from pathlib import Path


def test_result_boundary():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["all_fixed_derivative_orders_proved"] is True
    assert data["finite_head_bridge"] is False
    assert data["power_gain"] > 0.0
    assert data["gate_A"] is False
