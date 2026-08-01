from decimal import Decimal
from fractions import Fraction

import pytest

from prefix_sync import (
    R_H,
    R_TRACE,
    U_RADIUS,
    one_alias_cut,
    physical_constants,
    prefix_weight,
    sideband_orders,
    synchronization_diagnostic,
    tail_exponents,
)


def test_exact_radius_ratio_and_one_alias_cut():
    assert R_H == Fraction(17, 20)
    assert R_TRACE == Fraction(7, 5)
    assert U_RADIUS == Fraction(28, 17)
    for k in (2, 3, 5, 9, 17, 33):
        critical, lower = sideband_orders(k)
        assert (critical, lower) == (2 * k, 2 * k - 2)
        assert one_alias_cut(k, 4 * k) is True


def test_invalid_cut_fails_closed():
    with pytest.raises(ValueError):
        one_alias_cut(1, 4)
    with pytest.raises(ValueError):
        one_alias_cut(3, 6)
    with pytest.raises(ValueError):
        one_alias_cut(3, 13)
    with pytest.raises(ValueError):
        one_alias_cut(3, True)


def test_tail_exponents_are_strictly_positive_diagnostics():
    exponents = tail_exponents()
    assert exponents["noise"] > Decimal("0.3")
    assert exponents["target"] > Decimal("0.05")


def test_exact_source_constant_inequalities_are_visible():
    lam = physical_constants()["lambda"]
    assert lam < Decimal(17) / 10
    assert U_RADIUS.numerator / U_RADIUS.denominator < float(lam)
    assert lam < (Decimal(10) / 7) ** 2


def test_prefix_weights_match_the_two_critical_denominators():
    for k in (3, 5, 9, 17, 33):
        critical, lower = sideband_orders(k)
        radius = Decimal(7) / 5
        assert abs(prefix_weight(critical) - radius**critical / Decimal(critical)) < Decimal("1e-20")
        assert abs(prefix_weight(lower) - radius**lower / Decimal(lower)) < Decimal("1e-20")


def test_diagnostics_keep_both_orders_inside_the_common_cut():
    for k in (3, 5, 9, 17, 33):
        row = synchronization_diagnostic(k)
        assert row["u"] == 4 * k
        assert 2 * k < row["u"] <= 4 * k
        assert row["critical_order"] == 2 * k
        assert row["lower_sideband_order"] == 2 * k - 2
        assert row["finite_rows_are_diagnostics_only"] is True


def test_two_atom_majorant_grows_with_the_clock():
    rows = [synchronization_diagnostic(k) for k in (5, 9, 17, 33)]
    assert rows[-1]["separate_absolute_two_atom_majorant_diagnostic"] > rows[0][
        "separate_absolute_two_atom_majorant_diagnostic"
    ]
    assert rows[-1]["separate_absolute_two_atom_majorant_diagnostic"] > Decimal(1000)
