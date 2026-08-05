from __future__ import annotations

from math import isclose

from prime_return_zeta.core import (
    A0,
    dirichlet_coefficient,
    first_coordinates,
    gcd_sequence,
    henon,
    henon_inverse,
    local_cycle_determinant,
    local_cycle_trace,
    low_rank_prime_set,
    modular_return_rank,
    primes_up_to,
    return_divisibility_holds,
)


def test_polynomial_inverse_exact() -> None:
    for point in ((0, 0), (1, -2), (-7, 11), (123, -456)):
        assert henon_inverse(henon(point)) == point
        assert henon(henon_inverse(point)) == point


def test_a0_escape_prefix_and_gcd_terms() -> None:
    coordinates = first_coordinates(A0, 6)
    assert coordinates[:5] == [0, 1, -5, -150, -134994]
    assert all(value < 0 for value in coordinates[2:])
    assert all(
        abs(coordinates[index]) > abs(coordinates[index - 1])
        for index in range(3, len(coordinates))
    )
    assert gcd_sequence(A0, 4) == [1, 1, 5, 6]


def test_return_divisibility_finite_reproduction() -> None:
    assert return_divisibility_holds(A0, primes_up_to(43), 12)


def test_low_rank_prime_identity_at_threshold_five() -> None:
    direct = [
        prime
        for prime in primes_up_to(43)
        if modular_return_rank(A0, prime) < 5
    ]
    assert low_rank_prime_set(A0, 5) == direct == [2, 3, 5]


def test_rank_bound_for_reduced_permutation() -> None:
    for prime in primes_up_to(101):
        assert 1 <= modular_return_rank(A0, prime) <= prime * prime


def test_local_cycle_trace_and_determinant() -> None:
    for rank in range(1, 9):
        assert [local_cycle_trace(rank, n) for n in range(1, 2 * rank + 1)].count(rank) == 2
        z = 0.17 + 0.11j
        assert isclose(
            abs(local_cycle_determinant(rank, z) - (1 - z**rank)),
            0.0,
            abs_tol=1e-15,
        )


def test_dirichlet_coefficients_are_zero_one_and_not_completely_multiplicative() -> None:
    ranks = {2: 4, 3: 4, 5: 3}
    assert dirichlet_coefficient(1, ranks) == 1
    assert dirichlet_coefficient(2, ranks) == 0
    assert dirichlet_coefficient(2**4, ranks) == 1
    assert dirichlet_coefficient(3**4 * 5**3, ranks) == 1
    assert dirichlet_coefficient(3**2 * 5**3, ranks) == 0


def test_inverse_length_block_identity_is_rank_insensitive() -> None:
    prime = 7
    s = 2.5
    for rank in (1, 2, 5, 13):
        z = prime ** (-s / rank)
        assert isclose(local_cycle_determinant(rank, z), 1 - prime ** (-s))
