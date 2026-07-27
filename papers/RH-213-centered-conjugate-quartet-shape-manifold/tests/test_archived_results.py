import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_shape_manifold():
    payload = json.loads((ROOT / "results/shape_manifold_audit.json").read_text())
    assert payload["finite_endpoint_count"] == 32
    assert payload["random_identity_case_count"] == 400
    assert payload["maximum_endpoint_manifold_residual"] < 1e-12
    assert payload["maximum_random_coefficient_error"] < 1e-12
    assert payload["theorem_boundary"]["shape_parameterization_exact"]
