from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from parity_anchor import (  # noqa: E402
    geometric_odd_tail,
    odd_anchor,
    parity_anchor_from_physical_trace,
)


def test_exact_odd_formula_and_tail():
    value = odd_anchor(3, 1.6785735104283223)
    assert value == pytest.approx(0.2841984186057946)
    assert geometric_odd_tail(29, 1.6785735104283223) < 2.263e-6


def test_even_and_odd_dispatch():
    assert parity_anchor_from_physical_trace(
        3, 0.17453335382628332, 1.6785735104283223
    ) == pytest.approx(0.2841984186057946)
    assert parity_anchor_from_physical_trace(
        2, 1.1801429862402304, 1.6785735104283223
    ) == pytest.approx(0.5143679864267854)


def test_invalid_order_is_rejected():
    with pytest.raises(ValueError):
        odd_anchor(2, 1.6785735104283223)
