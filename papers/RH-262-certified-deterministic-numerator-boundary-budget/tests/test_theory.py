from pathlib import Path
import sys

from flint import arb, ctx
import pytest


ROOT = Path(__file__).resolve().parents[1]
RH13_SRC = ROOT.parent / "RH-13-validated-reduced-sector-spectral-gap/src"
sys.path.insert(0, str(RH13_SRC))

from boundary_budget import (  # noqa: E402
    cauchy_tail_factor,
    certified_tail_budget,
    certify_boundary_budget,
)
from validated_gap.certificate import certify_reduced_gap  # noqa: E402


@pytest.fixture(scope="module")
def budget():
    ctx.dps = 100
    reduced = certify_reduced_gap(
        decimal_precision=100, dimension=50, tail_degree=100
    )
    return certify_boundary_budget(reduced)


def test_fixed_circle_budget_is_strictly_below_clean_claim(budget):
    assert budget.numerator_circle < arb("1.647058824")
    assert budget.cube_geometric_ratio < arb("0.715126024")
    assert budget.total_log < arb("107.906078")
    assert budget.total_log < arb(108)


def test_order_29_clean_tail_budget():
    factor, additive, multiplicative = certified_tail_budget(
        boundary_supremum=arb(108),
        inner_radius=arb(1),
        outer_radius=arb(7) / 5,
        first_omitted_order=29,
    )
    assert factor < arb("0.000202468")
    assert additive < arb("0.021866475")
    assert multiplicative < arb("0.022107298")


def test_cauchy_factor_rejects_invalid_radii():
    with pytest.raises(ValueError):
        cauchy_tail_factor(
            inner_radius=arb(1), outer_radius=arb(1), first_omitted_order=29
        )
