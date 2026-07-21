import numpy as np
import pytest

from nested_krylov import nested_krylov_certificate


def two_block() -> tuple[np.ndarray, np.ndarray]:
    return (
        np.asarray([[0.2, 0.3], [0.0, 0.7]], dtype=np.complex128),
        np.asarray([0.0, 0.4], dtype=np.complex128),
    )


def test_nested_level_repairs_two_block_residual() -> None:
    operator, source = two_block()
    one = nested_krylov_certificate(operator, source, 16, (1,))
    nested = nested_krylov_certificate(operator, source, 16, (1, 1))
    assert one.upper_bound >= one.exact_norm
    assert nested.upper_bound >= nested.exact_norm * (1.0 - 1.0e-12)
    assert nested.upper_bound == pytest.approx(nested.exact_norm, rel=1.0e-11)
    assert nested.remainder_bound == pytest.approx(0.0)
    assert nested.upper_bound < one.upper_bound


def test_full_first_level_breakdown_is_exact() -> None:
    operator, source = two_block()
    certificate = nested_krylov_certificate(operator, source, 12, (2,))
    assert certificate.terminal_breakdown
    assert certificate.remainder_bound == pytest.approx(0.0)
    assert certificate.upper_bound == pytest.approx(
        certificate.exact_norm, rel=1.0e-11
    )


def test_nonnormal_chain_remains_an_upper_at_every_depth() -> None:
    operator = np.asarray(
        [
            [0.95, 0.42, 0.0, 0.0],
            [0.0, 0.70, 0.38, 0.0],
            [0.0, 0.0, 0.50, 0.31],
            [0.0, 0.0, 0.0, 0.30],
        ],
        dtype=np.complex128,
    )
    source = np.asarray([0.0, 0.0, 0.0, 1.0])
    uppers = []
    for depth in range(1, 5):
        certificate = nested_krylov_certificate(
            operator, source, 20, (1,) * depth
        )
        assert certificate.upper_bound >= certificate.exact_norm * (
            1.0 - 1.0e-11
        )
        uppers.append(certificate.upper_bound)
    assert uppers[-1] == pytest.approx(
        nested_krylov_certificate(operator, source, 20, (4,)).exact_norm,
        rel=1.0e-10,
    )


@pytest.mark.parametrize(
    "call",
    [
        lambda: nested_krylov_certificate(np.eye(2), np.ones(2), 1, ()),
        lambda: nested_krylov_certificate(np.eye(2), np.ones(2), -1, (1,)),
        lambda: nested_krylov_certificate(np.eye(2), np.ones(2), 1, (3,)),
        lambda: nested_krylov_certificate(
            np.eye(2), np.ones(2), 1, (1,), operator_norm=-1.0
        ),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
