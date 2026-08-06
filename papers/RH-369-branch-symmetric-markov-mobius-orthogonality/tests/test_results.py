from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_result_firewall_and_schema_constants() -> None:
    payload = json.loads((ROOT / "results" / "result.json").read_text())
    assert payload["status"] == "RH-369_branch_symmetric_markov_mobius_orthogonality"
    assert payload["route_verdict"] == {"route_a": "GO", "route_b": "STOP_SCOPED"}
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["false_claims"].values())
    assert payload["source_audit"]["pass"] is True
    assert payload["finite_checks"]["all_pass"] is True
    assert all(row["pass"] for row in payload["parameter_checks"])


def test_result_has_fixed_parameter_firewall() -> None:
    payload = json.loads((ROOT / "results" / "result.json").read_text())
    notes = payload["claim_boundary"]["notes"]
    assert any("fixed t" in note for note in notes)
    assert any("conditional" in note for note in notes)
