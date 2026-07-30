import json
from pathlib import Path


def test_reaudit_and_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["row_count"] == 7
    assert data["all_rows_root_error_improved"] is True
    assert data["multiplier_constant_interval_certified"] is False
    assert data["aggregate_cloud_transport_proved"] is False
    assert data["gate_A"] is False
