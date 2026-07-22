from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("reduced_cross_factorization_audit.json")
    assert len(audit["rows"]) == 5
    assert audit["all_executed_reduced_factorization_gates_green"]
    summary = audit["audit_summary"]
    assert summary["channel_count"] == 10
    assert summary["update_count"] == 120
    assert summary["green_channel_count"] == 10
    assert summary["tail_equivalent_update_count"] == 120
    assert summary["direct_ritz_monotone_count"] == 120
    assert summary["maximum_endpoint_to_reference_ratio"] < 1.01
    assert summary["maximum_reduced_to_ambient_tail_ratio"] < 1.0001
    assert summary["weak_cutoff_mode_count"] == 5
    assert summary["raw_reconstruction_unstable_count"] >= 8
    assert summary["moment_compression_unstable_count"] >= 50


def test_boundary() -> None:
    boundary = load("reduced_cross_factorization_audit.json")["theorem_boundary"]
    assert boundary["projected_cross_gram_identity"]
    assert boundary["cross_cubic_moment_identity"]
    assert boundary["reduced_compressed_factorization_theorem"]
    assert boundary["ambient_cross_svd_removed_after_qr_stabilization"]
    assert not boundary["binary64_moment_only_factorization_stable"]
    assert not boundary["ambient_gram_packet_action_removed"]
    assert not boundary["uniform_cross_spectral_gap_proved"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    smoke = load("reduced_cross_factorization_smoke.json")
    assert len(smoke["rows"]) == 1
    assert smoke["audit_summary"]["update_count"] == 8
