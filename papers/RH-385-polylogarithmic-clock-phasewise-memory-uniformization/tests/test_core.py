"""Independent finite-interface tests for RH-385."""

from copy import deepcopy
from fractions import Fraction
from math import lcm

import pytest

from polylog_clock import (
    CERTIFICATE_FIXTURE_SHA256,
    MUTATION_NAMES,
    apply_mutation,
    build_certificate,
    coefficient_vector,
    compatible,
    cutoff_mask,
    finite_clock_extrema,
    payload_sha256,
    plus_edges,
    primorial_square,
    truth_values,
    verify_certificate,
    zero_table_ids,
)


@pytest.fixture(scope="module")
def certificate() -> dict[str, object]:
    return build_certificate()


def test_exact_certificate_digest_and_counts(certificate: dict[str, object]) -> None:
    assert payload_sha256(certificate) == CERTIFICATE_FIXTURE_SHA256
    assert certificate["counts"] == {
        "truth_tables": 512,
        "interpolation_evaluations": 4608,
        "phasewise_c11_zero_tables": 192,
        "distinct_zero_score_vectors": 24,
        "cutoff_period_rows": 4,
        "dft_channels": 3,
        "triangular_clock_rows": 3,
        "mutation_rows": 24,
    }


def test_truth_table_enumeration_and_c11_histogram(certificate: dict[str, object]) -> None:
    assert len({truth_values(table_id) for table_id in range(512)}) == 512
    assert certificate["coefficient_contract"]["c11_histogram"] == {
        "-1": 32, "-1/2": 128, "0": 192, "1/2": 128, "1": 32,
    }
    assert len(zero_table_ids()) == 192


def test_coefficient_alphabets_and_vector_multiplicity(certificate: dict[str, object]) -> None:
    vectors = [coefficient_vector(table_id) for table_id in zero_table_ids()]
    assert {vector[0] for vector in vectors} == {Fraction(-1), Fraction(0), Fraction(1)}
    assert {vector[1] for vector in vectors} == {Fraction(-1), Fraction(0), Fraction(1)}
    assert {vector[2] for vector in vectors} == {Fraction(0)}
    assert {vector[3] for vector in vectors} == {Fraction(-1), Fraction(0), Fraction(1)}
    assert {vector[4] for vector in vectors} == set(map(Fraction, range(-2, 3)))
    assert {vector[5] for vector in vectors} == set(map(Fraction, range(-2, 3)))
    rows = certificate["coefficient_contract"]["zero_vector_multiplicities"]
    assert len(rows) == 24 and {row["multiplicity"] for row in rows} == {8}


def test_all_4608_interpolation_rows_pass(certificate: dict[str, object]) -> None:
    rows = certificate["interpolation_evaluations"]
    assert len(rows) == 512 * 9
    assert all(row["pass"] and row["expected"] == row["actual"] for row in rows)


def test_self_compatible_c21_minus_two_witness(certificate: dict[str, object]) -> None:
    witness = certificate["coefficient_contract"]["c21_minus_two_self_compatible_witness"]
    assert witness == 40
    assert coefficient_vector(witness) == tuple(map(Fraction, (1, 0, 0, 0, -2, 0)))
    assert plus_edges(witness) == frozenset({(0, -1), (0, 1)})
    assert compatible(witness, witness)


def test_cutoff_periods_and_nonminimal_firewall(certificate: dict[str, object]) -> None:
    assert [primorial_square(cutoff) for cutoff in (2, 3, 5, 7)] == [4, 36, 900, 44100]
    contract = certificate["period_contract"]
    assert contract["periods_are_not_asserted_minimal"] is True
    row = contract["lcm_fixtures"][2]
    assert row["Q"] == lcm(row["q"], row["M_P"]) == 180
    assert row["relevant_mask_minimal_period"] == 36


def test_normalized_dft_keeps_sup_norm_factor(certificate: dict[str, object]) -> None:
    dft = certificate["dft_contract"]
    assert dft["channel_sup_norms"] == [1, 1, 2]
    assert dft["channel_total"] == 4
    fixture = dft["c21_factor_two_fixture"]
    assert fixture["period_values"] == [-2, -2, 0, -2]
    assert fixture["l1"] == "3"
    assert fixture["exceeds_sqrt_Q_without_sup_norm"] is True
    assert fixture["within_factor_two_bound"] is True


