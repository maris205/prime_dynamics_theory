import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_boundary_audit():
    payload = json.loads((ROOT / "results/boundary_audit.json").read_text())
    assert payload["random_identity_case_count"] == 600
    assert payload["maximum_random_discriminant_relative_error"] < 1e-12
    assert payload["maximum_uniform_bound_violation"] == 0.0
    assert payload["theorem_boundary"]["degeneracy_strata_exact"]
    assert not payload["theorem_boundary"]["u_converges_to_one"]
