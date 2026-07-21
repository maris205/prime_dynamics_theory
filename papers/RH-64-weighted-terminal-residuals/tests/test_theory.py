import numpy as np
import pytest

from weighted_residual import (
    lyapunov_metric,
    metric_contraction,
    weighted_nested_certificate,
)


def two_block() -> tuple[np.ndarray, np.ndarray]:
    return (
        np.asarray([[0.2, 0.3], [0.0, 0.7]], dtype=np.complex128),
        np.asarray([0.0, 0.4], dtype=np.complex128),
    )


def test_lyapunov_metric_is_positive_and_contracts() -> None:
    operator, _ = two_block()
    metric = lyapunov_metric(operator)
    assert np.min(np.linalg.eigvalsh(metric)) > 0.0
    assert metric_contraction(operator, metric) < 1.0


def test_weighted_certificate_dominates_exact_metric_power() -> None:
    operator, source = two_block()
    metric = lyapunov_metric(operator)
    certificate = weighted_nested_certificate(
        operator, source, metric, 16, (1,)
    )
    assert certificate.upper_bound >= certificate.exact_metric_norm * (
        1.0 - 1.0e-11
    )
    nested = weighted_nested_certificate(
        operator, source, metric, 16, (1, 1)
    )
    assert nested.upper_bound == pytest.approx(
        nested.exact_metric_norm, rel=1.0e-10
    )


def test_weighted_full_breakdown_is_exact() -> None:
    operator = np.diag([0.8, 0.3]).astype(np.complex128)
    source = np.asarray([1.0, 0.0])
    metric = lyapunov_metric(operator)
    certificate = weighted_nested_certificate(
        operator, source, metric, 12, (1,)
    )
    assert certificate.terminal_breakdown
    assert certificate.terminal_remainder_bound == pytest.approx(0.0)
    assert certificate.upper_bound == pytest.approx(
        certificate.exact_metric_norm, rel=1.0e-11
    )


@pytest.mark.parametrize(
    "call",
    [
        lambda: lyapunov_metric(np.eye(2) * 1.1),
        lambda: weighted_nested_certificate(
            np.eye(2), np.ones(2), np.eye(3), 1, (1,)
        ),
        lambda: weighted_nested_certificate(
            np.eye(2) * 0.2, np.ones(2), np.eye(2), -1, (1,)
        ),
        lambda: weighted_nested_certificate(
            np.eye(2) * 0.2, np.ones(2), np.eye(2), 1, ()
        ),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
