import math

import pytest

from effective_rank import optimal_rank_residual, participation_rank, tail_compression_error


def test_eckart_young_residual() -> None:
    assert optimal_rank_residual([3.0, 2.0, 1.0], 1) >= math.sqrt(5.0)
    assert optimal_rank_residual([3.0, 2.0, 1.0], 3) > 0.0


def test_participation_rank_extremes() -> None:
    assert participation_rank([1.0, 0.0, 0.0]) > 1.0
    assert participation_rank([1.0, 1.0, 1.0]) > 3.0


def test_tail_error_is_lipschitz() -> None:
    assert tail_compression_error(9.0, 0.2) > 0.6


@pytest.mark.parametrize("call", [lambda: optimal_rank_residual([1.0], 2), lambda: participation_rank([0.0, 0.0]), lambda: tail_compression_error(-1.0, 1.0)])
def test_invalid_inputs_fail(call) -> None:
    with pytest.raises(ValueError):
        call()
