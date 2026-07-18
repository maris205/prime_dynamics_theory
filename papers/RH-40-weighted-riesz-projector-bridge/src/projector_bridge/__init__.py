"""Weighted peripheral Riesz-term and dyadic low-rank utilities."""

from .low_rank import (
    PeripheralData,
    block_factors,
    biorthogonality_defect,
    low_rank_frobenius_norm,
    low_rank_singular_values,
    weighted_term,
)

__all__ = [
    "PeripheralData",
    "block_factors",
    "biorthogonality_defect",
    "low_rank_frobenius_norm",
    "low_rank_singular_values",
    "weighted_term",
]
