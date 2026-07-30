import json
from pathlib import Path


def test_result_boundary():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["uniform_error_class_threshold_sharp"] is True
    assert data["actual_noisy_uniform_rate_proved"] is False
    assert data["direct_weighted_prefix_proved"] is False
    assert not any(data["gates"].values())
