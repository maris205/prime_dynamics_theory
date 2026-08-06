from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_result_claim_firewall_and_audits() -> None:
    result = json.loads((ROOT / "results/result.json").read_text())
    assert result["status"] == "RH-370_fold_compatible_ulam_spike_barrier"
    assert result["route_verdict"] == {"route_a": "GO", "route_b": "STOP_SCOPED"}
    assert all(value is False for value in result["gates"].values())
    assert all(value is False for value in result["false_claims"].values())
    assert result["source_audit"]["pass"] is True
    assert result["finite_checks"]["all_pass"] is True
    assert result["spike_checks"]["all_pass"] is True
