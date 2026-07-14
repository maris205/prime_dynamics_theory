from __future__ import annotations

import numpy as np

from bulk_scattering import (
    LAMBDA_FIXED,
    beta_one_reduced_matrix,
    bulk_determinant,
    cloud_det2,
    component_physical_trace,
    fit_outer_cloud,
    full_even_physical_trace,
    geometric_cloud,
    geometric_section,
    odd_physical_trace,
    pole_removed_bulk_determinant,
    scaled_geometric_profile,
    scattering_profile,
    sparse_folded_gaussian_matrix,
)


def test_exact_endpoint_reconstruction_at_first_iterate() -> None:
    even_beta_one = 1.2384911978162352
    component = component_physical_trace(even_beta_one, 1)
    full = full_even_physical_trace(even_beta_one, 1)
    assert abs(component - 0.8651581546472628) < 3.0e-15
    assert abs(full - 1.1801429862402304) < 3.0e-15
    assert abs(odd_physical_trace(1) - 0.37333304316897203) < 3.0e-15


def test_reduced_circle_traces_reconstruct_direct_physical_data() -> None:
    expected = np.asarray(
        [
            1.1801429862402304,
            1.4198783447036916,
            1.6221410887189234,
            1.7638731479009206,
            1.8555077105429811,
            1.9125745570267334,
            1.947439879820811,
            1.968518085449592,
            1.9811845485117667,
            1.9887693744422983,
        ]
    )
    values = np.linalg.eigvals(beta_one_reduced_matrix(120))
    observed = np.asarray(
        [
            full_even_physical_trace(1.0 + np.sum(values**n).real, n)
            for n in range(1, 11)
        ]
    )
    assert np.max(np.abs(observed - expected)) < 2.0e-11


def test_endpoint_product_factorization_matches_the_trace_germ() -> None:
    reduced_values = np.linalg.eigvals(beta_one_reduced_matrix(120))
    for z in (0.35, 0.75, 0.90):
        logarithm = 0.0
        for length in range(2, 81):
            if length % 2:
                centered_trace = odd_physical_trace(length)
            else:
                iterate = length // 2
                even_sector = 1.0 + np.sum(reduced_values**iterate).real
                centered_trace = (
                    full_even_physical_trace(even_sector, iterate) - 2.0
                )
            logarithm -= centered_trace * z**length / length
        direct_trace_germ = np.exp(logarithm)
        assert abs(direct_trace_germ - bulk_determinant(z)) < 2.0e-11


def test_geometric_cloud_is_the_exact_pole_section() -> None:
    degree = 7
    cloud = geometric_cloud(degree)
    assert abs(np.sum(cloud)) < 3.0e-15
    for z in (0.2, 0.7, 1.1):
        q = z * z / LAMBDA_FIXED
        expected = geometric_section(degree, q)
        observed = cloud_det2(cloud, z)
        assert abs(observed - expected) < 2.0e-12


def test_geometric_scattering_limit() -> None:
    for s in (-2.0, -0.5, 0.0, 0.75, 2.0):
        observed = scaled_geometric_profile(1000, s)
        expected = scattering_profile(s)
        assert abs(observed - expected) < 6.0e-3


def test_synthetic_outer_cloud_fit_recovers_degree() -> None:
    outer = geometric_cloud(6) * np.exp(0.01j)
    inner_angles = np.linspace(0.2, 2.9, 12)
    inner = 0.31 * np.exp(1j * inner_angles)
    values = np.concatenate((outer, inner, np.conjugate(inner)))
    fit = fit_outer_cloud(values)
    assert fit.effective_degree == 6
    assert fit.phase_rms < 0.011


def test_sparse_operator_and_pole_residual() -> None:
    matrix = sparse_folded_gaussian_matrix(256, 0.03)
    row_error = np.max(np.abs(np.asarray(matrix.sum(axis=1)).ravel() - 1.0))
    assert row_error < 5.0e-15

    root = np.sqrt(LAMBDA_FIXED)
    residual = pole_removed_bulk_determinant(root)
    assert np.isfinite(residual.real)
    assert abs(residual) > 0.2
    for epsilon in (2.0e-3, 1.0e-3):
        z = root * (1.0 - epsilon)
        direct = (1.0 - z * z / LAMBDA_FIXED) * bulk_determinant(z)
        assert abs(direct - pole_removed_bulk_determinant(z)) < 2.0e-11
