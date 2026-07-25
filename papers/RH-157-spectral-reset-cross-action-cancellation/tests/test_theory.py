import numpy as np
import pytest

from cross_cancellation import coupling_radius, singular_interval


def test_exact_cross_cancellation() -> None:
    memory = np.diag([4.0, 3.0, 2.0, 1.0])
    projector = np.diag([1.0, 1.0, 0.0, 0.0])
    tail = np.array([[0.1, 0.0, 0.2, 0.0], [0.0, 0.1, 0.0, 0.3], [0.2, 0.0, 0.1, 0.0], [0.0, 0.3, 0.0, 0.1]])
    recent = memory - tail
    complement = np.eye(4) - projector
    assert np.allclose(complement @ recent @ projector, -complement @ tail @ projector)


def test_coupling_radius() -> None:
    assert coupling_radius(2.0, 0.1, 0.01) == pytest.approx(0.41)


def test_singular_interval() -> None:
    assert singular_interval(0.5, 0.2) == pytest.approx((0.3, 0.7))
    assert singular_interval(0.1, 0.2)[0] == 0.0


def test_no_positive_universal_lower() -> None:
    memory = np.diag([3.0, 2.0, 1.0])
    projector = np.diag([1.0, 1.0, 0.0])
    tail = np.diag([0.1, 0.1, 0.0])
    assert np.linalg.norm((np.eye(3) - projector) @ tail @ projector) == 0.0


def test_invalid() -> None:
    with pytest.raises(ValueError):
        coupling_radius(1.0, 2.0, 0.0)
