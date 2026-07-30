import json
from pathlib import Path


def test_result_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["aliases_below_minimal_bridge"] == 1
    assert data["aliases_below_slope_four"] == 2
    assert data["natural_rank_equals_noisy_head_proved"] is False
    assert data["typed_errors_diverge_proved"] is False
    assert not any(data["gates"].values())
