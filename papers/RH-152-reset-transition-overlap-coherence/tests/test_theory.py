import math

import pytest

from reset_overlap import aligned_frame_radius, overlap_inverse_upper, polar_transition_radius, robust_overlap_lower


def test_aligned_frame_radius() -> None:
    assert aligned_frame_radius(0.0) == 0.0
    assert aligned_frame_radius(1.0) == pytest.approx(math.sqrt(2.0))


def test_overlap_lower() -> None:
    result = robust_overlap_lower(0.8, 0.01, 0.02)
    assert result["invertible"]
    assert 0.0 < result["robust_lower"] < 0.8


def test_vacuous_overlap() -> None:
    result = robust_overlap_lower(0.01, 0.5, 0.5)
    assert not result["invertible"]


def test_inverse_and_polar() -> None:
    assert overlap_inverse_upper(0.25) == 4.0
    assert math.isinf(overlap_inverse_upper(0.0))
    assert polar_transition_radius(0.5, 0.1)["stable"]
    assert not polar_transition_radius(0.1, 0.1)["stable"]


def test_invalid() -> None:
    with pytest.raises(ValueError):
        robust_overlap_lower(2.0, 0.0, 0.0)
