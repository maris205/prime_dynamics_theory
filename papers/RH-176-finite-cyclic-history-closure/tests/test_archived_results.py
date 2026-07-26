import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cyclic_archive():
    payload = json.loads((ROOT / "results/cyclic_closure_audit.json").read_text())
    assert payload["determinant_case_count"] == 240
    assert payload["maximum_geometric_identity_error"] < 1e-12
    assert payload["maximum_orientation_determinant_error"] < 1e-12
    assert payload["all_wrap_norm_defects_one"]
    assert payload["all_fixed_support_defects_zero"]
