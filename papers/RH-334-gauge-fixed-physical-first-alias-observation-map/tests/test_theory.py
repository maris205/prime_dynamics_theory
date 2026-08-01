from fractions import Fraction

import mpmath as mp
import pytest

from physical_observation import (
    EXPECTED_COEFFICIENT_TYPE,
    critical_data,
    deterministic_map,
    exact_block_folding_fixture,
    exact_fraction_ledger,
    finite_nystrom_folding_check,
    folded_derivative,
    folded_map,
    frozen_windows,
    period_two_bijection_rows,
    period_two_slot_weights,
    period_two_total_weight,
    period_two_witness,
    positive_gauge_shift_check,
    validate_coefficient_type,
    validate_localized_weight_partition,
)


def test_algebraic_constants_critical_itinerary_and_nonperiodic_cusp():
    data = critical_data()
    assert 1 < data.u < 2
    with mp.workdps(110):
        assert abs(data.u**3 - 2 * data.u**2 + 2 * data.u - 2) < mp.mpf("1e-105")
        assert mp.almosteq(deterministic_map(0, data), 1)
        assert mp.almosteq(deterministic_map(1, data), -data.r)
        assert mp.almosteq(deterministic_map(-data.r, data), data.r)
        assert mp.almosteq(deterministic_map(data.r, data), data.r)
        assert mp.almosteq(folded_map(data.fold_cusp, data), 0)
        assert data.fold_cusp != data.r
    with pytest.raises(ValueError):
        folded_derivative(data.fold_cusp, data)
    with mp.workdps(7):
        low_ambient = (
            deterministic_map(data.r, data),
            folded_map(data.r, data),
            folded_derivative(data.r, data),
        )
    with mp.workdps(45):
        high_ambient = (
            deterministic_map(data.r, data),
            folded_map(data.r, data),
            folded_derivative(data.r, data),
        )
    assert [mp.nstr(value, 90) for value in low_ambient] == [
        mp.nstr(value, 90) for value in high_ambient
    ]


def test_exact_period_two_factor_and_negative_point_witness():
    witness = period_two_witness()
    data = witness.critical
    with mp.workdps(110):
        assert -1 < witness.x_minus < 0 < witness.x_plus < 1
        assert mp.almosteq(deterministic_map(witness.x_minus, data), witness.x_plus)
        assert mp.almosteq(deterministic_map(witness.x_plus, data), witness.x_minus)
        for point in (witness.x_minus, witness.x_plus):
            second_factor = data.u**2 * point**2 - data.u * point + 1 - data.u
            assert abs(second_factor) < mp.mpf("1e-105")


def test_period_two_fixed_point_bijection_has_one_signed_lift_per_folded_point():
    rows = period_two_bijection_rows()
    assert len(rows) == 3
    assert len({mp.nstr(row["folded_point"], 90) for row in rows}) == 3
    assert sum(row["signed_lift"] < 0 for row in rows) == 1
    assert all(row["signed_fixed_residual"] < mp.mpf("1e-100") for row in rows)
    assert all(row["folded_fixed_residual"] < mp.mpf("1e-100") for row in rows)
    witness = period_two_witness()
    expected_folded = {witness.critical.r, witness.x_plus, witness.y_minus}
    assert {row["folded_point"] for row in rows} == expected_folded
    assert all(row["signed_multiplier"] != 1 for row in rows)


def test_multiplier_preservation_simplicity_and_exact_weights():
    witness = period_two_witness()
    rows = period_two_bijection_rows()
    with mp.workdps(110):
        for row in rows:
            assert mp.almosteq(row["signed_multiplier"], row["folded_multiplier"])
            assert row["signed_multiplier"] != 1
        assert mp.almosteq(witness.cycle_multiplier, -4 * witness.critical.r)
        assert mp.almosteq(witness.cycle_weight, 1 / (4 * witness.critical.u - 3))
        assert mp.almosteq(
            witness.fixed_weight, 1 / (witness.critical.lambda_fixed**2 - 1)
        )


