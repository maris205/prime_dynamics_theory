import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_packet_audit():
    summary = load("spectral_packet_audit.json")["audit_summary"]
    assert summary["channel_rank_record_count"] == 30
    assert summary["rank1_universal_stable_count"] == 7
    assert summary["rank2_universal_stable_count"] == 7
    assert summary["rank4_universal_stable_count"] == 4
    assert summary["rank4_universal_gap_wall_count"] == 6
    assert summary["rank4_ideal_svd_stable_count"] == 10
    assert summary["minimum_rank4_ideal_svd_gap_ratio"] > 1.02
    assert summary["synthetic_failure_count"] == 0


def test_claim_boundary_and_smoke():
    data = load("spectral_packet_audit.json")
    assert data["theorem_boundary"]["approximate_gap_projector_enclosure"]
    assert data["theorem_boundary"]["two_radius_gap_obstruction"]
    assert not data["theorem_boundary"]["quadratic_svd_radius_interval_validated"]
    assert not data["theorem_boundary"]["all_ten_rank4_packets_certified"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    assert load("spectral_packet_smoke.json")["audit_summary"]["channel_rank_record_count"] == 6

