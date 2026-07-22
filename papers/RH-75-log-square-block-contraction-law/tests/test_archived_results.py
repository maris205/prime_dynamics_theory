import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_anchor_archive_is_green() -> None:
    payload = json.loads((ROOT / "results" / "log_square_block_audit.json").read_text(encoding="utf-8"))
    channels = [channel for row in payload["rows"] for channel in row["channels"]]
    assert payload["all_executed_anchors_green"]
    assert len(channels) == 10
    assert max(channel["normalized_q_over_sqrt_sigma_upper"] for channel in channels) <= payload["constants"]["q_constant"]


def test_smoke_archive_is_present() -> None:
    payload = json.loads((ROOT / "results" / "log_square_block_smoke.json").read_text(encoding="utf-8"))
    assert payload["all_executed_anchors_green"]
    assert len(payload["rows"]) == 1
