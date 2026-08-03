"""Public API for the RH-354 near-alias direct-tail checks."""

from .core import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    PHYSICAL_LAMBDA_DIAGNOSTIC,
    Q,
    R,
    R_H,
    alias_tail_majorant,
    linear_root_diagnostic,
    rate_certificate,
    raw_method_certificate,
    result_status,
    threshold_diagnostics,
)

__all__ = [
    "FIXTURE_LAMBDA",
    "LAMBDA_LOWER",
    "LAMBDA_UPPER",
    "PHYSICAL_LAMBDA_DIAGNOSTIC",
    "Q",
    "R",
    "R_H",
    "alias_tail_majorant",
    "linear_root_diagnostic",
    "rate_certificate",
    "raw_method_certificate",
    "result_status",
    "threshold_diagnostics",
]
