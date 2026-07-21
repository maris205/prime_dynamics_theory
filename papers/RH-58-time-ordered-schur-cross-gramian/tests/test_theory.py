import math

import numpy as np
import pytest
from scipy.linalg import solve_discrete_lyapunov

from schur_fusion import (
    cross_stein_recursion_audit,
    gram_budget,
    ordered_radial_schur,
    scalar_path_majorant,
    schur_source_gram,
    schur_state_gram,
)


def example():
    operator = np.asarray(
        [[0.12, 0.9, -0.25], [0.0, 0.46, 0.7], [0.0, 0.0, -0.78]],
        dtype=np.complex128,
    )
    source = np.asarray([[0.7, -0.1], [0.2, 0.5], [-0.3, 0.4]])
    observation = np.asarray([[0.8, 0.1, -0.4], [0.2, -0.6, 0.5]])
    return operator, source, observation


def test_ordered_schur_is_unitary_and_radially_grouped() -> None:
    operator, _, _ = example()
    partition = ordered_radial_schur(
        operator,
        (0.2, 0.6),
        names=("central", "middle", "edge"),
    )
    assert partition.names == ("central", "middle", "edge")
    assert partition.sizes == (1, 1, 1)
    assert partition.reconstruction_defect < 1.0e-13
    assert partition.unitary_defect < 1.0e-13
    assert partition.strict_lower_defect < 1.0e-13


def test_dual_packet_grams_reconstruct_the_same_hardy_energy() -> None:
    operator, source, observation = example()
    partition = ordered_radial_schur(
        operator, (0.2, 0.6), names=("central", "middle", "edge")
    )
    controllability = solve_discrete_lyapunov(
        operator, source @ source.conjugate().T
    )
    observability = solve_discrete_lyapunov(
        operator.conjugate().T, observation.conjugate().T @ observation
    )
    state = gram_budget(
        schur_state_gram(controllability, observation, partition)
    )
    initial = gram_budget(
        schur_source_gram(observability, source, partition)
    )
    direct = math.sqrt(
        float(np.trace(observation @ controllability @ observation.conjugate().T).real)
    )
    assert state.exact_energy == pytest.approx(direct, rel=2.0e-13)
    assert initial.exact_energy == pytest.approx(direct, rel=2.0e-13)
    assert state.minimum_gram_eigenvalue > -1.0e-12
    assert initial.minimum_gram_eigenvalue > -1.0e-12


def test_reverse_cross_stein_recursion_and_majorant() -> None:
    operator, source, observation = example()
    partition = ordered_radial_schur(
        operator, (0.2, 0.6), names=("central", "middle", "edge")
    )
    gramian = solve_discrete_lyapunov(
        operator, source @ source.conjugate().T
    )
    audit = cross_stein_recursion_audit(gramian, source, partition)
    majorant = scalar_path_majorant(
        source, observation, partition, horizon=8
    )
    exact_squared = float(
        np.trace(observation @ gramian @ observation.conjugate().T).real
    )
    assert audit.maximum_residual_norm < 2.0e-12
    assert majorant.energy_squared_upper >= exact_squared * (1.0 - 2.0e-12)
    for row in audit.rows:
        assert (
            row.gramian_norm
            <= majorant.gramian_norm_uppers[row.left_block, row.right_block]
            * (1.0 + 2.0e-12)
        )


def test_invalid_cuts_and_noncontracting_horizon_are_rejected() -> None:
    operator, source, observation = example()
    with pytest.raises(ValueError):
        ordered_radial_schur(operator, (0.6, 0.2))
    partition = ordered_radial_schur(
        operator, (0.2, 0.6), names=("central", "middle", "edge")
    )
    with pytest.raises(ValueError):
        scalar_path_majorant(source, observation, partition, horizon=0)
