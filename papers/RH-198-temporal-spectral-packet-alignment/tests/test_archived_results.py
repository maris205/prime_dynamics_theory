import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_alignment_audit():
    payload = json.loads((ROOT / "results/packet_alignment_audit.json").read_text())
    assert payload["accepted_window_count"] == 12
    assert payload["all_alignment_log_slopes_negative"]
    assert payload["all_alignment_endpoints_are_minima"]
    assert payload["minimum_alignment_fit_r_squared"] > 0.89
    assert payload["latest_maximum_subspace_gap"] < 0.051
