import numpy as np
import pytest

from covariance_envelope import (
    block_components,
    coefficient_frame,
    covariance_certificate,
    diagonal_cancellation_ledger,
    lyapunov_metric,
)


def chain_components():
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
    coefficients = np.asarray([1.0, np.exp(1.3j)])
    metric = lyapunov_metric(operator)
    return block_components(
        operator, sources, metric, 16, 1, coefficients
    )


def test_coefficient_frame_is_unitary_and_aligns_ray() -> None:
    coefficients = np.asarray([1.0, 2.0j, -0.5])
    frame = coefficient_frame(coefficients)
    assert frame.conjugate().T @ frame == pytest.approx(np.eye(3))
    assert frame[:, 0] == pytest.approx(
        coefficients / np.linalg.norm(coefficients)
    )


@pytest.mark.parametrize("epsilon", [1.0, 1.0e-4, 1.0e-8])
def test_covariance_envelope_dominates_exact_gram(epsilon: float) -> None:
    certificate = covariance_certificate(chain_components(), epsilon)
    assert certificate.minimum_slack_eigenvalue > -1.0e-9


def test_focusing_approaches_directional_optimum() -> None:
    components = chain_components()
    isotropic = covariance_certificate(components, 1.0)
    focused = covariance_certificate(components, 1.0e-10)
    assert focused.physical_gain <= isotropic.physical_gain
    assert abs(
        focused.physical_gain - focused.directional_optimal_gain
    ) < abs(
        isotropic.physical_gain - isotropic.directional_optimal_gain
    )


def test_exact_cancellation_has_sharpness_size_tradeoff() -> None:
    isotropic = diagonal_cancellation_ledger(1.0)
    focused = diagonal_cancellation_ledger(1.0e-24)
    assert 2.0 < isotropic.physical_gain < 3.0
    assert focused.physical_gain < 1.002
    assert focused.global_spectral_gain > 400.0


@pytest.mark.parametrize(
    "call",
    [
        lambda: coefficient_frame(np.zeros(2)),
        lambda: diagonal_cancellation_ledger(0.0),
        lambda: diagonal_cancellation_ledger(1.0, slow=1.1),
        lambda: covariance_certificate(chain_components(), 2.0),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
