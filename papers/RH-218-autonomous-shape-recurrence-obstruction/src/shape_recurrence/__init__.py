"""Autonomous shape-recurrence audit."""

from .core import (
    SCALAR_MODELS,
    AffineShapeMap,
    ScalarRecurrence,
    error_metrics,
    evaluate_polynomial_shape_map,
    fit_affine_shape_map,
    fit_scalar_recurrence,
    inverse_transform,
    lagrange_autonomous_map,
    transform,
)

__all__ = [
    "SCALAR_MODELS",
    "AffineShapeMap",
    "ScalarRecurrence",
    "error_metrics",
    "evaluate_polynomial_shape_map",
    "fit_affine_shape_map",
    "fit_scalar_recurrence",
    "inverse_transform",
    "lagrange_autonomous_map",
    "transform",
]
