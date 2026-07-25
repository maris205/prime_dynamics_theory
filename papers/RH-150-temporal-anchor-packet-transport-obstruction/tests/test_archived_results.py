from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_audit_headline() -> None:
    data = json.loads((ROOT / "results/packet_transport_audit.json").read_text())
    summary = data["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["rank_mismatch_channel_count"] == 8
    assert summary["equal_rank_vacuous_transfer_count"] == 2
    assert summary["informative_inherited_seed_count"] == 0
    assert summary["source_aligned_seed_certificate_count"] == 10
    assert summary["complete_transport_chain_count"] == 0
    assert summary["failure_gate_counts"]["branch"] == 7
    assert summary["failure_gate_counts"]["ritz_gap"] == 3
    assert summary["minimum_decisive_failure_ratio"] > 1.0


def test_program_boundary() -> None:
    data = json.loads((ROOT / "results/packet_transport_audit.json").read_text())
    boundary = data["theorem_boundary"]
    assert boundary["typed_temporal_rank_anchor_theorem"]
    assert boundary["all_source_aligned_clock_rank_seeds_certified"]
    assert not boundary["rh142_packets_are_valid_rh96_seeds"]
    assert not boundary["any_complete_recursive_transport_chain"]
    assert not boundary["actual_exact_recursive_chain_disproved"]
    assert not boundary["riemann_hypothesis"]
