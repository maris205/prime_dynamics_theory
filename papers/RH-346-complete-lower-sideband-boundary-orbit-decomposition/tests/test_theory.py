from decimal import Decimal, localcontext
from fractions import Fraction

import pytest

from lower_sideband_orbit import physical_constants, sideband_row, typed_ledger_fixture


def test_physical_constants_keep_the_hardy_superunit_scale():
    constants = physical_constants()
    assert constants["lambda"] > 1
    assert constants["beta"] * Decimal("1.4") > 1


def test_sideband_uses_m_equal_k_minus_one_on_the_same_clock():
    for k in (3, 5, 9, 17, 33):
        row = sideband_row(k)
        assert row["m"] == k - 1
        assert row["sideband_order"] == 2 * k - 2


def test_complete_folded_lower_orbit_has_exact_count_and_closes():
    for k in (3, 5, 9, 17, 33):
        row = sideband_row(k)
        assert row["complete_count"] == 2 * row["m"]
        assert row["distinct_folded_count"] == 2 * row["m"]
        assert row["orbit_closure_error"] < Decimal("1e-70")


def test_eventual_cell_counts_retain_only_left_far_critical_allocation():
    for k in (5, 9, 17, 33):
        row = sideband_row(k)
        assert row["left_count"] == row["epsilon"]
        assert row["right_count"] == 0
        assert row["far_count"] == 2 * row["m"] - row["epsilon"]
        assert row["cell_count_identity"] == 2 * row["m"]


def test_epsilon_is_the_inclusive_lower_q_b_threshold():
    for k in (3, 5, 9, 17):
        row = sideband_row(k)
        assert row["epsilon"] == int(row["critical_q_b"] <= row["window_A"])


def test_full_partial_and_missing_point_identities():
    with localcontext() as context:
        context.prec = 100
        for k in (3, 5, 9, 17, 33):
            row = sideband_row(k)
            m = row["m"]
            assert row["full_atom"] == Decimal(2 * m) * row["point_weight"]
            assert row["partial_atom"] == Decimal(2 * m - 1) * row["point_weight"]
            assert abs(row["full_atom"] - row["partial_atom"] - row["point_weight"]) < Decimal("1e-95")


def test_missing_point_and_full_atom_are_super_target():
    rows = [sideband_row(k) for k in (5, 9, 17, 33)]
    assert rows[-1]["point_over_target"] > rows[0]["point_over_target"]
    assert rows[-1]["full_over_target"] > rows[0]["full_over_target"]
    assert rows[-1]["point_over_target"] > Decimal(1000)


def test_radial_sideband_is_relatively_small_but_not_dropped():
    rows = [sideband_row(k) for k in (5, 9, 17, 33)]
    magnitudes = [abs(row["radial_over_full"]) for row in rows]
    assert magnitudes[-1] < magnitudes[0]
    assert abs(rows[-1]["combined_over_full"] - 1) < abs(rows[0]["combined_over_full"] - 1)


def test_lower_parity_leading_ratio_has_the_shifted_phase_scale():
    rows = [sideband_row(k) for k in (5, 9, 17, 33)]
    values = [row["parity_leading_over_full"] for row in rows]
    assert max(values) - min(values) < Decimal("0.02")


def test_typed_rational_ledger_is_exact():
    fixture = typed_ledger_fixture(
        raw_rest=Fraction(29, 7),
        parity=Fraction(11, 5),
        radial_sideband=Fraction(13, 9),
        full_atom=Fraction(17, 8),
        head_defect=Fraction(19, 12),
    )
    assert fixture["raw_residual"] == 0
    assert fixture["direct_residual"] == 0
    assert fixture["p"] == fixture["compensation_residual"]


def test_invalid_domains_fail_closed():
    with pytest.raises(ValueError):
        physical_constants(40)
    with pytest.raises(ValueError):
        sideband_row(2)
    with pytest.raises(ValueError):
        sideband_row(3, window_A=0)
    with pytest.raises(TypeError):
        sideband_row(3, phase_eta=0.5)
