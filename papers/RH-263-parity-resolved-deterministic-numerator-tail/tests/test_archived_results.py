import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_archived_parity_audit():
    payload = json.loads((ROOT / "results/parity_anchor_audit.json").read_text())
    assert payload["orders_cross_checked"] == 27
    assert payload["odd_orders_cross_checked"] == 13
    assert payload["even_orders_cross_checked"] == 14
    assert payload["maximum_absolute_cross_check_residual"] < 1.0e-12
    assert payload["theorem_boundary"]["all_order_deterministic_parity_dictionary"]
    assert payload["theorem_boundary"]["cloud_coefficient_bridge"] is False
    assert all(
        payload["theorem_boundary"][f"gate_{letter}"] is False
        for letter in "ABCDE"
    )
