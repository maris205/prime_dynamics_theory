from __future__ import annotations

import numpy as np

from nested_grid import (
    coordinate_block_action,
    coordinate_block_adjoint_action,
    continuation_gate,
)
from outward_residuals import (
    ComponentwiseBall,
    componentwise_dense_exact_matmul,
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


class MatrixGraph:
    def __init__(self, matrix: np.ndarray):
        self.matrix = np.asarray(matrix)

    def two_step(self, source: ComponentwiseBall) -> ComponentwiseBall:
        return componentwise_dense_exact_matmul(self.matrix, source)

    def two_step_adjoint(self, source: ComponentwiseBall) -> ComponentwiseBall:
        return componentwise_dense_exact_matmul(self.matrix.T, source)


def test_dyadic_coordinate_maps_are_inverse() -> None:
    j, k, r, s = coordinate_matrices(7)
    transform = np.column_stack((j, k))
    inverse = np.vstack((r, s))
    np.testing.assert_array_equal(inverse @ transform, np.eye(14))
    np.testing.assert_array_equal(transform @ inverse, np.eye(14))


def test_componentwise_coordinate_blocks_enclose_dense_blocks() -> None:
    rng = np.random.default_rng(11235)
    dimension = 5
    coarse = rng.normal(size=(dimension, dimension)) / 7.0
    fine = rng.normal(size=(2 * dimension, 2 * dimension)) / 11.0
    coarse_graph = MatrixGraph(coarse)
    fine_graph = MatrixGraph(fine)
    j, k, r, s = coordinate_matrices(dimension)
    expected = {
        "coarse_consistency": r @ fine @ j - coarse,
        "coarse_to_detail": s @ fine @ j,
        "detail_to_coarse": r @ fine @ k,
        "detail_block": s @ fine @ k,
    }
    identity = ComponentwiseBall.exact(np.eye(dimension))
    for name, target in expected.items():
        ball = coordinate_block_action(
            name, coarse_graph, fine_graph, identity
        )
        error = np.abs(ball.center - target)
        assert np.all(error <= ball.radius + 5.0e-15)
        adjoint = coordinate_block_adjoint_action(
            name, coarse_graph, fine_graph, identity
        )
        adjoint_error = np.abs(adjoint.center - target.T)
        assert np.all(adjoint_error <= adjoint.radius + 5.0e-15)


def test_schur_determinant_identity() -> None:
    rng = np.random.default_rng(2718)
    dimension = 4
    fine = rng.normal(size=(2 * dimension, 2 * dimension)) / 9.0
    j, k, r, s = coordinate_matrices(dimension)
    a = r @ fine @ j
    b = r @ fine @ k
    c = s @ fine @ j
    d = s @ fine @ k
    zeta = 1.7 + 0.4j
    detail = zeta * np.eye(dimension) - d
    effective = zeta * np.eye(dimension) - a - b @ np.linalg.solve(detail, c)
    left = np.linalg.det(zeta * np.eye(2 * dimension) - fine)
    right = np.linalg.det(detail) * np.linalg.det(effective)
    np.testing.assert_allclose(left, right, rtol=3.0e-13, atol=3.0e-13)


def test_continuation_gate_composition() -> None:
    gate = continuation_gate(
        -0.31 - 0.55j,
        0.25,
        coarse_consistency_upper=2.0e-4,
        coarse_to_detail_upper=1.2e-2,
        detail_to_coarse_upper=1.4e-2,
        detail_norm_upper=1.5e-4,
    )
    assert gate.detail_spectrum_outside_counting_circle
    assert gate.detail_resolvent_upper < 3.0
    assert gate.self_energy_upper < 5.0e-4
    assert gate.effective_perturbation_upper < 7.0e-4
    assert gate.admissible_coarse_resolvent_upper > 1400.0
