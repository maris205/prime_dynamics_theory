from __future__ import annotations

import numpy as np

from sector_branches import (
    branch_profile_basis,
    bright_dark_transform,
    compressed_branch_cycle,
    dense_matrix,
    forced_relative_phase,
    phase_weighted_return,
    rank_one_branch_matrix,
)


def test_equal_branch_unit_phase_forces_cubic_angle() -> None:
    phase = forced_relative_phase(2.0, 2.0, 2.0)
    assert abs(phase - 2.0 * np.pi / 3.0) < 2.0e-15


def test_rank_one_branch_matrix_has_one_dark_channel() -> None:
    matrix = rank_one_branch_matrix(np.asarray((1.0, 1.0)), np.asarray((0.3, 0.3)))
    values = np.linalg.eigvals(matrix)
    assert np.min(np.abs(values)) < 2.0e-15
    transformed = bright_dark_transform(matrix)
    assert abs(transformed[1, 1]) < 2.0e-15
    assert abs(transformed[0, 0] - 0.6) < 2.0e-15


def test_rank_one_cubic_phase_preserves_one_branch_eigenvalue() -> None:
    matrix = rank_one_branch_matrix(
        np.asarray((1.0, 1.0)),
        np.asarray((0.3, 0.3)),
        phase=2.0 * np.pi / 3.0,
    )
    assert abs(max(np.abs(np.linalg.eigvals(matrix))) - 0.3) < 2.0e-15


def test_rank_one_branch_matrix_rejects_nonbinary_space() -> None:
    with np.testing.assert_raises(ValueError):
        rank_one_branch_matrix(np.ones(3), np.ones(3))


def test_phase_weighted_return_cancels_equal_branches_at_pi() -> None:
    left = np.asarray(((0.4, 0.1), (0.2, 0.3)))
    assert np.linalg.norm(phase_weighted_return(left, left, np.pi)) < 3.0e-16
    cubic = phase_weighted_return(left, left, 2.0 * np.pi / 3.0)
    assert abs(np.linalg.norm(cubic) / np.linalg.norm(left) - 1.0) < 2.0e-15


def test_sylvester_branch_and_endpoint_nonzero_spectra_agree() -> None:
    entrance = np.asarray(((0.8, 0.2), (0.1, 0.7), (0.3, -0.1)))
    exit_map = np.asarray(((0.6, 0.1, 0.2), (-0.2, 0.9, 0.3)))
    endpoint = exit_map @ entrance
    branch = entrance @ exit_map
    endpoint_values = np.linalg.eigvals(endpoint)
    branch_values = np.linalg.eigvals(branch)
    for value in endpoint_values:
        assert np.min(np.abs(branch_values - value)) < 2.0e-14


def test_profile_basis_and_compressed_cycle() -> None:
    profile = np.asarray((0.8, 0.5, 0.4, 0.7))
    left = np.asarray((True, True, False, False))
    right = np.asarray((False, False, True, True))
    basis = branch_profile_basis(profile, left, right)
    assert abs(np.vdot(basis[0], basis[1])) < 2.0e-15
    transition = np.asarray(
        (
            (0.6, 0.2, 0.1, 0.1),
            (0.2, 0.5, 0.2, 0.1),
            (0.1, 0.2, 0.5, 0.2),
            (0.1, 0.1, 0.2, 0.6),
        )
    )
    matrix = compressed_branch_cycle(
        lambda value: transition @ value,
        [np.ones(4, dtype=bool)],
        basis,
    )
    assert matrix.shape == (2, 2)
    assert np.min(matrix.real) > 0.0


def test_dense_matrix_materialization() -> None:
    matrix = np.asarray(((0.7, 0.2), (0.1, 0.6)))
    observed = dense_matrix(lambda value: matrix @ value, 2)
    assert np.linalg.norm(observed - matrix) < 2.0e-15
