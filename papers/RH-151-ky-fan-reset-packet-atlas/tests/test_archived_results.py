from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_audit() -> None:
    data = json.loads((ROOT / "results/reset_packet_audit.json").read_text())
    summary = data["audit_summary"]
    assert summary["snapshot_count"] == 130
    assert summary["direct_reset_certificate_count"] == 130
    assert summary["minimum_direct_reset_gap_ratio"] > 60.0
    assert summary["maximum_direct_reset_projector_radius"] < 0.01
    assert summary["ky_fan_dominance_failure_count"] == 0
    assert summary["reset_capture_dominance_failure_count"] == 0
    assert summary["universal_branch_free_informative_count"] == 11


def test_boundary() -> None:
    boundary = json.loads((ROOT / "results/reset_packet_audit.json").read_text())["theorem_boundary"]
    assert boundary["all_frozen_source_memory_snapshots_reset_certified"]
    assert not boundary["ky_fan_only_recursive_transport_uniformly_informative"]
    assert not boundary["reset_packets_inserted_into_outward_assembly"]
    assert not boundary["riemann_hypothesis"]
