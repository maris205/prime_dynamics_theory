import numpy as np
import pytest

from krylov_tail import (
    arnoldi,
    geometric_power_upper,
    krylov_power_certificate,
    stein_krylov_tail_upper,
)


def example() -> tuple[np.ndarray, np.ndarray]:
    operator = np.asarray(
        [[0.2, 0.35], [0.0, 0.65]], dtype=np.complex128
    )
    source = np.asarray([0.4, 0.7], dtype=np.complex128)
    return operator, source


def test_arnoldi_identity_and_orthogonality() -> None:
    operator, source = example()
    certificate = arnoldi(operator, source, 2)
    basis = certificate.basis
    hessenberg = certificate.hessenberg
    selector = np.zeros(basis.shape[1], dtype=np.complex128)
    selector[-1] = 1.0
    defect = operator @ basis - basis @ hessenberg - np.outer(
        certificate.residual_vector, selector.conjugate()
    )
    assert np.linalg.norm(basis.conjugate().T @ basis - np.eye(2)) < 1.0e-12
    assert np.linalg.norm(defect) < 1.0e-12


def test_krylov_upper_dominates_exact_power_and_improves_at_full_dimension() -> None:
    operator, source = example()
    geometric = geometric_power_upper(
        np.linalg.norm(operator, 2), source, 8
    )
    one_step = krylov_power_certificate(operator, source, 8, 1)
    full = krylov_power_certificate(operator, source, 8, 2)
    exact = np.linalg.norm(np.linalg.matrix_power(operator, 8) @ source)
    assert one_step.upper_bound >= exact * (1.0 - 1.0e-12)
    assert full.upper_bound >= exact * (1.0 - 1.0e-12)
    assert full.upper_bound <= geometric + 1.0e-12
    assert full.upper_bound == pytest.approx(exact, rel=1.0e-11)


def test_eigenvector_breakdown_is_exact() -> None:
    operator = np.diag([0.8, 0.3]).astype(np.complex128)
    source = np.asarray([1.0, 0.0], dtype=np.complex128)
    certificate = krylov_power_certificate(operator, source, 12, 1)
    assert certificate.breakdown
    assert certificate.residual_bound == pytest.approx(0.0)
    assert certificate.upper_bound == pytest.approx(0.8**12)
    assert stein_krylov_tail_upper(4.0, certificate) == pytest.approx(
        2.0 * 0.8**12
    )


@pytest.mark.parametrize(
    "call",
    [
        lambda: arnoldi(np.eye(2), np.ones(2), 0),
        lambda: krylov_power_certificate(np.eye(2), np.ones(2), -1, 1),
        lambda: geometric_power_upper(-1.0, np.ones(2), 1),
        lambda: stein_krylov_tail_upper(-1.0, krylov_power_certificate(
            np.eye(2) * 0.2, np.ones(2), 1, 1
        )),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
