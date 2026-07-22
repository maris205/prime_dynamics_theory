import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_result_is_present() -> None:
    payload = json.loads(
        (ROOT / "results" / "depth_barrier_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"].startswith("rh68_")
    assert len(payload["exact_rings"]) == 1
