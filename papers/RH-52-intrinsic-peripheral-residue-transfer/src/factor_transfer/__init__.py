"""Weak-factor and peripheral-residue transfer algebra."""

from .algebra import (
    FactorNorms,
    WeakResidueBudget,
    aggregate_left_masses,
    average_right_values,
    left_haar_detail_l2,
    left_mass_norms,
    normalize_l1,
    normalize_linf,
    rank_one_difference_frobenius,
    rank_one_frobenius,
    right_value_norms,
    weak_residue_budget,
    weak_to_l2_factor_upper,
)

__all__ = [
    "FactorNorms",
    "WeakResidueBudget",
    "aggregate_left_masses",
    "average_right_values",
    "left_haar_detail_l2",
    "left_mass_norms",
    "normalize_l1",
    "normalize_linf",
    "rank_one_difference_frobenius",
    "rank_one_frobenius",
    "right_value_norms",
    "weak_residue_budget",
    "weak_to_l2_factor_upper",
]
