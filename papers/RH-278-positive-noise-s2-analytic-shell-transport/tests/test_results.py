import json
from pathlib import Path


def test_local_not_zero_noise():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["positive_noise_local_package"] is True
    assert data["zero_noise_uniform_package"] is False
    assert data["gate_A"] is False
