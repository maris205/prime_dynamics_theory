import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["taylor_projection_exactly_optimal"] is True
    assert data["inverse_square_root_rate_proved"] is True
    assert data["spectral_realization_rate_proved"] is False
    assert not any(data["gates"].values())
