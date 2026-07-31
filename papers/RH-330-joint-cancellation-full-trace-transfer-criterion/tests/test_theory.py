from fractions import Fraction

import pytest

from full_trace_transfer import (
    OBSERVABLE_FIELDS,
    add_observable_slots,
    balanced_replacement,
    collapse_shell,
    critical_weighted_contribution,
    gauge_shift,
    grouped_signed_interval,
    joint_replacement_defect,
    observable_residual,
    outward_decimal_interval,
    repairing_replacement,
    replacement_defects,
    rh331_interface,
    split_residual,
    symmetric_packet_interval,
    transfer_audit_row,
    transfer_identity,
    unpaired_subalias_replacement,
    weighted_prefix_decomposition,
    weighted_signed_ledger,
    zero_observable_slots,
)


def sample_model():
    return {
        "boundary": Fraction(1, 2),
        "shell": Fraction(-1, 3),
        "remainder": Fraction(1, 7),
        "parity": Fraction(2, 5),
        "alias": Fraction(3, 4),
    }


def test_observable_signed_ledger():
    slots = sample_model()
    assert observable_residual(slots) == (
        slots["boundary"]
        + slots["shell"]
        + slots["remainder"]
        + slots["parity"]
        - slots["alias"]
    )


def test_exact_actual_model_transfer_identity():
    model = sample_model()
    defects = {
        "boundary": Fraction(1, 6),
        "shell": Fraction(1, 12),
        "remainder": Fraction(-1, 56),
        "parity": Fraction(1, 35),
        "alias": Fraction(1, 20),
    }
    actual = add_observable_slots(model, defects)
    row = transfer_identity(actual, model)
    assert replacement_defects(actual, model) == defects
    assert row["joint_replacement_defect"] == joint_replacement_defect(defects)
    assert row["actual_residual"] == row["model_residual"] + row[
        "joint_replacement_defect"
    ]
    assert row["identity_error"] == 0


def test_exchange_observation_gauge_invariance():
    split = {
        "boundary": Fraction(2),
        "exchange": Fraction(7, 3),
        "observation": Fraction(-5, 6),
        "remainder": Fraction(1, 7),
        "parity": Fraction(3, 5),
        "alias": Fraction(11, 4),
    }
    shifted = gauge_shift(split, Fraction(13, 9))
    assert split_residual(shifted) == split_residual(split)
    assert collapse_shell(shifted) == collapse_shell(split)
    assert observable_residual(collapse_shell(split)) == split_residual(split)


def test_critical_weighted_prefix_extraction():
    k = 7
    radius = Fraction(7, 5)
    target = k * radius ** (-2 * k)
    error = Fraction(11, 13)
    assert critical_weighted_contribution(error, target) == (
        abs(error) * radius ** (2 * k) / (2 * k)
    )
    row = weighted_prefix_decomposition(Fraction(1, 10), error, target)
    assert row["total_weighted_prefix"] == (
        row["off_alias_budget"] + row["critical_contribution"]
    )


def test_independent_symmetric_packet_interval_is_sharp():
    centers = zero_observable_slots()
    radii = {field: Fraction(index + 1, 100) for index, field in enumerate(OBSERVABLE_FIELDS)}
    row = symmetric_packet_interval(Fraction(2), centers, radii)
    assert row["radius"] == sum(radii.values())
    assert row["lower"] == 2 - row["radius"]
    assert row["upper"] == 2 + row["radius"]
    assert row["best_absolute_residual"] == row["lower"]
    assert row["worst_absolute_residual"] == row["upper"]


def test_grouped_signed_interval_retains_centers():
    row = grouped_signed_interval(
        Fraction(3, 2),
        [Fraction(-1), Fraction(-1, 2)],
        [Fraction(1, 10), Fraction(1, 20)],
    )
    assert row == {
        "center": Fraction(0),
        "radius": Fraction(3, 20),
        "lower": Fraction(-3, 20),
        "upper": Fraction(3, 20),
        "best_absolute_residual": Fraction(0),
        "worst_absolute_residual": Fraction(3, 20),
    }


def test_weighted_signed_duhamel_ledger_retains_cancellation():
    row = weighted_signed_ledger(
        [1, 1, -1, -1],
        [2, 3, 2, 3],
        [Fraction(5, 7)] * 4,
    )
    assert row["term_count"] == 4
    assert row["signed_sum"] == 0
    assert row["absolute_majorant"] == Fraction(50, 7)


def test_balanced_and_same_sign_defects_have_same_component_bounds():
    scale = Fraction(17, 5)
    balanced = balanced_replacement(scale)
    same_sign = zero_observable_slots()
    same_sign["boundary"] = scale
    same_sign["shell"] = scale
    assert [abs(balanced[field]) for field in OBSERVABLE_FIELDS] == [
        abs(same_sign[field]) for field in OBSERVABLE_FIELDS
    ]
    assert joint_replacement_defect(balanced) == 0
    assert joint_replacement_defect(same_sign) == 2 * scale


def test_repairing_defect_closes_to_H_over_k():
    model_error = Fraction(-23, 7)
    target = Fraction(5, 11)
    k = 9
    repair = repairing_replacement(model_error, target, k)
    assert model_error + joint_replacement_defect(repair) == target / k


def test_subalias_defect_is_exactly_A_over_k():
    alias = Fraction(31, 7)
    k = 8
    defects = unpaired_subalias_replacement(alias, k)
    assert joint_replacement_defect(defects) == alias / k
    assert joint_replacement_defect(defects) / alias == Fraction(1, k)


def test_transfer_audit_row_exact_verdicts():
    row = transfer_audit_row(
        8,
        model_residual=Fraction(-17),
        alias_scale=Fraction(20),
        target=Fraction(1, 100),
    )
    assert row["repaired_residual_is_H_over_k_exact"] is True
    assert row["balanced_cancellation_exact"] is True
    assert row["same_unsigned_bounds_have_opposite_verdicts_exact"] is True
    assert row["subalias_is_smaller_than_alias_exact"] is True
    assert row["subalias_exceeds_target_exact"] is True
    assert row["duhamel_term_count"] == 32
    assert row["duhamel_signed_sum_exact"] == "0/1"


def test_outward_intervals_enclose_all_signs():
    for value in (Fraction(-11, 7), Fraction(0), Fraction(13, 9)):
        lower, upper = outward_decimal_interval(value, digits=8)
        assert Fraction(lower) <= value <= Fraction(upper)


def test_interface_keeps_actual_hypotheses_open():
    interface = rh331_interface()
    assert interface["exact_transfer_identity"] == "e_actual=e_model+Theta"
    assert interface["actual_identification_map_proved"] is False
    assert interface["actual_joint_replacement_little_o_proved"] is False
    assert interface["actual_full_trace_replacement_proved"] is False


@pytest.mark.parametrize(
    "call",
    [
        lambda: observable_residual({"boundary": 0}),
        lambda: grouped_signed_interval(0, [0], [0, 0]),
        lambda: grouped_signed_interval(0, [0], [-1]),
        lambda: weighted_signed_ledger([0], [1], [1]),
        lambda: weighted_signed_ledger([1], [-1], [1]),
        lambda: critical_weighted_contribution(1, 0),
        lambda: weighted_prefix_decomposition(-1, 0, 1),
        lambda: transfer_audit_row(1, model_residual=0, alias_scale=1, target=1),
    ],
)
def test_validation(call):
    with pytest.raises(ValueError):
        call()
