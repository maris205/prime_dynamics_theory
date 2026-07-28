import json
from pathlib import Path


def test_archived_riesz_projection_audit():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/riesz_projection_audit.json").read_text()
    )
    assert payload["endpoint_count"] == 32
    assert payload["maximum_projector_operator_norm"] > 1.0e8
    assert payload["projector_norm_above_million_count"] > 0
    assert payload["maximum_right_eigenpair_residual"] < 1.0e-8
    assert payload["theorem_boundary"]["finite_biorthogonal_projector_formula"]
    assert not payload["theorem_boundary"]["uniform_projector_bound_supported"]
