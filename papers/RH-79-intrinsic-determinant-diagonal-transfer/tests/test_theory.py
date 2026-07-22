import pytest

from determinant_transfer import determinant_disk_error, square_trace_error


def test_square_error_formula() -> None:
    assert square_trace_error(0.1, 2.0) > 0.41


def test_determinant_error_vanishes_on_zero_disk() -> None:
    assert determinant_disk_error(0.0, 1.0, 2.0) > 0.0


def test_smaller_disk_improves_bound() -> None:
    assert determinant_disk_error(0.001, 0.1, 2.0) < determinant_disk_error(0.01, 0.1, 2.0)


@pytest.mark.parametrize("call", [lambda: square_trace_error(-1.0, 1.0), lambda: determinant_disk_error(-1.0, 1.0, 1.0)])
def test_invalid_inputs_fail(call) -> None:
    with pytest.raises(ValueError):
        call()
