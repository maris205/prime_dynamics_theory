import json
from pathlib import Path


def test_archived_gap_barrier():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/pseudospectral_gap_audit.json").read_text()
    )
    assert payload["endpoint_count"] == 32
    assert payload["maximum_projector_operator_norm"] > 1e12
    assert payload["minimum_gap_to_projector_norm_ratio"] < 1e-12
    assert payload["fixed_gap_model_growth_factor"] > 1e8
    assert payload["theorem_boundary"]["fixed_eigenvalue_gap_does_not_bound_projector_norm"]
