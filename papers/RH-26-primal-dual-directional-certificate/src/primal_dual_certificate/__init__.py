"""Goal-oriented primal-dual closure of low-rank Feshbach errors."""

from .algebra import (
    PrimalDualCorrection,
    exact_identity_residual,
    primal_dual_correction,
    primal_dual_correction_from_residuals,
    resolvent_budget,
)

__all__ = [
    "PrimalDualCorrection",
    "exact_identity_residual",
    "primal_dual_correction",
    "primal_dual_correction_from_residuals",
    "resolvent_budget",
]
