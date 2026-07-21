import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_result_has_two_models() -> None:
    payload = json.loads(
        (ROOT / "results" / "nested_krylov_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"].startswith("rh63_")
    assert len(payload["models"]) == 2