def test_square_mask_means(certificate: dict[str, object]) -> None:
    rows = certificate["square_means"]
    assert [(row["one_count"], row["pair_count"]) for row in rows] == [
        (3, 2), (24, 14), (576, 322), (27648, 15134),
    ]
    assert all(row["one_mean"] == row["one_formula"] for row in rows)
    assert all(row["pair_mean"] == row["pair_formula"] for row in rows)


def test_tail_and_padding_ledger(certificate: dict[str, object]) -> None:
    tail = certificate["tail_and_padding"]
    assert tail["tail_fixture"]["difference_count"] == 118
    assert tail["tail_fixture"]["finite_tail_total"] == 8
    assert tail["tail_fixture"]["limit_tail_total"] == 5
    assert tail["ledger"] == {
        "fourier_multiplier": 4,
        "tail_multiplier": 13,
        "period_multiplier": 6,
        "padding_multiplier": 4,
    }
    assert sum(row["cost"] for row in tail["padding_rows"]) == 4
    assert tail["eta_zero"] == 0 and tail["eta_minus_one"] == 1


def test_small_clock_triangular_dp_is_independent(certificate: dict[str, object]) -> None:
    expected = [(-22, 34), (-22, 34), (-32, 34)]
    assert [finite_clock_extrema(96, q) for q in (1, 2, 3)] == expected
    rows = certificate["small_clock_triangular_dp"]
    assert [(row["minimum_sum"], row["maximum_sum"]) for row in rows] == expected
    assert [row["G_N"] for row in rows] == ["17/48"] * 3


def test_diagonal_empty_sentinel(certificate: dict[str, object]) -> None:
    assert certificate["diagonal_sentinel"] == {
        "first_square_clock": 36,
        "below_36": "no_square_clock_available",
        "never_substitute_q1": True,
    }


def test_twenty_four_mutations_fail_field_level_semantic_verification(certificate: dict[str, object]) -> None:
    assert len(MUTATION_NAMES) == len(set(MUTATION_NAMES)) == 24
    for name in MUTATION_NAMES:
        mutated = apply_mutation(certificate, name)
        assert payload_sha256(mutated) != payload_sha256(certificate), name
        with pytest.raises((ArithmeticError, KeyError, RuntimeError, TypeError, ValueError)):
            verify_certificate(mutated, compare_fresh=False)


def test_bool_for_int_alias_is_rejected(certificate: dict[str, object]) -> None:
    attacks = (
        ("coefficient_contract", "c01_alphabet", 1, False),
        ("truth_tables", 0, "truth", 0, True),
        ("dft_contract", "channel_sup_norms", 0, True),
        ("tail_and_padding", "eta_zero", False),
        ("tail_and_padding", "eta_minus_one", True),
    )
    for attack in attacks:
        mutated = deepcopy(certificate)
        *path, replacement = attack
        target = mutated
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = replacement
        with pytest.raises(ValueError):
            verify_certificate(mutated, compare_fresh=False)


def test_semantic_metadata_rebinding_and_nonboolean_mode_fail(certificate: dict[str, object]) -> None:
    attacks = (
        ("period_contract", "lcm_fixtures", 0, "kind", "rebound"),
        ("dft_contract", "normalization", "rebound"),
        ("dft_contract", "c21_factor_two_fixture", "sqrt_Q", 3),
        ("tail_and_padding", "padding_rows", 0, "reason", "rebound"),
        ("diagonal_sentinel", "first_square_clock", 35),
        ("coefficient_contract", "names", 0, "rebound"),
    )
    for attack in attacks:
        mutated = deepcopy(certificate)
        *path, replacement = attack
        target = mutated
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = replacement
        with pytest.raises(ValueError):
            verify_certificate(mutated, compare_fresh=False)
    for invalid in (0, 1, "false", None):
        with pytest.raises(TypeError):
            verify_certificate(certificate, compare_fresh=invalid)


def test_public_integer_apis_reject_bool_and_bad_cutoff() -> None:
    with pytest.raises(TypeError):
        truth_values(True)
    with pytest.raises(TypeError):
        primorial_square(False)
    with pytest.raises(ValueError):
        cutoff_mask(1, 1)
