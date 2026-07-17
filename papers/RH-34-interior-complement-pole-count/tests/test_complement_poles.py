from __future__ import annotations

import numpy as np
from scipy.linalg import schur

from complement_poles import (
    classify_binary64_diagonal,
    combine_frobenius_bounds,
    similarity_certificate,
)


def test_exact_binary64_circle_classification_includes_boundary_case() -> None:
    values = np.asarray([0.0 + 0.0j, 1.0 + 0.0j, 2.0 + 0.0j])
    result = classify_binary64_diagonal(values, 0.0 + 0.0j, 1.0)
    assert result.inside_count == 1
    assert result.boundary_count == 1
    assert result.outside_count == 1
    assert [row["exact_squared_margin_sign"] for row in result.records] == [
        -1,
        0,
        1,
    ]


def test_block_frobenius_combination_is_outward() -> None:
    result = combine_frobenius_bounds([3.0, 4.0])
    assert result >= 5.0
    assert result < np.nextafter(5.0, np.inf, dtype=np.float64) * 2.0


def test_similarity_certificate_controls_a_small_schur_comparison() -> None:
    matrix = np.asarray(
        [
            [1.3 + 0.1j, 0.2 - 0.3j, 0.0],
            [0.0, 1.7 - 0.2j, 0.4 + 0.1j],
            [0.1, 0.0, 2.1 + 0.3j],
        ],
        dtype=np.complex128,
    )
    triangular, vectors = schur(matrix, output="complex")
    triangular = np.triu(triangular)
    residual = matrix @ vectors - vectors @ triangular
    defect = vectors.conj().T @ vectors - np.eye(3)
    residual_upper = np.nextafter(
        np.linalg.norm(residual, ord="fro") + 1.0e-13, np.inf
    )
    defect_upper = np.nextafter(
        np.linalg.norm(defect, ord="fro") + 1.0e-13, np.inf
    )
    zeta = 0.25 + 0.1j
    direct_resolvent = np.linalg.norm(
        np.linalg.inv(zeta * np.eye(3) - matrix), ord=2
    )
    resolvent_upper = np.nextafter(direct_resolvent + 1.0e-12, np.inf)
    certificate = similarity_certificate(
        defect_upper, residual_upper, resolvent_upper
    )
    transformed = np.linalg.solve(vectors, matrix @ vectors)
    transformed_error = np.linalg.norm(transformed - triangular, ord=2)
    transformed_resolvent = np.linalg.norm(
        np.linalg.inv(zeta * np.eye(3) - transformed), ord=2
    )
    assert certificate.invertibility_certified
    assert certificate.homotopy_certified
    assert transformed_error <= certificate.transformed_residual_upper
    assert transformed_resolvent <= certificate.transformed_resolvent_upper
