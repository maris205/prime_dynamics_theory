import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_factorized_arb_audit():
    data = load("factorized_arb_audit.json")
    summary = data["audit_summary"]
    assert data["precision_bits"] == 512
    assert summary["channel_count"] == 10
    assert summary["packet_certified_count"] == 10
    assert summary["frobenius_certificate_count"] == 8
    assert summary["interval_eigen_rescue_count"] == 2
    assert summary["packet_failure_count"] == 0
    assert summary["minimum_gap_ratio"] > 1.02
    assert summary["maximum_projector_radius"] < 0.958


def test_boundary_and_smoke():
    data = load("factorized_arb_audit.json")
    boundary = data["theorem_boundary"]
    assert boundary["all_ten_frozen_binary_source_packets_certified"]
    assert boundary["direct_arb_normalized_snapshot_enclosure"]
    assert not boundary["coarse_projector_enclosures_are_tight"]
    assert not boundary["thresholded_recursive_packet_update_enclosed"]
    assert not boundary["riemann_hypothesis"]
    smoke = load("factorized_arb_smoke.json")["audit_summary"]
    assert smoke["channel_count"] == 2
    assert smoke["interval_eigen_rescue_count"] == 2

