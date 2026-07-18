from __future__ import annotations

import numpy as np

from projector_bridge import (
    PeripheralData,
    block_factors,
    biorthogonality_defect,
    low_rank_frobenius_norm,
    low_rank_singular_values,
    weighted_term,
)


def coordinate_matrices(dimension: int):
    identity = np.eye(dimension)
    j = np.repeat(identity, 2, axis=0)
    w = np.empty_like(j)
    w[0::2] = identity
    w[1::2] = -identity
    return j, w, 0.5 * j.T, 0.5 * w.T


def random_peripheral(rng, dimension: int, rank: int) -> PeripheralData:
    right = rng.normal(size=(dimension, rank))
    left = rng.normal(size=(dimension, rank))
    gram = left.T @ right
    left = left @ np.linalg.inv(gram).T
    values = rng.uniform(-0.9, 1.0, size=rank)
    return PeripheralData(right=right, left=left, values=values)


def test_low_rank_haar_factors_equal_dense_blocks() -> None:
    rng = np.random.default_rng(4040)
    coarse = random_peripheral(rng, 7, 2)
    fine = random_peripheral(rng, 14, 2)
    q_coarse = weighted_term(coarse)
    q_fine = weighted_term(fine)
    j, w, r, s = coordinate_matrices(7)
    expected = {
        "coarse_consistency": r @ q_fine @ j - q_coarse,
        "coarse_to_detail": s @ q_fine @ j,
        "detail_to_coarse": r @ q_fine @ w,
        "detail_block": s @ q_fine @ w,
    }
    for name, (left_factor, right_factor) in block_factors(coarse, fine).items():
        actual = left_factor @ right_factor.T
        np.testing.assert_allclose(actual, expected[name], rtol=2.0e-13, atol=2.0e-13)


def test_small_gram_norms_match_dense_svd() -> None:
    rng = np.random.default_rng(4041)
    a = rng.normal(size=(23, 4))
    b = rng.normal(size=(23, 4))
    dense = a @ b.T
    np.testing.assert_allclose(
        low_rank_frobenius_norm(a, b), np.linalg.norm(dense, "fro"), rtol=2.0e-14
    )
    np.testing.assert_allclose(
        low_rank_singular_values(a, b),
        np.linalg.svd(dense, compute_uv=False)[:4],
        rtol=2.0e-13,
        atol=2.0e-13,
    )


def test_biorthogonality_defect_detects_exact_pair() -> None:
    rng = np.random.default_rng(4042)
    data = random_peripheral(rng, 19, 2)
    assert biorthogonality_defect(data) < 1.0e-13


def test_weighted_term_is_invariant_under_mode_gauge_and_order() -> None:
    rng = np.random.default_rng(4043)
    data = random_peripheral(rng, 17, 3)
    scales = np.asarray([-2.5, 0.37, 4.1])
    permutation = np.asarray([2, 0, 1])
    gauged = PeripheralData(
        right=(data.right * scales[None, :])[:, permutation],
        left=(data.left / scales[None, :])[:, permutation],
        values=data.values[permutation],
    )
    np.testing.assert_allclose(
        weighted_term(gauged),
        weighted_term(data),
        rtol=2.0e-14,
        atol=2.0e-14,
    )
