from __future__ import annotations

import pytest

from differential_ritz_envelope import cross_covariance_derivative_bound, spectral_projector_derivative_bound, two_gap_refresh_derivative_bound


def test_differential_bounds() -> None:
    assert spectral_projector_derivative_bound(0.5, 0.25) >= 4.0
    assert cross_covariance_derivative_bound(2.0, 0.5) >= 6.0
    assert two_gap_refresh_derivative_bound(1.0, 0.5, 0.25) > 100.0


def test_invalid_gaps() -> None:
    with pytest.raises(ValueError):
        spectral_projector_derivative_bound(1.0, 0.0)
    with pytest.raises(ValueError):
        two_gap_refresh_derivative_bound(1.0, -1.0, 1.0)
