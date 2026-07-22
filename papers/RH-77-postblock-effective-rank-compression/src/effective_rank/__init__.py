"""Postblock low-rank compression theorems."""

from .bounds import (
    optimal_rank_residual,
    participation_rank,
    tail_compression_error,
)

__all__ = ["optimal_rank_residual", "participation_rank", "tail_compression_error"]
