from __future__ import annotations

import json
from pathlib import Path

from experiments.build_result import build_payload


ROOT = Path(__file__).resolve().parents[1]


def test_source_lock_and_phase_counts() -> None:
    payload = build_payload()
    assert payload["source_audit"]["pass"] is True
    assert len(payload["source_audit"]["rows"]) == 23
    phase = payload["phase_scan"]
    assert phase["row_count"] == 136
    assert phase["aligned_rows"] == 4
    assert phase["crossing_rows"] == 132


def test_route_and_gate_firewall() -> None:
    payload = build_payload()
    assert payload["route_verdict"] == {"route_a": "GO", "route_b": "STOP_SCOPED"}
    assert not any(payload["gates"].values())
    assert not any(payload["false_claims"].values())
    assert payload["overlap_ledger"]["distinct_edge"] is True


def test_persisted_result_is_current() -> None:
    payload = build_payload()
    persisted = json.loads((ROOT / "results/result.json").read_text())
    assert persisted == payload
