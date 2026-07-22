from __future__ import annotations

import cmath

import pytest

from cloud_relative import (
    complement_normal_bound,
    determinant_continuity_bound,
    fixed_pole_cancellation,
    ideal_cloud_factor,
    interior_cancellation_error_bound,
)


@pytest.mark.parametrize("degree", [0, 1, 3, 7, 16])
@pytest.mark.parametrize("q", [0.0, 0.2, -0.4, 0.7 + 0.1j, cmath.exp(0.3j)])
def test_fixed_pole_identity(degree: int, q: complex) -> None:
    left = (1.0 - q) ** 2 * ideal_cloud_factor(q, degree)
    right = fixed_pole_cancellation(q, degree)
    assert abs(left - right) < 2e-12 * max(1.0, abs(right))


def test_removable_value() -> None:
    assert ideal_cloud_factor(1.0, 7) == 64.0


@pytest.mark.parametrize("radius", [0.2, 0.5, 0.8, 0.95])
def test_interior_bound(radius: float) -> None:
    degree = 9
    for phase in range(32):
        q = radius * cmath.exp(2j * cmath.pi * phase / 32)
        error = abs(fixed_pole_cancellation(q, degree) - 1.0)
        bound = interior_cancellation_error_bound(radius, degree)
        assert error <= bound * (1.0 + 1e-9) + 1e-15


def test_exterior_growth() -> None:
    q = 1.05
    assert abs(fixed_pole_cancellation(q, 64)) > abs(fixed_pole_cancellation(q, 16))


def test_relative_determinant_bounds() -> None:
    assert complement_normal_bound(2.0, 3.0) > 400.0
    assert determinant_continuity_bound(1.0, 1e-4, 2.0, 2.1) > 0.0


@pytest.mark.parametrize("radius", [-0.1, 1.0, 1.1])
def test_bad_interior_radius(radius: float) -> None:
    with pytest.raises(ValueError):
        interior_cancellation_error_bound(radius, 2)
