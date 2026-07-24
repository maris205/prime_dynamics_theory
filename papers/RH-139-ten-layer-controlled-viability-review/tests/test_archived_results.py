import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_ten_layer_review():
    data = load("ten_layer_review.json")
    summary = data["audit_summary"]
    assert summary["reviewed_upstream_layer_count"] == 9
    assert summary["total_layer_count_including_review"] == 10
    assert summary["constructive_layer_count"] == 7
    assert summary["mixed_layer_count"] == 3
    assert summary["archive_verification_failure_count"] == 0
    assert summary["forbidden_claim_failure_count"] == 0
    assert summary["viability_floor_failure_count"] == 0
    assert summary["floor_free_complete_chain_count"] == 0
    assert summary["metric_balanced_contractive_count"] == 183
    assert summary["finite_safe_chain_count"] == 28
    assert summary["outward_positive_chain_count"] == 28


def test_revised_frontier_removes_per_step_contraction():
    frontier = load("ten_layer_review.json")["revised_frontier"]
    assert frontier["mathematical_exact_matrix_frontier"] == [
        "eventual_uniform_controlled_tail_gap",
        "positive_normalized_base_liminf",
    ]
    assert "subunit_affine_coefficient_at_every_step" in frontier["removed_as_unnecessary"]


def test_boundary_and_smoke():
    data = load("ten_layer_review.json")
    assert data["theorem_boundary"]["controlled_viability_eventual_support_theorem"]
    assert not data["theorem_boundary"]["eventual_uniform_tail_gap_proved_for_model"]
    assert not data["theorem_boundary"]["positive_normalized_base_liminf_proved_for_model"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    assert load("ten_layer_review_smoke.json")["audit_summary"]["reviewed_upstream_layer_count"] == 3
