import pytest

from certificate_ledger import geometric_log_tail_bound, obligation_status, safe_ratio


def test_geometric_envelope_tail_formula():
    bound = geometric_log_tail_bound(48.0, 0.700876, 1.0, 29)
    assert bound == pytest.approx(0.00018475085356742355)
    assert bound < 0.000184751


def test_obligation_vector_has_fixed_order_and_requires_all_five():
    status = obligation_status(
        legal_anchored_head=False,
        coefficient_bridge=False,
        uniform_quotient_tail=False,
        analytic_target_tail=True,
        certified_target_boundary_constant=True,
    )
    assert status["obligation_vector"] == [False, False, False, True, True]
    assert status["satisfied_component_count"] == 2
    assert status["complete"] is False


def test_complete_status_and_invalid_interfaces():
    complete = obligation_status(
        legal_anchored_head=True,
        coefficient_bridge=True,
        uniform_quotient_tail=True,
        analytic_target_tail=True,
        certified_target_boundary_constant=True,
    )
    assert complete["complete"] is True
    with pytest.raises(ValueError):
        geometric_log_tail_bound(48.0, 1.0, 1.0, 29)
    with pytest.raises(ValueError):
        safe_ratio(1.0, 0.0)
    with pytest.raises(ValueError):
        obligation_status(
            legal_anchored_head=False,
            coefficient_bridge=False,
            uniform_quotient_tail=False,
            analytic_target_tail=True,
        )


def test_safe_endpoint_comparison_factor():
    factor = safe_ratio(0.00018475085356742355, 0.000026624745)
    assert factor > 6.93
