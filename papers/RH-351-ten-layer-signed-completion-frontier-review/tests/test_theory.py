from fractions import Fraction

import pytest

from signed_completion_review import (
    DIRECTORY_NAMES,
    LAYER_LEDGER,
    ROUTE_COORDINATE,
    affine_completion,
    opposite_completion_witness,
    review_status,
)


def test_ten_layers_and_route_coordinate_are_locked():
    data = review_status()
    assert data["paper_numbers"] == list(range(342, 352))
    assert len(DIRECTORY_NAMES) == 10
    assert len(LAYER_LEDGER) == 10
    assert data["layer_count"] == 10
    assert data["proved_scoped_conclusion_count"] == 10
    assert data["discharged_actual_signed_remainder_count"] == 0
    assert data["route_coordinate"] == ROUTE_COORDINATE


def test_rh241_moving_noisy_frontier_is_distinguished_from_deterministic_inputs():
    ancestry = review_status()["rh241_ancestry"]
    assert ancestry["moving_noisy_all_order_trace_envelope_still_open"] is True
    assert ancestry["no_over_extraction_coefficient_bridge_still_open"] is True
    assert ancestry["deterministic_numerator_anchor_later_proved_by_RH263"] is True
    assert ancestry["deterministic_all_order_envelope_later_proved_by_RH267"] is True
    assert ancestry["deterministic_sharp_radius_later_proved_by_RH268"] is True
    assert ancestry["RH350_selected_lower_even_uniformity_is_not_RH241_noisy_envelope"] is True
    assert ancestry["gate_A_still_open"] is True


def test_affine_completion_realizes_any_prescribed_residual_exactly():
    demand = (Fraction(9, 2), Fraction(7, 3), Fraction(5, 4))
    parity = (Fraction(4, 3), Fraction(11, 5), Fraction(2, 7))
    residual = (Fraction(-3, 8), Fraction(0), Fraction(13, 9))
    weights = (Fraction(1), Fraction(2, 3), Fraction(5, 11))
    row = affine_completion(demand, parity, residual, weights)
    assert row["direct_residual"] == residual
    assert row["completion_Y"] == tuple(
        source - packet + target
        for source, packet, target in zip(demand, parity, residual)
    )
    assert row["physical_operator_constructed"] is False


def test_opposite_completions_obey_exact_budget_exchange():
    row = opposite_completion_witness(
        demand=(8, 4, 2, 1),
        parity=(8, 3, 1, 0),
        weights=(1, Fraction(1, 2), Fraction(1, 4), Fraction(1, 8)),
    )
    close = row["close"]
    far = row["far"]
    exchange = row["budget_exchange"]
    assert close["direct_residual"] == (0, 0, 0, 0)
    assert far["completion_Y"] == (0, 0, 0, 0)
    assert exchange["close_Y_equals_far_direct"] is True
    assert exchange["far_Y_equals_close_direct_zero"] is True
    assert exchange["common_nonzero_budget"] > 0
    assert row["physical_operator_constructed"] is False


def test_close_branch_does_not_satisfy_small_Y_when_far_budget_is_nonzero():
    row = opposite_completion_witness(
        demand=(16, 8, 4),
        parity=(16, 4, 1),
        weights=(1, Fraction(1, 2), Fraction(1, 4)),
    )
    assert row["far"]["weighted_direct_budget"] > 0
    assert row["close"]["weighted_Y_budget"] == row["far"]["weighted_direct_budget"]
    assert row["far"]["weighted_Y_budget"] == 0


def test_invalid_completion_domains_fail_closed():
    with pytest.raises(ValueError):
        affine_completion((), (), (), ())
    with pytest.raises(ValueError):
        affine_completion((1,), (1, 2), (0,), (1,))
    with pytest.raises(ValueError):
        affine_completion((1,), (1,), (0,), (0,))
    with pytest.raises(TypeError):
        affine_completion((True,), (1,), (0,), (1,))
    with pytest.raises(TypeError):
        affine_completion((1.0,), (1,), (0,), (1,))
    with pytest.raises(ValueError):
        opposite_completion_witness((1,), (1, 2), (1,))


def test_information_class_theorem_scope_is_exact():
    theorem = review_status()["information_class_theorem"]
    assert theorem["affine_surjectivity"] == "Y=S-P+r_gives_p=r_exactly"
    assert theorem["close_completion"] == "Y=S-P_gives_p=0"
    assert theorem["far_completion"] == "Y=0_gives_p=P-S"
    assert theorem["far_weighted_law"].startswith("L(far)=F_")
    assert theorem["physical_realizability_claimed"] is False
    assert theorem["actual_physical_verdict_determined"] is False


def test_claim_firewall_and_archive_counts_remain_open():
    data = review_status()
    assert data["open_obligation_count"] == 8
    assert not any(data["open_obligations"].values())
    assert len(data["false_claims"]) == 22
    assert not any(data["false_claims"].values())
    assert not any(data["gates"].values())
    assert data["expected_upstream_publication_files"] == 135
    assert data["expected_review_publication_files"] == 19
    assert data["expected_batch_publication_files"] == 154
    assert data["expected_batch_tree_files"] == 176


def test_finite_rows_are_exact_algebra_checks_only():
    data = review_status()
    assert len(data["finite_witness_rows"]) == 3
    assert data["finite_rows_are_abstract_algebra_checks_only"] is True
    for row in data["finite_witness_rows"]:
        assert row["budget_exchange"]["close_Y_equals_far_direct"] is True
        assert row["budget_exchange"]["far_Y_equals_close_direct_zero"] is True
        assert row["physical_operator_constructed"] is False
