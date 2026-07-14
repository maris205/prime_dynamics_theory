"""Bright/dark Schur reduction and target-coupling diagnostics."""

from .algebra import (
    NestedSchurData,
    SchurAudit,
    audit_matrix,
    bright_dark_transform,
    bright_root,
    characteristic,
    diagonal_gauge_transform,
    nested_schur_data,
    required_coupling,
    schur_function,
    self_energy,
    small_coupling_root_bound,
)

__all__ = [
    "NestedSchurData",
    "SchurAudit",
    "audit_matrix",
    "bright_dark_transform",
    "bright_root",
    "characteristic",
    "diagonal_gauge_transform",
    "nested_schur_data",
    "required_coupling",
    "schur_function",
    "self_energy",
    "small_coupling_root_bound",
]
