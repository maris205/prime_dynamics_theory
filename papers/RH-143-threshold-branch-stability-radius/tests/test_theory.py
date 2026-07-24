import numpy as np
import pytest

from threshold_branch import branch_radius, cross_projector_error_bound, selected_width


def test_interior_branch_radius_is_attained_at_both_walls():
    singular = [1.0, 0.2, 0.01, 0.0005]
    tau = 0.001
    result = branch_radius(singular, tau, minimum=1, maximum=4)
    assert result["selected_width"] == 3
    expected = min((0.01 - tau) / (1 + tau), (tau - 0.0005) / (1 + tau))
    assert result["absolute_radius"] == pytest.approx(expected)


def test_clipping_removes_irrelevant_boundary():
    low = branch_radius([1.0, 1e-6, 1e-7, 1e-8], 1e-4, minimum=2, maximum=4)
    high = branch_radius([1.0, 0.5, 0.2, 0.1], 1e-4, minimum=2, maximum=4)
    assert low["selected_width"] == 2
    assert low["absolute_radius"] == pytest.approx((1e-4 - 1e-7) / (1 + 1e-4))
    assert high["selected_width"] == 4
    assert high["absolute_radius"] == pytest.approx((0.1 - 1e-4) / (1 + 1e-4))


def test_cross_projector_lipschitz_formula():
    assert cross_projector_error_bound(0.01, 2.0, 0.1) == pytest.approx(0.41)


def test_bad_singular_data_are_rejected():
    with pytest.raises(ValueError):
        selected_width([1.0, 2.0], 0.1)
    with pytest.raises(ValueError):
        cross_projector_error_bound(-1.0, 1.0, 0.0)

