import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit():
    data = load("dyadic_gauge_audit.json")
    summary = data["audit_summary"]
    assert summary["pair_count"] == 96
    assert summary["finite_nonzero_natural_pair_count"] == 42
    assert summary["infinite_natural_factor_count"] == 24
    assert summary["natural_positive_transfer_count"] == 65
    assert summary["optimal_positive_transfer_count"] == 67
    assert summary["natural_positive_transport_eligible_count"] == 35
    assert summary["optimal_positive_transport_eligible_count"] == 37
    assert summary["optimal_positive_lost_by_natural_count"] == 2
    assert summary["maximum_gram_alignment_error"] < 1e-14
    assert summary["maximum_eligible_natural_to_optimal_log10"] > 9.9


def test_boundary_and_smoke():
    data = load("dyadic_gauge_audit.json")
    assert data["theorem_boundary"]["dyadic_packet_polar_gauge_constructed"]
    assert not data["theorem_boundary"]["uniform_natural_tail_factor_proved"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    assert load("dyadic_gauge_smoke.json")["audit_summary"]["pair_count"] == 4
