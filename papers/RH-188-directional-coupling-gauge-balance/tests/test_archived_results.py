import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_directional_balance():
    payload = json.loads((ROOT / "results/directional_balance_audit.json").read_text())
    assert payload["window_count"] == 126
    assert payload["local_l4_relative_product_below_0_01_count"] > 0
