from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from return_entropy_tower.core import (
    A0,
    coprime_moduli_polynomial,
    evaluate_polynomial,
    fixed_point_count,
    normalized_entropy_fraction,
    pairwise_coprime,
    primes_up_to,
    return_power_moduli,
    return_rank_table,
    truncated_multiples_mobius_recovery,
    universal_first_defect,
    zeta_coefficients,
)


def test_primary_seed_return_ranks() -> None:
    primes = primes_up_to(29)
    ranks = return_rank_table(A0, primes)
    assert ranks == {
        2: 4,
        3: 4,
        5: 3,
        7: 13,
        11: 36,
        13: 20,
        17: 8,
        19: 17,
        23: 37,
        29: 6,
    }
    assert all(1 <= rank <= prime * prime for prime, rank in ranks.items())


def test_return_power_moduli_are_pairwise_coprime_and_entropy_increases() -> None:
    ranks = {2: 4, 3: 4, 5: 3, 7: 13}
    densities = []
    for level in (1, 2, 3):
        moduli = return_power_moduli(ranks, level)
        assert pairwise_coprime(moduli)
        density = normalized_entropy_fraction(moduli)
        assert Fraction(0, 1) < density < Fraction(1, 1)
        densities.append(density)
    assert densities[0] < densities[1] < densities[2]


def test_gcd_stratified_count_reduces_prime_powers_to_prime_wheel() -> None:
    ranks = {2: 4, 3: 4, 5: 3}
    expected = {1: (2, 3, 1), 2: (6, 13, 2), 3: (30, 4501, 150)}
    for level in (1, 2, 3):
        for prime_count, target in expected.items():
            prefix = dict(list(ranks.items())[:prime_count])
            row = universal_first_defect(prefix, level)
            assert (
                row["primorial_period"],
                row["fixed_point_count_at_first_defect"],
                row["primitive_orbit_defect"],
            ) == target


def test_first_zeta_coefficient_defect_is_exact() -> None:
    ranks = {2: 4, 3: 4, 5: 3}
    moduli = return_power_moduli(ranks, 2)
    coefficients = zeta_coefficients(moduli, 30)
    assert coefficients[:30] == [1] * 30
    assert coefficients[30] == 151
    assert fixed_point_count(moduli, 30) == 4501


def test_primorial_divisibility_is_the_exact_elimination_criterion() -> None:
    ranks = {2: 4, 3: 4, 5: 3}
    for level in (1, 2, 3):
        moduli = return_power_moduli(ranks, level)
        for period in range(1, 61):
            assert (fixed_point_count(moduli, period) == 1) == (period % 30 != 0)


def test_source_prime_wheel_polynomial_values() -> None:
    assert evaluate_polynomial(coprime_moduli_polynomial((2,)), 2) == 3
    assert evaluate_polynomial(coprime_moduli_polynomial((2, 3)), 2) == 13
    assert evaluate_polynomial(coprime_moduli_polynomial((2, 3, 5)), 2) == 4501


def test_truncated_multiples_mobius_identity_is_high_precision() -> None:
    ranks = {2: 4, 3: 4, 5: 3, 7: 13, 11: 36, 13: 20}
    for order in (1, 2, 3):
        row = truncated_multiples_mobius_recovery(
            ranks, order, maximum_multiplier=16, precision=80
        )
        assert row["target_moment"] > Decimal(0)
        assert row["absolute_error"] < Decimal("1e-18")
