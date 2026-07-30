import json
from pathlib import Path


def test_scoped_boundary():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["actual_cloud_nonbridge_proved"] is False
    assert data["gate_A"] is False
