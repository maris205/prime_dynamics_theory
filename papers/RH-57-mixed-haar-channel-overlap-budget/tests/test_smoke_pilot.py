import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_pilot_has_two_all_column_levels() -> None:
    payload = json.loads(
        (ROOT / "results" / "mixed_overlap_pilot_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"] == "binary64_grouped_riesz_cross_stein_overlap_audit"
    assert len(payload["rows"]) == 2
    assert payload["rows"][-1]["left"]["block_reconstruction_relative_defect"] < 1.0e-9
    assert payload["rows"][-1]["right"]["block_reconstruction_relative_defect"] < 1.0e-9
