import json
from pathlib import Path


def test_result_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["rate_free_weighted_full_trace_bridge"] is True
    assert data["minimal_logarithmic_clock_reached"] is False
    assert data["weighted_head_transport_proved"] is False
    assert data["determinant_gluing_activated"] is False
    assert not any(data["gates"].values())
