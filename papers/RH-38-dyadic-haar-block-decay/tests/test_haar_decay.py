from __future__ import annotations

import numpy as np

from haar_decay import (
    DerivativeEnvelope,
    HaarBlockBounds,
    discrete_normalization_defect,
    ideal_midpoint_haar_bounds,
    renormalized_constants,
    square_block_bounds,
)


def coordinate_matrices(dimension: int):
    identity = np.eye(dimension)
    j = np.repeat(identity, 2, axis=0)
    k = np.empty_like(j)
    k[0::2] = identity
    k[1::2] = -identity
    r = 0.5 * j.T
    s = 0.5 * k.T
    return j, k, r, s


def smooth_kernel(x, y):
    return 1.0 + 0.2 * x + 0.1 * y + 0.05 * x * y + 0.04 * x * x + 0.03 * y * y


def ideal_matrix(dimension: int):
    h = 1.0 / dimension
    nodes = (np.arange(dimension) + 0.5) * h
    return h * smooth_kernel(nodes[:, None], nodes[None, :])


def test_ideal_smooth_kernel_obeys_all_four_bounds() -> None:
    dimension = 40
    h = 1.0 / dimension
    coarse = ideal_matrix(dimension)
    fine = ideal_matrix(2 * dimension)
    j, k, r, s = coordinate_matrices(dimension)
    blocks = {
        "coarse_consistency": r @ fine @ j - coarse,
        "coarse_to_detail": s @ fine @ j,
        "detail_to_coarse": r @ fine @ k,
        "detail_block": s @ fine @ k,
    }
    bounds = ideal_midpoint_haar_bounds(
        h,
        DerivativeEnvelope(x=0.33, y=0.21, xx=0.08, xy=0.05, yy=0.06),
    )
    for name, matrix in blocks.items():
        assert np.linalg.norm(matrix, 2) <= getattr(bounds, name) * (1.0 + 1.0e-12)


def test_discrete_row_normalization_defect() -> None:
    dimension = 48
    h = 1.0 / dimension
    nodes = (np.arange(dimension) + 0.5) * h

    def raw(x, y):
        return 1.0 + 0.1 * x + 0.2 * y + 0.05 * x * y + 0.03 * y * y

    values = raw(nodes[:, None], nodes[None, :])
    discrete = values / np.sum(values, axis=1, keepdims=True)
    normalizer = 1.11 + 0.125 * nodes
    ideal = h * values / normalizer[:, None]
    defect = discrete - ideal
    upper = discrete_normalization_defect(
        h,
        raw_kernel_upper=1.38,
        raw_yy_upper=0.06,
        continuum_normalizer_lower=1.11,
    )
    assert np.linalg.norm(defect, 2) <= upper * (1.0 + 1.0e-12)


def test_block_squaring_bound() -> None:
    rng = np.random.default_rng(3817)
    dimension = 5
    coarse = rng.normal(size=(dimension, dimension)) / 8.0
    error = rng.normal(size=(dimension, dimension)) / 300.0
    b = rng.normal(size=(dimension, dimension)) / 40.0
    c = rng.normal(size=(dimension, dimension)) / 45.0
    d = rng.normal(size=(dimension, dimension)) / 350.0
    one_step = HaarBlockBounds(
        coarse_consistency=np.linalg.norm(error, 2),
        coarse_to_detail=np.linalg.norm(c, 2),
        detail_to_coarse=np.linalg.norm(b, 2),
        detail_block=np.linalg.norm(d, 2),
    )
    bounds = square_block_bounds(np.linalg.norm(coarse, 2), one_step)
    fine = np.block([[coarse + error, b], [c, d]])
    squared = fine @ fine
    actual = {
        "coarse_consistency": squared[:dimension, :dimension] - coarse @ coarse,
        "coarse_to_detail": squared[dimension:, :dimension],
        "detail_to_coarse": squared[:dimension, dimension:],
        "detail_block": squared[dimension:, dimension:],
    }
    for name, matrix in actual.items():
        assert np.linalg.norm(matrix, 2) <= getattr(bounds, name) * (1.0 + 1.0e-12)


def test_renormalized_constants_remove_the_expected_powers() -> None:
    h = 0.125
    bounds = HaarBlockBounds(3.0 * h * h, 4.0 * h, 5.0 * h, 6.0 * h * h)
    scaled = renormalized_constants(bounds, h)
    assert scaled == HaarBlockBounds(3.0, 4.0, 5.0, 6.0)
