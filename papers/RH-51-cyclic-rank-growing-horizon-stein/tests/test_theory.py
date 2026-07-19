from __future__ import annotations

import numpy as np

from structured_stein import (
    block_stein_defect,
    conic_vector_witness,
    controllability_gramian,
    cyclic_rank_profile,
    finite_horizon_gramian,
    isotropic_block_completion,
    low_rank_isotropic_floor,
    stein_defect,
    supersolution_audit,
)


def stable_random_pair(seed: int = 5101):
    rng = np.random.default_rng(seed)
    operator = rng.normal(size=(7, 7)) / 5.0
    operator *= 0.63 / max(abs(np.linalg.eigvals(operator)))
    source = rng.normal(size=(7, 2))
    return operator, source


def test_exact_gramian_is_the_minimal_positive_supersolution() -> None:
    operator, source = stable_random_pair()
    gramian = controllability_gramian(operator, source)
    background = controllability_gramian(operator, np.eye(7))
    candidate = gramian + 0.3 * background
    audit = supersolution_audit(operator, source, candidate)
    assert audit.admissible
    assert audit.defect_minimum_eigenvalue > 0.29
    assert audit.dominates_exact_gramian_minimum_eigenvalue > 0.0
    assert np.linalg.norm(stein_defect(operator, gramian, source), 2) < 2.0e-11


def test_gramian_range_equals_the_directional_cyclic_span() -> None:
    dimension = 6
    operator = np.zeros((dimension, dimension))
    operator[np.arange(1, dimension), np.arange(dimension - 1)] = 0.4
    source = np.eye(dimension)[:, :1]
    gramian = controllability_gramian(operator, source)
    profile = cyclic_rank_profile(
        operator, source, dimension - 1, relative_tolerance=1.0e-12
    )
    assert [row["numerical_rank"] for row in profile] == list(
        range(1, dimension + 1)
    )
    assert np.linalg.matrix_rank(gramian, tol=1.0e-13) == dimension


def test_one_step_supersolution_telescopes_to_every_block() -> None:
    operator, source = stable_random_pair(5102)
    gramian = controllability_gramian(operator, source)
    background = controllability_gramian(operator, np.eye(7))
    candidate = gramian + 0.1 * background
    for horizon in (1, 2, 5, 9):
        defect = block_stein_defect(
            operator, candidate, source, horizon
        )
        assert np.min(np.linalg.eigvalsh(defect)) > -2.0e-10


def test_isotropic_block_completion_dominates_the_infinite_gramian() -> None:
    operator, source = stable_random_pair(5103)
    horizon = 18
    completion = isotropic_block_completion(operator, source, horizon)
    gramian = controllability_gramian(operator, source)
    assert completion.power_norm < 1.0
    assert completion.block_defect_minimum_eigenvalue > -2.0e-9
    assert np.min(
        np.linalg.eigvalsh(completion.candidate - gramian)
    ) > -2.0e-9
    partial = finite_horizon_gramian(operator, source, horizon)
    assert np.min(np.linalg.eigvalsh(completion.candidate - partial)) >= 0.0


def test_scalar_identity_cone_has_a_rank_one_dual_witness() -> None:
    operator = np.asarray(((0.5, 2.0), (0.0, 0.4)))
    source = np.eye(2)
    defect = np.eye(2) - operator @ operator.T
    _, vectors = np.linalg.eigh(defect)
    witness = conic_vector_witness(
        operator, source, (np.eye(2),), vectors[:, 0]
    )
    assert witness.obstructs_cone
    assert witness.generator_quadratic_forms[0] < 0.0
    assert witness.source_quadratic_form > 0.99


def test_low_rank_plus_identity_floor_is_the_next_gramian_eigenvalue() -> None:
    gramian = np.diag((9.0, 4.0, 2.0, 0.5))
    assert low_rank_isotropic_floor(gramian, 0) == 9.0
    assert low_rank_isotropic_floor(gramian, 1) == 4.0
    assert low_rank_isotropic_floor(gramian, 2) == 2.0
    assert low_rank_isotropic_floor(gramian, 4) == 0.0
