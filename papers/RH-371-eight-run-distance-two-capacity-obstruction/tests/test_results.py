import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_result_firewall() -> None:
    result = json.loads((ROOT / "results/result.json").read_text())
    assert result["status"] == "RH-371_eight_run_distance_two_capacity_obstruction"
    assert result["route_verdict"] == {"route_a": "GO", "route_b": "STOP_SCOPED"}
    assert all(value is False for value in result["gates"].values())
    assert all(value is False for value in result["false_claims"].values())
    assert result["source_audit"]["pass"] is True
    assert result["finite_checks"]["all_pass"] is True
    assert result["periodic_audit"]["cyclic_ledger_equal"] is True
    assert result["periodic_audit"]["open_lag2_differs"] is True
