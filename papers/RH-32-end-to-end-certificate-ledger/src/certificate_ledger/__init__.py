"""Rigorous finite-model count and contour-composition certificates."""

from .composition import (
    ArcTransportRecord,
    ComposedBound,
    compose_lifted_bound,
    transport_arc_cover,
)
from .counts import (
    AmbiguousCircleError,
    CircleClassification,
    certify_projected_model,
    classify_eigenvalue_balls,
)
from .provenance import sha256_file

__all__ = [
    "AmbiguousCircleError",
    "ArcTransportRecord",
    "CircleClassification",
    "ComposedBound",
    "certify_projected_model",
    "classify_eigenvalue_balls",
    "compose_lifted_bound",
    "sha256_file",
    "transport_arc_cover",
]
