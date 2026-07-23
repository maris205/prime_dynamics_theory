from __future__ import annotations

import numpy as np
import pytest

from fourth_cross_support import (
    barrier_snapshot,
    finite_tail_operator_bound,
    fourth_support_certificate,
    normalized_gram,
    source_seeded_barrier_data,
    support_margin,
    weyl_ratio_lower_bound,
)


def test_weyl_ratio_bound_on_random_perturbations() -> None:
    rng = np.random.default_rng(108)
    for _ in range(30):
        recent = rng.normal(size=(9, 5))
        error = rng.normal(size=(9, 5))
        error *= 1e-3 / np.linalg.norm(error, 2)
        recent_singular = np.linalg.svd(recent, compute_uv=False)
        actual_singular = np.linalg.svd(recent + error, compute_uv=False)
        lower = weyl_ratio_lower_bound(recent_singular, 1e-3)
        assert actual_singular[3] / actual_singular[0] + 1e-14 >= lower


def test_support_margin_matches_ratio_certificate() -> None:
    singular = [4.0, 3.0, 2.0, 0.1]
    delta = 1e-3
    threshold = 0.02
    certificate = fourth_support_certificate(singular, delta, threshold)
    assert certificate["support_certified"]
    assert certificate["ratio_lower_bound"] >= threshold
    assert support_margin(singular, delta, threshold) > 0.0


def test_finite_tail_operator_bound() -> None:
    eta = 1.0 / 512.0
    assert finite_tail_operator_bound(eta, 5, 0) == 0.0
    finite = finite_tail_operator_bound(eta, 5, 7)
    uniform = finite_tail_operator_bound(eta, 5)
    assert 0.0 < finite <= uniform


def test_exact_source_seeded_barrier() -> None:
    reference = source_seeded_barrier_data(1.0)
    for epsilon in (1.0, 0.5, 1e-3, 0.0):
        data = source_seeded_barrier_data(epsilon)
        assert abs(data["trace_clock"] - (1.0 + 1.0 / 512.0)) < 1e-14
        assert np.linalg.norm(data["packet_block"] - reference["packet_block"]) < 1e-14
        assert np.linalg.norm(data["complement_block"] - reference["complement_block"]) < 1e-14
        assert np.allclose(data["singular_values"][:3], np.array([4.0, 3.0, 2.0]) / 34.0)
        assert abs(data["ratio"] - epsilon / 4.0) < 1e-14


def test_barrier_snapshot_is_normalized_psd() -> None:
    gram = normalized_gram(barrier_snapshot(0.25))
    assert abs(np.trace(gram) - 1.0) < 1e-14
    assert np.linalg.eigvalsh(gram).min() > -1e-14


def test_validation() -> None:
    with pytest.raises(ValueError):
        finite_tail_operator_bound(1.0, 5)
    with pytest.raises(ValueError):
        finite_tail_operator_bound(0.5, 0)
    with pytest.raises(ValueError):
        barrier_snapshot(-0.1)
    with pytest.raises(ValueError):
        weyl_ratio_lower_bound([1.0, 0.5, 0.25], 0.1)
