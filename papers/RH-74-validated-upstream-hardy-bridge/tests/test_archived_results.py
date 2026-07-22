import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_archive_is_green() -> None:
    payload = json.loads(
        (ROOT / "results" / "validated_upstream_bridge_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"].startswith("rh74_")
    assert payload["all_executed_channels_green"]
    assert len(payload["rows"]) == 1


def test_full_archive_closes_all_ten_channels() -> None:
    payload = json.loads(
        (ROOT / "results" / "validated_upstream_bridge_audit.json").read_text(
            encoding="utf-8"
        )
    )
    channels = [channel for row in payload["rows"] for channel in row["channels"]]
    assert len(channels) == 10
    assert all(channel["finite_scale_one_percent_green"] for channel in channels)
    assert max(channel["bridge_to_slack_ratio_upper"] for channel in channels) < 0.003
