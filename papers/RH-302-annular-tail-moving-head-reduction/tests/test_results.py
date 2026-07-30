import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["slope_four_annular_tail_proved"] is True
    assert data["full_norm_equivalent_to_moving_head"] is True
    assert data["actual_annular_convergence"] is False
    assert not any(data["gates"].values())
