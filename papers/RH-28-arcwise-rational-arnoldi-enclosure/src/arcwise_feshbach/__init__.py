"""Arcwise rational Arnoldi enclosures for stored Feshbach models."""

from .coordinates import (
    CoordinateDisc,
    coordinate_difference,
    coordinate_extension_sum,
    enclose_coordinate_increment,
    enclose_shifted_coordinate_ball,
    enclose_shifted_coordinates,
    nonnegative_frobenius_upper,
    positive_fixed_point_upper,
)
from .geometry import (
    ArcDisc,
    bisect_circular_arc_disc,
    circular_arc_discs,
    fractional_circular_arc_disc,
)
from .evaluator import (
    ArcBudget,
    evaluate_arc_budget,
    family_inverse_norm_upper,
    projected_feshbach_ball,
)
from .relations import (
    PrimalRelationSummary,
    RelationSummary,
    StaticArcCertificate,
    basis_two_norm_upper,
    build_static_arc_certificate,
)

__all__ = [
    "ArcDisc",
    "ArcBudget",
    "CoordinateDisc",
    "PrimalRelationSummary",
    "RelationSummary",
    "StaticArcCertificate",
    "basis_two_norm_upper",
    "build_static_arc_certificate",
    "bisect_circular_arc_disc",
    "circular_arc_discs",
    "coordinate_difference",
    "coordinate_extension_sum",
    "enclose_coordinate_increment",
    "enclose_shifted_coordinate_ball",
    "enclose_shifted_coordinates",
    "evaluate_arc_budget",
    "family_inverse_norm_upper",
    "fractional_circular_arc_disc",
    "nonnegative_frobenius_upper",
    "positive_fixed_point_upper",
    "projected_feshbach_ball",
]
