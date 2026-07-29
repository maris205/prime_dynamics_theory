import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_unit_cap_obstruction():
    payload = json.loads((ROOT / "results/unit_cap_integer_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["integer_cap"] == 1
    assert payload["integer_selector_pass_count"] == 0
    assert payload["minimum_integer_distance"] > 0.1
    assert payload["maximum_mip_gap"] == 0.0
    assert payload["total_signed_lattice_point_count"] > 1_000_000_000
    assert payload["theorem_boundary"]["unit_cap_signed_integer_class_excluded"] is True
    assert payload["theorem_boundary"]["larger_integer_caps_excluded"] is False
    assert payload["theorem_boundary"]["gate_A"] is False
