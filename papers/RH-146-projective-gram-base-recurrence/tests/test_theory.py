from __future__ import annotations

import math

import numpy as np

from projective_gram import cumulative_base_lower, normalized_base, projective_distance


def test_diagonal_equality_shows_sharp_half() -> None:
    source = np.eye(2)
    target = np.diag([math.exp(3.0), 1.0])
    distance = projective_distance(source, target)
    assert math.isclose(distance, 3.0, rel_tol=1e-12)
    assert math.isclose(
        normalized_base(target),
        math.exp(-distance / 2.0) * normalized_base(source),
        rel_tol=1e-12,
    )


def test_projective_recurrence_on_random_spd_pairs() -> None:
    rng = np.random.default_rng(146)
    for _ in range(64):
        left = rng.normal(size=(4, 4))
        right = rng.normal(size=(4, 4))
        source = left.T @ left + 0.2 * np.eye(4)
        target = right.T @ right + 0.2 * np.eye(4)
        lower = math.exp(-projective_distance(source, target) / 2.0) * normalized_base(source)
        assert normalized_base(target) >= lower * (1.0 - 1e-12)


def test_cumulative_bound_and_bounded_obstruction() -> None:
    distances = [1.0] * 12
    assert math.isclose(cumulative_base_lower(1.0, distances), math.exp(-6.0))
    bases = [normalized_base(np.diag([math.exp(n), 1.0])) for n in range(13)]
    steps = [
        projective_distance(np.diag([math.exp(n), 1.0]), np.diag([math.exp(n + 1), 1.0]))
        for n in range(12)
    ]
    assert np.allclose(steps, 1.0)
    assert bases[-1] < bases[0] and bases[-1] == cumulative_base_lower(bases[0], steps)

