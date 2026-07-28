import json
from pathlib import Path


def test_archived_trace_jet_coherence():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/trace_jet_coherence.json").read_text()
    )
    assert payload["channel_case_count"] == 16
    assert payload["channel_radius_case_count"] == 48
    assert payload["unit_disk_gate_pass_count"] == 16
    assert payload["maximum_unit_disk_trace_jet_distance"] < 0.02
    assert not payload["theorem_boundary"]["all_order_channel_determinant_coherence"]
