import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_pilot_records_a_valid_phase_tail_completion() -> None:
    payload = json.loads(
        (ROOT / "results" / "phase_tail_pilot_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"] == (
        "binary64_phase_aware_finite_horizon_stein_tail_audit"
    )
    assert len(payload["rows"]) == 2
    for row in payload["rows"]:
        for side in ("left", "right"):
            channel = row[side]
            selected = channel["horizons"][str(payload["selected_horizon"])]
            assert channel["selected_phase_aware_upper"] >= (
                channel["exact_hardy_energy"] * (1.0 - 1.0e-9)
            )
            assert selected["finite_gram_minimum_eigenvalue"] > -1.0e-9
            assert selected["tail_sum"] >= 0.0
            assert channel["horizons"]["0"]["phase_aware_upper"] >= (
                channel["selected_phase_aware_upper"] * (1.0 - 1.0e-9)
            )
