import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["minimal_rank_theta_law_proved"] is True
    assert data["minimal_squared_mass_theta_law_proved"] is True
    assert data["actual_noisy_rank_law_proved"] is False
    assert data["rows"][-1]["normalized_divisor_feedback"] < 0.01
    assert not any(data["gates"].values())
