"""Phase-coherence block-depth barriers."""

from .coherence import (
    ProjectionAudit,
    arc_phases,
    jittered_ring_phases,
    phase_krylov_vectors,
    projection_audit,
    required_depth,
    uniform_ring_phases,
)

__all__ = [
    "ProjectionAudit",
    "arc_phases",
    "jittered_ring_phases",
    "phase_krylov_vectors",
    "projection_audit",
    "required_depth",
    "uniform_ring_phases",
]
