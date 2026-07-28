import json
from pathlib import Path


def test_archived_spectral_factor():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/spectral_factor_audit.json").read_text()
    )
    assert payload["factorization_case_count"] == 6144
    assert payload["maximum_grid_factorization_error"] < 1e-10
    assert payload["inherited_maximum_projector_norm"] > 1e12
    assert payload["theorem_boundary"]["finite_det2_multiset_factorization_exact"]
    assert not payload["theorem_boundary"]["small_noise_cloud_divisor_identified"]
