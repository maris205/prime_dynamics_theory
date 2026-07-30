import json
from pathlib import Path


def test_result_scoped_sharpness():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["sharp_for_mass_cap_class"] is True
    assert data["physical_saturation_claimed"] is False
    assert data["gate_A"] is False
