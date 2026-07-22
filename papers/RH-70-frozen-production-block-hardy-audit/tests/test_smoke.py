import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_result_is_present() -> None:
    payload = json.loads(
        (ROOT / "results" / "frozen_production_interval_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"].startswith("rh70_")
    assert len(payload["rows"]) == 1
    assert payload["theorem_boundary"]["all_executed_frozen_rows_green"]
    for channel in payload["rows"][0]["channels"]:
        assert channel["certified_block_contraction"]
        assert channel["archived_energy_inside_interval"]
        assert channel["relative_enclosure_width_upper"] <= 1.01
