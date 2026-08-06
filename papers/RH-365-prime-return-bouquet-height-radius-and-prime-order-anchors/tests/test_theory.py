from __future__ import annotations

from math import ceil, gcd, isclose, sqrt

import pytest

from prime_return_bouquet.core import (
    P0,
    bouquet_traces,
    certified_radius_bracket,
    distinct_prime_factors,
    finite_rank_table,
    first_coordinates,
    gcd_height_bounds,
    gcd_terms,
    height_bounds,
    height_value,
    henon,
    henon_inverse,
    local_cycle_determinant,
    logarithmic_majorant,
    midpoint_value,
    naive_schatten_partial_sum,
    primitive_rank_counts,
    trace_envelope,
    zeta_coefficients,
)


def test_integral_inverse_and_orbit_indexing() -> None:
    for point in (P0, (1, -2), (-7, 11), (123, -456)):
        assert henon_inverse(henon(point)) == point
        assert henon(henon_inverse(point)) == point
    coordinates = first_coordinates(6)
    assert coordinates == [0, 1, -5, -150, -134994, -109340280065, -71731781068155818290355]


def test_midpoint_identities_match_exact_gcd_terms() -> None:
    terms = gcd_terms(16)
    assert terms[:6] == [1, 1, 5, 6, 151, 145]
    assert [midpoint_value(order) for order in range(1, 17)] == terms


def test_quadratic_height_recurrence_and_step_bounds() -> None:
    assert height_value(2) == 5
    assert height_value(3) == 150
    coordinates = first_coordinates(16)
    for index in range(3, 16):
        assert -coordinates[index + 1] == (
            6 * (-coordinates[index]) ** 2 - (-coordinates[index - 1]) - 1
        )
    for index in range(2, 16):
        value = height_value(index)
        next_value = height_value(index + 1)
        assert 5 * value * value <= next_value <= 6 * value * value


def test_closed_height_and_gcd_bounds_include_all_special_bases() -> None:
    for index in range(2, 16):
        lower, upper = height_bounds(index)
        assert lower <= height_value(index) <= upper
    terms = gcd_terms(16)
    assert terms[2:5] == [5, 6, 151]
    for order in range(3, 17):
        lower, upper = gcd_height_bounds(order)
        assert lower <= terms[order - 1] <= upper
        middle = ceil(order / 2)
        if order >= 6:
            b_middle = height_value(middle)
            assert 25 * terms[order - 1] >= 24 * b_middle
            assert terms[order - 1] < b_middle


def test_finite_rank_counts_and_all_trace_rows() -> None:
    ranks = finite_rank_table(12)
    assert ranks[5] == 3
    assert ranks[2] == ranks[3] == 4
    assert primitive_rank_counts(12) == [0, 0, 1, 2, 1, 1, 1, 2, 1, 2, 4, 3]
    traces = bouquet_traces(12)
    assert traces == [0, 0, 3, 8, 5, 9, 7, 24, 12, 25, 44, 53]
    assert all(traces[n - 1] <= trace_envelope(n) for n in range(1, 13))


def test_odd_prime_anchors_and_raw_coefficient_firewall() -> None:
    terms = gcd_terms(12)
    ranks = finite_rank_table(12)
    counts = primitive_rank_counts(12)
    traces = bouquet_traces(12)
    for order in (3, 5, 7, 11):
        factors = distinct_prime_factors(terms[order - 1])
        assert factors
        assert all(ranks[prime] == order for prime in factors)
        assert len(factors) == counts[order - 1] == traces[order - 1] // order
    coefficients = zeta_coefficients(12)
    assert coefficients == [1, 0, 0, 1, 2, 1, 2, 3, 6, 5, 8, 13, 18]
    assert coefficients[7] == 3 != counts[6] == 1
    assert coefficients[11] == 13 != counts[10] == 4


def test_strict_analytic_majorant_and_radius_bracket() -> None:
    assert logarithmic_majorant(0.0) == 0.0
    assert 0 < logarithmic_majorant(0.5) < logarithmic_majorant(0.65)
    with pytest.raises(ValueError, match="strict certified disk"):
        logarithmic_majorant(1.0 / sqrt(2.0))
    bracket = certified_radius_bracket()
    assert isclose(bracket["lower"], 2.0 ** -0.5)
    assert bracket["upper"] == 1.0


def test_naive_direct_sum_partial_schatten_burden_and_local_factors() -> None:
    dimensions = [3, 4, 4, 5, 6]
    first = naive_schatten_partial_sum(dimensions[:2], 0.5, 2.0)
    second = naive_schatten_partial_sum(dimensions, 0.5, 2.0)
    assert 0 < first < second
    for rank in dimensions:
        z = 0.17 + 0.11j
        assert local_cycle_determinant(rank, z) == 1 - z**rank
