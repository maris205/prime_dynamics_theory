from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from weighted_kernel import (
    factor_correction_ledger,
    intrinsic_kernel_envelope,
)


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_two_sided_correction_identity() -> None:
    rng = np.random.default_rng(20260719)
    matrix = rng.normal(size=(5, 5))
    right = rng.normal(size=5)
    left = rng.normal(size=5)
    gram = float(left @ right)
    if abs(gram) < 0.2:
        left[0] += 1.0
        gram = float(left @ right)
    projection = np.outer(right, left) / gram
    eigenvalue = -0.93
    residual_operator = matrix - eigenvalue * np.eye(5)
    correction = (
        -residual_operator @ projection
        - projection @ residual_operator
        + projection @ residual_operator @ projection
    )
    corrected = matrix + correction
    assert np.allclose(projection @ projection, projection)
    assert np.allclose(corrected @ projection, eigenvalue * projection)
    assert np.allclose(projection @ corrected, eigenvalue * projection)


def test_factor_correction_gate_is_tiny() -> None:
    ledger = factor_correction_ledger(
        contour_radius=0.05,
        contour_maximum_modulus=1.04,
        contour_resolvent_upper=85.0,
        approximate_eigenvalue_modulus=0.99,
        right_norm_upper=1.01,
        left_norm_upper=1.12,
        right_residual_upper=4.0e-13,
        left_residual_upper=1.3e-12,
        gram_lower=0.999999999999,
        gram_upper=1.000000000001,
        grushin_scalar_error_upper=4.0e-13,
    )
    assert ledger.admissible
    assert ledger.correction_neumann_product_upper < 2.0e-10
    assert ledger.weighted_term_error_upper < 1.0e-9


def test_kernel_midpoint_envelope_is_second_order() -> None:
    first = intrinsic_kernel_envelope(
        contour_radius=0.05,
        contour_maximum_modulus=1.04,
        contour_minimum_modulus=0.93,
        contour_resolvent_upper=113.0,
        kernel_source_first_upper=670.0,
        kernel_target_first_upper=383.0,
        kernel_source_second_upper=196100.0,
        kernel_source_target_upper=82100.0,
        kernel_target_second_upper=47500.0,
        midpoint_dimension=65536,
    )
    second = intrinsic_kernel_envelope(
        contour_radius=0.05,
        contour_maximum_modulus=1.04,
        contour_minimum_modulus=0.93,
        contour_resolvent_upper=113.0,
        kernel_source_first_upper=670.0,
        kernel_target_first_upper=383.0,
        kernel_source_second_upper=196100.0,
        kernel_source_target_upper=82100.0,
        kernel_target_second_upper=47500.0,
        midpoint_dimension=131072,
    )
    assert first.midpoint_to_cell_average_upper < 1.9e-5
    assert second.midpoint_to_cell_average_upper < (
        first.midpoint_to_cell_average_upper / 3.99
    )


def sampled_rank_one(dimension: int) -> np.ndarray:
    h = 1.0 / dimension
    points = (np.arange(dimension) + 0.5) * h
    right = 1.0 + points + 0.4 * points**2
    left = 1.0 - 0.3 * points + 0.7 * points**2
    return h * np.outer(right, left)


def haar_blocks(coarse_dimension: int) -> dict[str, np.ndarray]:
    coarse = sampled_rank_one(coarse_dimension)
    fine = sampled_rank_one(2 * coarse_dimension)
    average = np.zeros((2 * coarse_dimension, coarse_dimension))
    detail = np.zeros_like(average)
    scale = 1.0 / np.sqrt(2.0)
    for index in range(coarse_dimension):
        average[2 * index : 2 * index + 2, index] = scale
        detail[2 * index, index] = scale
        detail[2 * index + 1, index] = -scale
    return {
        "coarse_consistency": average.T @ fine @ average - coarse,
        "coarse_to_detail": detail.T @ fine @ average,
        "detail_to_coarse": average.T @ fine @ detail,
        "detail_block": detail.T @ fine @ detail,
    }


def test_smooth_midpoint_haar_quarter_half_law() -> None:
    first = haar_blocks(48)
    second = haar_blocks(96)
    targets = {
        "coarse_consistency": 0.25,
        "coarse_to_detail": 0.5,
        "detail_to_coarse": 0.5,
        "detail_block": 0.25,
    }
    for name, target in targets.items():
        ratio = np.linalg.norm(second[name], "fro") / np.linalg.norm(
            first[name], "fro"
        )
        assert abs(ratio - target) < 2.0e-4


def test_archived_weighted_kernel_certificate_closes() -> None:
    data = load("validated_weighted_parity_kernel.json")
    assert data["status"] == (
        "rigorous_intrinsic_continuum_parity_kernel_and_adaptive_deflation"
    )
    assert data["stored_factor_validation"][
        "all_three_levels_are_actual_spectral_factors"
    ]
    assert data["stored_parity_haar_law"][
        "all_ratio_targets_within_one_thousandth"
    ]
    assert data["continuum_complement_schur"][
        "improved_continuum_L2_resolvent_upper"
    ] < 113.0
    family = data["improved_uniform_matrix_family"]
    assert family["certified_threshold_dimension"] == 65536
    assert family["uniform_fixed_and_adaptive_sparse_resolvent_upper"] < 268.0
    assert family["uniform_weighted_riesz_cutoff_upper"] < 8.0e-10
    assert data["intrinsic_continuum_kernel"][
        "continuum_operator_distance_from_center_upper"
    ] < 1.72
