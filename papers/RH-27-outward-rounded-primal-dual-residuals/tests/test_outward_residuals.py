from __future__ import annotations

import numpy as np
from scipy.sparse import csr_matrix

from outward_residuals import (
    ComponentwiseStoredFactorGraph,
    FrobeniusBall,
    LongDoubleFactorGraph,
    StoredFactorGraph,
    add,
    ball_utilization,
    certify_budget,
    dense_exact_matmul,
    dot_gamma,
    gamma,
    inverse_certificate,
    inverse_product_norm_upper,
    longdouble_frobenius,
    scalar_multiply,
    sparse_abs_operator_upper,
    sparse_exact_matmul,
)


def test_gamma_and_dot_constants_are_monotone() -> None:
    assert gamma(0) == 0.0
    assert gamma(100) > gamma(10) > 0.0
    assert dot_gamma(100, real_matrix=False) > dot_gamma(
        100, real_matrix=True
    )


def test_dense_ball_contains_longdouble_perturbation() -> None:
    rng = np.random.default_rng(20260715)
    operator = rng.normal(size=(9, 7))
    center = rng.normal(size=(7, 3)) + 1.0j * rng.normal(size=(7, 3))
    direction = rng.normal(size=(7, 3)) + 1.0j * rng.normal(size=(7, 3))
    direction /= np.linalg.norm(direction)
    radius = 2.0e-11
    perturbation = 0.91 * radius * direction
    enclosed = dense_exact_matmul(operator, FrobeniusBall(center, radius))
    reference = np.asarray(operator, dtype=np.clongdouble) @ (
        np.asarray(center, dtype=np.clongdouble)
        + np.asarray(perturbation, dtype=np.clongdouble)
    )
    defect = float(
        longdouble_frobenius(
            reference - np.asarray(enclosed.center, dtype=np.clongdouble)
        )
    )
    assert defect <= enclosed.radius


def test_sparse_ball_contains_longdouble_product() -> None:
    rng = np.random.default_rng(31)
    dense = rng.uniform(size=(17, 17))
    dense[dense < 0.72] = 0.0
    matrix = csr_matrix(dense)
    values = rng.normal(size=(17, 2)) + 1.0j * rng.normal(size=(17, 2))
    enclosed = sparse_exact_matmul(
        matrix,
        FrobeniusBall.exact(values),
        abs_operator_upper=sparse_abs_operator_upper(matrix),
        maximum_row_nonzeros=int(np.max(np.diff(matrix.indptr))),
    )
    reference = np.asarray(dense, dtype=np.clongdouble) @ np.asarray(
        values, dtype=np.clongdouble
    )
    assert ball_utilization(reference, enclosed) <= 1.0


def test_addition_and_scalar_enclosures_contain_longdouble_values() -> None:
    first = FrobeniusBall(np.array([[1.0 + 2.0j], [3.0 - 1.0j]]), 1.0e-12)
    second = FrobeniusBall(np.array([[-0.5j], [2.0 + 4.0j]]), 3.0e-12)
    summed = add(first, second)
    scaled = scalar_multiply(0.7 - 0.2j, summed)
    first_error = np.array([[0.3e-12], [-0.2e-12j]])
    second_error = np.array([[0.4e-12j], [0.5e-12]])
    reference = np.clongdouble(0.7 - 0.2j) * (
        np.asarray(first.center + first_error, dtype=np.clongdouble)
        + np.asarray(second.center + second_error, dtype=np.clongdouble)
    )
    assert ball_utilization(reference, scaled) <= 1.0


def test_neumann_inverse_certificate_bounds_direct_products() -> None:
    rng = np.random.default_rng(47)
    matrix = rng.normal(size=(5, 5)) + 1.0j * rng.normal(size=(5, 5))
    matrix += 5.0 * np.eye(5)
    right = rng.normal(size=(5, 3)) + 1.0j * rng.normal(size=(5, 3))
    certificate = inverse_certificate(matrix)
    upper = inverse_product_norm_upper(
        certificate, FrobeniusBall.exact(right)
    )
    direct = np.linalg.solve(matrix, right)
    assert certificate.defect_norm_upper < 1.0e-12
    assert np.linalg.norm(direct, ord="fro") <= upper


