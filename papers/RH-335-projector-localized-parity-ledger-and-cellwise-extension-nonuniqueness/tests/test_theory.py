from fractions import Fraction

import pytest

from projector_ledger import (
    E_MINUS_FIXTURE,
    K_FIXTURE,
    LEFT_MINUS,
    RIGHT_MINUS,
    commutator_fixture,
    exact_fixture_audit,
    extension_nonuniqueness_fixture,
    identity,
    localized_ledger_fixture,
    matrix_add,
    matrix_multiply,
    matrix_scale,
    matrix_trace,
    outer,
    perron_projector,
    projector_masses,
    remaining_projector,
    scaled_rank_one_projector,
    vector_dot,
    vector_sum,
)


F = Fraction


def test_fixture_is_strictly_positive_row_stochastic():
    assert all(value > 0 for row in K_FIXTURE for value in row)
    assert tuple(vector_sum(row) for row in K_FIXTURE) == (F(1), F(1), F(1))


def test_three_exact_spectral_projectors_resolve_the_identity():
    audit = exact_fixture_audit()
    e_zero = perron_projector()
    e_plus = remaining_projector()
    assert matrix_add(matrix_add(e_zero, E_MINUS_FIXTURE), e_plus) == identity(3)
    assert audit["cross_projector_products_zero"] is True
    assert matrix_multiply(K_FIXTURE, e_zero) == e_zero
    assert matrix_multiply(K_FIXTURE, E_MINUS_FIXTURE) == matrix_scale(
        -F(2, 5), E_MINUS_FIXTURE
    )
    assert matrix_multiply(K_FIXTURE, e_plus) == matrix_scale(F(1, 5), e_plus)


def test_minus_projector_is_rank_one_idempotent_and_two_sided_spectral():
    assert vector_dot(LEFT_MINUS, RIGHT_MINUS) == 1
    assert outer(RIGHT_MINUS, LEFT_MINUS) == E_MINUS_FIXTURE
    assert matrix_multiply(E_MINUS_FIXTURE, E_MINUS_FIXTURE) == E_MINUS_FIXTURE
    expected = matrix_scale(-F(2, 5), E_MINUS_FIXTURE)
    assert matrix_multiply(K_FIXTURE, E_MINUS_FIXTURE) == expected
    assert matrix_multiply(E_MINUS_FIXTURE, K_FIXTURE) == expected
    assert matrix_trace(E_MINUS_FIXTURE) == 1


def test_left_right_normalization_scaling_does_not_change_projector():
    assert scaled_rank_one_projector(F(7, 3), F(11, 5)) == E_MINUS_FIXTURE
    assert scaled_rank_one_projector(-F(11, 5), F(13, 7)) == E_MINUS_FIXTURE
    with pytest.raises(ValueError):
        scaled_rank_one_projector(F(0), F(1))
    with pytest.raises(ValueError):
        scaled_rank_one_projector(F(1), F(0))


def test_projector_singleton_masses_form_a_signed_measure_not_probabilities():
    masses = projector_masses()
    assert masses == (F(10, 17), -F(4, 51), F(25, 51))
    assert vector_sum(masses) == 1
    assert masses[1] < 0


def test_localized_corrected_cells_have_the_independently_checked_values():
    ledger = localized_ledger_fixture()
    assert ledger["localized_noisy"] == (F(43, 85), F(53, 425), F(242, 425))
    assert ledger["parity_scalar"] == F(21, 25)
    assert ledger["corrected_cells"] == (
        F(400, 289),
        F(400, 4913),
        F(6672, 4913),
    )


def test_localized_partition_sum_equals_global_hardy_difference():
    ledger = localized_ledger_fixture()
    assert ledger["corrected_total"] == F(48, 17)
    assert ledger["global_difference"] == F(48, 17)
    assert ledger["corrected_total"] == ledger["global_difference"]


def test_perron_plus_parity_local_deflation_strictly_fails_to_commute():
    fixture = commutator_fixture()
    assert fixture["commutator_is_nonzero"] is True
    assert fixture["commutator"] == (
        (F(0), -F(7, 85), F(0)),
        (F(207, 425), F(0), F(109, 255)),
        (F(0), -F(29, 255), F(0)),
    )
    assert fixture["commutator_trace"] == 0


def test_zero_total_signed_extension_changes_cells_but_not_global_scalar():
    fixture = extension_nonuniqueness_fixture()
    assert fixture["projector_gauge_allocation"] == (
        F(42, 85),
        -F(28, 425),
        F(7, 17),
    )
    assert fixture["zero_total_perturbation"] == (F(1, 51), -F(1, 51), F(0))
    assert fixture["perturbation_total"] == 0
    assert fixture["allocations_are_distinct"] is True
    assert fixture["base_total"] == fixture["alternative_total"] == F(21, 25)


def test_n2_fixture_is_not_mutated_into_an_invalid_k1_counterloop_claim():
    fixture = localized_ledger_fixture()
    assert fixture["n"] == 2
    assert "k" not in fixture
