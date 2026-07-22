from __future__ import annotations

import pytest

from stopped_hybrid_clock import (
    absolute_debits,
    certified_endpoint_upper,
    cumulative_budget,
    debit_fits,
    gate_slack,
    hybrid_contributions,
    remaining_budget,
    stopped_allowance,
)


def test_stopped_telescoping_and_budget() -> None:
    endpoints = (2.0, 2.25, 2.1, 2.3)
    contributions = hybrid_contributions(endpoints)
    assert abs(sum(contributions) - (endpoints[-1] - endpoints[0])) < 1e-15
    debits = absolute_debits(contributions)
    cumulative = cumulative_budget(debits)
    assert cumulative[-1] >= abs(endpoints[-1] - endpoints[0])


def test_gate_allowance_certifies_endpoint() -> None:
    reference = 2.0
    baseline = 2.001
    slack = gate_slack(reference, baseline, 1.01)
    allowance = stopped_allowance(reference, baseline, gate=1.01, safety_fraction=0.99)
    assert 0.0 < allowance < slack
    assert debit_fits(0.0, allowance / 2.0, allowance)
    assert not debit_fits(allowance / 2.0, allowance, allowance)
    endpoint = certified_endpoint_upper(baseline, allowance)
    assert endpoint < 1.01 * reference
    assert remaining_budget(allowance, allowance / 3.0) > 0.0


def test_validation() -> None:
    with pytest.raises(ValueError):
        hybrid_contributions([1.0])
    with pytest.raises(ValueError):
        stopped_allowance(1.0, 0.9, safety_fraction=1.1)
    with pytest.raises(ValueError):
        debit_fits(-1.0, 0.0, 1.0)
