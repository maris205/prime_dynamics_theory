import math

import pytest

from reset_support import native_support_lower, support_tail_factor


def test_tail_factor() -> None:
    assert support_tail_factor(0.0) == 1.0
    assert support_tail_factor(1.0) == 0.0
    assert support_tail_factor(0.25) == pytest.approx(0.5**4)


def test_support_formula() -> None:
    result = native_support_lower(4.0, 9.0, 1.0, 0.5)
    assert result["recent_positive"]
    assert result["subunit_tail"]
    assert result["recent_base_lower"] == pytest.approx(0.5 * math.sqrt(3.0 / 9.0))
    assert result["relative_tail_upper"] == pytest.approx(1.0 / 3.0)
    assert result["support_lower"] > 0.0


def test_sharp_boundary() -> None:
    assert native_support_lower(2.0, 2.0, 1.0, 1.0)["support_lower"] == 0.0


def test_invalid() -> None:
    with pytest.raises(ValueError):
        native_support_lower(2.0, 1.0, 0.0, 1.0)
