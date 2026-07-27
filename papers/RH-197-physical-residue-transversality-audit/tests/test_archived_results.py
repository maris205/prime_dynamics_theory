import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_physical_transversality():
    payload = json.loads((ROOT / "results/physical_transversality_audit.json").read_text())
    assert payload["unique_mode_count"] == 8
    assert payload["accepted_window_count"] == 12
    assert payload["minimum_physical_residue_modulus"] > 0.01
    assert payload["maximum_canonical_optimal_norm_product"] < 1000.0
    assert payload["latest_maximum_relative_condition_difference"] < 0.02
