from __future__ import annotations

import math

import numpy as np
import pytest

from exterior_fourth_support import (
    elementary_symmetric_four,
    exterior_dimension,
    finite_memory_exterior_certificate,
    normalized_spectral_four_volume,
    normalized_trace_four_volume,
    scalar_volume_interval,
    sharp_scalar_volume_barrier,
    spectral_four_volume,
    trace_four_volume,
    volume_loss_factor,
)


def test_spectral_exterior_certificate_on_random_perturbations() -> None:
    rng = np.random.default_rng(109)
    for rows, columns in ((10, 4), (12, 5), (14, 7)):
        for _ in range(20):
            recent = rng.normal(size=(rows, columns))
            perturbation = rng.normal(size=(rows, columns))
            perturbation *= 1.0e-3 / np.linalg.norm(perturbation, 2)
            recent_singular = np.linalg.svd(recent, compute_uv=False)
            full_singular = np.linalg.svd(recent + perturbation, compute_uv=False)
            certificate = finite_memory_exterior_certificate(recent_singular, 1.0e-3, 1.0e-10)
            actual_ratio = full_singular[3] / full_singular[0]
            assert actual_ratio + 2.0e-14 >= certificate["spectral_volume_lower_bound"]
            assert actual_ratio + 2.0e-14 >= certificate["trace_volume_lower_bound"]
            assert certificate["spectral_volume_lower_bound"] + 2.0e-14 >= certificate["trace_volume_lower_bound"]


def test_spectral_and_trace_exterior_identities() -> None:
    singular = np.array([4.0, 3.0, 2.0, 1.0, 0.5])
    assert spectral_four_volume(singular) == pytest.approx(24.0)
    expected_e4 = elementary_symmetric_four(singular**2)
    assert trace_four_volume(singular) ** 2 == pytest.approx(expected_e4)
    assert normalized_trace_four_volume(singular) >= normalized_spectral_four_volume(singular)
    assert normalized_trace_four_volume(singular) <= math.sqrt(exterior_dimension(5)) * normalized_spectral_four_volume(singular)


def test_rank_four_reduced_moment_case_is_determinantal() -> None:
    rng = np.random.default_rng(110)
    cross = rng.normal(size=(9, 4))
    gram = cross.T @ cross
    singular = np.linalg.svd(cross, compute_uv=False)
    assert spectral_four_volume(singular) ** 2 == pytest.approx(np.linalg.det(gram), rel=1e-12)
    assert trace_four_volume(singular) == pytest.approx(spectral_four_volume(singular), rel=1e-12)


def test_sharp_scalar_volume_interval_and_loss_identity() -> None:
    for volume in (1.0, 1.0e-3, 1.0e-9):
        lower, upper = scalar_volume_interval(volume)
        assert lower == pytest.approx(volume)
        assert upper == pytest.approx(volume ** (1.0 / 3.0))
    singular = np.array([1.0, 0.4, 0.2, 0.01])
    ratio = singular[3] / singular[0]
    volume = normalized_spectral_four_volume(singular)
    assert volume == pytest.approx(ratio * volume_loss_factor(singular))
    assert ratio**3 <= volume <= ratio


def test_exact_source_seeded_scalar_volume_barrier() -> None:
    for volume in (1.0, 1.0e-3, 1.0e-9, 0.0):
        data = sharp_scalar_volume_barrier(volume)
        linear = data["linear"]
        cubic = data["cubic"]
        assert data["trace_clock_constant"]
        assert data["diagonal_blocks_constant"]
        assert np.linalg.eigvalsh(linear["snapshot"]).min() > -1.0e-14
        assert np.linalg.eigvalsh(cubic["snapshot"]).min() > -1.0e-14
        assert linear["normalized_volume"] == pytest.approx(volume, abs=1e-15)
        assert cubic["normalized_volume"] == pytest.approx(volume, abs=1e-15)
        assert linear["ratio"] == pytest.approx(volume, abs=1e-15)
        assert cubic["ratio"] == pytest.approx(volume ** (1.0 / 3.0), abs=1e-15)


def test_validation() -> None:
    with pytest.raises(ValueError):
        exterior_dimension(3)
    with pytest.raises(ValueError):
        finite_memory_exterior_certificate([1.0, 0.5, 0.25], 0.0, 1e-8)
    with pytest.raises(ValueError):
        finite_memory_exterior_certificate([1.0, 0.5, 0.25, 0.1], -1.0, 1e-8)
    with pytest.raises(ValueError):
        scalar_volume_interval(1.1)
    with pytest.raises(ValueError):
        sharp_scalar_volume_barrier(-0.1)
