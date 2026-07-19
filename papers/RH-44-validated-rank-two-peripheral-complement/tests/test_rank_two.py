from __future__ import annotations

import numpy as np

from rank_two_complement import (
    combine_kernel_envelopes,
    perron_kernel_envelope,
    rank_two_cutoff_upper,
)


def test_perron_kernel_is_source_independent_and_second_order() -> None:
    first = perron_kernel_envelope(
        contour_radius=0.05,
        contour_resolvent_upper=82.0,
        kernel_target_first_upper=383.0,
        kernel_target_second_upper=47500.0,
        midpoint_dimension=65536,
    )
    second = perron_kernel_envelope(
        contour_radius=0.05,
        contour_resolvent_upper=82.0,
        kernel_target_first_upper=383.0,
        kernel_target_second_upper=47500.0,
        midpoint_dimension=131072,
    )
    assert first.kernel_hilbert_schmidt_lower == 1.0
    assert first.source_first_hilbert_schmidt_upper == 0.0
    assert first.source_second_hilbert_schmidt_upper == 0.0
    assert first.source_target_hilbert_schmidt_upper == 0.0
    assert second.midpoint_to_cell_average_upper < (
        first.midpoint_to_cell_average_upper / 3.99
    )


def test_kernel_envelopes_add_outward() -> None:
    perron = perron_kernel_envelope(
        contour_radius=0.05,
        contour_resolvent_upper=82.0,
        kernel_target_first_upper=383.0,
        kernel_target_second_upper=47500.0,
        midpoint_dimension=65536,
    )
    parity = {
        "kernel_hilbert_schmidt_upper": 5.9,
        "source_first_hilbert_schmidt_upper": 3.0,
        "target_first_hilbert_schmidt_upper": 2.0,
        "source_second_hilbert_schmidt_upper": 7.0,
        "source_target_hilbert_schmidt_upper": 8.0,
        "target_second_hilbert_schmidt_upper": 9.0,
        "source_second_target_second_hilbert_schmidt_upper": 10.0,
        "midpoint_to_cell_average_upper": 1.0e-5,
        "midpoint_dimension": 65536,
    }
    combined = combine_kernel_envelopes(perron, parity)
    assert combined["kernel_hilbert_schmidt_upper"] > 10.0
    assert combined["source_first_hilbert_schmidt_upper"] >= 3.0
    assert combined["target_first_hilbert_schmidt_upper"] > 2.0


def test_rank_two_cutoff_adds_matrix_once() -> None:
    weighted, deflated = rank_two_cutoff_upper(2.0e-13, 2.0e-10, 7.3e-10)
    assert 9.3e-10 <= weighted < 9.31e-10
    assert weighted < deflated < weighted + 2.01e-13


def test_bulk_power_trace_and_determinant_identities() -> None:
    rng = np.random.default_rng(20260720)
    basis = rng.normal(size=(5, 5))
    while abs(np.linalg.det(basis)) < 0.1:
        basis = rng.normal(size=(5, 5))
    inverse = np.linalg.inv(basis)
    eigenvalues = np.array([1.0, -0.83, 0.31, -0.17, 0.08])
    matrix = basis @ np.diag(eigenvalues) @ inverse
    perron_projection = basis[:, :1] @ inverse[:1, :]
    parity_projection = basis[:, 1:2] @ inverse[1:2, :]
    perron_term = perron_projection
    parity_term = eigenvalues[1] * parity_projection
    bulk = matrix - perron_term - parity_term

    for power in range(1, 6):
        expected = (
            np.linalg.matrix_power(matrix, power)
            - perron_term
            - eigenvalues[1] ** (power - 1) * parity_term
        )
        assert np.allclose(np.linalg.matrix_power(bulk, power), expected)
        assert np.isclose(
            np.trace(np.linalg.matrix_power(bulk, power)),
            np.trace(np.linalg.matrix_power(matrix, power))
            - 1.0
            - eigenvalues[1] ** power,
        )

    z = 0.23
    left = np.linalg.det(np.eye(5) - z * matrix)
    right = (
        (1.0 - z)
        * (1.0 - z * eigenvalues[1])
        * np.linalg.det(np.eye(5) - z * bulk)
    )
    assert np.isclose(left, right)
