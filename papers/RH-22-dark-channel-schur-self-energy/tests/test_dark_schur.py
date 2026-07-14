from __future__ import annotations

import numpy as np

from dark_schur import (
    audit_matrix,
    bright_dark_transform,
    characteristic,
    diagonal_gauge_transform,
    nested_schur_data,
    required_coupling,
    schur_function,
    self_energy,
    small_coupling_root_bound,
)


def test_scalar_schur_determinant_identity() -> None:
    matrix = np.asarray(((0.7, 0.13 - 0.02j), (-0.08j, 0.11)))
    zeta = 0.31 + 0.17j
    observed = characteristic(matrix, zeta)
    expected = (zeta - matrix[1, 1]) * schur_function(matrix, zeta)
    assert abs(observed - expected) < 2.0e-16


def test_required_product_places_target_exactly() -> None:
    a, d, target = 0.61, -0.03, 0.24
    product = required_coupling(a, d, target)
    matrix = np.asarray(((a, 1.0), (product, d)), dtype=np.complex128)
    assert abs(characteristic(matrix, target)) < 2.0e-17
    assert abs(schur_function(matrix, target)) < 2.0e-16


def test_diagonal_gauge_preserves_product_and_schur_function() -> None:
    matrix = np.asarray(((0.52, 0.04 + 0.01j), (-0.03, 0.07)))
    transformed = diagonal_gauge_transform(matrix, 2.0 - 0.5j, -0.7j)
    assert abs(transformed[0, 1] * transformed[1, 0] - matrix[0, 1] * matrix[1, 0]) < 2.0e-17
    assert abs(schur_function(transformed, 0.23j) - schur_function(matrix, 0.23j)) < 2.0e-16


def test_real_sign_obstruction_is_visible_in_required_product() -> None:
    a, d, target = 0.6, -0.02, 0.2
    assert d < target < a
    assert required_coupling(a, d, target).real < 0.0
    matrix = np.asarray(((a, 0.1), (0.03, d)))
    assert self_energy(matrix, target).real > 0.0
    assert audit_matrix(matrix, target).signed_coupling_ratio.real < 0.0


def test_small_coupling_bound_contains_bright_root() -> None:
    matrix = np.asarray(((0.63 + 0.05j, 0.002j), (0.004 - 0.001j, 0.08)))
    audit = audit_matrix(matrix, 0.21)
    bound = small_coupling_root_bound(matrix)
    assert np.isfinite(bound)
    assert abs(audit.bright_root_shift) < bound
    assert audit.small_coupling_parameter < 0.25


def test_audit_coverage_identity() -> None:
    matrix = np.asarray(((0.60, -0.002), (0.003, 0.01)))
    target = 0.22
    audit = audit_matrix(matrix, target)
    lhs = abs(audit.self_energy_at_target) / abs(audit.required_shift)
    rhs = abs(audit.signed_coupling_ratio)
    assert abs(lhs - rhs) < 2.0e-16
    assert abs(
        audit.determinant_residual
        - (target - audit.dark_pole) * audit.schur_residual
    ) < 2.0e-16


def test_hadamard_transform_is_involutive_and_spectral() -> None:
    matrix = np.asarray(((0.3, 0.2), (0.1, 0.4)))
    transformed = bright_dark_transform(matrix)
    restored = bright_dark_transform(transformed)
    assert np.linalg.norm(restored - matrix) < 3.0e-16
    assert np.linalg.norm(
        np.sort_complex(np.linalg.eigvals(transformed))
        - np.sort_complex(np.linalg.eigvals(matrix))
    ) < 3.0e-16


def test_dark_pole_is_rejected() -> None:
    matrix = np.asarray(((0.6, 0.1), (0.03, 0.02)))
    with np.testing.assert_raises(ZeroDivisionError):
        audit_matrix(matrix, 0.02)


def test_nested_schur_elimination_recovers_full_determinant() -> None:
    matrix = np.asarray(
        (
            (0.61, 0.03, 0.08, -0.02),
            (-0.04, 0.09, 0.01, 0.06),
            (0.07, -0.03, 0.21, 0.02),
            (0.01, 0.05, -0.04, -0.12),
        ),
        dtype=np.complex128,
    )
    zeta = 0.31 + 0.17j
    data = nested_schur_data(matrix, zeta)
    assert abs(
        data.full_determinant
        - data.external_determinant * data.reduced_determinant
    ) < 2.0e-15
    assert abs(
        data.reduced_determinant
        - (zeta - data.dark_pole) * data.scalar_schur_function
    ) < 2.0e-15
