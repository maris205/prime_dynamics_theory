import pytest

from peripheral_validation import (
    newton_contraction_radius,
    parity_projector_error,
)


def test_newton_radius_closes_small_residual() -> None:
    result = newton_contraction_radius(1.0e-12, 1.0e-10, 20.0)
    assert result.radius >= result.beta
    assert result.contraction < 1.0
    assert result.self_map_margin >= -1.0e-15


def test_projector_error_vanishes_with_vector_errors() -> None:
    result = parity_projector_error(1.0, 2.0, 0.0, 0.0)
    assert result.gram_lower == 1.0
    assert result.projector_error_upper == 0.0


def test_projector_error_is_positive_and_finite() -> None:
    result = parity_projector_error(1.0, 3.0, 1.0e-8, 2.0e-8)
    assert 0.99 < result.gram_lower < 1.0
    assert 0.0 < result.projector_error_upper < 1.0e-6


@pytest.mark.parametrize(
    "call",
    [
        lambda: newton_contraction_radius(-1.0, 0.0, 1.0),
        lambda: newton_contraction_radius(1.0, 1.0, 1.0),
        lambda: parity_projector_error(1.0, 1.0, -1.0, 0.0),
        lambda: parity_projector_error(1.0, 2.0, 0.6, 0.0),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
