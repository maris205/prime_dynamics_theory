import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_normalization_audit():
    payload = json.loads((ROOT / "results/intrinsic_normalization_audit.json").read_text())
    summary = payload["normalization_summary"]
    assert len(payload["endpoint_rows"]) == 32
    assert payload["maximum_conjugacy_error"] < 1e-9
    assert payload["legacy_anchor_maximum_root_matching_error"] < 1e-10
    assert payload["legacy_anchor_maximum_coefficient_error"] < 1e-10
    assert summary["raw"]["adjacent_fine_relative_error_mean"] < summary["centered_rms"]["adjacent_fine_relative_error_mean"]
    assert summary["raw"]["adjacent_fine_relative_error_mean"] < summary["determinant_radius"]["adjacent_fine_relative_error_mean"]
    assert not payload["theorem_boundary"]["natural_normalization_contraction"]
