import json
from pathlib import Path


def test_gate_and_completion_boundary():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["complete_certificate_count"] == 0
    assert all(value is False for value in data["macro_gates"].values())
    assert data["small_noise_uniform_quotient"] is False
