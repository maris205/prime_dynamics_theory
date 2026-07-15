"""Directional contour correction for packet-complement Feshbach maps."""

from .algebra import (
    DirectionalCorrection,
    TailMajorant,
    circular_lipschitz_lower_bound,
    determinant_winding,
    exact_directional_correction,
    fom_external_solution,
    geometric_tail_majorant,
    global_scalar_majorant,
    matrix_rouche_ratio,
)

__all__ = [
    "DirectionalCorrection",
    "TailMajorant",
    "circular_lipschitz_lower_bound",
    "determinant_winding",
    "exact_directional_correction",
    "fom_external_solution",
    "geometric_tail_majorant",
    "global_scalar_majorant",
    "matrix_rouche_ratio",
]
