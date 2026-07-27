import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_prediction_audit():
    payload = json.loads((ROOT / "results/prediction_audit.json").read_text())
    assert payload["same_winner_both_channels"]
    assert all(row["best_two_point_holdout_model"] == "power_gap" for row in payload["channel_rows"])
    assert all(row["constant_eta_maximum_absolute_error"] < 0.003 for row in payload["channel_rows"])
    assert not payload["theorem_boundary"]["asymptotic_law_identified"]
