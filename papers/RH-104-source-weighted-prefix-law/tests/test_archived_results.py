from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("prefix_transient_audit.json")
    assert len(audit["rows"]) == 5
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["source_block_zero_power_anchor_envelope"]
    assert summary["directional_prefix_zero_power_anchor_envelope"]
    assert summary["maximum_actual_directional_prefix_energy"] < 1.77
    assert summary["maximum_crude_prefix_upper"] > 20.0
    assert summary["maximum_crude_to_directional_ratio"] > 10.0
    assert audit["barrier"]["normalized_packet_relative_tail"] == 0.0
    assert audit["barrier"]["block_contraction"] == 0.0
    assert audit["barrier"]["prefix_energy_power"] == 1.5


def test_boundary_and_smoke() -> None:
    audit = load("prefix_transient_audit.json")
    boundary = audit["theorem_boundary"]
    assert boundary["source_weighted_prefix_ledger_theorem"]
    assert boundary["block_tail_transfer_theorem"]
    assert boundary["physical_five_anchor_directional_prefix_validated"]
    assert not boundary["uniform_directional_prefix_law_proved"]
    assert not boundary["block_contraction_alone_closes_prefix"]
    assert not boundary["riemann_hypothesis"]
    smoke = load("prefix_transient_smoke.json")
    assert len(smoke["rows"]) == 1
