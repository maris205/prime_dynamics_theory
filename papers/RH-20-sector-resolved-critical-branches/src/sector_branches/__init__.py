"""Sector-resolved two-branch return algebra."""

from .algebra import (
    bright_dark_transform,
    forced_relative_phase,
    phase_weighted_return,
    rank_one_branch_matrix,
)
from .operators import (
    branch_profile_basis,
    compressed_branch_cycle,
    dense_matrix,
)

__all__ = [
    "branch_profile_basis",
    "bright_dark_transform",
    "compressed_branch_cycle",
    "dense_matrix",
    "forced_relative_phase",
    "phase_weighted_return",
    "rank_one_branch_matrix",
]
