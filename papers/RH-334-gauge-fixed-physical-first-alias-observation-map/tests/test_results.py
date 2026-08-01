import json
from pathlib import Path

import mpmath as mp

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_is_deterministic_with_exact_reproduction_row_counts():
    data = _result()
    assert data == result_payload()
    assert len(data["period_two_bijection_rows"]) == 3
    assert len(data["finite_nystrom_folding"]["rows"]) == 3
    assert len(data["false_claims"]) == 20


def test_operator_hypotheses_and_basepoint_typing_are_locked():
    data = _result()
    typing = data["operator_typing"]
    assert data["coefficient_type"] == "hardy_full_trace_constituent"
    assert typing["signed_domain"] == "I=[-1,1]"
    assert typing["folded_domain"] == "I_plus=[0,1]"
    assert typing["operator_action"] == "backward_observable"
    assert typing["multiplication_role"] == "M_J_marks_source_basepoint"
    assert typing["kernel_orientation"] == "first_variable_source_second_variable_destination"
    assert typing["signed_folded_orientation"] == "signed_x_maps_to_folded_y=abs(x)"
    assert typing["noisy_operator_trace_orders"] == "n>=2"
    assert typing["deterministic_bijection_orders"] == "n>=1"
    assert typing["localized_peripheral_projectors"] is False
    assert typing["localized_floquet_sectors"] is False


def test_witness_and_frozen_partition_record_the_exact_rh327_defect():
    data = _result()
    witness = data["n2_witness"]
    partition = data["frozen_partition"]
    assert mp.mpf(witness["x_minus"]) < 0 < mp.mpf(witness["x_plus"])
    assert witness["cycle_weight_exact_formula"] == "1/(4*u_c-3)"
    assert mp.almosteq(
        mp.mpf(witness["corrected_total"]) - mp.mpf(witness["old_positive_x_total"]),
        mp.mpf(witness["exact_missing_weight"]),
    )
    assert partition["expected_corrected_symbolic_slots"] == ["0", "w_c", "w_r+w_c"]
    assert partition["expected_old_symbolic_slots"] == ["0", "w_c", "w_r"]
    assert partition["windows_frozen_before_evaluation"] is True
    assert partition["deterministic_membership_rule"] == "abs(x)_in_J"
    assert partition["endpoint_ownership"] == {
        "minus_left": "J_minus",
        "fold_cusp_b": "J_plus",
        "plus_right": "J_plus",
        "outside_union": "F",
    }
    assert partition["corrected_P_abs_slots"]["J_plus"] == witness["cycle_weight_w_c"]
    assert partition["old_positive_x_slots"]["F"] == witness["fixed_weight_w_r"]


def test_first_alias_coefficient_ledger_and_modulus_distinction_are_exact():
    data = _result()
    ledger = data["exact_fraction_ledger"]
    relations = data["coefficient_relations"]
    assert ledger["q_FT_direct"] == ledger["q_FT_slots"]
    assert ledger["q_path_error"] == "0/1"
    assert ledger["tau_relation_error"] == "0/1"
    assert relations["first_alias_identity"] == "q_FT=B+S+R+P-A"
    assert relations["slot_sign_pattern"] == "+B+S+R+P-A"
    assert relations["localized_slot_scale"] == "r_H^(-n)"
    assert relations["q_FT_equals"] == "e_sigma_k_2k"
    assert relations["q_FT_is_modulus_complement_without_d_zero"] is False


def test_mutation_locks_and_numeric_rows_are_explicitly_noncertified():
    data = _result()
    assert all(data["mutation_locks"].values())
    assert data["exact_rational_block_folding"]["identity_holds"] is True
    assert data["finite_nystrom_folding"]["certification_status"] == (
        "finite_nystrom_distributive_identity_check_only"
    )
    assert data["partition_dependence_reproduction"]["certification_status"] == (
        "positive_quadrature_reproduction_only"
    )
    assert data["finite_rows_promoted_to_continuum_certificates"] is False


def test_all_forbidden_claims_and_gates_remain_false():
    data = _result()
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())
    for key in (
        "slot_asymptotics_proved",
        "far_remainder_o_H_k_proved",
        "forward_probability_identified_with_cyclic_trace",
        "actual_model_replacement_proved",
        "duhamel_full_cycle_closure_proved",
        "off_alias_background_closed",
        "head_counterloop_transport_proved",
        "determinant_gluing_activated",
    ):
        assert data["false_claims"][key] is False
