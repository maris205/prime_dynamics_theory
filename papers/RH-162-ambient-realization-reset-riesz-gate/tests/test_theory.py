import numpy as np
import pytest

from ambient_realization import polar_repair_bounds, realization_coupling_bounds


def test_scalar_bounds_and_validation():
    result = realization_coupling_bounds(0.2, 0.03)
    assert result["feedback_product_upper"] == pytest.approx(0.006)
    assert polar_repair_bounds(0.0)["correction_upper"] == 0.0
    assert not polar_repair_bounds(1.0)["repair_certified"]
    with pytest.raises(ValueError):
        realization_coupling_bounds(-1.0, 0.0)


def test_realization_inequalities_on_random_matrix():
    rng = np.random.default_rng(162)
    for _ in range(32):
        h, e, r = 9, 6, 3
        j, _ = np.linalg.qr(rng.normal(size=(h, e)))
        p = np.diag([1.0] * r + [0.0] * (e - r))
        m = np.diag(rng.normal(size=e))
        a = rng.normal(size=(h, h))
        phat = j @ p @ j.T
        qhat = np.eye(h) - phat
        primal = (a @ j - j @ m) @ p
        adjoint = (a.T @ j - j @ m.T) @ p
        outward = qhat @ a @ phat
        inward = phat @ a @ qhat
        assert np.linalg.norm(outward, 2) <= np.linalg.norm(primal, 2) + 1e-11
        assert np.linalg.norm(inward, 2) <= np.linalg.norm(adjoint, 2) + 1e-11


def test_no_map_witness_changes_coupling():
    a = np.diag([0.0, 1.0])
    j0 = np.array([[1.0], [0.0]])
    j1 = np.array([[2.0**-0.5], [2.0**-0.5]])
    couplings = []
    for j in (j0, j1):
        p = j @ j.T
        couplings.append(np.linalg.norm((np.eye(2) - p) @ a @ p, 2))
    assert couplings[0] == 0.0
    assert couplings[1] == pytest.approx(0.5)
