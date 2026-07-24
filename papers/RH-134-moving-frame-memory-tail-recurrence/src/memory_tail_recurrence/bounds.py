"""Exact tail birth identity and sharp Young moving-frame bound."""

from __future__ import annotations

import math
import numpy as np


def _sym(value: np.ndarray, name: str) -> np.ndarray:
    matrix = np.asarray(value, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or np.any(~np.isfinite(matrix)):
        raise ValueError(f"{name} must be a finite square matrix")
    return (matrix + matrix.T) / 2.0


def _eta(value: float) -> float:
    decay = float(value)
    if not math.isfinite(decay) or decay < 0.0 or decay >= 1.0:
        raise ValueError("eta must lie in [0,1)")
    return decay


def memory_tail_update(tail: np.ndarray, boundary_snapshot: np.ndarray, eta: float, depth: int) -> np.ndarray:
    """Return the exact update ``eta T + eta**depth X_boundary``."""
    old = _sym(tail, "tail")
    snapshot = _sym(boundary_snapshot, "boundary snapshot")
    if old.shape != snapshot.shape:
        raise ValueError("tail and snapshot dimensions differ")
    decay = _eta(eta)
    memory = int(depth)
    if memory <= 0:
        raise ValueError("depth must be positive")
    result = decay * old + decay**memory * snapshot
    return (result + result.T) / 2.0


def moving_frame_tail_upper(
    old_compressed_tail: np.ndarray,
    old_tail_norm_upper: float,
    boundary_compressed_snapshot: np.ndarray,
    target_to_source: np.ndarray,
    frame_defect_norm: float,
    eta: float,
    depth: int,
    tau: float,
) -> dict[str, object]:
    """Bound the next compressed raw tail in a moving target frame."""
    old = _sym(old_compressed_tail, "old compressed tail")
    birth = _sym(boundary_compressed_snapshot, "boundary compressed snapshot")
    orthogonal = np.asarray(target_to_source, dtype=float)
    if orthogonal.shape != old.shape or birth.shape != old.shape:
        raise ValueError("compressed dimensions differ")
    if np.linalg.norm(orthogonal.T @ orthogonal - np.eye(old.shape[0]), 2) > 1e-9:
        raise ValueError("target-to-source map must be orthogonal")
    tail_norm = float(old_tail_norm_upper)
    defect = float(frame_defect_norm)
    parameter = float(tau)
    decay = _eta(eta)
    memory = int(depth)
    if not math.isfinite(tail_norm) or tail_norm < 0.0:
        raise ValueError("tail norm upper must be finite and nonnegative")
    if not math.isfinite(defect) or defect < 0.0:
        raise ValueError("frame defect norm must be finite and nonnegative")
    if not math.isfinite(parameter) or parameter <= 0.0:
        raise ValueError("tau must be finite and positive")
    if memory <= 0:
        raise ValueError("depth must be positive")
    transported = decay * (1.0 + parameter) * orthogonal.T @ old @ orthogonal
    frame_scalar = decay * (1.0 + 1.0 / parameter) * tail_norm * defect**2
    frame_forcing = frame_scalar * np.eye(old.shape[0])
    birth_forcing = decay**memory * birth
    upper = transported + frame_forcing + birth_forcing
    return {
        "upper": (upper + upper.T) / 2.0,
        "transported": (transported + transported.T) / 2.0,
        "frame_forcing": frame_forcing,
        "birth_forcing": (birth_forcing + birth_forcing.T) / 2.0,
        "raw_multiplicative_factor": decay * (1.0 + parameter),
        "frame_forcing_scalar": frame_scalar,
    }


def envelope_ratio(eta: float, depth: int, past_snapshot_count: int) -> float:
    """Return ``delta_{p+1}/delta_p`` for a nonempty finite tail."""
    decay = _eta(eta)
    memory = int(depth)
    count = int(past_snapshot_count)
    if memory <= 0:
        raise ValueError("depth must be positive")
    if count <= 0:
        raise ValueError("past snapshot count must be positive")
    numerator = 1.0 - decay ** (count + 1)
    denominator = 1.0 - decay**count
    return numerator / denominator
