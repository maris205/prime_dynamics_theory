import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_composition_archive_is_green() -> None:
    payload = json.loads((ROOT / "results" / "stage_composition_audit.json").read_text(encoding="utf-8"))
    assert payload["all_executed_composition_gates_green"]
    assert len(payload["rows"]) == 5
    assert all(row["quarter_power_gate"] for row in payload["rows"])


def test_stress_schedule_decays_on_anchors() -> None:
    payload = json.loads((ROOT / "results" / "stage_composition_audit.json").read_text(encoding="utf-8"))
    values = [row["identification_stress_envelope_upper"] for row in payload["rows"]]
    assert all(right < left for left, right in zip(values, values[1:]))
