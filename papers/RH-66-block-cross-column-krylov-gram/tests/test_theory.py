import numpy as np
import pytest

from block_krylov_gram import (
    block_gram_certificate,
    directional_certificate,
    lyapunov_metric,
)


def chain_model() -> tuple[np.ndarray, np.ndarray]:
    operator = np.asarray(
        [
            [0.95, 0.42, 0.0, 0.0],
            [0.0, 0.70, 0.38, 0.0],
            [0.0, 0.0, 0.50, 0.31],
            [0.0, 0.0, 0.0, 0.30],
        ],
        dtype=np.complex128,
    )
    sources = np.asarray(
        [[0.0, 0.0], [0.1, -0.05], [0.3, 0.2], [1.0, -0.7]],
        dtype=np.complex128,
    )
    return operator, sources


def test_psd_gram_envelope_dominates_exact_gram() -> None:
    operator, sources = chain_model()
    metric = lyapunov_metric(operator)
    certificate = block_gram_certificate(
        operator, sources, metric, 16, 1
    )
    slack = certificate.gram_envelope - certificate.exact_gram
    slack = 0.5 * (slack + slack.conjugate().T)
    assert np.min(np.linalg.eigvalsh(slack)) > -1.0e-9


def test_directional_certificate_dominates_complex_phase_energy() -> None:
    operator, sources = chain_model()
    metric = lyapunov_metric(operator)
    coefficients = np.asarray([1.0, np.exp(1.3j)])
    certificate = directional_certificate(
        operator, sources, metric, 16, 1, coefficients
    )
    assert certificate.upper_energy >= certificate.exact_energy * (
        1.0 - 1.0e-10
    )


def test_full_block_krylov_closure_is_exact() -> None:
    operator, sources = chain_model()
    metric = lyapunov_metric(operator)
    certificate = directional_certificate(
        operator, sources, metric, 16, 2, np.ones(2)
    )
    assert certificate.upper_energy == pytest.approx(
        certificate.exact_energy, rel=1.0e-10, abs=1.0e-12
    )


def test_cancelling_direction_is_preserved() -> None:
    operator = np.diag([0.995, 0.55, 0.2]).astype(np.complex128)
    sources = np.asarray(
        [[1.0, -1.0], [1.0, 1.0], [0.2, -0.2]],
        dtype=np.complex128,
    )
    metric = lyapunov_metric(operator)
    certificate = directional_certificate(
        operator, sources, metric, 32, 1, np.ones(2)
    )
    assert certificate.upper_energy / certificate.exact_energy < 1.00001


@pytest.mark.parametrize(
    "call",
    [
        lambda: lyapunov_metric(np.eye(2) * 1.1),
        lambda: block_gram_certificate(
            np.eye(2) * 0.2, np.ones((3, 1)), np.eye(2), 1, 1
        ),
        lambda: block_gram_certificate(
            np.eye(2) * 0.2, np.ones((2, 1)), np.eye(2), -1, 1
        ),
        lambda: directional_certificate(
            np.eye(2) * 0.2,
            np.ones((2, 1)),
            np.eye(2),
            1,
            1,
            np.ones(2),
        ),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
