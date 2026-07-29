import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_extended_anchor_atlas():
    payload = json.loads((ROOT / "results/extended_anchor_atlas.json").read_text())
    assert payload["minimum_order"] == 2
    assert payload["maximum_order"] == 28
    assert payload["new_order_count"] == 16
    assert payload["physical_fixed_point_count_at_order_28"] == 32767
    assert payload["order_13_to_28_unit_disk_log_norm"] < 0.0025
    assert payload["theorem_boundary"]["orders_13_to_28_finite_atlas"] is True
    assert payload["theorem_boundary"]["finite_root_rate_is_all_order_theorem"] is False
    assert payload["theorem_boundary"]["gate_A"] is False
