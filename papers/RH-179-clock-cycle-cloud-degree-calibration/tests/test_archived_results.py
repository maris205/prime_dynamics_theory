import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_clock_cycle_archive():
    payload = json.loads((ROOT / "results/clock_cycle_audit.json").read_text())
    assert payload["row_count"] == 7
    assert payload["observed_rank_cycle_gap_values"] == [3, 4]
    assert payload["actual_reset_overlap_count"] == 1
    assert payload["translation_identity_failure_count"] == 0
    assert payload["actual_reset_rank_mismatch_count"] == 0
    assert not payload["theorem_boundary"]["unique_cycle_calibration"]
