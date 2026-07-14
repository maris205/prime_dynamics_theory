from __future__ import annotations

import numpy as np

from complement_excursions import (
    PeripheralProjector,
    apply_deflated,
    apply_endpoint_return,
    apply_restricted_return,
    critical_branch_masks,
    cyclic_time_lift,
    feshbach_map,
    phase_projection,
    power_eigenpair,
    time_fourier_blocks,
)


def test_time_lift_is_exact_fourier_replication() -> None:
    operator = np.asarray(((0.7, 0.2), (-0.1, 0.45)), dtype=float)
    period = 4
    lifted = cyclic_time_lift(operator, period)
    expected = np.concatenate(
        [np.linalg.eigvals(block) for block in time_fourier_blocks(operator, period)]
    )
    observed = np.linalg.eigvals(lifted)
    for value in expected:
        assert np.min(np.abs(observed - value)) < 3.0e-14
    z = 0.23 - 0.17j
    left = np.linalg.det(np.eye(lifted.shape[0]) - z * lifted)
    right = np.linalg.det(
        np.eye(operator.shape[0])
        - z**period * np.linalg.matrix_power(operator, period)
    )
    assert abs(left - right) < 2.0e-14


def test_phase_projections_resolve_the_time_lift() -> None:
    operator = np.asarray(((0.6, 0.1), (0.2, 0.4)))
    period = 3
    lifted = cyclic_time_lift(operator, period)
    projections = [phase_projection(2, period, index) for index in range(period)]
    assert np.linalg.norm(sum(projections) - np.eye(6)) < 2.0e-14
    for first, projection in enumerate(projections):
        assert np.linalg.norm(projection @ projection - projection) < 2.0e-14
        assert np.linalg.norm(lifted @ projection - projection @ lifted) < 2.0e-14
        for second in range(first):
            assert np.linalg.norm(projection @ projections[second]) < 2.0e-14


def test_feshbach_factorization_is_exact() -> None:
    operator = np.asarray(((0.4, 0.2), (-0.1, 0.55)))
    lifted = cyclic_time_lift(operator, 3)
    mask = np.asarray((True, False, False, True, True, False))
    projection = np.diag(mask.astype(float))
    zeta = 0.91 + 0.24j
    feshbach, _ = feshbach_map(lifted, projection, zeta)
    q_basis = np.eye(6)[:, ~mask]
    cqq = q_basis.T @ lifted @ q_basis
    observed = np.linalg.det(zeta * np.eye(6) - lifted)
    expected = np.linalg.det(zeta * np.eye(3) - cqq) * np.linalg.det(feshbach)
    assert abs(observed - expected) < 3.0e-14


def test_left_plus_right_return_equals_branch_complete_return() -> None:
    transition = np.asarray(
        (
            (0.4, 0.3, 0.2, 0.1),
            (0.1, 0.5, 0.3, 0.1),
            (0.2, 0.2, 0.4, 0.2),
            (0.15, 0.25, 0.2, 0.4),
        )
    )
    grid = (np.arange(4) + 0.5) / 4.0
    base = [
        np.asarray((True, True, False, False)),
        np.asarray((False, True, True, False)),
        np.asarray((False, False, True, False)),
    ]
    left, right, both = critical_branch_masks(
        grid,
        base,
        final_center=0.625,
        final_width=0.3,
        window_multiple=1.0,
        partition=0.7,
    )
    endpoint_indices = np.flatnonzero(left[0])
    vector = np.asarray((0.8, -0.2))
    action = lambda value, masks: apply_restricted_return(
        lambda source: transition @ source,
        masks,
        endpoint_indices,
        value,
        dimension=4,
    )
    assert np.linalg.norm(action(vector, both) - action(vector, left) - action(vector, right)) < 2.0e-14


def test_endpoint_return_and_power_iteration() -> None:
    transition = np.asarray(((0.8, 0.2), (0.3, 0.7)))
    mask = np.asarray((True, True))
    indices = np.arange(2)
    operator = lambda vector: apply_endpoint_return(
        lambda source: transition @ source,
        mask,
        indices,
        vector,
        period=3,
        dimension=2,
    )
    pair = power_eigenpair(operator, np.ones(2), iterations=20)
    expected = max(abs(np.linalg.eigvals(np.linalg.matrix_power(transition, 3))))
    assert abs(pair.eigenvalue - expected) < 2.0e-12
    assert pair.residual < 2.0e-12


def test_rank_two_deflation_action() -> None:
    matrix = np.diag((1.0, -0.9, 0.4))
    projectors = (
        PeripheralProjector(1.0, np.asarray((1.0, 0.0, 0.0)), np.asarray((1.0, 0.0, 0.0)), 0.0, 0.0),
        PeripheralProjector(-0.9, np.asarray((0.0, 1.0, 0.0)), np.asarray((0.0, 1.0, 0.0)), 0.0, 0.0),
    )
    observed = apply_deflated(matrix, projectors, np.asarray((2.0, 3.0, 5.0)))
    assert np.linalg.norm(observed - np.asarray((0.0, 0.0, 2.0))) < 2.0e-15
