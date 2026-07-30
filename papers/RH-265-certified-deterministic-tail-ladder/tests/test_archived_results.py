import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_archived_tail_ladder():
    payload = json.loads((ROOT / "results/tail_ladder.json").read_text())
    assert payload["orders"] == [13, 21, 29, 37, 45, 53, 61]
    assert payload["order_29_is_current_anchor_aligned"] is True
    assert payload["higher_orders_are_conditional_interfaces"] is True
    assert payload["monotone_total_tail_in_200_dps_replay"] is True
    assert all(
        payload["theorem_boundary"][f"gate_{letter}"] is False
        for letter in "ABCDE"
    )
