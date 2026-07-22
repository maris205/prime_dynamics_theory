import pytest

from block_scaling import dyadic_horizon, uniform_hardy_envelope


def test_log_square_horizons() -> None:
    assert [dyadic_horizon(k) for k in range(5)] == [4, 9, 16, 25, 36]


def test_uniform_envelope_is_polylogarithmic() -> None:
    result = uniform_hardy_envelope(
        level=4,
        sigma=0.01,
        sigma_zero=0.16,
        q_constant=0.086,
        observation_density_constant=2.561,
        source_constant=3.1,
        source_log_power=0.0,
        finite_constant=0.552,
        finite_log_power=1.0,
    )
    assert result.horizon == 36
    assert result.block_contraction_certified
    assert result.tail_energy_squared_upper < 0.06
    assert result.full_energy_squared_upper < 3.4


@pytest.mark.parametrize(
    "call",
    [
        lambda: dyadic_horizon(-1),
        lambda: uniform_hardy_envelope(
            level=0,
            sigma=0.2,
            sigma_zero=0.16,
            q_constant=0.1,
            observation_density_constant=1.0,
            source_constant=1.0,
            source_log_power=0.0,
            finite_constant=1.0,
            finite_log_power=0.0,
        ),
        lambda: uniform_hardy_envelope(
            level=0,
            sigma=0.1,
            sigma_zero=0.1,
            q_constant=4.0,
            observation_density_constant=1.0,
            source_constant=1.0,
            source_log_power=0.0,
            finite_constant=1.0,
            finite_log_power=0.0,
        ),
    ],
)
def test_invalid_inputs_fail(call) -> None:
    with pytest.raises(ValueError):
        call()
