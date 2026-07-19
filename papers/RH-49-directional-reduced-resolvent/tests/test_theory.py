from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.sparse import csr_matrix

from directional_reduced import (
    directional_residual_upper,
    mixed_gain_from_hilbert_schmidt,
    packet_envelope,
    packet_limit_profile,
    rank_one_projection,
    reduced_resolvent_dense,
)


def test_rank_one_deflation_equals_laurent_subtraction() -> None:
    rng = np.random.default_rng(4901)
    basis = rng.normal(size=(7, 7)) + 1j * rng.normal(size=(7, 7))
    while abs(np.linalg.det(basis)) < 1.0e-4:
        basis = rng.normal(size=(7, 7)) + 1j * rng.normal(size=(7, 7))
    eigenvalues = np.asarray((1.0, -0.91, 0.63, -0.4, 0.2j, -0.2j, 0.05))
    inverse_basis = np.linalg.inv(basis)
    operator = basis @ np.diag(eigenvalues) @ inverse_basis
    index = 1
    right = basis[:, index]
    left = np.conjugate(inverse_basis[index, :])
    projection = rank_one_projection(right, left)
    z = -0.83 + 0.07j
    reduced = reduced_resolvent_dense(
        operator, z, eigenvalues[index], right, left
    )
    laurent = np.linalg.inv(z * np.eye(7) - operator) - projection / (
        z - eigenvalues[index]
    )
    assert np.linalg.norm(projection @ projection - projection) < 2.0e-13
    assert np.linalg.norm(operator @ projection - projection @ operator) < 2.0e-12
    assert np.linalg.norm(reduced - laurent) < 2.0e-11


def test_stable_rank_transfer_bounds_both_mixed_placements() -> None:
    rng = np.random.default_rng(4902)
    b = rng.normal(size=(8, 6))
    c = rng.normal(size=(5, 8))
    left = rng.normal(size=(8, 8))
    right = rng.normal(size=(8, 8))
    left_image = left @ b
    right_image = c @ right
    left_hs_gain = np.linalg.norm(left_image, "fro") / np.linalg.norm(b, "fro")
    right_hs_gain = np.linalg.norm(right_image, "fro") / np.linalg.norm(c, "fro")
    left_operator_gain = np.linalg.norm(left_image, 2) / np.linalg.norm(b, 2)
    right_operator_gain = np.linalg.norm(right_image, 2) / np.linalg.norm(c, 2)
    exact_mixed = min(
        left_hs_gain * right_operator_gain,
        left_operator_gain * right_hs_gain,
    )
    transfer = mixed_gain_from_hilbert_schmidt(
        left_hs_gain,
        right_hs_gain,
        b_hilbert_schmidt_upper=np.linalg.norm(b, "fro"),
        b_operator_lower=np.linalg.norm(b, 2),
        c_hilbert_schmidt_upper=np.linalg.norm(c, "fro"),
        c_operator_lower=np.linalg.norm(c, 2),
    )
    assert exact_mixed <= transfer.mixed_gain_upper * (1.0 + 2.0e-14)


def test_residual_ledger_bounds_exact_directional_action() -> None:
    rng = np.random.default_rng(4903)
    operator = rng.normal(size=(9, 9)) + 3.0 * np.eye(9)
    source = rng.normal(size=(9, 4))
    exact = np.linalg.solve(operator, source)
    approximation = exact + 1.0e-5 * rng.normal(size=exact.shape)
    residual = source - operator @ approximation
    denominator = np.linalg.norm(source, "fro")
    ledger = directional_residual_upper(
        np.linalg.norm(approximation, "fro"),
        np.linalg.norm(residual, "fro"),
        np.linalg.norm(np.linalg.inv(operator), 2),
        denominator,
    )
    assert np.linalg.norm(exact, "fro") / denominator <= (
        ledger.normalized_gain_upper * (1.0 + 2.0e-14)
    )


def test_endpoint_packet_is_normalized_and_detects_the_fold() -> None:
    square, _ = quad(
        lambda value: float(packet_envelope(value)) ** 2,
        0.0,
        np.inf,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
    )
    assert math.isclose(square, 1.0, rel_tol=2.0e-13, abs_tol=2.0e-13)
    assert packet_limit_profile(0.0, 1.5436890126920764) < -0.49


def test_sparse_haar_materialization_matches_dense_blocks() -> None:
    from experiments.run_coupling_stable_rank_pilot import (
        sparse_haar_couplings,
    )
    from experiments.run_reduced_directional_pilot import (
        coarse_to_fine,
        detail_to_fine,
    )

    rng = np.random.default_rng(4904)
    operator = rng.normal(size=(18, 18))
    b, c = sparse_haar_couplings(csr_matrix(operator))
    identity = np.eye(9)
    coarse = np.column_stack(
        [coarse_to_fine(identity[:, index]) for index in range(9)]
    )
    detail = np.column_stack(
        [detail_to_fine(identity[:, index]) for index in range(9)]
    )
    assert np.linalg.norm(b.toarray() - coarse.T @ operator @ detail) < 3.0e-14
    assert np.linalg.norm(c.toarray() - detail.T @ operator @ coarse) < 3.0e-14


def test_production_primal_and_adjoint_deflated_solves_match_dense() -> None:
    from experiments.run_mixed_operator_gain_pilot import (
        reduced_adjoint_solve,
    )
    from experiments.run_reduced_directional_pilot import reduced_solve

    rng = np.random.default_rng(4905)
    basis = rng.normal(size=(20, 20))
    while abs(np.linalg.det(basis)) < 1.0e-5:
        basis = rng.normal(size=(20, 20))
    eigenvalues = np.linspace(-0.82, 0.78, 20)
    eigenvalues[7] = 0.93
    inverse_basis = np.linalg.inv(basis)
    operator = basis @ np.diag(eigenvalues) @ inverse_basis
    right = basis[:, 7]
    left = inverse_basis[7, :]
    pairing = float(np.dot(left, right))
    left = left / pairing
    projection = np.outer(right, left)
    complement = np.eye(20) - projection
    deflated = operator - eigenvalues[7] * projection
    z = 0.88 + 0.09j
    reduced = np.linalg.solve(z * np.eye(20) - deflated, complement)
    source = rng.normal(size=20) + 1j * rng.normal(size=20)
    primal, _ = reduced_solve(
        csr_matrix(operator),
        z,
        float(eigenvalues[7]),
        right,
        left,
        source,
        tolerance=2.0e-12,
        restart=40,
        maximum_cycles=20,
    )
    adjoint, _ = reduced_adjoint_solve(
        csr_matrix(operator),
        z,
        float(eigenvalues[7]),
        right,
        left,
        source,
        tolerance=2.0e-12,
    )
    assert np.linalg.norm(primal - reduced @ source) / np.linalg.norm(
        reduced @ source
    ) < 2.0e-10
    assert np.linalg.norm(adjoint - reduced.conjugate().T @ source) / np.linalg.norm(
        reduced.conjugate().T @ source
    ) < 2.0e-10
