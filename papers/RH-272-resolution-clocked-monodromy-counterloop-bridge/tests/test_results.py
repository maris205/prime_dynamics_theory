import json
from pathlib import Path


def test_result_boundary():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["spectral_cloud_identification"] is False
    assert data["gate_A"] is False
    assert data["gates_B_to_E"] is False
