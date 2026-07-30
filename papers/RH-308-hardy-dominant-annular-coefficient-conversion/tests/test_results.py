import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["hinfinity_improved_by_hardy_embedding"] is True
    assert data["hinfinity_unit_ball_square_root_gap_order_sharp"] is True
    assert data["actual_norm_decay_proved"] is False
    assert [row["rudin_shapiro_length"] for row in data["rows"]] == [8, 64, 512]
    assert not any(data["gates"].values())
