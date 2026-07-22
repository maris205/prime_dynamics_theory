"""A posteriori peripheral eigenpair certificates."""

from .certificates import (
    NewtonRadius,
    ProjectorError,
    newton_contraction_radius,
    parity_projector_error,
)

__all__ = [
    "NewtonRadius",
    "ProjectorError",
    "newton_contraction_radius",
    "parity_projector_error",
]
