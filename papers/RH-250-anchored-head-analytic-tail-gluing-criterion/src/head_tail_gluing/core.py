"""Elementary but exact coefficient-to-determinant gluing estimates."""

from __future__ import annotations

import math


def logarithmic_gluing_error(
    head_error: float,
    quotient_tail_bound: float,
    target_tail_bound: float,
) -> float:
    """Bound the absolute difference of two logarithmic determinant series."""

    values = (float(head_error), float(quotient_tail_bound), float(target_tail_bound))
    if any(value < 0.0 for value in values):
        raise ValueError("all error budgets must be nonnegative")
    return sum(values)


def determinant_difference_bound(log_error: float, log_budget: float) -> float:
    """Convert a log-series error into an exponential determinant error."""

    error = float(log_error)
    budget = float(log_budget)
    if error < 0.0 or budget < 0.0:
        raise ValueError("errors and budgets must be nonnegative")
    return float(math.exp(budget) * error)
