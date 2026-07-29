import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_binary_collapse_audit():
    payload = json.loads((ROOT / "results/polynomial_selector_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["real_conjugate_closed_idempotent_selector_pass_count"] == 0
    assert payload["eligible_binary_mask_count"] == 62030604700
    assert payload["maximum_interpolation_residual"] < 1e-7
    assert payload["theorem_boundary"]["polynomial_idempotents_collapse_to_binary_spectral_masks"] is True
    assert payload["theorem_boundary"][
        "real_conjugate_closed_resolved_window_idempotent_selectors_excluded"
    ] is True
    assert payload["theorem_boundary"]["non_idempotent_signed_quotient_grouping_excluded"] is False
    assert payload["theorem_boundary"]["gate_A"] is False
