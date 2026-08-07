from fractions import Fraction

from phasewise_memory.core import (
    EulerValue,
    FIXED_CLOCK_EXPECTED,
    _decimal_partial_kappa_interval,
    canonical_census,
    certified_constants,
    cofinal_lift_protocol,
    density_aggregation_certificate,
    density_vectors,
    fixed_clock_certificate,
    q36_strict_gain_certificate,
    square_clock_certificate,
    value_sign,
)


def test_512_and_192_census() -> None:
    census = canonical_census()
    assert census["all_pass"]
    assert census["total_tables"] == 512
    assert census["c11_zero_tables"] == 192
    assert census["canonical_target_counts"] == {"0": 120, "J": 40, "K": 24, "I": 8}
    assert census["compatibility_matrix"] == [
        [True, True, True, True],
        [True, True, False, False],
        [True, True, False, False],
        [True, True, False, False],
    ]
    assert census["subset_reduction_precedes_k_to_i"]
    assert census["k_i_full_compatibility_equivalent"]
    assert census["reflection_neighbor_pair_checks"] == 512 * 512
    assert census["reflection_neighbor_pair_failures"] == 0


def test_certified_comparator_and_density_normalization() -> None:
    constants = certified_constants()
    assert constants.pi2_low < constants.pi2_high
    assert constants.kappa_low < constants.kappa_high
    assert constants.h_low < constants.h_high
    assert value_sign(EulerValue(Fraction(1, 2), Fraction(-1, 7))) > 0
    ambiguous = EulerValue(-(constants.h_low + constants.h_high) / 2, Fraction(1))
    try:
        value_sign(ambiguous, constants)
    except ArithmeticError:
        pass
    else:
        raise AssertionError("fail-closed comparator accepted an ambiguous interval")
    for q in range(1, 13):
        delta, theta = density_vectors(q)
        assert sum(delta, Fraction(0)) == 6
        assert sum(theta, Fraction(0)) == 1


def test_directed_partial_product_contains_exact_small_cutoffs() -> None:
    for primes in ((2,), (2, 3), (2, 3, 5, 7), (2, 3, 5, 7, 11, 13)):
        exact = Fraction(1)
        for prime in primes:
            exact *= Fraction(prime * prime - 2, prime * prime)
        low, high = _decimal_partial_kappa_interval(primes, precision=18)
        assert low <= exact <= high
        assert low <= high


def test_small_clock_dp_and_independent_set_crosscheck() -> None:
    for q in range(1, 7):
        row = fixed_clock_certificate(q)
        assert row["all_pass"]
        assert row["G"] == FIXED_CLOCK_EXPECTED[q].exact_dict()


def test_exact_fixture_clocks() -> None:
    for q in (36, 180, 900):
        row = fixed_clock_certificate(q)
        assert row["all_pass"]
        assert row["G"] == FIXED_CLOCK_EXPECTED[q].exact_dict()
    assert fixed_clock_certificate(36)["formula"] == "(9/2)/pi^2-(1/7)*kappa2"


def test_q36_gain_and_square_clock_formula() -> None:
    assert q36_strict_gain_certificate()["certified_sign_pass"]
    rows = [square_clock_certificate(y, run_dp_check=False) for y in (1, 2, 3)]
    assert all(row["all_pass"] for row in rows)
    assert [row["mathcal_E_y"] for row in rows] == [1, 23, 1105]
    assert rows[0]["G_formula"] == FIXED_CLOCK_EXPECTED[36].exact_dict()
    assert rows[1]["G_formula"] == FIXED_CLOCK_EXPECTED[900].exact_dict()
    assert rows[2]["G_formula"] == FIXED_CLOCK_EXPECTED[44100].exact_dict()


def test_cofinal_protocol_rejects_uncovered_primes() -> None:
    row = cofinal_lift_protocol(180, 2)
    assert row["all_pass"]
    assert row["lift_score_pass"]
    assert row["decomposition_pass"]
    assert row["retained_independent_pass"]
    assert row["retained_one_site_weight_pass"]
    assert row["retained_bound_pass"]
    assert row["discarded_charge_precondition_pass"]
    try:
        cofinal_lift_protocol(180, 1)
    except ValueError as exc:
        assert "every odd prime divisor" in str(exc)
    else:
        raise AssertionError("uncovered odd prime was accepted")


def test_exact_density_aggregation_on_720_fibers() -> None:
    for q in (1, 3, 5, 8, 9, 16, 45, 80, 144, 720):
        row = density_aggregation_certificate(q, 720)
        assert row["all_pass"]
        assert row["fiber_size"] == 720 // q
    try:
        density_aggregation_certificate(7, 720)
    except ValueError as exc:
        assert "q | Q" in str(exc)
    else:
        raise AssertionError("non-dividing clocks were accepted")
