from pathlib import Path
import sys

from flint import arb, ctx
import pytest

ROOT = Path(__file__).resolve().parents[1]
for relative in (
    "../RH-13-validated-reduced-sector-spectral-gap/src",
    "../RH-262-certified-deterministic-numerator-boundary-budget/src",
    "../RH-264-direct-factorwise-deterministic-tail-certificate/src",
):
    sys.path.insert(0, str(ROOT / relative))

from tail_ladder import build_ladder, validate_orders  # noqa: E402
from validated_gap.certificate import certify_reduced_gap  # noqa: E402


def test_order_validation():
    assert validate_orders((13, 21, 29)) == (13, 21, 29)
    with pytest.raises(ValueError):
        validate_orders((13, 20))


def test_small_ladder():
    ctx.dps = 100
    reduced = certify_reduced_gap(
        decimal_precision=100, dimension=50, tail_degree=100
    )
    rows = build_ladder(reduced, (29, 37))
    assert rows[0].total < arb("0.000026624745")
    assert rows[1].total < arb("0.000000932147")
