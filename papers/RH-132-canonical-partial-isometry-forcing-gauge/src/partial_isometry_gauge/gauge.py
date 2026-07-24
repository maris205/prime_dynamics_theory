"""Principal-angle polar gauges and positive-part forcing."""

from __future__ import annotations

import math
import numpy as np


def _basis(value: np.ndarray, name: str) -> np.ndarray:
    basis = np.asarray(value, dtype=float)
    if basis.ndim != 2 or basis.shape[1] == 0 or np.any(~np.isfinite(basis)):
        raise ValueError(f"{name} must be a finite nonempty basis")
    defect = float(np.linalg.norm(basis.T @ basis - np.eye(basis.shape[1]), 2))
    if defect > 1e-9:
        raise ValueError(f"{name} must have orthonormal columns")
    return basis


def _sym(value: np.ndarray, name: str) -> np.ndarray:
    matrix = np.asarray(value, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or np.any(~np.isfinite(matrix)):
        raise ValueError(f"{name} must be a finite square matrix")
    return (matrix + matrix.T) / 2.0


def canonical_partial_isometry(
    source_basis: np.ndarray,
    target_basis: np.ndarray,
    *,
    overlap_tolerance: float | None = None,
) -> dict[str, object]:
    """Return the polar partial isometry of ``P_target P_source``.

    The map acts in the common ambient space.  Its initial and final
    projectors retain only principal directions with cosine above the
    declared overlap tolerance.
    """
    source = _basis(source_basis, "source basis")
    target = _basis(target_basis, "target basis")
    if source.shape[0] != target.shape[0]:
        raise ValueError("source and target bases need a common ambient space")
    overlap = target.T @ source
    left, singular, right = np.linalg.svd(overlap, full_matrices=False)
    scale = float(singular[0]) if singular.size else 0.0
    tolerance = (
        128.0 * np.finfo(float).eps * max(overlap.shape) * max(1.0, scale)
        if overlap_tolerance is None
        else float(overlap_tolerance)
    )
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("overlap tolerance must be finite and nonnegative")
    rank = int(np.sum(singular > tolerance))
    if rank:
        source_principal = source @ right[:rank].T
        target_principal = target @ left[:, :rank]
        transport = target_principal @ source_principal.T
    else:
        source_principal = np.empty((source.shape[0], 0))
        target_principal = np.empty((source.shape[0], 0))
        transport = np.zeros((source.shape[0], source.shape[0]))
    initial = source_principal @ source_principal.T
    final = target_principal @ target_principal.T
    principal = np.arccos(np.clip(singular, 0.0, 1.0))
    return {
        "transport": transport,
        "initial_projector": initial,
        "final_projector": final,
        "source_projector": source @ source.T,
        "target_projector": target @ target.T,
        "overlap_rank": rank,
        "principal_cosines": singular,
        "principal_angles": principal,
        "overlap_tolerance": tolerance,
        "initial_defect": float(np.linalg.norm(transport.T @ transport - initial, 2)),
        "final_defect": float(np.linalg.norm(transport @ transport.T - final, 2)),
        "procrustes_distance_squared": float(source.shape[1] + target.shape[1] - 2.0 * np.sum(singular)),
    }


def minimal_trace_forcing(
    target_tail: np.ndarray,
    transported_tail: np.ndarray,
    multiplicative_factor: float,
    *,
    final_projector: np.ndarray | None = None,
) -> dict[str, object]:
    """Return ``(D' - b D_transport)_+`` and its sharp trace cost."""
    target = _sym(target_tail, "target tail")
    transported = _sym(transported_tail, "transported tail")
    if target.shape != transported.shape:
        raise ValueError("tail matrices must have the same shape")
    factor = float(multiplicative_factor)
    if not math.isfinite(factor) or factor < 0.0:
        raise ValueError("multiplicative factor must be finite and nonnegative")
    difference = target - factor * transported
    values, vectors = np.linalg.eigh(difference)
    positive = np.maximum(values, 0.0)
    forcing = (vectors * positive) @ vectors.T
    slack = factor * transported + forcing - target
    if final_projector is None:
        unmatched = 0.0
    else:
        final = _sym(final_projector, "final projector")
        if final.shape != target.shape:
            raise ValueError("final projector has incompatible shape")
        complement = np.eye(target.shape[0]) - final
        unmatched = float(np.trace(complement @ target @ complement))
    return {
        "forcing": forcing,
        "trace_cost": float(np.sum(positive)),
        "minimum_slack_eigenvalue": float(np.linalg.eigvalsh((slack + slack.T) / 2.0)[0]),
        "unmatched_target_trace_lower": unmatched,
        "difference_positive_eigenvalues": positive,
    }
