from __future__ import annotations

import math

from cyclic_ulam_edge.core import (
    aligned_block,
    crossing_projection,
    finite_checks,
    geometry_residuals,
    local_defect,
    matvec,
    sign_mode_residual,
    sign_vector,
)


def test_frozen_geometry_residual_is_small() -> None:
    assert max(abs(value) for value in geometry_residuals().values()) < 1.0e-12


def test_aligned_block_is_row_stochastic_and_anti_diagonal() -> None:
    matrix = aligned_block(3, 5)
    assert all(abs(sum(row) - 1.0) < 1.0e-15 for row in matrix)
    assert all(matrix[i][j] == 0.0 for i in range(3) for j in range(3))
    assert all(matrix[i][j] == 0.0 for i in range(3, 8) for j in range(3, 8))


def test_sign_mode_is_exact_in_the_finite_witness() -> None:
    matrix = aligned_block(4, 6)
    signs = sign_vector(4, 6)
    assert all(
        math.isclose(value, -sign, rel_tol=0.0, abs_tol=1.0e-15)
        for value, sign in zip(matvec(matrix, signs), signs)
    )
    assert sign_mode_residual(4, 6) < 1.0e-15


def test_crossing_identity_and_width_weighting() -> None:
    for theta in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0):
        assert abs(crossing_projection(theta) - 4.0 * theta * (1.0 - theta)) < 1.0e-15
        assert abs(local_defect(0.3, theta) - 0.3 * crossing_projection(theta)) < 1.0e-15


def test_finite_ledger_reports_all_exact_checks() -> None:
    payload = finite_checks()
    assert payload["crossing_identity_pass"] is True
    assert payload["sign_mode_residual"] == 0.0
    assert payload["aligned_projected_same_band_mass"] == 0.0
