from __future__ import annotations

import math

import numpy as np

from cutoff_bridge import (
    adaptive_cutoff_multiple,
    cutoff_bound,
    haar_cutoff_defect,
    support_half_width,
)


def folded_probabilities(dimension: int, sigma: float, mean: float) -> np.ndarray:
    nodes = (np.arange(dimension) + 0.5) / dimension
    weights = np.exp(-0.5 * ((nodes - mean) / sigma) ** 2)
    weights += np.exp(-0.5 * ((-nodes - mean) / sigma) ** 2)
    return weights / np.sum(weights)


def test_archived_support_geometry_has_the_claimed_buffer() -> None:
    sigma = 0.037
    multiple = 6.25
    for dimension in (64, 127, 256):
        h = 1.0 / dimension
        half_width = support_half_width(dimension, sigma, multiple)
        nodes = (np.arange(dimension) + 0.5) * h
        for absolute_mean in np.linspace(0.0, 1.0, 41):
            center = math.floor(absolute_mean * dimension - 0.5)
            retained = np.abs(np.arange(dimension) - center) <= half_width
            if np.any(~retained):
                assert np.min(np.abs(nodes[~retained] - absolute_mean)) >= (
                    half_width * h - 2.0e-15
                )


def test_twice_tail_identity_and_analytic_bounds() -> None:
    dimension = 192
    sigma = 0.035
    multiple = 5.5
    half_width = support_half_width(dimension, sigma, multiple)
    bound = cutoff_bound(dimension, sigma, multiple)
    for mean in np.linspace(1.0 - 1.5436890127, 1.0, 31):
        probabilities = folded_probabilities(dimension, sigma, mean)
        center = math.floor(abs(mean) * dimension - 0.5)
        retained = np.abs(np.arange(dimension) - center) <= half_width
        omitted = float(np.sum(probabilities[~retained]))
        truncated = np.zeros_like(probabilities)
        truncated[retained] = probabilities[retained] / (1.0 - omitted)
        row_error = float(np.sum(np.abs(probabilities - truncated)))
        assert abs(row_error - 2.0 * omitted) < 5.0e-15
        assert omitted <= bound.omitted_mass_upper
        assert row_error <= bound.infinity_norm_upper


def test_haar_bridge_uses_only_unitary_coordinate_compressions() -> None:
    coarse = cutoff_bound(2048, 0.01, 8.0)
    fine = cutoff_bound(4096, 0.01, 8.0)
    defect = haar_cutoff_defect(coarse, fine)
    assert defect.coarse_consistency == coarse.two_norm_upper + fine.two_norm_upper
    assert defect.coarse_to_detail == fine.two_norm_upper
    assert defect.detail_to_coarse == fine.two_norm_upper
    assert defect.detail_block == fine.two_norm_upper


def test_adaptive_schedule_keeps_the_defect_second_order() -> None:
    ratios = []
    for dimension in (1024, 4096, 16384, 65536, 262144, 1048576):
        h = 1.0 / dimension
        multiple = adaptive_cutoff_multiple(h)
        ratios.append(cutoff_bound(dimension, 0.01, multiple).two_norm_upper / h**2)
    assert max(ratios) < 20.0
    assert ratios[-1] < ratios[2]
