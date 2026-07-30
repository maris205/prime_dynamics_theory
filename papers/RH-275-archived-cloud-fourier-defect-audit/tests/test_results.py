import json
from pathlib import Path


def test_scope_flags():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["row_count"] == 7
    assert data["asymptotic_nonconvergence_proved"] is False
    assert data["upstream_interval_certified"] is False
    assert data["gate_A"] is False
