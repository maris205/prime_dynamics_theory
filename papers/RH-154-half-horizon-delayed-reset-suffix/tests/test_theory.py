import math

import pytest

from delayed_suffix import common_suffix_floor, suffix_length, suffix_log_drawdown


def test_suffix_length() -> None:
    assert suffix_length(5, 0.5) == 3
    assert suffix_length(10, 0.5) == 5


def test_common_floor() -> None:
    chains = [[0.01, 0.4, 0.8, 0.9], [0.2, 0.3, 0.6, 0.7]]
    assert common_suffix_floor(chains, 0.5) == 0.6


def test_floor_is_sharp_for_terminal_retention() -> None:
    chain = [0.01, 0.4, 0.8, 0.9]
    assert common_suffix_floor([chain], 0.5) == min(chain[-2:])
    assert min(chain[-3:]) <= common_suffix_floor([chain], 0.5)


def test_drawdown() -> None:
    assert suffix_log_drawdown([0.5, 0.25], 1.0) == pytest.approx(math.log(8.0))


def test_invalid() -> None:
    with pytest.raises(ValueError):
        suffix_length(0, 0.5)
