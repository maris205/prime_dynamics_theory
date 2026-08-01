from decimal import Decimal

import pytest

from sideband_atom import (
    sideband_component_index,
    sideband_diagnostic,
    sideband_in_one_alias_cut,
    sideband_order,
)


def test_first_lower_even_sideband_is_mandatory_for_every_cut():
    for k in (3, 5, 9, 17, 33):
        assert sideband_order(k) == 2 * k - 2
        assert sideband_component_index(k) == k - 1
        for cut in (2 * k + 1, 3 * k, 4 * k):
            assert sideband_in_one_alias_cut(k, cut) is True


def test_invalid_cut_and_small_k_fail_closed():
    with pytest.raises(ValueError):
        sideband_order(2)
    with pytest.raises(ValueError):
        sideband_in_one_alias_cut(3, 6)
    with pytest.raises(ValueError):
        sideband_in_one_alias_cut(3, 13)


def test_period_2k_minus_2_orbit_subset_is_far_on_the_k_clock():
    for k in (3, 5, 9, 17, 33):
        row = sideband_diagnostic(k)
        assert row["sideband_order"] == 2 * k - 2
        assert row["excluded_index"] == 2 * k - 4
        assert row["certified_subset_count"] == 2 * k - 3
        assert row["certified_subset_far_count"] == 2 * k - 3
        assert row["orbit_closure_error"] < Decimal("1e-70")


def test_weighted_identity_is_exact_to_decimal_precision():
    for k in (3, 5, 9, 17, 33):
        row = sideband_diagnostic(k)
        assert row["weighted_identity_error"] < Decimal("1e-90")


def test_atom_is_super_target_and_its_weighted_absolute_term_grows():
    rows = [sideband_diagnostic(k) for k in (5, 9, 17, 33)]
    assert rows[-1]["atom_over_sideband_target"] > rows[0]["atom_over_sideband_target"]
    assert rows[-1]["atom_over_sideband_target"] > Decimal(1000)
    assert rows[-1]["absolute_weighted_atom"] > rows[0]["absolute_weighted_atom"]


def test_window_parameter_must_be_positive():
    with pytest.raises(ValueError):
        sideband_diagnostic(3, window_A=0)
