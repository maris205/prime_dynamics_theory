import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_transverse_audit():
    payload = json.loads((ROOT / "results/transverse_quenching_audit.json").read_text())
    assert payload["random_bound_case_count"] == 800
    assert payload["maximum_random_bound_violation"] == 0.0
    assert payload["finest_maximum_transverse_ratio"] < payload["coarsest_mature_maximum_transverse_ratio"]
    assert payload["maximum_telescoping_residual"] < 1e-12
    assert not payload["theorem_boundary"]["one_dimensional_flow_theorem"]
