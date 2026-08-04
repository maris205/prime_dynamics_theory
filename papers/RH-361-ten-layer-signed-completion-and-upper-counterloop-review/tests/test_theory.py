from fractions import Fraction

import pytest

from signed_counterloop_review import (
    DIRECTORY_NAMES,
    LAYER_LEDGER,
    UPSTREAM_FALSE_CLAIM_COUNTS,
    opposite_typed_fibers,
    review_status,
    typed_defect_fiber,
)


def test_ten_layers_and_exact_type_partition_are_locked():
    data = review_status()
    assert data["paper_numbers"] == list(range(352, 362))
    assert len(DIRECTORY_NAMES) == 10
    assert len(LAYER_LEDGER) == 10
    assert data["layer_count"] == 10
    assert data["actual_direct_layer_numbers"] == [352, 353, 354]
    assert data["deterministic_counterloop_layer_numbers"] == list(range(355, 361))
    assert data["review_layer_number"] == 361
    assert data["unconditional_scoped_conclusion_count"] == 10
    assert data["conditional_actual_head_layer_count"] == 6


def test_actual_and_deterministic_layer_types_are_not_conflated():
    for layer in LAYER_LEDGER[:3]:
        assert layer["object_type"].startswith("actual_")
        assert layer["actual_head_transfer"] == "not_the_claim"
    for layer in LAYER_LEDGER[3:9]:
        assert "deterministic" in layer["object_type"]
        assert layer["actual_head_transfer"] == "conditional_on_same_clock_unnormalized_D_4k"


def test_typed_defect_fiber_obeys_both_exact_identities():
    row = typed_defect_fiber(
        direct=(Fraction(1, 3), Fraction(-2, 5), Fraction(7, 11)),
        counterloop=(8, 4, 2),
        defect=(3, -5, 9),
        weights=(1, Fraction(1, 2), Fraction(1, 4)),
    )
    assert row["p_equals_q_minus_d_exact"] is True
    assert row["d_equals_h_minus_s_exact"] is True
    assert row["full_trace_q"] == tuple(
        p + d for p, d in zip(row["direct_p"], row["defect_d"])
    )
    assert row["actual_head_h"] == tuple(
        s + d for s, d in zip(row["counterloop_s"], row["defect_d"])
    )
    assert row["physical_operator_constructed"] is False
    assert row["spectral_submultiset_claimed"] is False


def test_same_p_and_s_admit_opposite_coefficient_fibers():
    row = opposite_typed_fibers(
        direct=(Fraction(1, 7), Fraction(-1, 9), Fraction(1, 11)),
        counterloop=(16, 8, 4),
        nonzero_defect=(32, -16, 8),
        weights=(1, Fraction(1, 2), Fraction(1, 4)),
    )
    assert row["same_direct_p"] is True
    assert row["same_counterloop_s"] is True
    assert row["full_trace_budget_changed"] is True
    assert row["head_budget_changed"] is True
    assert row["physical_operator_constructed"] is False
    assert row["spectral_submultiset_claimed"] is False


def test_p_and_s_give_no_uniform_upper_or_positive_individual_lower_bounds():
    p = (Fraction(1, 10), Fraction(-1, 12))
    s = (100, 50)
    weights = (1, 1)
    small = typed_defect_fiber(p, s, (1, -1), weights)
    large = typed_defect_fiber(p, s, (1000, -1000), weights)
    zero_q = typed_defect_fiber(p, s, tuple(-value for value in p), weights)
    zero_h = typed_defect_fiber(p, s, tuple(-value for value in s), weights)
    assert small["weighted_direct_budget"] == large["weighted_direct_budget"]
    assert small["weighted_counterloop_budget"] == large["weighted_counterloop_budget"]
    assert large["weighted_full_trace_budget"] > 100 * small["weighted_full_trace_budget"]
    assert large["weighted_head_budget"] > small["weighted_head_budget"]
    assert zero_q["weighted_full_trace_budget"] == 0
    assert zero_h["weighted_head_budget"] == 0


def test_large_counterloop_moments_do_not_force_actual_head_moments_algebraically():
    row = typed_defect_fiber(
        direct=(0, 0, 0),
        counterloop=(64, 32, 16),
        defect=(-64, -32, -16),
        weights=(1, 1, 1),
    )
    assert row["weighted_counterloop_budget"] > 0
    assert row["weighted_head_budget"] == 0
    assert row["spectral_submultiset_claimed"] is False


def test_invalid_fiber_domains_fail_closed():
    with pytest.raises(ValueError):
        typed_defect_fiber((), (), (), ())
    with pytest.raises(ValueError):
        typed_defect_fiber((1,), (1, 2), (0,), (1,))
    with pytest.raises(ValueError):
        typed_defect_fiber((1,), (1,), (0,), (0,))
    with pytest.raises(TypeError):
        typed_defect_fiber((True,), (1,), (0,), (1,))
    with pytest.raises(TypeError):
        typed_defect_fiber((1.0,), (1,), (0,), (1,))
    with pytest.raises(ValueError):
        opposite_typed_fibers((1,), (1,), (0,), (1,))


def test_terminal_lag_route_closes_only_at_deterministic_type():
    route = review_status()["terminal_lag_route"]
    assert route["status"] == "deterministic_route_closed_through_transform_phase_diagram"
    assert route["geometric_localization"] == "RH-358"
    assert route["logarithmic_inverse_accuracy"] == "RH-359"
    assert route["exponential_tilt_phase_transition"] == "RH-360"
    assert route["actual_transfer_requires_D_4k"] is True


def test_open_frontiers_and_claim_firewall_remain_exact():
    data = review_status()
    theorem = data["typed_separation_theorem"]
    assert theorem["bridge_proved_in_batch"] is False
    assert theorem["p_alone_determines_q"] is False
    assert theorem["s_alone_determines_h"] is False
    assert theorem["spectral_submultiset_inclusion_proved"] is False
    assert theorem["physical_counterexample_constructed"] is False
    assert data["rh241_frontier"]["moving_noisy_all_order_envelope_open"] is True
    assert data["rh241_frontier"]["coefficient_bridge_open"] is True
    assert data["rh288_status"]["active"] is False
    assert data["open_obligation_count"] == 8
    assert not any(data["open_obligations"].values())
    assert len(data["false_claims"]) == 20
    assert not any(data["false_claims"].values())
    assert not any(data["gates"].values())


def test_exact_batch_audit_and_archive_counts_are_locked():
    data = review_status()
    assert sum(UPSTREAM_FALSE_CLAIM_COUNTS) == 129
    assert data["upstream_gate_values_expected_false"] == 45
    assert data["upstream_false_claim_values_expected_false"] == 129
    assert data["batch_gate_values_expected_false"] == 50
    assert data["batch_false_claim_values_expected_false"] == 149
    assert data["expected_upstream_publication_files"] == 156
    assert data["expected_review_publication_files"] == 20
    assert data["expected_batch_publication_files"] == 176
    assert data["expected_batch_tree_files"] == 198


def test_finite_rows_are_typed_algebra_reproduction_only():
    data = review_status()
    assert len(data["finite_typed_fiber_rows"]) == 3
    assert data["finite_rows_are_coefficient_ledger_reproduction_only"] is True
    for row in data["finite_typed_fiber_rows"]:
        assert row["same_direct_p"] is True
        assert row["same_counterloop_s"] is True
        assert row["full_trace_budget_changed"] is True
        assert row["head_budget_changed"] is True
        assert row["physical_operator_constructed"] is False
        assert row["spectral_submultiset_claimed"] is False
