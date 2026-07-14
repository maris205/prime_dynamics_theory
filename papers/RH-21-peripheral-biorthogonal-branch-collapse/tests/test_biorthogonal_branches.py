from __future__ import annotations

import numpy as np

from biorthogonal_branches import (
    bright_coordinate_dual,
    bright_projector,
    canonical_biorthogonal_pair,
    close_branch_histories,
    complement_project,
    gauge_transform,
    merge_metrics,
    propagate_branch_histories,
    reduced_branch_cycle,
)


def peripheral_modes() -> tuple[np.ndarray, np.ndarray]:
    right = np.asarray(
        ((1.0, 0.2), (0.3, 1.0), (-0.1, 0.4), (0.2, -0.3), (0.5, 0.1))
    )
    left = right @ np.linalg.inv(right.T @ right)
    return right, left


def test_complement_projection_is_idempotent() -> None:
    right, left = peripheral_modes()
    values = np.arange(15.0).reshape(5, 3)
    once = complement_project(values, right, left)
    twice = complement_project(once, right, left)
    assert np.linalg.norm(once - twice) < 2.0e-14
    assert np.linalg.norm(left.T @ once) < 2.0e-14


def test_canonical_pair_is_peripherally_biorthogonal() -> None:
    right, left = peripheral_modes()
    trial = np.asarray(
        ((0.7, 0.1), (0.2, 0.8), (0.5, -0.3), (-0.2, 0.4), (0.1, 0.6))
    )
    pair = canonical_biorthogonal_pair(trial, right, left)
    assert np.linalg.norm(pair.analysis @ pair.synthesis - np.eye(2)) < 2.0e-14
    assert np.linalg.norm(pair.analysis @ right) < 2.0e-14
    assert np.linalg.norm(left.T @ pair.synthesis) < 2.0e-14


def test_gauge_transform_preserves_spectrum() -> None:
    matrix = np.asarray(((0.7, 0.2), (0.1, -0.3)))
    gauge = np.asarray(((1.4, 0.2), (-0.3, 0.8)))
    transformed = gauge_transform(matrix, gauge)
    first = np.sort_complex(np.linalg.eigvals(matrix))
    second = np.sort_complex(np.linalg.eigvals(transformed))
    assert np.linalg.norm(first - second) < 2.0e-14


def test_bright_projector_does_not_half_an_invariant_return() -> None:
    projector = bright_projector()
    bright = np.ones((2, 1))
    entrance = bright @ np.asarray(((0.4, -0.2, 0.1),))
    exit_map = np.asarray(((0.3,), (-0.1,), (0.6,))) @ bright.T / 2.0
    endpoint = exit_map @ entrance
    reduced = exit_map @ projector @ entrance
    assert np.linalg.norm(projector @ projector - projector) < 2.0e-15
    assert np.linalg.norm(endpoint - reduced) < 2.0e-15
    assert np.linalg.norm(0.5 * projector @ (0.5 * projector) - 0.5 * projector) > 0.1


def test_exchange_symmetric_metric_has_half_bright_dual() -> None:
    metric = np.asarray(((1.3, 0.2), (0.2, 1.3)))
    weights = bright_coordinate_dual(metric)
    assert np.linalg.norm(weights - 0.5) < 2.0e-15
    assert abs(weights @ np.ones(2) - 1.0) < 2.0e-15


def test_merge_metrics_match_exact_singular_values() -> None:
    cosine = 0.97
    first = np.asarray((1.0, 0.0))
    second = np.asarray((cosine, np.sqrt(1.0 - cosine * cosine)))
    metrics = merge_metrics(first, second)
    assert abs(metrics.dark_singular_value - np.sqrt(1.0 - cosine)) < 2.0e-15
    assert abs(
        metrics.gram_condition - (1.0 + cosine) / (1.0 - cosine)
    ) < 2.0e-12


def test_propagation_and_reduced_cycle() -> None:
    transition = np.asarray(
        (
            (0.7, 0.1, 0.1, 0.1),
            (0.2, 0.6, 0.1, 0.1),
            (0.1, 0.2, 0.6, 0.1),
            (0.1, 0.1, 0.2, 0.6),
        )
    )
    basis = np.asarray(((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (0.0, 0.0)))
    masks = [np.ones(4, dtype=bool), np.ones(4, dtype=bool)]
    histories = propagate_branch_histories(lambda value: transition @ value, masks, basis)
    assert len(histories) == 3
    closed = close_branch_histories(
        lambda value: transition @ value, np.ones(4, dtype=bool), histories[0]
    )
    reduced = reduced_branch_cycle(
        lambda value: transition @ value,
        masks,
        np.ones(4, dtype=bool),
        basis,
        basis.T,
    )
    assert np.linalg.norm(reduced - basis.T @ closed) < 2.0e-15
