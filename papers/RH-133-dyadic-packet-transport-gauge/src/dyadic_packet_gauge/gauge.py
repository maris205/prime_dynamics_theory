"""Natural geometric gauges induced by a fixed interscale isometry."""

from __future__ import annotations

import math
import numpy as np


def _frame(value: np.ndarray, name: str) -> np.ndarray:
    frame = np.asarray(value, dtype=float)
    if frame.ndim != 2 or frame.shape[1] == 0 or np.any(~np.isfinite(frame)):
        raise ValueError(f"{name} must be a finite nonempty frame")
    if np.linalg.norm(frame.T @ frame - np.eye(frame.shape[1]), 2) > 1e-9:
        raise ValueError(f"{name} must have orthonormal columns")
    return frame


def _positive(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    value = (value + value.T) / 2.0
    if np.linalg.eigvalsh(value)[0] <= 0.0:
        raise ValueError(f"{name} must be positive definite")
    return value


def dyadic_polar_alignment(source_frame: np.ndarray, target_frame: np.ndarray, embedding: np.ndarray) -> dict[str, object]:
    """Align an embedded source frame to a target frame by overlap polar SVD."""
    source = _frame(source_frame, "source frame")
    target = _frame(target_frame, "target frame")
    prolongation = np.asarray(embedding, dtype=float)
    if prolongation.shape != (target.shape[0], source.shape[0]):
        raise ValueError("embedding has incompatible shape")
    if np.linalg.norm(prolongation.T @ prolongation - np.eye(source.shape[0]), 2) > 1e-9:
        raise ValueError("embedding must be an isometry")
    embedded = prolongation @ source
    overlap = target.T @ embedded
    left, singular, right = np.linalg.svd(overlap, full_matrices=False)
    source_to_target = left @ right
    target_to_source = source_to_target.T
    return {
        "embedded_source_frame": embedded,
        "source_to_target": source_to_target,
        "target_to_source": target_to_source,
        "principal_cosines": singular,
        "principal_angles": np.arccos(np.clip(singular, 0.0, 1.0)),
        "minimum_principal_cosine": float(singular[-1]),
        "maximum_principal_angle": float(np.arccos(np.clip(singular[-1], 0.0, 1.0))),
        "aligned_frame_distance": float(np.linalg.norm(target @ source_to_target - embedded, "fro")),
    }


def _root_pair(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(matrix)
    root = (vectors * values**0.5) @ vectors.T
    inverse = (vectors * values**-0.5) @ vectors.T
    return root, inverse


def exact_gram_metric_lift(source_gram: np.ndarray, target_gram: np.ndarray, target_to_source: np.ndarray) -> dict[str, object]:
    """Lift an orthogonal geometric alignment to ``S.T G S = G'``."""
    source = _positive(source_gram, "source gram")
    target = _positive(target_gram, "target gram")
    orthogonal = np.asarray(target_to_source, dtype=float)
    if orthogonal.shape != source.shape or target.shape != source.shape:
        raise ValueError("metric lift dimensions do not agree")
    if np.linalg.norm(orthogonal.T @ orthogonal - np.eye(source.shape[0]), 2) > 1e-9:
        raise ValueError("geometric alignment must be orthogonal")
    target_root, _ = _root_pair(target)
    _, source_inverse = _root_pair(source)
    gauge = source_inverse @ orthogonal @ target_root
    return {
        "gauge": gauge,
        "gram_alignment_error": float(np.linalg.norm(gauge.T @ source @ gauge - target, 2)),
        "gauge_determinant": float(np.linalg.det(gauge)),
    }


def tail_inflation_factor(source_tail: np.ndarray, target_tail: np.ndarray, gauge: np.ndarray) -> float:
    """Least finite ``b`` in ``D' <= b S.T D S`` for positive tails."""
    source = _positive(source_tail, "source tail")
    target = _positive(target_tail, "target tail")
    transform = np.asarray(gauge, dtype=float)
    transported = transform.T @ source @ transform
    _, inverse = _root_pair((transported + transported.T) / 2.0)
    relative = inverse @ target @ inverse
    value = float(np.linalg.eigvalsh((relative + relative.T) / 2.0)[-1])
    if not math.isfinite(value):
        raise ValueError("tail inflation is not finite")
    return max(0.0, value)
