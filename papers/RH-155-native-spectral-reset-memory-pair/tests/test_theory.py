import math

import pytest

from reset_memory_pair import full_tail_ratio_upper, geometric_tail_mass, recent_tail_ratio_upper


def test_geometric_tail() -> None:
    assert geometric_tail_mass(0.5, 2, 1) == 0.0
    assert geometric_tail_mass(0.5, 2, 3) == pytest.approx(0.25 + 0.125)
    assert geometric_tail_mass(0.5, 2) == 0.5


def test_ratio_conversion() -> None:
    assert full_tail_ratio_upper(4.0, 1.0) == 0.25
    result = recent_tail_ratio_upper(4.0, 1.0)
    assert result["recent_positive"]
    assert result["subunit"]
    assert result["ratio_upper"] == pytest.approx(1.0 / 3.0)


def test_sharp_subunit_gate() -> None:
    assert recent_tail_ratio_upper(2.1, 1.0)["subunit"]
    assert not recent_tail_ratio_upper(2.0, 1.0)["subunit"]


def test_recent_singularity() -> None:
    result = recent_tail_ratio_upper(1.0, 1.0)
    assert not result["recent_positive"]
    assert math.isinf(result["ratio_upper"])


def test_invalid() -> None:
    with pytest.raises(ValueError):
        geometric_tail_mass(1.0, 5)
