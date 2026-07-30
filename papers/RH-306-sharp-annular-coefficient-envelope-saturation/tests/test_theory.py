import math

from envelope_saturation import (
    envelope_mass,
    model_hardy_tail_bounds,
    model_sup_tail_bounds,
    saturation_identity_ratio,
)


def test_mass_and_tails_move_in_opposite_directions():
    assert envelope_mass(40) > envelope_mass(20)
    assert model_hardy_tail_bounds(40, 1.41)[1] < model_hardy_tail_bounds(20, 1.41)[1]
    assert model_sup_tail_bounds(40, 1.41)[1] < model_sup_tail_bounds(20, 1.41)[1]


def test_sup_tail_dominates_hardy_tail():
    assert model_sup_tail_bounds(30, 1.41)[1] > model_hardy_tail_bounds(30, 1.41)[1]


def test_mass_saturates_the_same_constant_used_by_the_model_tail():
    assert math.isclose(saturation_identity_ratio(37), 1.0)
    assert math.isclose(
        model_sup_tail_bounds(30, 1.41, constant=48.0)[0],
        48.0 * model_sup_tail_bounds(30, 1.41, constant=1.0)[0],
    )
    assert math.isclose(
        model_hardy_tail_bounds(30, 1.41, constant=48.0)[0],
        48.0 * model_hardy_tail_bounds(30, 1.41, constant=1.0)[0],
    )


def test_infinite_tail_bounds_are_ordered():
    for bounds in (
        model_sup_tail_bounds(20, 1.41),
        model_hardy_tail_bounds(20, 1.41),
    ):
        assert 0.0 < bounds[0] < bounds[1]
