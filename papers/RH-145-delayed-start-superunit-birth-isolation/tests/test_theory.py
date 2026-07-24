import pytest

from delayed_start import eventual_directional_floor, recurrent_floor_obstruction, suffix_statistics


def test_eventual_floor_formula():
    assert eventual_directional_floor(0.25, 0.5) == pytest.approx(0.5**5)
    assert eventual_directional_floor(1.0, 0.5) == 0.0


def test_recurrent_floor_witness_and_suffix_statistics():
    assert recurrent_floor_obstruction([1.1, 2.0, 1.0])
    assert not recurrent_floor_obstruction([1.1, 0.2, 1.3])
    rows = [{"sigma": 0.1, "positive": False, "floor": 0.0}, {"sigma": 0.05, "positive": True, "floor": 0.2}]
    result = suffix_statistics(rows, 0.05)
    assert result["count"] == 1
    assert result["positive_count"] == 1
    assert result["minimum_positive_floor"] == pytest.approx(0.2)


def test_bad_inputs_are_rejected():
    with pytest.raises(ValueError):
        eventual_directional_floor(-1.0, 1.0)
    with pytest.raises(ValueError):
        recurrent_floor_obstruction([float("nan")])

