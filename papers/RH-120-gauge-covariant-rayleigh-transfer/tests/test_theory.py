from __future__ import annotations

import numpy as np
import pytest

from gauge_rayleigh_transfer import gauge_transfer_certificate, relative_gamma, transfer_gamma_bound


def spd(rng: np.random.Generator, n: int = 4) -> np.ndarray:
    x = rng.normal(size=(n, n))
    return x.T @ x + 0.4 * np.eye(n)


def test_random_transfer() -> None:
    rng = np.random.default_rng(120)
    for _ in range(40):
        g, d = spd(rng), spd(rng)
        s = rng.normal(size=(4, 4)) + 2.0 * np.eye(4)
        a, b = 0.3 + rng.random(), 0.2 + 2.0 * rng.random()
        h = rng.normal(size=(4, 4))
        gp = a * s.T @ g @ s + h.T @ h
        dp = (0.1 + 0.8 * rng.random()) * b * s.T @ d @ s
        cert = gauge_transfer_certificate(g, d, gp, dp, s, a, b)
        assert cert["gamma_conclusion_holds"]
        assert cert["volume_conclusion_holds"]


def test_exact_congruence_invariance() -> None:
    rng = np.random.default_rng(2120)
    g, d = spd(rng), spd(rng)
    s = rng.normal(size=(4, 4)) + 3.0 * np.eye(4)
    assert relative_gamma(s.T @ g @ s, s.T @ d @ s) == pytest.approx(relative_gamma(g, d), rel=2e-12)


def test_sharp_scalar_family() -> None:
    g = np.diag([1.0, 2.0, 3.0, 4.0])
    d = 0.09 * g
    s = np.diag([2.0, 1.0, 0.5, 3.0])
    a, b = 0.7, 1.4
    cert = gauge_transfer_certificate(g, d, a * s.T @ g @ s, b * s.T @ d @ s, s, a, b)
    assert cert["target_gamma"] == pytest.approx(cert["gamma_upper"], rel=2e-12)
    assert cert["target_volume"] == pytest.approx(cert["target_volume_lower"], rel=2e-12)


def test_validation() -> None:
    with pytest.raises(ValueError):
        relative_gamma(np.diag([1.0, 0.0]), np.eye(2))
    with pytest.raises(ValueError):
        transfer_gamma_bound(1.0, 0.0, 1.0)

