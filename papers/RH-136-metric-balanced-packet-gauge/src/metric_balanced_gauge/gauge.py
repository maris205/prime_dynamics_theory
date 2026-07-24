"""Balance Gram inflation against Euclidean frame displacement."""

from __future__ import annotations

import numpy as np


def _positive(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    value = (value + value.T) / 2.0
    if np.linalg.eigvalsh(value)[0] <= 0.0:
        raise ValueError(f"{name} must be positive definite")
    return value


def polar_frame_alignment(source_frame: np.ndarray, target_frame: np.ndarray) -> np.ndarray:
    """Return the target-to-source orthogonal Procrustes map."""
    source = np.asarray(source_frame, dtype=float)
    target = np.asarray(target_frame, dtype=float)
    if source.shape != target.shape or source.ndim != 2 or np.any(~np.isfinite(source)) or np.any(~np.isfinite(target)):
        raise ValueError("frames must be finite and have the same shape")
    left, _, right = np.linalg.svd(source.T @ target, full_matrices=False)
    return left @ right


def metric_optimal_alignment(source_gram: np.ndarray, target_gram: np.ndarray) -> dict[str, object]:
    """Match ordered Gram eigenframes to minimize one-sided inflation."""
    source = _positive(source_gram, "source gram")
    target = _positive(target_gram, "target gram")
    if source.shape != target.shape:
        raise ValueError("Gram dimensions differ")
    source_values, source_vectors = np.linalg.eigh(source)
    target_values, target_vectors = np.linalg.eigh(target)
    orthogonal = source_vectors @ target_vectors.T
    factor = float(np.max(source_values / target_values))
    return {
        "target_to_source": orthogonal,
        "minimum_metric_factor": factor,
        "source_eigenvalues": source_values,
        "target_eigenvalues": target_values,
    }


def metric_inflation(
    source_gram: np.ndarray,
    target_gram: np.ndarray,
    target_to_source: np.ndarray,
) -> float:
    """Return the least c with O^T G O <= c G' for an orthogonal O."""
    source = _positive(source_gram, "source gram")
    target = _positive(target_gram, "target gram")
    orthogonal = np.asarray(target_to_source, dtype=float)
    if source.shape != target.shape or orthogonal.shape != source.shape:
        raise ValueError("Gram and orthogonal dimensions differ")
    if np.any(~np.isfinite(orthogonal)):
        raise ValueError("orthogonal map must be finite")
    if np.linalg.norm(orthogonal.T @ orthogonal - np.eye(source.shape[0]), 2) > 1e-8:
        raise ValueError("target-to-source map must be orthogonal")
    target_values, target_vectors = np.linalg.eigh(target)
    inverse = target_vectors @ np.diag(target_values ** -0.5) @ target_vectors.T
    relative = inverse @ orthogonal.T @ source @ orthogonal @ inverse
    return float(np.linalg.eigvalsh((relative + relative.T) / 2.0)[-1])


def polar_blend(first: np.ndarray, second: np.ndarray, weight: float) -> np.ndarray:
    """Project a convex matrix blend back to the orthogonal group."""
    left = np.asarray(first, dtype=float)
    right = np.asarray(second, dtype=float)
    value = float(weight)
    if left.shape != right.shape or left.ndim != 2 or left.shape[0] != left.shape[1]:
        raise ValueError("orthogonal matrices must have the same square shape")
    if not 0.0 <= value <= 1.0:
        raise ValueError("weight must lie in [0,1]")
    blended = (1.0 - value) * left + value * right
    u, _, vh = np.linalg.svd(blended)
    return u @ vh
