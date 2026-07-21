import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_audit_records_the_stein_norm_gap() -> None:
    payload = json.loads(
        (ROOT / "results" / "horizon_scaling_audit.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(payload["rows"]) == 5
    assert payload["program_boundary"]["stage_A1_closed"] is False
    assert payload["program_boundary"]["directional_tail_certificate"] is False
    assert payload["fits"]["left_gap"]["power"] > 1.0
    assert payload["fits"]["right_gap"]["power"] > 0.7
    endpoint = payload["rows"][-1]
    assert endpoint["left"]["geometric_horizons"]["0.05"] >= 800
    assert endpoint["right"]["geometric_horizons"]["0.05"] >= 200
