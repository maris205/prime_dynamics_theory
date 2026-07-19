from __future__ import annotations

import math

import numpy as np
from scipy.sparse import csr_matrix

from bulk_trace import (
    bulk_square_determinant,
    bulk_trace_norm_ledger,
    determinant_lipschitz_upper,
    even_trace_error_upper,
    hilbert_schmidt_galerkin_defect,
    low_rank_bulk_log_determinant,
    permutation_sign,
)


def trace_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.svd(matrix, compute_uv=False).sum())


def test_hilbert_schmidt_square_lands_in_trace_norm() -> None:
    rng = np.random.default_rng(20260721)
    first = rng.normal(size=(9, 9)) / 4.0
    second = rng.normal(size=(9, 9)) / 4.0
    actual = trace_norm(first @ first - second @ second)
    upper = np.linalg.norm(first - second, ord="fro") * (
        np.linalg.norm(first, ord="fro")
        + np.linalg.norm(second, ord="fro")
    )
    assert actual <= upper * (1.0 + 1.0e-13)


def test_bulk_ledger_is_exactly_the_trace_ideal_composition() -> None:
    ledger = bulk_trace_norm_ledger(
        markov_hilbert_schmidt_error_upper=0.03,
        perron_weighted_operator_error_upper=0.01,
        parity_weighted_operator_error_upper=0.02,
        continuum_bulk_hilbert_schmidt_upper=4.0,
    )
    expected_weighted = math.sqrt(2.0) * 0.03
    assert ledger.rank_two_weighted_hilbert_schmidt_error_upper >= expected_weighted
    assert ledger.rank_two_weighted_hilbert_schmidt_error_upper < expected_weighted * (
        1.0 + 1.0e-14
    )
    expected_bulk = 0.03 + expected_weighted
    assert ledger.bulk_hilbert_schmidt_error_upper >= expected_bulk
    expected_trace = expected_bulk * (4.0 + 4.0 + expected_bulk)
    assert ledger.square_trace_norm_error_upper >= expected_trace
    assert ledger.square_trace_norm_error_upper < expected_trace * (1.0 + 1.0e-14)


def test_cellwise_poincare_rate_is_first_order() -> None:
    first = hilbert_schmidt_galerkin_defect(1024, 3.0, 4.0)
    second = hilbert_schmidt_galerkin_defect(2048, 3.0, 4.0)
    assert second == first / 2.0


def test_fredholm_determinant_lipschitz_bound() -> None:
    rng = np.random.default_rng(45)
    first = rng.normal(size=(5, 5)) / 20.0
    second = first + rng.normal(size=(5, 5)) / 1000.0
    radius = 0.1
    actual = abs(
        np.linalg.det(np.eye(5) - radius * first)
        - np.linalg.det(np.eye(5) - radius * second)
    )
    upper = determinant_lipschitz_upper(
        disk_radius=radius,
        trace_norm_error_upper=trace_norm(first - second),
        first_trace_norm_upper=trace_norm(first),
        second_trace_norm_upper=trace_norm(second),
    )
    assert actual <= upper


def test_even_trace_telescoping_bound() -> None:
    rng = np.random.default_rng(51)
    first = rng.normal(size=(4, 4)) / 10.0
    second = first + rng.normal(size=(4, 4)) / 100.0
    power = 4
    actual = abs(
        np.trace(np.linalg.matrix_power(first, power))
        - np.trace(np.linalg.matrix_power(second, power))
    )
    upper = even_trace_error_upper(
        square_power=power,
        square_trace_norm_error_upper=trace_norm(first - second),
        square_operator_norm_upper=max(
            np.linalg.norm(first, ord=2), np.linalg.norm(second, ord=2)
        ),
    )
    assert actual <= upper * (1.0 + 1.0e-13)


def test_sparse_rank_two_determinant_lemma_matches_dense() -> None:
    rng = np.random.default_rng(3)
    matrix = rng.normal(size=(10, 10)) / 25.0
    right = rng.normal(size=(10, 2))
    left = rng.normal(size=(10, 2))
    values = np.asarray((0.7, -0.4))
    bulk = matrix - (right * values[None, :]) @ left.T
    parameter = 0.13
    computed = low_rank_bulk_log_determinant(
        csr_matrix(matrix), right, left, values, parameter
    ).value
    expected = np.linalg.det(np.eye(10) - parameter * bulk)
    assert np.isclose(computed, expected, rtol=2.0e-13, atol=2.0e-13)


def test_symmetric_det2_identity_for_bulk_square() -> None:
    rng = np.random.default_rng(9)
    matrix = rng.normal(size=(8, 8)) / 30.0
    right = rng.normal(size=(8, 2))
    left = rng.normal(size=(8, 2))
    values = np.asarray((0.6, -0.3))
    bulk = matrix - (right * values[None, :]) @ left.T
    w = 0.02
    computed = bulk_square_determinant(
        csr_matrix(matrix), right, left, values, w
    )
    expected = np.linalg.det(np.eye(8) - w * (bulk @ bulk))
    assert np.isclose(
        computed.square_determinant, expected, rtol=2.0e-13, atol=2.0e-13
    )
    assert computed.symmetric_det2_identity_error < 1.0e-13


def test_permutation_sign() -> None:
    assert permutation_sign(np.asarray((0, 1, 2, 3))) == 1
    assert permutation_sign(np.asarray((1, 0, 2, 3))) == -1
    assert permutation_sign(np.asarray((1, 2, 0, 3))) == 1
