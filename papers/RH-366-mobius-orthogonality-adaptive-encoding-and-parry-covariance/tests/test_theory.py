from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import sqrt

from mobius_henon_dichotomy.core import (
    ADJACENCY,
    EVEN_COVARIANCE_RATIO,
    Qsqrt5,
    brute_force_extrema,
    capacity_extreme,
    capacity_extrema,
    covariance_exact,
    cyclic_states_from_signs,
    exceptional_score,
    exceptional_signs,
    graph_equivalence_count,
    is_admissible_signs,
    mobius_sieve,
    parry_variance_exact,
)


def test_mobius_small_values() -> None:
    assert mobius_sieve(12) == [0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0]


def test_exceptional_word_and_integer_identity() -> None:
    mu = mobius_sieve(10_000)
    signs = exceptional_signs(mu)
    direct, identity = exceptional_score(mu)
    assert is_admissible_signs(signs[1:])
    assert direct == identity


def test_residue_rule_prevents_distance_two_plus_pairs() -> None:
    mu = mobius_sieve(4096)
    signs = exceptional_signs(mu)
    for index in range(1, len(signs) - 2):
        assert not (signs[index] == signs[index + 2] == 1)


def test_cyclic_sign_rule_matches_frozen_graph() -> None:
    audit = graph_equivalence_count(8)
    assert audit["pass"] is True
    assert audit["checked"] == sum(2**length for length in range(3, 9))


def test_each_admissible_cyclic_word_has_valid_state_edges() -> None:
    for length in range(3, 8):
        for word in product((-1, 1), repeat=length):
            if not is_admissible_signs(word, cyclic=True):
                continue
            states = cyclic_states_from_signs(word)
            assert all(ADJACENCY[states[i]][states[(i + 1) % length]] for i in range(length))


def test_capacity_dynamic_program_matches_brute_force_through_twelve() -> None:
    mu = mobius_sieve(12)
    for length in range(1, 13):
        assert capacity_extrema(mu[1:length + 1]) == brute_force_extrema(mu[1:length + 1])


def test_capacity_witnesses_are_admissible_and_recompute() -> None:
    values = mobius_sieve(64)[1:]
    for maximize in (False, True):
        score, signs = capacity_extreme(values, maximize=maximize)
        assert is_admissible_signs(signs)
        assert score == sum(value * sign for value, sign in zip(values, signs))


def test_exact_covariance_base_and_recurrence() -> None:
    assert covariance_exact(0) == Qsqrt5(Fraction(1), Fraction(0))
    assert covariance_exact(1) == Qsqrt5()
    assert covariance_exact(2) == EVEN_COVARIANCE_RATIO
    for k in range(5):
        assert covariance_exact(2 * k + 1) == Qsqrt5()
        assert covariance_exact(2 * (k + 1)) == covariance_exact(2 * k) * EVEN_COVARIANCE_RATIO


def test_exact_covariance_numeric_values() -> None:
    ratio = -(3.0 - sqrt(5.0)) / 2.0
    for lag in range(11):
        expected = 0.0 if lag % 2 else ratio ** (lag // 2)
        assert abs(covariance_exact(lag).numeric() - expected) < 1.0e-14


def test_exact_variance_is_nonnegative_and_obeys_sqrt5_bound() -> None:
    mu = mobius_sieve(32)
    for length in range(1, 33):
        value = parry_variance_exact(mu, length).numeric()
        assert value >= -1.0e-12
        assert value <= sqrt(5.0) * length + 1.0e-12
