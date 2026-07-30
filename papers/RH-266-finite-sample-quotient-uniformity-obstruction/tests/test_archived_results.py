import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_archived_obstruction():
    payload = json.loads((ROOT / "results/uniformity_obstruction.json").read_text())
    assert payload["finite_metrics"]["audited_endpoint_count"] == 23
    assert payload["finite_metrics"]["missing_endpoint_count"] == 9
    assert payload["finite_metrics"]["power_12_contractive_count"] == 23
    assert payload["coverage"]["uniform_conclusion_available"] is False
    assert payload["theorem_boundary"]["underlying_family_proved_nonuniform"] is False
    assert all(payload["theorem_boundary"][f"gate_{letter}"] is False for letter in "ABCDE")