def random_factor_graph(seed: int = 59):
    rng = np.random.default_rng(seed)
    dimension = 18
    rank = 3
    peripheral_rank = 2
    raw = rng.uniform(size=(dimension, dimension))
    raw[raw < 0.78] = 0.0
    raw += 0.2 * np.eye(dimension)
    raw /= raw.sum(axis=1, keepdims=True)
    matrix = csr_matrix(raw)
    right = rng.normal(size=(dimension, peripheral_rank)) / 5.0
    left = rng.normal(size=(dimension, peripheral_rank)) / 5.0
    values = np.array([0.9, -0.7])
    synthesis = rng.normal(size=(dimension, rank)) / 4.0
    analysis = rng.normal(size=(rank, dimension)) / 4.0
    stored = StoredFactorGraph(
        matrix, right, left, values, synthesis, analysis
    )
    extended = LongDoubleFactorGraph(
        matrix, right, left, values, synthesis, analysis
    )
    return rng, stored, extended


def test_full_factor_graph_encloses_longdouble_blocks_and_node() -> None:
    rng, stored, extended = random_factor_graph()
    blocks = stored.build_blocks()
    reference_blocks = extended.build_blocks()
    assert ball_utilization(reference_blocks.direct, blocks.direct) <= 1.0
    assert ball_utilization(reference_blocks.forcing, blocks.forcing) <= 1.0
    assert (
        ball_utilization(
            reference_blocks.observation_adjoint,
            blocks.observation_adjoint,
        )
        <= 1.0
    )

    rank = stored.synthesis.shape[1]
    dimension = stored.matrix.shape[0]
    base_solution = rng.normal(size=(dimension, rank)) / 7.0
    deep_solution = base_solution + rng.normal(size=(dimension, rank)) / 30.0
    dual_solution = rng.normal(size=(dimension, rank)) / 6.0
    zeta = 0.4 + 0.2j
    base_feshbach = (
        1.5 * np.eye(rank)
        + rng.normal(size=(rank, rank)) / 20.0
        + 1.0j * rng.normal(size=(rank, rank)) / 20.0
    )
    node = stored.node_enclosures(
        blocks,
        zeta,
        base_feshbach,
        base_solution,
        deep_solution,
        dual_solution,
    )
    reference = extended.node(
        reference_blocks,
        zeta,
        base_feshbach,
        base_solution,
        deep_solution,
        dual_solution,
    )
    for name in (
        "primal_residual",
        "dual_residual",
        "base_consistency",
        "primal_increment",
        "primal_correction",
        "dual_weighted_correction",
        "total_computed_correction",
    ):
        assert ball_utilization(getattr(reference, name), getattr(node, name)) <= 1.0

    budget = certify_budget(
        base_feshbach,
        node.total_computed_correction,
        node.primal_residual,
        node.dual_residual,
    )
    assert budget.correction_ratio_upper > 0.0
    assert budget.remainder_coefficient_upper > 0.0
    assert budget.resolvent_budget_lower >= 0.0


def test_componentwise_graph_tightens_and_contains_longdouble_node() -> None:
    rng, stored, extended = random_factor_graph(83)
    componentwise = ComponentwiseStoredFactorGraph(
        stored.matrix,
        stored.right,
        stored.left,
        stored.values,
        stored.synthesis,
        stored.analysis,
    )
    scalar_blocks = stored.build_blocks()
    component_blocks = componentwise.build_blocks()
    reference_blocks = extended.build_blocks()
    assert (
        ball_utilization(
            reference_blocks.forcing,
            component_blocks.forcing.as_frobenius_ball(),
        )
        <= 1.0
    )
    assert (
        component_blocks.forcing.radius_frobenius_upper
        <= scalar_blocks.forcing.radius
    )

    rank = stored.synthesis.shape[1]
    dimension = stored.matrix.shape[0]
    base_solution = rng.normal(size=(dimension, rank)) / 5.0
    deep_solution = base_solution + rng.normal(size=(dimension, rank)) / 40.0
    dual_solution = rng.normal(size=(dimension, rank)) / 8.0
    zeta = 0.31 - 0.17j
    base_feshbach = 1.2 * np.eye(rank) + (
        rng.normal(size=(rank, rank))
        + 1.0j * rng.normal(size=(rank, rank))
    ) / 30.0
    node = componentwise.node(
        component_blocks,
        zeta,
        base_feshbach,
        base_solution,
        deep_solution,
        dual_solution,
    )
    reference = extended.node(
        reference_blocks,
        zeta,
        base_feshbach,
        base_solution,
        deep_solution,
        dual_solution,
    )
    for name in (
        "primal_residual",
        "dual_residual",
        "base_consistency",
        "total_computed_correction",
    ):
        assert (
            ball_utilization(
                getattr(reference, name),
                getattr(node, name).as_frobenius_ball(),
            )
            <= 1.0
        )
