from __future__ import annotations

import math

import numpy as np

from intrinsic_identification import (
    compress_factors,
    detail_resolvent_upper,
    directional_schur_bound,
    dyadic_tail_upper,
    low_rank_difference_frobenius,
    low_rank_frobenius,
    low_rank_singular_values,
    power_law_ledger,
    self_energy_upper,
)


def test_low_rank_utilities_match_dense_algebra() -> None:
    rng = np.random.default_rng(20260719)
    u = rng.normal(size=(12, 3))
    v = rng.normal(size=(12, 3))
    dense = u @ v.T
    assert math.isclose(
        low_rank_frobenius(u, v),
        np.linalg.norm(dense, "fro"),
        rel_tol=2.0e-14,
    )
    assert np.allclose(
        low_rank_singular_values(u, v),
        np.linalg.svd(dense, compute_uv=False)[:3],
        rtol=2.0e-13,
        atol=2.0e-13,
    )
    u2 = rng.normal(size=(12, 2))
    v2 = rng.normal(size=(12, 2))
    assert math.isclose(
        low_rank_difference_frobenius(u, v, u2, v2),
        np.linalg.norm(dense - u2 @ v2.T, "fro"),
        rel_tol=2.0e-13,
    )


def test_nested_factor_compression_is_the_top_left_haar_block() -> None:
    rng = np.random.default_rng(48)
    u = rng.normal(size=(16, 2))
    v = rng.normal(size=(16, 2))
    coarse_u, coarse_v = compress_factors(u, v, 2)
    restriction = np.zeros((8, 16))
    for index in range(8):
        restriction[index, 2 * index : 2 * index + 2] = 0.5
    prolongation = 2.0 * restriction.T
    expected = restriction @ (u @ v.T) @ prolongation
    assert np.allclose(coarse_u @ coarse_v.T, expected, atol=2.0e-14)


def test_scalar_schur_and_dyadic_ledgers() -> None:
    rd = detail_resolvent_upper(0.9, 0.1)
    assert math.isclose(rd, 1.25)
    assert math.isclose(self_energy_upper(rd, 0.02, 0.03), 0.00075)
    bound = directional_schur_bound(
        contour_length_over_two_pi=0.05,
        contour_maximum_modulus=1.05,
        detail_resolvent=rd,
        left_directional_hilbert_schmidt=0.2,
        right_directional_operator=0.3,
    )
    assert math.isclose(
        bound.identification_hilbert_schmidt_upper,
        0.05 * 1.05 * 1.25 * 0.2 * 0.3,
    )
    assert math.isclose(dyadic_tail_upper(3.0, 0.25), 4.0)


def contour_weighted_term(
    matrix: np.ndarray, center: complex, radius: float, nodes: int = 2048
) -> np.ndarray:
    dimension = matrix.shape[0]
    result = np.zeros_like(matrix, dtype=np.complex128)
    for index in range(nodes):
        theta = 2.0 * np.pi * index / nodes
        phase = np.exp(1j * theta)
        z = center + radius * phase
        resolvent = np.linalg.inv(z * np.eye(dimension) - matrix)
        result += z * resolvent * radius * phase / nodes
    return result


def test_exact_top_left_schur_integral_identity() -> None:
    a = np.array([[1.02, 0.04], [0.01, 0.22]])
    b = np.array([[0.018, -0.011], [0.006, 0.004]])
    c = np.array([[0.012, 0.003], [-0.008, 0.009]])
    d = np.array([[0.08, 0.02], [-0.01, -0.14]])
    full = np.block([[a, b], [c, d]])
    center = 1.02
    radius = 0.16
    q_full = contour_weighted_term(full, center, radius)
    q_coarse = contour_weighted_term(a, center, radius)
    direct = q_full[:2, :2] - q_coarse

    integral = np.zeros((2, 2), dtype=np.complex128)
    nodes = 2048
    for index in range(nodes):
        theta = 2.0 * np.pi * index / nodes
        phase = np.exp(1j * theta)
        z = center + radius * phase
        r_a = np.linalg.inv(z * np.eye(2) - a)
        r_d = np.linalg.inv(z * np.eye(2) - d)
        schur = np.linalg.inv(z * np.eye(2) - a - b @ r_d @ c)
        integral += z * schur @ b @ r_d @ c @ r_a * radius * phase / nodes
    assert np.linalg.norm(direct - integral, "fro") < 2.0e-12


def test_power_thresholds() -> None:
    polylog = power_law_ledger(2.05, 0.0)
    assert polylog.identification_is_lower_order
    edge = power_law_ledger(2.05, 0.5)
    assert edge.identification_is_lower_order
    failed = power_law_ledger(2.05, 0.75)
    assert not failed.identification_is_lower_order
    assert math.isclose(
        failed.identification_over_anchored_hilbert_schmidt_exponent,
        -0.2,
    )
