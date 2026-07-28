import json
from pathlib import Path


def test_archived_fredholm_dictionary():
    payload = json.loads((Path(__file__).parents[1] / "results/fredholm_dictionary_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["maximum_reciprocal_polynomial_identity_error"] < 1e-10
    assert payload["maximum_fredholm_zero_factor_residual"] < 1e-12
    assert payload["all_reciprocal_zeros_outside_unit_disk"]
    assert payload["theorem_boundary"]["fixed_noise_hilbert_schmidt_det2_inherited_from_RH7"]
    assert not payload["theorem_boundary"]["small_noise_local_uniform_limit"]
