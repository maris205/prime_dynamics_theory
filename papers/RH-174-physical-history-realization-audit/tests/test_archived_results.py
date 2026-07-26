import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_history_archive():
    payload = json.loads((ROOT / "results/physical_history_audit.json").read_text())
    assert payload["snapshot_count"] == 130
    assert payload["update_count"] == 120
    assert payload["metric_summaries"]["gram_factorization_operator_residual"]["maximum"] < 2e-14
    assert payload["metric_summaries"]["stable_polar_isometry_defect"]["maximum"] < 2e-12
    assert payload["threshold_counts"]["adjoint_residual_at_most_0_25"] == 0
    assert payload["threshold_counts"]["two_sided_residuals_at_most_0_25"] == 0
    assert not payload["theorem_boundary"]["history_to_rh80_transfer_intertwiner"]
