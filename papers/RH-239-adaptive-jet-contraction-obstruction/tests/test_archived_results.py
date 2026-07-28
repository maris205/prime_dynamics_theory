import json
from pathlib import Path


def test_archived_adaptive_contraction():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/adaptive_jet_contraction.json").read_text()
    )
    assert payload["adjacent_case_count"] == 30
    assert payload["channel_case_count"] == 16
    assert payload["minimum_adjacent_bound_slack"] >= -1e-12
    assert payload["minimum_channel_bound_slack"] >= -1e-12
    assert payload["theorem_boundary"]["epsilon_to_zero_implies_fixed_finite_jet_cauchy"]
    assert not payload["theorem_boundary"]["finite_jet_contraction_implies_full_det2_convergence"]
