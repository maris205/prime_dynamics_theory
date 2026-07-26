import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def payload() -> dict:
    return json.loads((ROOT / "results/typed_assembly_audit.json").read_text())


def test_current_frontier_and_statuses() -> None:
    data = payload()
    assert data["audit_summary"]["minimal_completion_bundle_count"] == 2
    assert data["audit_summary"]["current_first_missing_interface"] == "S_native"
    assert data["current_statuses"]["R"] == "open"
    assert data["current_statuses"]["U"] == "open"


def test_frozen_examples_cover_both_rank_outcomes() -> None:
    examples = payload()["packet_riesz_examples"]
    assert sum(row["spectral_rank_certified"] for row in examples) == 6
    assert sum(row["packet_bridge_certified"] for row in examples) == 3
    assert sum(not row["packet_bridge_certified"] for row in examples) == 3


def test_claim_boundary_is_not_promoted() -> None:
    boundary = payload()["theorem_boundary"]
    assert boundary["abstract_typed_assembly_theorem"]
    assert boundary["packet_riesz_bound"]
    assert boundary["trace_class_fredholm_branch"]
    assert boundary["hilbert_schmidt_regularized_branch"]
    for key in (
        "one_step_two_step_limits_identified",
        "eventual_reset_interfaces_proved",
        "physical_packet_to_riesz_bridge_proved",
        "uniform_complement_limit_proved",
        "canonical_intrinsic_determinant_constructed",
        "gate_A_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        assert not boundary[key]
