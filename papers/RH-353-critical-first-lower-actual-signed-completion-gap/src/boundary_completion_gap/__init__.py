"""Public API for the RH-353 boundary completion gap artifact."""

from .core import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    Q,
    R,
    R_H,
    boundary_completion,
    finite_rows,
    minimax_certificate,
    rate_certificate,
    result_status,
    weighted_supply_bound,
)

__all__ = [
    "FIXTURE_LAMBDA",
    "LAMBDA_LOWER",
    "LAMBDA_UPPER",
    "Q",
    "R",
    "R_H",
    "boundary_completion",
    "finite_rows",
    "minimax_certificate",
    "rate_certificate",
    "result_status",
    "weighted_supply_bound",
]
