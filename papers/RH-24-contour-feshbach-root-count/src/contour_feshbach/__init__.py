"""Contour-wise rational Feshbach reduction and root counting."""

from .model import (
    BatchedArnoldiFeshbach,
    ContourAudit,
    FeshbachEvaluation,
    RootResult,
    SampledRoucheAudit,
    build_batched_arnoldi_feshbach,
    circle_contour_audit,
    determinant_newton_root,
    sampled_rouche_audit,
)

__all__ = [
    "BatchedArnoldiFeshbach",
    "ContourAudit",
    "FeshbachEvaluation",
    "RootResult",
    "SampledRoucheAudit",
    "build_batched_arnoldi_feshbach",
    "circle_contour_audit",
    "determinant_newton_root",
    "sampled_rouche_audit",
]
