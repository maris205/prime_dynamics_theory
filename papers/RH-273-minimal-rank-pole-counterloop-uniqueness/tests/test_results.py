import json
from pathlib import Path


def test_boundary_flag():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["noisy_spectral_identification"] is False
    assert data["gate_A"] is False
