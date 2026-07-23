from __future__ import annotations

import numpy as np
import pytest

from memory_depth import (
    finite_history_tail_bound,
    first_certifying_depth,
    snapshot_action_cost,
    weyl_ratio_lower_bound,
)


def test_finite_tail_splits_one_increment_at_a_time() -> None:
    eta = 0.2
    length = 7
    for depth in range(1, length):
        current = finite_history_tail_bound(eta, depth, length)
        following = finite_history_tail_bound(eta, depth + 1, length)
        assert current - following == pytest.approx(eta**depth)
    assert finite_history_tail_bound(eta, length, length) == 0.0


def test_nested_weyl_bounds_are_monotone() -> None:
    rng = np.random.default_rng(116)
    increments = []
    for depth in range(8):
        matrix = rng.normal(size=(10, 6))
        matrix *= 0.4**depth / max(np.linalg.norm(matrix, 2), 1.0)
        increments.append(matrix)
    full = sum(increments)
    recent = np.zeros_like(full)
    lowers = []
    for depth, increment in enumerate(increments, start=1):
        recent += increment
        radius = sum(np.linalg.norm(value, 2) for value in increments[depth:])
        singular = np.linalg.svd(recent, compute_uv=False)
        lower = weyl_ratio_lower_bound(singular, radius)
        lowers.append(lower)
        actual = np.linalg.svd(full, compute_uv=False)
        assert lower <= actual[3] / actual[0] + 1e-13
    assert all(right + 1e-13 >= left for left, right in zip(lowers, lowers[1:]))


def test_first_passage_and_cost() -> None:
    bounds = [(1, 0.0), (2, 1e-7), (3, 2e-5), (4, 3e-5)]
    assert first_certifying_depth(bounds, 1e-6) == 3
    assert first_certifying_depth(bounds, 1e-4) is None
    assert snapshot_action_cost(3, 7) == 21


def test_validation() -> None:
    with pytest.raises(ValueError):
        finite_history_tail_bound(1.0, 2, 4)
    with pytest.raises(ValueError):
        first_certifying_depth([(2, 0.1), (1, 0.2)], 0.15)
    with pytest.raises(ValueError):
        weyl_ratio_lower_bound([1.0, 0.5, 0.2], 0.0)
