"""Finite-anchor scale-law diagnostics and barriers."""

from .barrier import (
    anchor_matching_extension,
    bounded_anchor_matching_extension,
    log_lagrange_interpolant,
    loglog_fit,
    smooth_cutoff,
)

__all__ = [
    "anchor_matching_extension",
    "bounded_anchor_matching_extension",
    "log_lagrange_interpolant",
    "loglog_fit",
    "smooth_cutoff",
]
