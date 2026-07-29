import math

import pytest

from certificate_ledger import (
    cauchy_target_tail_bound,
    complete_certificate_status,
    determinant_certificate_bound,
    logarithmic_certificate_bound,
)


def test_logarithmic_budget_adds_three_independent_terms():
    assert logarithmic_certificate_bound(0.1, 0.2, 0.3) == pytest.approx(0.6)


def test_cauchy_budget_and_exponential_conversion():
    tail = cauchy_target_tail_bound(2.0, 1.0, 1.25, 13)
    assert tail == pytest.approx(2.0 * 0.8**13 / 0.2)
    bound = determinant_certificate_bound(0.4, 0.1)
    assert bound == pytest.approx(math.exp(0.4) * math.expm1(0.1))


def test_complete_certificate_requires_every_component():
    incomplete = complete_certificate_status(
        legal_anchored_head=False,
        coefficient_bridge=False,
        uniform_quotient_tail=False,
        analytic_target_tail=True,
        certified_target_boundary_constant=False,
    )
    assert incomplete["satisfied_component_count"] == 1
    assert incomplete["complete"] is False
    complete = complete_certificate_status(
        legal_anchored_head=True,
        coefficient_bridge=True,
        uniform_quotient_tail=True,
        analytic_target_tail=True,
        certified_target_boundary_constant=True,
    )
    assert complete["complete"] is True


def test_invalid_budgets_are_rejected():
    with pytest.raises(ValueError):
        logarithmic_certificate_bound(-1.0, 0.0, 0.0)
    with pytest.raises(ValueError):
        cauchy_target_tail_bound(1.0, 1.0, 1.0, 13)
    with pytest.raises(ValueError):
        determinant_certificate_bound(float("inf"), 0.1)
