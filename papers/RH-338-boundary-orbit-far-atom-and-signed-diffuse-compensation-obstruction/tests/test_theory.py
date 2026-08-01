from decimal import Decimal

import pytest

from far_atom import (
    boundary_orbit,
    boundary_point,
    certified_far_count,
    diagnostic_row,
    fixed_gap_diagnostics,
    physical_constants,
)


def test_physical_constants_have_the_archived_ordering():
    constants = physical_constants()
    assert Decimal(1) < constants["u_c"] < Decimal(2)
    assert Decimal(1) < constants["lambda"] < Decimal(2)
    assert constants["r"] < constants["b"] < Decimal(1)
    assert constants["beta"] > 0


def test_three_fixed_gap_diagnostics_are_strictly_positive():
    gaps = fixed_gap_diagnostics()
    assert all(value > 0 for value in gaps.values())


def test_certified_subset_deletes_exactly_one_marked_point():
    for k in (2, 4, 8, 16, 32):
        assert certified_far_count(k) == 2 * k - 1
    with pytest.raises(ValueError):
        certified_far_count(1)


def test_decimal_boundary_orbits_reproduce_the_analytic_far_subset():
    for k in (2, 4, 8, 16, 32):
        row = diagnostic_row(k)
        assert row["excluded_index"] == 2 * k - 2
        assert row["certified_subset_count"] == 2 * k - 1
        assert row["certified_subset_far_count"] == 2 * k - 1
        assert row["orbit_closure_error"] < Decimal("1e-70")


def test_atom_is_alias_sized_and_super_target_in_finite_diagnostics():
    rows = [diagnostic_row(k) for k in (4, 8, 16, 32)]
    errors = [abs(row["atom_over_alias"] - 1) for row in rows]
    assert errors[-1] < errors[0]
    assert rows[-1]["atom_over_target"] > rows[0]["atom_over_target"]
    assert rows[-1]["atom_over_target"] > Decimal(1000)


def test_invalid_domains_fail_closed():
    with pytest.raises(ValueError):
        boundary_point(0)
    with pytest.raises(ValueError):
        boundary_orbit(1)
    with pytest.raises(ValueError):
        diagnostic_row(2, window_A=0)
