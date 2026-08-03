from decimal import Decimal
from fractions import Fraction

import pytest

from lower_even_ladder import (
    ladder_row,
    lower_even_entry,
    physical_constants,
    typed_compensation_fixture,
)


def test_punctured_ladder_excludes_the_two_selected_orders():
    for k in (8, 12, 16, 20):
        row = ladder_row(k)
        assert row["m_end"] == k - 2
        assert row["order_count"] == k - 3
        assert all(entry["order"] not in (2 * k, 2 * k - 2) for entry in row["entries"])


def test_each_full_atom_weight_is_exactly_one_point_weight_times_R_power():
    for k in (8, 12, 16):
        row = ladder_row(k)
        assert row["max_orbit_identity_error"] < Decimal("1e-80")


def test_orbit_ladder_tracks_the_geometric_asymptotic():
    rows = [ladder_row(k) for k in (8, 12, 16, 20)]
    errors = [abs(row["orbit_over_asymptotic"] - 1) for row in rows]
    assert errors[-1] < errors[0]
    assert abs(rows[-1]["orbit_over_exact_geometric"] - 1) < Decimal("0.04")


def test_radial_aggregate_is_lower_order_than_the_orbit_ladder():
    rows = [ladder_row(k) for k in (8, 12, 16, 20)]
    ratios = [row["absolute_radial_over_orbit"] for row in rows]
    assert ratios[-1] < ratios[0]
    assert ratios[-1] < Decimal("0.08")


def test_combined_absolute_demand_has_the_same_leading_mass():
    rows = [ladder_row(k) for k in (8, 12, 16, 20)]
    errors = [abs(row["absolute_combined_over_orbit"] - 1) for row in rows]
    assert errors[-1] < errors[0]
    assert errors[-1] < Decimal("0.08")
    assert rows[-1]["combined_demand_weighted_sum"] > 0


def test_orbit_ladder_is_exponentially_growing():
    rows = [ladder_row(k) for k in (8, 12, 16, 20)]
    masses = [row["orbit_weighted_sum"] for row in rows]
    assert all(right > left for left, right in zip(masses, masses[1:]))
    assert masses[-1] > Decimal(100)


def test_reverse_triangle_fixture_is_exact():
    fixture = typed_compensation_fixture(
        demands=(Fraction(3, 2), Fraction(5, 3), Fraction(7, 4)),
        supplies=(Fraction(3, 2), Fraction(5, 3), Fraction(9, 4)),
    )
    assert fixture["dimension"] == 3
    assert fixture["residual_mass"] == Fraction(1, 2)
    assert fixture["reverse_triangle_slack"] >= 0


def test_superunit_ratio_is_source_consistent():
    constants = physical_constants()
    assert constants["lambda"] > 1
    assert constants["x"] > 1


def test_invalid_domains_fail_closed():
    with pytest.raises(ValueError):
        physical_constants(40)
    with pytest.raises(ValueError):
        lower_even_entry(4, 2)
    with pytest.raises(ValueError):
        lower_even_entry(8, 7)
    with pytest.raises(ValueError):
        ladder_row(8, 1)
    with pytest.raises(ValueError):
        typed_compensation_fixture((Fraction(1),), ())
