from __future__ import annotations

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr

from endpoint_rank import (
    CONTRACTION_FIXED,
    HALF_ENERGY_THRESHOLD,
    boundary_clearances,
    boundary_ratios,
    conditioned_gaussian_affinity,
    endpoint_residual_energy,
    half_logarithmic_clock,
    hilbert_schmidt_energy,
    projected_gram_matrix,
    resolution_singular_values,
    scaled_boundary_constants,
    threshold_rank,
)


def test_boundary_ladder_matches_independent_periodic_data() -> None:
    expected = np.asarray(
        [
            0.09898156619342557,
            0.04277109103665755,
            0.01703019518376936,
            0.006494732565471173,
            0.0024124835598513528,
            0.0008809810289052145,
            0.0003182118992920424,
        ]
    )
    observed = boundary_clearances(50)
    assert np.max(np.abs(observed[: expected.size] - expected)) < 3.0e-15
    assert abs(boundary_ratios(observed)[-1] - CONTRACTION_FIXED) < 2.0e-8
    assert abs(scaled_boundary_constants(observed)[-1] - 0.4608051492) < 3.0e-10


def test_conditioned_affinity_matches_direct_hilbert_integral() -> None:
    def fingerprint(x: float, clearance_ratio: float) -> float:
        density = (
            np.exp(-0.5 * (x + clearance_ratio) ** 2)
            / np.sqrt(2.0 * np.pi)
            / ndtr(clearance_ratio)
        )
        return float(np.sqrt(density))

    for first, second in ((0.0, 0.7), (0.3, 2.0), (1.1, 4.2)):
        direct = quad(
            lambda x: fingerprint(x, first) * fingerprint(x, second),
            -np.inf,
            0.0,
            epsabs=2.0e-13,
        )[0]
        exact = conditioned_gaussian_affinity(first, second)
        assert abs(direct - exact) < 3.0e-12

    def linear_row(x: float, clearance_ratio: float) -> float:
        normalization = np.sqrt(np.sqrt(np.pi) * ndtr(np.sqrt(2.0) * clearance_ratio))
        return float(np.exp(-0.5 * (x + clearance_ratio) ** 2) / normalization)

    for first, second in ((0.0, 0.7), (0.3, 2.0), (1.1, 4.2)):
        direct = quad(
            lambda x: linear_row(x, first) * linear_row(x, second),
            -np.inf,
            0.0,
            epsabs=2.0e-13,
        )[0]
        exact = conditioned_gaussian_affinity(first, second, power=1.0)
        assert abs(direct - exact) < 3.0e-12


def test_endpoint_projection_has_the_exact_small_scale_energy() -> None:
    coefficient = (np.pi - 2.0) / (4.0 * np.pi)
    for value in (1.0e-3, 2.0e-3, 4.0e-3):
        scaled = endpoint_residual_energy(value) / value**2
        assert abs(scaled - coefficient) < 5.0e-4
    assert endpoint_residual_energy(12.0) > 1.0 - 2.0e-12


def test_projected_gram_is_positive_and_matches_column_energies() -> None:
    clearances = boundary_clearances(50)
    sigma = 2.0e-4
    gram, dimensionless = projected_gram_matrix(clearances, sigma)
    assert np.min(np.linalg.eigvalsh(gram)) > -2.0e-12
    expected_diagonal = endpoint_residual_energy(dimensionless)
    assert np.max(np.abs(np.diag(gram) - expected_diagonal)) < 3.0e-15


def test_half_energy_rank_matches_archived_noise_sequence() -> None:
    clearances = boundary_clearances(70)
    noise = (1.0e-2, 4.0e-3, 2.0e-3, 1.0e-3, 5.0e-4, 2.0e-4, 1.0e-4)
    expected = (2, 3, 4, 5, 5, 6, 7)
    observed = tuple(
        threshold_rank(
            clearances,
            sigma,
            threshold=HALF_ENERGY_THRESHOLD,
        )
        for sigma in noise
    )
    assert observed == expected


def test_rank_is_stable_under_tail_truncation() -> None:
    clearances = boundary_clearances(80)
    counts = [
        threshold_rank(clearances, 1.0e-8, tail_ratio=tail_ratio)
        for tail_ratio in (1.0e-6, 1.0e-8, 1.0e-10, 1.0e-12)
    ]
    assert counts == [16, 16, 16, 16]
    singular_values = resolution_singular_values(clearances, 1.0e-8)
    assert singular_values[15] > HALF_ENERGY_THRESHOLD
    assert singular_values[16] < HALF_ENERGY_THRESHOLD


def test_hilbert_schmidt_energy_and_rank_follow_the_half_log_clock() -> None:
    clearances = boundary_clearances(80)
    noise = np.logspace(-2.0, -14.0, 49)
    clock = half_logarithmic_clock(noise)
    energies = np.asarray(
        [hilbert_schmidt_energy(clearances, sigma) for sigma in noise]
    )
    ranks = np.asarray([threshold_rank(clearances, sigma) for sigma in noise])
    assert np.ptp(energies - clock) < 0.25
    assert np.ptp(ranks - clock) < 1.2

    linear_energies = np.asarray(
        [
            hilbert_schmidt_energy(clearances, sigma, power=1.0)
            for sigma in noise
        ]
    )
    linear_ranks = np.asarray(
        [threshold_rank(clearances, sigma, power=1.0) for sigma in noise]
    )
    assert np.ptp(linear_energies - clock) < 0.25
    assert np.ptp(linear_ranks - clock) < 1.2
