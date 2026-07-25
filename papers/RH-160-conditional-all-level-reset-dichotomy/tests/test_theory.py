import numpy as np
import pytest

from reset_dichotomy import (
    directional_path_floor,
    directional_uniform_floor,
    native_interface_floor,
    native_uniform_floor,
    outward_cross_lowers,
)


def test_native_uniform_formula() -> None:
    result = native_uniform_floor(3.0, 4.0, 0.5, 0.25)
    ratio = 0.5 / 2.5
    expected = 0.25 * np.sqrt(2.5 / 4.0) * (1.0 - np.sqrt(ratio)) ** 4
    assert result["subunit_tail"]
    assert result["support_floor"] == pytest.approx(expected)
    assert native_interface_floor(0.25, 2.5 / 4.0, ratio) == pytest.approx(expected)


def test_native_loewner_tail_bound() -> None:
    rng = np.random.default_rng(160)
    ell, tau = 3.0, 0.5
    values = rng.normal(size=(5, 5))
    direction = values @ values.T
    direction *= tau / float(np.linalg.norm(direction, 2))
    full = np.diag([5.0, 4.5, 4.0, 3.5, ell])
    recent = full - direction
    q = tau / (ell - tau)
    assert np.linalg.eigvalsh(recent)[0] >= ell - tau - 1e-12
    assert np.linalg.eigvalsh(q * recent - direction)[0] >= -1e-12


def test_directional_transport_floor() -> None:
    assert directional_uniform_floor(0.5, 3, 0.2, 2.0) == pytest.approx(0.0125)
    assert directional_path_floor(0.3, 0.2, 2.0) == pytest.approx(0.03)


def test_outward_cross_interval() -> None:
    assert outward_cross_lowers(1.0, 0.4, 0.1) == pytest.approx((0.3, 1.1))
    assert outward_cross_lowers(1.0, 0.05, 0.1)[0] == 0.0


def test_omission_mechanisms_approach_zero() -> None:
    overlap = [native_interface_floor(1.0 / n, 0.4, 0.2) for n in (2, 8, 32)]
    spread = [native_interface_floor(0.5, 1.0 / (n * n), 0.2) for n in (2, 8, 32)]
    lag = [directional_uniform_floor(0.5, n, 0.5, 1.0) for n in (2, 8, 32)]
    assert overlap[0] > overlap[1] > overlap[2] > 0.0
    assert spread[0] > spread[1] > spread[2] > 0.0
    assert lag[0] > lag[1] > lag[2] > 0.0


def test_invalid_interfaces() -> None:
    with pytest.raises(ValueError):
        native_uniform_floor(1.0, 0.5, 0.1, 0.2)
    with pytest.raises(ValueError):
        directional_uniform_floor(0.5, 0, 0.1, 1.0)
    with pytest.raises(ValueError):
        outward_cross_lowers(0.1, 0.2, 0.0)
