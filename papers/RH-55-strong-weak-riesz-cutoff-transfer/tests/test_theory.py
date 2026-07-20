import math

import numpy as np
import pytest

from riesz_cutoff import (
    adaptive_tail_envelope,
    critical_kappa_for_mesh_power,
    cutoff_norm_ledger,
    gaussian_shape_critical_kappa,
    gaussian_shape_envelope,
    midpoint_ulam_ledger,
    rh39_omitted_mass_upper,
    riesz_defect_upper,
    sandwich_defect_upper,
)


def test_sandwich_ledger_has_exact_three_terms() -> None:
    result = sandwich_defect_upper(
        outer_weak_defect=0.02,
        reference_resolvent=3.0,
        reference_smoothing=4.0,
        perturbed_smoothing=5.0,
        perturbed_resolvent=6.0,
        strong_defect=0.01,
        strong_input_defect=0.03,
    )
    assert result.outer_left == pytest.approx(0.24)
    assert result.resolvent == pytest.approx(3.6)
    assert result.outer_right == pytest.approx(0.9)
    assert result.total == pytest.approx(4.74)


def test_riesz_integral_uses_inverse_modulus_weights() -> None:
    sandwich = sandwich_defect_upper(
        outer_weak_defect=0.01,
        reference_resolvent=1.0,
        reference_smoothing=1.0,
        perturbed_smoothing=1.0,
        perturbed_resolvent=1.0,
        strong_defect=0.0,
        strong_input_defect=0.0,
    )
    result = riesz_defect_upper(
        contour_length=2.0 * math.pi,
        minimum_modulus=0.5,
        sandwich=sandwich,
    )
    assert result.projector == pytest.approx(0.04)
    assert result.weighted == pytest.approx(0.02)


def test_cutoff_ledger_tracks_row_bv_and_l2_inflation() -> None:
    result = cutoff_norm_ledger(0.01, 2.0e-6)
    assert result.weak_l1_to_l1 == pytest.approx(4.0e-6)
    assert result.strong_l1_to_bv == pytest.approx(8.04e-4)
    assert result.strong_bv_to_bv == result.strong_l1_to_bv
    assert result.weak_l1_to_l2 == pytest.approx(4.0e-5)


def test_critical_adaptive_exponent_is_seven_quarters() -> None:
    assert critical_kappa_for_mesh_power(2.0) == pytest.approx(1.75)
    assert critical_kappa_for_mesh_power(3.0) == pytest.approx(1.5)


def test_gaussian_shape_refinement_lowers_threshold_to_five_quarters() -> None:
    assert gaussian_shape_critical_kappa(2.0) == pytest.approx(1.25)
    assert gaussian_shape_critical_kappa(3.0) == pytest.approx(5.0 / 6.0)


def test_kappa_two_beats_sqrt_sigma_on_near_critical_schedule() -> None:
    ratios = []
    for sigma in (1.0e-3, 1.0e-5, 1.0e-7):
        mesh = sigma * sigma / math.log(1.0 / sigma)
        ratios.append(
            adaptive_tail_envelope(mesh, sigma, 2.0).normalized_by_sqrt_sigma
        )
    assert ratios[2] < ratios[1] < ratios[0]


def test_shape_aware_kappa_two_is_little_o_sqrt_sigma() -> None:
    ratios = []
    for sigma in (1.0e-3, 1.0e-5, 1.0e-7):
        mesh = sigma * sigma / math.log(1.0 / sigma)
        ratios.append(
            gaussian_shape_envelope(
                mesh, sigma, 2.0
            ).normalized_by_sqrt_sigma
        )
    assert ratios[2] < ratios[1] < ratios[0]


def test_kappa_below_threshold_fails_on_power_two_boundary() -> None:
    values = [
        adaptive_tail_envelope(sigma * sigma, sigma, 1.5).riesz_envelope
        for sigma in (1.0e-3, 1.0e-5, 1.0e-7)
    ]
    assert values[2] > values[1] > values[0]


def test_midpoint_to_ulam_strong_scale_is_bulk_square_clock() -> None:
    good = midpoint_ulam_ledger(1.0e-7, 1.0e-3)
    bad = midpoint_ulam_ledger(1.0e-5, 1.0e-3)
    assert good.row_l1 == pytest.approx(1.0e-8)
    assert good.strong_bv == pytest.approx(0.1)
    assert good.inside_bulk_square_regime
    assert not bad.inside_bulk_square_regime


def test_rh39_bound_matches_archived_five_sigma_scale() -> None:
    value = rh39_omitted_mass_upper(1.0 / 512.0, 0.01, 5.0)
    assert value == pytest.approx(4.965522022961893e-7)


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        cutoff_norm_ledger(0.0, 1.0e-4)
    with pytest.raises(ValueError):
        adaptive_tail_envelope(2.0, 0.1, 2.0)


def test_two_sided_functional_calculus_identity_by_quadrature() -> None:
    operator = np.asarray([[0.92, 0.17], [0.0, 0.31]], dtype=np.complex128)
    center = 0.92
    radius = 0.08
    projector = np.zeros_like(operator)
    weighted = np.zeros_like(operator)
    count = 2048
    for index in range(count):
        angle = 2.0 * math.pi * (index + 0.5) / count
        z = center + radius * np.exp(1j * angle)
        dz_over_2pi_i = radius * np.exp(1j * angle) / count
        resolvent = np.linalg.inv(z * np.eye(2) - operator)
        sandwich = operator @ resolvent @ operator
        projector += dz_over_2pi_i * sandwich / (z * z)
        weighted += dz_over_2pi_i * sandwich / z
    expected = np.asarray([[1.0, 0.17 / (0.92 - 0.31)], [0.0, 0.0]])
    assert np.linalg.norm(projector - expected) < 1.0e-12
    assert np.linalg.norm(weighted - 0.92 * expected) < 1.0e-12


def test_sandwich_upper_dominates_euclidean_matrix_defect() -> None:
    reference = np.asarray([[0.72, 0.08], [0.03, 0.41]])
    perturbed = reference + np.asarray([[1.0e-4, -2.0e-4], [0.5e-4, 1.0e-4]])
    z = 0.93 + 0.17j
    resolvent = np.linalg.inv(z * np.eye(2) - reference)
    perturbed_resolvent = np.linalg.inv(z * np.eye(2) - perturbed)
    defect = np.linalg.norm(reference - perturbed, 2)
    upper = sandwich_defect_upper(
        outer_weak_defect=defect,
        reference_resolvent=np.linalg.norm(resolvent, 2),
        reference_smoothing=np.linalg.norm(reference, 2),
        perturbed_smoothing=np.linalg.norm(perturbed, 2),
        perturbed_resolvent=np.linalg.norm(perturbed_resolvent, 2),
        strong_defect=defect,
        strong_input_defect=defect,
    )
    actual = np.linalg.norm(
        reference @ resolvent @ reference
        - perturbed @ perturbed_resolvent @ perturbed,
        2,
    )
    assert actual <= upper.total * (1.0 + 1.0e-12)
    gaussian_shape_critical_kappa,
    gaussian_shape_envelope,
