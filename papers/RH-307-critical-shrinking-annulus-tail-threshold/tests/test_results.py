import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["mass_and_cap_information_class_threshold_proved"] is True
    assert data["repeated_q_model_saturation_proved"] is True
    assert data["actual_moving_head_control_proved"] is False
    assert all(row["radius_is_certified"] for row in data["rows"])
    assert not any(data["gates"].values())
