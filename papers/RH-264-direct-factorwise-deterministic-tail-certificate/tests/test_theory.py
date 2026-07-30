from pathlib import Path
import sys

from flint import arb, ctx
import pytest

ROOT = Path(__file__).resolve().parents[1]
RH13_SRC = ROOT.parent / "RH-13-validated-reduced-sector-spectral-gap/src"
RH262_SRC = ROOT.parent / "RH-262-certified-deterministic-numerator-boundary-budget/src"
sys.path.insert(0, str(RH262_SRC))
sys.path.insert(0, str(RH13_SRC))

from direct_tail import direct_tail_majorant, odd_tail_exact_majorant  # noqa: E402
from validated_gap.certificate import certify_reduced_gap  # noqa: E402


@pytest.fixture(scope="module")
def tail():
    ctx.dps = 100
    reduced = certify_reduced_gap(
        decimal_precision=100, dimension=50, tail_degree=100
    )
    return direct_tail_majorant(reduced, inner_radius=arb(1), first_omitted_order=29)


def test_factorwise_tail_is_small(tail):
    assert tail.even_total < arb("0.000024488616")
    assert tail.odd < arb("0.000002136130")
    assert tail.total < arb("0.000026624745")
    assert tail.multiplicative_error < arb("0.000026625100")


def test_odd_tail_requires_odd_order():
    with pytest.raises(ValueError):
        odd_tail_exact_majorant(
            first_order=28, ratio=arb("0.7"), lam=arb("1.6")
        )
