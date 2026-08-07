import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_result_ledger():
    payload = json.loads((ROOT / "results" / "result.json").read_text())
    assert payload["status"] == "RH-373_composite_clock_mobius_capacity_floor"
    assert payload["source_locks"]["count"] == 10
    assert payload["source_locks"]["pass"]
    assert payload["certificate"]["all_pass"]
    assert payload["certificate"]["counts"] == {
        "selected": 80,
        "weight_1_over_24": 12,
        "weight_5_over_96": 68,
        "weight_zero": 0,
    }
    assert payload["theorem"]["density"] == "97/(24*pi^2)"
    assert payload["claim_boundary"]["route_a"] == "GO"
    assert payload["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert not any(payload["gates"].values())
