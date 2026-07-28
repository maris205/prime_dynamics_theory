import json
from pathlib import Path


def test_archived_trace_envelope():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/trace_envelope_audit.json").read_text()
    )
    assert payload["observed_order_count"] == 11
    assert payload["global_observed_unit_amplitude_rate"] < 0.5
    assert payload["fine_observed_unit_amplitude_rate"] < 0.3
    assert payload["theorem_boundary"]["all_order_geometric_trace_envelope_implies_normal_relative_det2"]
    assert not payload["theorem_boundary"]["order_thirteen_and_above_controlled"]
