from __future__ import annotations

import math

from flint import acb, arb

from certificate_ledger import (
    AmbiguousCircleError,
    classify_eigenvalue_balls,
    compose_lifted_bound,
    transport_arc_cover,
)


def test_circle_classifier_accepts_strict_balls() -> None:
    values = [acb(arb("0.2 +/- 0.01"), 0), acb(arb("1.4 +/- 0.01"), 0)]
    result = classify_eigenvalue_balls(values, acb(0), arb(1))
    assert result.inside_count == 1
    assert result.outside_count == 1
    assert result.ambiguous_count == 0
    result.require_complete()


def test_circle_classifier_rejects_boundary_ball() -> None:
    result = classify_eigenvalue_balls(
        [acb(arb("1.0 +/- 0.01"), 0)], acb(0), arb(1)
    )
    assert result.ambiguous_count == 1
    try:
        result.require_complete()
    except AmbiguousCircleError:
        pass
    else:
        raise AssertionError("boundary-intersecting ball was accepted")


def test_lifted_formula_and_selected_arc_transport() -> None:
    result, _ = compose_lifted_bound(
        threshold=0.01,
        singular_scalar=0.2,
        right_residual_upper=1.0e-5,
        left_residual_upper=2.0e-5,
        lift=1.0,
        selected_arc_radius_upper=1.0e-3,
        selected_arc_budget_lower=1.0e6,
    )
    assert result.denominator_lower > 0.0
    assert result.center_inverse_upper > result.lifted_inverse_upper
    assert result.selected_arc_inverse_upper > result.center_inverse_upper
    assert result.selected_arc_closed


def test_one_center_transport_distinguishes_local_and_remote_arcs() -> None:
    arcs = [
        {
            "arc": "0",
            "center_real": "0.0",
            "center_imag": "0.0",
            "disc_radius": "0.01",
            "resolvent_budget_lower": "1000.0",
        },
        {
            "arc": "1",
            "center_real": "0.2",
            "center_imag": "0.0",
            "disc_radius": "0.01",
            "resolvent_budget_lower": "1000.0",
        },
    ]
    records = transport_arc_cover(
        sigma=0.1,
        source_center=0.0j,
        center_inverse_upper=arb(10.0),
        arcs=arcs,
        selected_arc=0,
    )
    assert records[0].status == "closed"
    assert records[1].status == "neumann_failure"
    assert records[0].neumann_product_upper < 1.0
    assert records[1].neumann_product_lower > 1.0
    assert math.isfinite(records[0].transported_inverse_upper)
