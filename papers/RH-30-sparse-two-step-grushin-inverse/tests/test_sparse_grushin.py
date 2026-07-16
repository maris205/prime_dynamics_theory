from __future__ import annotations

import numpy as np
from scipy.sparse import csr_matrix

from sparse_grushin import (
    build_sparse_grushin_system,
    combine_frobenius_bounds,
    dense_lifted_complement,
    neumann_inverse_certificate,
)


def synthetic_factors(seed: int = 20260716):
    rng = np.random.default_rng(seed)
    dimension = 7
    packet_rank = 2
    peripheral_rank = 2
    matrix = 0.18 * rng.standard_normal((dimension, dimension))
    right = rng.standard_normal((dimension, peripheral_rank))
    left = rng.standard_normal((dimension, peripheral_rank))
    values = np.array([0.7, -0.5])
    synthesis = rng.standard_normal((dimension, packet_rank))
    analysis = np.linalg.pinv(synthesis)
    dangerous_left = rng.standard_normal(dimension) + 1.0j * rng.standard_normal(
        dimension
    )
    dangerous_right = rng.standard_normal(dimension) + 1.0j * rng.standard_normal(
        dimension
    )
    return (
        matrix,
        right,
        left,
        values,
        synthesis,
        analysis,
        dangerous_left,
        dangerous_right,
    )


def test_bordered_schur_inverse_block_matches_lifted_inverse() -> None:
    factors = synthetic_factors()
    singular = 0.04
    point = 0.31 - 0.47j
    system = build_sparse_grushin_system(
        csr_matrix(factors[0]),
        *factors[1:],
        singular,
        point,
    )
    lifted = dense_lifted_complement(
        factors[0],
        *factors[1:],
        singular,
        point,
    )
    inverse = np.linalg.inv(system.matrix.toarray())
    leading = inverse[: lifted.shape[0], : lifted.shape[0]]
    np.testing.assert_allclose(leading, np.linalg.inv(lifted), rtol=2.0e-11, atol=2.0e-11)


def test_channel_balancing_preserves_low_rank_product() -> None:
    factors = synthetic_factors(7)
    singular = 0.03
    point = -0.12 - 0.38j
    balanced = build_sparse_grushin_system(
        csr_matrix(factors[0]),
        *factors[1:],
        singular,
        point,
        balance_channels=True,
    )
    raw = build_sparse_grushin_system(
        csr_matrix(factors[0]),
        *factors[1:],
        singular,
        point,
        balance_channels=False,
    )
    np.testing.assert_allclose(
        balanced.update.columns @ balanced.update.rows,
        raw.update.columns @ raw.update.rows,
        rtol=3.0e-13,
        atol=3.0e-13,
    )


def test_auxiliary_scaling_preserves_physical_inverse_block() -> None:
    factors = synthetic_factors(99)
    singular = 0.025
    point = 0.22 - 0.41j
    lifted = dense_lifted_complement(
        factors[0],
        *factors[1:],
        singular,
        point,
    )
    reference = np.linalg.inv(lifted)
    for scale in (0.25, 1.0, 4.0):
        system = build_sparse_grushin_system(
            csr_matrix(factors[0]),
            *factors[1:],
            singular,
            point,
            auxiliary_scale=scale,
        )
        leading = np.linalg.inv(system.matrix.toarray())[:7, :7]
        np.testing.assert_allclose(leading, reference, rtol=3.0e-11, atol=3.0e-11)


def test_frobenius_neumann_certificate_bounds_inverse() -> None:
    matrix = np.array([[2.0, -0.3], [0.4, 1.7]], dtype=np.complex128)
    approximate = np.linalg.inv(matrix) + np.array(
        [[1.0e-4, -2.0e-4], [0.0, 1.0e-4]], dtype=np.complex128
    )
    inverse_upper = combine_frobenius_bounds(
        [np.linalg.norm(approximate[:, :1]), np.linalg.norm(approximate[:, 1:])]
    )
    residual_upper = combine_frobenius_bounds(
        [
            np.linalg.norm((np.eye(2) - matrix @ approximate)[:, :1]),
            np.linalg.norm((np.eye(2) - matrix @ approximate)[:, 1:]),
        ]
    )
    certificate = neumann_inverse_certificate(inverse_upper, residual_upper)
    assert certificate.admissible
    assert certificate.inverse_two_norm_upper >= np.linalg.norm(
        np.linalg.inv(matrix), 2
    )


def test_neumann_certificate_rejects_unit_residual() -> None:
    certificate = neumann_inverse_certificate(2.0, 1.0)
    assert not certificate.admissible
    assert np.isinf(certificate.inverse_two_norm_upper)
