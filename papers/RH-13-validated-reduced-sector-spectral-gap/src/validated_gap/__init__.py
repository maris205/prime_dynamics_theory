"""Validated reduced-sector spectral-gap tools."""

from .taylor_operator import (
    LAMBDA_FIXED,
    R_FIXED,
    U_CRITICAL,
    leading_eigenvalues,
    reduced_beta_one_matrix,
    sector_matrices,
    taylor_ingredients,
    weighted_absolute_radius,
)
from .certificate import CertifiedBounds, certify_reduced_gap

__all__ = [
    "LAMBDA_FIXED",
    "R_FIXED",
    "U_CRITICAL",
    "CertifiedBounds",
    "certify_reduced_gap",
    "leading_eigenvalues",
    "reduced_beta_one_matrix",
    "sector_matrices",
    "taylor_ingredients",
    "weighted_absolute_radius",
]
