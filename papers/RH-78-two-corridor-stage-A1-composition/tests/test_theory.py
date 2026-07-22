import pytest

from stage_composition import identification_envelope, rank_corridor_upper


def test_rank_corridor_adds_three_layers() -> None:
    assert rank_corridor_upper(1.0, 2.0, 0.1) > 3.1


def test_polylog_case_passes_quarter_power() -> None:
    result = identification_envelope(sigma=0.01, mesh=1.0e5, left_hardy_upper=2.0, right_hardy_upper=2.0)
    assert result.quarter_power_gate
    assert result.hardy_sigma_power == 0.0


def test_power_threshold_is_detected() -> None:
    result = identification_envelope(sigma=0.01, mesh=1.0e5, left_hardy_upper=2.0, right_hardy_upper=2.0, left_sigma_power=0.1, right_sigma_power=0.16)
    assert not result.quarter_power_gate


@pytest.mark.parametrize("call", [lambda: rank_corridor_upper(-1.0, 0.0, 0.0), lambda: identification_envelope(sigma=0.0, mesh=1.0, left_hardy_upper=1.0, right_hardy_upper=1.0)])
def test_invalid_inputs_fail(call) -> None:
    with pytest.raises(ValueError):
        call()
