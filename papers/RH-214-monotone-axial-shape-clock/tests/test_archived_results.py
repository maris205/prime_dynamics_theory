import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_shape_clock():
    payload = json.loads((ROOT / "results/shape_clock_audit.json").read_text())
    assert payload["scale_count"] == 16
    assert payload["all_u_transitions_strictly_positive"]
    assert payload["channel_summaries"]["left"]["mature_eta_corridor_sigma_at_most_0_02"]["width"] < 0.04
    assert payload["channel_summaries"]["right"]["u_clock"]["strict_increase_count"] == 15
    assert not payload["theorem_boundary"]["small_noise_limit"]
