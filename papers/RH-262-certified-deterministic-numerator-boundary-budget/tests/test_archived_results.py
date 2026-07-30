import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_boundary_budget():
    payload = json.loads(
        (ROOT / "results/certified_boundary_budget.json").read_text()
    )
    assert payload["certified_conclusions"]["M_7_over_5_lt_108"] is True
    assert len(payload["replays"]) == 3
    assert all(
        all(row["comparisons"].values()) for row in payload["replays"]
    )
    assert payload["obligation_vector"]["satisfied_count"] == 2
    assert payload["obligation_vector"]["complete"] is False
    assert all(
        payload["theorem_boundary"][f"gate_{letter}"] is False
        for letter in "ABCDE"
    )
