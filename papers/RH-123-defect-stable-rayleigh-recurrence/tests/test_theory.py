import numpy as np
import pytest

from defect_rayleigh_recurrence import defect_gamma_squared_bound, defect_transfer_certificate, iterate_affine_upper


def spd(rng):
    x = rng.normal(size=(4, 4)); return x.T @ x + .5 * np.eye(4)


def test_random_matrix_transfer() -> None:
    rng = np.random.default_rng(123)
    for _ in range(40):
        g, d = spd(rng), spd(rng); s = rng.normal(size=(4, 4)) + 3 * np.eye(4)
        a, b, eta, delta = .4 + rng.random(), .2 + rng.random(), .3 * rng.random(), .1 * rng.random()
        h = s.T @ g @ s; extra = rng.normal(size=(4, 4))
        gp = a * (1 - eta) * h + extra.T @ extra
        cap = b * s.T @ d @ s + delta * h
        dp = (.1 + .8 * rng.random()) * cap
        assert defect_transfer_certificate(g, d, gp, dp, s, a, b, eta, delta)["conclusion_holds"]


def test_scalar_sharpness() -> None:
    x, a, b, eta, delta = .09, .8, .7, .2, .03
    cert = defect_transfer_certificate(np.eye(1), x*np.eye(1), a*(1-eta)*np.eye(1), (b*x+delta)*np.eye(1), np.eye(1), a, b, eta, delta)
    assert cert["target_gamma_squared"] == pytest.approx(cert["target_gamma_squared_upper"])


def test_affine_closed_form() -> None:
    values = iterate_affine_upper(.5, .8, .03, 20)
    expected = .8**20 * .5 + .03 * (1-.8**20)/(1-.8)
    assert values[-1] == pytest.approx(expected)


def test_validation() -> None:
    with pytest.raises(ValueError): defect_gamma_squared_bound(1, 1, 1, 1, 0)

