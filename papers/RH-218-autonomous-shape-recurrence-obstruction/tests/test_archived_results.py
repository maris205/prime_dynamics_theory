import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_recurrence_audit():
    payload = json.loads((ROOT / "results/recurrence_audit.json").read_text())
    assert payload["pooled_affine_training_metrics"]["maximum_error"] < 0.003
    assert payload["pooled_affine_holdout_metrics"]["maximum_error"] > 0.04
    assert all(row["interpolating_polynomial_in_sample_error"]["maximum_error"] < 1e-12 for row in payload["channel_rows"])
    assert not payload["theorem_boundary"]["scale_independent_semigroup_identified"]
