import json
from pathlib import Path


def test_archived_det2_coherence():
    payload = json.loads((Path(__file__).parents[1] / "results/det2_coherence_audit.json").read_text())
    assert payload["channel_case_count"] == 16
    assert payload["adjacent_case_count"] == 30
    assert payload["channel_gate_pass_count"] == 16
    assert payload["maximum_channel_log_difference"] < 0.02
    assert not payload["both_channels_strictly_contract_on_last_four_transitions"]
    assert payload["theorem_boundary"]["finite_dual_channel_unit_disk_coherence"]
    assert not payload["theorem_boundary"]["cross_scale_det2_contraction"]
