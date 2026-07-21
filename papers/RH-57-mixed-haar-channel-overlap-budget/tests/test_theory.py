import math

import numpy as np
import pytest
from scipy.linalg import solve_discrete_lyapunov

from haar_overlap import (
    block_gram_from_gramian,
    gram_budget,
    hardy_cauchy_gram,
    radial_riesz_partition,
)


def test_simple_mode_cauchy_gram_matches_long_time_sum() -> None:
    values = np.asarray((0.62, -0.41, 0.18j), dtype=np.complex128)
    overlaps = (
        np.asarray([[0.7, -0.2j]]),
        np.asarray([[0.1 + 0.3j, -0.5]]),
        np.asarray([[-0.4j, 0.2]]),
    )
    radius = 0.85
    exact = hardy_cauchy_gram(values, overlaps, radius)
    partial = np.zeros_like(exact)
    for power in range(500):
        responses = [
            (value / radius) ** power * overlap
            for value, overlap in zip(values, overlaps)
        ]
        for row in range(3):
            for column in range(3):
                partial[row, column] += np.vdot(
                    responses[column], responses[row]
                )
    assert np.linalg.norm(exact - partial, 2) < 2.0e-13


def test_riesz_block_gram_reconstructs_full_hardy_energy() -> None:
    similarity = np.asarray(
        [[1.0, 2.0, -0.3], [0.1, 1.0, 0.8], [0.0, -0.2, 1.0]]
    )
    diagonal = np.diag((0.72, -0.46, 0.18))
    operator = similarity @ diagonal @ np.linalg.inv(similarity)
    source = np.asarray([[1.0, -0.2], [0.4, 0.7], [-0.3, 0.1]])
    observation = np.asarray([[0.8, -0.1, 0.5], [0.2, 0.4, -0.7]])
    gramian = solve_discrete_lyapunov(operator, source @ source.T)
    partition = radial_riesz_partition(
        operator,
        (0.3, 0.6),
        names=("central", "middle", "edge"),
    )
    block_gram = block_gram_from_gramian(
        gramian, observation, partition.projectors
    )
    budget = gram_budget(block_gram)
    direct = math.sqrt(
        float(np.trace(observation @ gramian @ observation.T).real)
    )
    assert partition.counts == (1, 1, 1)
    assert partition.partition_defect < 1.0e-12
    assert max(partition.commutator_defects) < 1.0e-12
    assert budget.exact_energy == pytest.approx(direct, rel=2.0e-13)
    assert direct <= budget.coherence_upper * (1.0 + 2.0e-13)
    assert direct <= budget.gershgorin_upper * (1.0 + 2.0e-13)
    assert direct <= budget.absolute_block_upper * (1.0 + 2.0e-13)
    assert 0.0 <= budget.signed_fusion_ratio <= budget.coherence_constant
    assert budget.minimum_gram_eigenvalue > -1.0e-12


def test_central_projector_is_complement_of_resolved_outer_blocks() -> None:
    operator = np.asarray(
        [[0.12, 3.0, 0.0], [0.0, 0.51, 1.2], [0.0, 0.0, -0.79]]
    )
    partition = radial_riesz_partition(
        operator,
        (0.2, 0.65),
        names=("central", "middle", "edge"),
    )
    identity = sum(partition.projectors, start=np.zeros_like(operator, dtype=complex))
    assert np.linalg.norm(identity - np.eye(3), 2) < 1.0e-12
    assert max(partition.idempotence_defects) < 1.0e-12
    assert partition.pairwise_product_defect < 1.0e-12


def test_invalid_partition_and_modal_radius_are_rejected() -> None:
    with pytest.raises(ValueError):
        radial_riesz_partition(np.eye(2), (0.5, 0.4))
    with pytest.raises(ValueError):
        hardy_cauchy_gram([0.9], [1.0], 0.85)
