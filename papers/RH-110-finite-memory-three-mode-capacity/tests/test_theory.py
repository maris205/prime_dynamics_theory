from __future__ import annotations

import numpy as np
import pytest

from three_mode_capacity import (
    capacity_aware_ratio_lower_bound,
    finite_memory_capacity_interval,
    normalized_spectral_four_volume,
    sharp_capacity_interval,
    three_mode_capacity,
)


def test_capacity_interval_on_random_perturbations() -> None:
    rng = np.random.default_rng(110)
    for _ in range(80):
        recent = rng.normal(size=(12, 6))
        error = rng.normal(size=(12, 6))
        error *= 1e-3 / np.linalg.norm(error, 2)
        shat = np.linalg.svd(recent, compute_uv=False)
        full = np.linalg.svd(recent + error, compute_uv=False)
        interval = finite_memory_capacity_interval(shat, 1e-3)
        actual = three_mode_capacity(full)
        assert interval["lower"] <= actual + 2e-14
        assert actual <= interval["upper"] + 2e-14


def test_capacity_recovery_is_a_ratio_lower_bound() -> None:
    rng = np.random.default_rng(111)
    for _ in range(50):
        recent = rng.normal(size=(11, 5))
        error = rng.normal(size=(11, 5))
        error *= 2e-4 / np.linalg.norm(error, 2)
        shat = np.linalg.svd(recent, compute_uv=False)
        full = np.linalg.svd(recent + error, compute_uv=False)
        bound = capacity_aware_ratio_lower_bound(shat, 2e-4)
        assert bound["recovered_ratio_lower"] <= full[3] / full[0] + 2e-14
        assert bound["recovered_ratio_lower"] <= bound["direct_weyl_ratio_lower"] + 2e-14


def test_exact_factorization() -> None:
    singular = np.array([5.0, 2.0, 1.0, 0.1, 0.01])
    ratio = singular[3] / singular[0]
    assert normalized_spectral_four_volume(singular) == pytest.approx(three_mode_capacity(singular) * ratio)


def test_sharp_capacity_interval() -> None:
    for volume in (1.0, 1e-3, 1e-9, 0.0):
        lower, upper = sharp_capacity_interval(volume)
        assert lower == pytest.approx(volume ** (2.0 / 3.0))
        assert upper == 1.0
        linear = [1.0, 1.0, 1.0, volume]
        root = volume ** (1.0 / 3.0)
        cubic = [1.0, root, root, root]
        assert three_mode_capacity(linear) == pytest.approx(upper)
        assert three_mode_capacity(cubic) == pytest.approx(lower)


def test_validation() -> None:
    with pytest.raises(ValueError):
        finite_memory_capacity_interval([1.0, 0.5, 0.2], 0.0)
    with pytest.raises(ValueError):
        finite_memory_capacity_interval([1.0, 0.5, 0.2, 0.1], -1.0)
    with pytest.raises(ValueError):
        sharp_capacity_interval(1.1)
