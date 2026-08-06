from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_result_claim_firewall_and_counts() -> None:
    payload = json.loads((ROOT / "results" / "result.json").read_text())
    assert payload["status"] == "RH-368_parity_factor_mobius_capacity_limit"
    assert payload["route_verdict"] == {"route_a": "GO", "route_b": "STOP_SCOPED"}
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["false_claims"].values())
    assert payload["source_audit"]["pass"] is True
    assert payload["finite_checks"]["all_pass"] is True
    assert payload["endpoint_diagnostic"]["N"] == 2**20
    assert payload["endpoint_diagnostic"]["capacity"] == 425095
