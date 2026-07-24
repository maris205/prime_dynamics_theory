import pytest

from backward_viability import backward_kernel, preimage_radius, young_map


def test_closed_form_preimage_matches_boundary():
    a, b, q, target = 2.0, 0.1, 0.2, 0.9
    radius = preimage_radius(target, a, b, q, cap=10.0)
    assert young_map(radius, a, b, q) == pytest.approx(target)
    assert young_map(0.99 * radius, a, b, q) < target


def test_zero_metric_is_a_reset_and_large_floor_is_empty():
    assert preimage_radius(0.9, 0.0, 0.1, 0.2) == 1.0
    assert preimage_radius(0.9, 10.0, 0.8, 0.2) == 0.0


def test_backward_control_can_choose_different_candidates():
    sequence = [
        [{"metric": 0.2, "frame": 0.0, "birth": 0.0}, {"metric": 2.0, "frame": 0.0, "birth": 0.0}],
        [{"metric": 0.5, "frame": 0.0, "birth": 0.1}],
    ]
    result = backward_kernel(sequence)
    assert result["radii"][0] == 1.0
    assert result["control_indices"][0] == 0


def test_bad_parameters_are_rejected():
    with pytest.raises(ValueError):
        preimage_radius(1.0, -1.0, 0.0, 0.0)
    with pytest.raises(ValueError):
        backward_kernel([[]])

