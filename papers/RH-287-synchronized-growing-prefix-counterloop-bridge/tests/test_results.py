import json
from pathlib import Path


def test_result_keeps_weighted_leaf_open():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["growing_prefix_exists"] is True
    assert data["explicit_noise_rate"] is False
    assert data["weighted_radius_prefix_proved"] is False
    assert data["gate_A"] is False
