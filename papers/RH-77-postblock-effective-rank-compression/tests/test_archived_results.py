import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_effective_rank_archive_is_green() -> None:
    payload = json.loads((ROOT / "results" / "effective_rank_audit.json").read_text(encoding="utf-8"))
    channels = [channel for row in payload["rows"] for channel in row["channels"]]
    assert payload["all_executed_rank_gates_green"]
    assert len(channels) == 10
    assert min(c["validated_rank_compression"]["rank_2"]["energy_capture_lower"] for c in channels) >= 0.99
    assert min(c["validated_rank_compression"]["rank_4"]["energy_capture_lower"] for c in channels) >= 0.999999


def test_rank_four_future_error_is_small() -> None:
    payload = json.loads((ROOT / "results" / "effective_rank_audit.json").read_text(encoding="utf-8"))
    channels = [channel for row in payload["rows"] for channel in row["channels"]]
    assert max(c["validated_rank_compression"]["rank_4"]["full_future_hardy_perturbation_upper"] for c in channels) < 6.0e-6