def test_frozen_boundary_owned_partition_and_corrected_slots():
    witness = period_two_witness()
    windows = frozen_windows()
    slots = period_two_slot_weights(corrected=True)
    assert windows.classify(windows.minus_left) == "J_minus"
    assert windows.classify(windows.fold_cusp) == "J_plus"
    assert windows.classify(windows.plus_right) == "J_plus"
    assert windows.classify(witness.x_plus) == "J_plus"
    assert windows.classify(witness.y_minus) == "F"
    assert windows.classify(witness.critical.r) == "F"
    assert mp.almosteq(slots["J_minus"], 0)
    assert mp.almosteq(slots["J_plus"], witness.cycle_weight)
    assert mp.almosteq(slots["F"], witness.fixed_weight + witness.cycle_weight)
    validate_localized_weight_partition(slots, period_two_total_weight())
    clipped = frozen_windows(sigma="100", radius="100")
    assert clipped.minus_left == 0 and clipped.plus_right == 1
    with pytest.raises(ValueError):
        windows.classify(mp.mpf("-0.001"))


def test_old_positive_x_binning_fails_closed_by_exactly_one_cycle_weight():
    witness = period_two_witness()
    old_slots = period_two_slot_weights(corrected=False)
    with pytest.raises(ValueError):
        validate_localized_weight_partition(old_slots, period_two_total_weight())
    with mp.workdps(110):
        assert mp.almosteq(
            period_two_total_weight() - mp.fsum(old_slots.values()),
            witness.cycle_weight,
        )


def test_exact_rational_block_folding_identity_is_localized():
    fixture = exact_block_folding_fixture()
    assert fixture["identity_holds"] is True
    assert fixture["signed_localized_traces"] == fixture["folded_localized_traces"]
    assert fixture["folded_localized_traces"] == (Fraction(43, 100), Fraction(229, 400))


def test_32_point_nystrom_lobe_distributivity_is_exact_on_the_symmetric_grid():
    check = finite_nystrom_folding_check()
    assert check["order"] == 32
    assert check["decimal_digits"] == 110
    assert check["certification_status"] == "finite_nystrom_distributive_identity_check_only"
    assert check["maximum_absolute_error"] < mp.mpf("1e-100")
    assert {row["slot"] for row in check["rows"]} == {"J_minus", "J_plus", "F"}


def test_exact_fraction_first_alias_ledger_has_two_zero_error_paths():
    ledger = exact_fraction_ledger()
    assert ledger["k"] == 2 and ledger["n"] == 4
    assert ledger["r_H"] == Fraction(17, 20)
    assert ledger["q_FT_direct"] == ledger["q_FT_slots"]
    assert ledger["q_path_error"] == 0
    boundary, shell, remainder = ledger["slots"]
    assert boundary > 0 and shell > 0 and remainder > 0
    assert ledger["parity_packet"] > 0 and ledger["alias_packet"] > 0
    assert ledger["q_FT_direct"] == (
        boundary
        + shell
        + remainder
        + ledger["parity_packet"]
        - ledger["alias_packet"]
    )
    assert ledger["slots"] == (
        Fraction(64000, 83521),
        Fraction(56000, 83521),
        Fraction(8000, 83521),
    )


def test_coefficient_type_and_modulus_complement_mutations_fail_closed():
    ledger = exact_fraction_ledger()
    validate_coefficient_type(EXPECTED_COEFFICIENT_TYPE)
    with pytest.raises(ValueError):
        validate_coefficient_type("modulus_complement")
    assert ledger["head_counterloop_discrepancy_d"] != 0
    assert ledger["tau_minus_a"] != ledger["q_FT_direct"]
    assert ledger["tau_relation_error"] == 0


def test_positive_window_partition_shift_is_nonzero_zero_sum_and_avoids_fix_t2():
    check = positive_gauge_shift_check()
    windows = frozen_windows()
    rows = period_two_bijection_rows()
    assert windows.minus_left < check["left"] < check["right"] < windows.fold_cusp
    assert mp.almosteq(check["length"], mp.mpf("0.02"))
    assert not any(
        check["left"] <= row["folded_point"] < check["right"] for row in rows
    )
    assert check["localized_trace"] > 0 and check["hardy_scaled_delta"] > 0
    assert check["contained_in_J_minus"] is True
    assert check["contains_period_two_point"] is False
    with mp.workdps(110):
        assert mp.fsum(check["shift_vector"]) == 0
