import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_archive_has_two_scales() -> None:
    payload = json.loads(
        (ROOT / "results" / "horizon_scaling_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"].startswith("rh61_")
    assert len(payload["rows"]) == 2
    assert payload["evidence_level"].startswith("archived")
