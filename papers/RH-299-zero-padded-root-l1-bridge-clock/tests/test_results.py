import json
from pathlib import Path


def test_result_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["zero_padded_transport_proved"] is True
    assert data["sharp_rate_law_proved"] is True
    assert data["actual_modulus_head_matching_proved"] is False
    assert data["weighted_head_budget_activated"] is False
    assert not any(data["gates"].values())
