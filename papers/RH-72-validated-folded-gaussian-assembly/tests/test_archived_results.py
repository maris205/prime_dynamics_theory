import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_archive_is_present() -> None:
    payload = json.loads(
        (ROOT / "results" / "interval_assembly_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"].startswith("rh72_")
    assert payload["all_rows_certified"]
    assert len(payload["rows"]) == 1
