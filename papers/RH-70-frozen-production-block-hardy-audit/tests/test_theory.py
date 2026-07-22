import numpy as np
import pytest
from scipy.linalg import solve_discrete_lyapunov

from production_hardy import (
    augmented_difference_system,
    block_hardy_certificate,
)


def test_block_hardy_certificate_dominates_exact_energy() -> None:
    operator = np.asarray([[0.5, 0.2], [0.0, 0.3]], dtype=np.complex128)
    source = np.asarray([[1.0], [0.4]], dtype=np.complex128)
    observation = np.asarray([[0.7, -0.2]], dtype=np.complex128)
    gram = solve_discrete_lyapunov(
        operator.conjugate().T,
        observation.conjugate().T @ observation,
    )
    exact = float(np.real(np.trace(source.conjugate().T @ gram @ source)))
    certificate = block_hardy_certificate(
        operator, source, observation, 4
    )
    assert certificate.full_energy_squared_upper >= exact * (1.0 - 1.0e-12)


def test_augmented_system_realizes_transfer_difference() -> None:
    operator = np.diag([0.5, 0.2]).astype(np.complex128)
    comparison = np.diag([0.45, 0.25]).astype(np.complex128)
    source = np.asarray([[1.0], [0.3]])
    source_tilde = np.asarray([[0.8], [0.4]])
    observation = np.asarray([[1.0, -0.2]])
    observation_tilde = np.asarray([[0.9, -0.1]])
    augmented = augmented_difference_system(
        operator,
        source,
        observation,
        comparison,
        source_tilde,
        observation_tilde,
    )
    for power in range(5):
        direct = (
            observation @ np.linalg.matrix_power(operator, power) @ source
            - observation_tilde
            @ np.linalg.matrix_power(comparison, power)
            @ source_tilde
        )
        realized = (
            augmented[2]
            @ np.linalg.matrix_power(augmented[0], power)
            @ augmented[1]
        )
        assert realized == pytest.approx(direct)


@pytest.mark.parametrize(
    "call",
    [
        lambda: block_hardy_certificate(
            np.eye(2), np.ones((2, 1)), np.ones((1, 2)), 0
        ),
        lambda: block_hardy_certificate(
            np.eye(2) * 1.1, np.ones((2, 1)), np.ones((1, 2)), 1
        ),
        lambda: augmented_difference_system(
            np.eye(2),
            np.ones((2, 1)),
            np.ones((1, 2)),
            np.eye(3),
            np.ones((3, 1)),
            np.ones((1, 3)),
        ),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
