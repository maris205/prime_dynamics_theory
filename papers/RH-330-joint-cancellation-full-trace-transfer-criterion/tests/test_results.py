import json
from fractions import Fraction
from pathlib import Path


RESULT = Path(__file__).parents[1] / "results" / "result.json"


def load_result():
    return json.loads(RESULT.read_text())


def test_positive_conditional_claims():
    data = load_result()
    for key in (
        "observable_five_slot_ledger_proved",
        "exact_actual_model_transfer_identity_proved",
        "exchange_observation_gauge_invariance_proved",
        "critical_weighted_prefix_extraction_identity_proved",
        "model_closure_transfer_iff_joint_defect_little_o_proved",
        "normalized_limit_transfer_under_joint_little_o_proved",
        "modular_critical_plus_far_sufficient_criterion_proved",
        "grouped_signed_enclosure_proved_sharp",
        "grouped_best_worst_residual_formulas_proved",
        "all_abstract_duhamel_terms_retained_before_grouping",
        "separate_absolute_majorant_sufficient_but_not_necessary",
        "same_unsigned_bounds_opposite_verdict_counterexample_proved",
        "order_H_replacement_insufficient_counterexample_proved",
        "little_o_alias_replacement_insufficient_for_closure_proved",
        "rh329_exact_repair_law_proved",
        "rh329_synthetic_closing_repair_counterexample_proved",
        "rh329_failure_transfer_under_subalias_joint_defect_proved",
        "full_trace_constituent_criterion_is_inactive",
    ):
        assert data[key] is True


def test_actual_and_program_claims_remain_false():
    data = load_result()
    for key in (
        "actual_to_rh329_identification_map_proved",
        "actual_critical_packet_identified_with_weighted_prefix_coefficient",
        "actual_exchange_observation_split_identified",
        "actual_two_channel_duhamel_signed_enclosures_proved",
        "actual_all_duhamel_weights_controlled",
        "actual_parity_alias_replacement_little_o_proved",
        "actual_far_remainder_signed_little_o_proved",
        "actual_off_alias_weighted_background_vanishing_proved",
        "actual_joint_replacement_little_o_H_proved",
        "actual_joint_replacement_little_o_alias_proved",
        "actual_critical_coefficient_little_o_proved",
        "actual_weighted_full_trace_prefix_vanishing_proved",
        "actual_full_trace_replacement_proved",
        "actual_full_trace_divergence_proved",
        "determinant_gluing_activated",
        "head_counterloop_budget_closed",
        "single_all_order_operator_constructed",
        "finite_rows_promoted_to_physical_asymptotics",
        "hilbert_polya_constructed",
        "riemann_zeros_identified",
        "von_mangoldt_trace_proved",
        "zeta_divisor_equality",
        "riemann_hypothesis_proved",
    ):
        assert data[key] is False
    assert not any(data["gates"].values())


def test_exact_identity_gauge_and_grouped_checks():
    data = load_result()
    assert Fraction(data["identity_check"]["identity_error"]["exact"]) == 0
    gauge = data["gauge_check"]
    values = [Fraction(entry["exact"]) for entry in gauge.values()]
    assert len(set(values)) == 1
    grouped = data["grouped_interval_check"]
    assert Fraction(grouped["center"]["exact"]) == 0
    assert Fraction(grouped["radius"]["exact"]) == Fraction(3, 20)
    prefix = data["critical_prefix_check"]
    assert Fraction(prefix["total_weighted_prefix"]["exact"]) == Fraction(7, 20)


def test_transfer_rows_and_exact_counts():
    data = load_result()
    assert data["row_orders"] == [2, 4, 8, 16, 24, 32]
    assert data["row_count"] == 6
    assert data["total_retained_synthetic_duhamel_terms"] == 344
    for row in data["rows"]:
        assert row["repaired_residual_is_H_over_k_exact"] is True
        assert Fraction(row["repaired_residual_to_target_exact"]) == Fraction(
            1, row["k"]
        )
        assert row["balanced_cancellation_exact"] is True
        assert row["same_unsigned_bounds_have_opposite_verdicts_exact"] is True
        assert row["subalias_is_smaller_than_alias_exact"] is True
        assert row["subalias_exceeds_target_exact"] is True
        assert row["duhamel_term_count"] == 4 * row["k"]
        assert row["duhamel_signed_sum_exact"] == "0/1"


def test_interfaces_are_explicitly_inactive():
    data = load_result()
    assert data["rh329_interface_consumed"]["isolated_model_joint_matching"] == "fails"
    interface = data["rh331_interface"]
    assert interface["duhamel_channels"] == [
        "minus_critical",
        "plus_critical",
    ]
    assert interface["actual_identification_map_proved"] is False
    assert interface["actual_joint_replacement_little_o_proved"] is False
    assert interface["actual_full_trace_replacement_proved"] is False
