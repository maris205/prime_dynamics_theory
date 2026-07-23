"""Four-frame determinant lower bounds for a matrix exterior norm."""
from __future__ import annotations
import math
import numpy as np

ORDER = 4

def _matrix(value: np.ndarray, minimum_columns: int = ORDER) -> np.ndarray:
    matrix = np.asarray(value, dtype=float)
    if matrix.ndim != 2 or matrix.shape[1] < minimum_columns:
        raise ValueError("a finite matrix with at least four columns is required")
    if np.any(~np.isfinite(matrix)):
        raise ValueError("matrix entries must be finite")
    return matrix

def _leading(value: float) -> float:
    leading = float(value)
    if not math.isfinite(leading) or leading < 0.0:
        raise ValueError("the leading upper bound must be finite and nonnegative")
    return leading

def top_right_frame(matrix: np.ndarray, order: int = ORDER) -> np.ndarray:
    """Return an orthonormal frame of leading right singular vectors."""
    operator = _matrix(matrix)
    degree = int(order)
    if degree < 1 or degree > min(operator.shape):
        raise ValueError("invalid frame order")
    _, _, vh = np.linalg.svd(operator, full_matrices=False)
    return vh[:degree].T

def frame_volume(action: np.ndarray) -> float:
    """Return the Euclidean four-volume of the columns of ``action``."""
    columns = np.asarray(action, dtype=float)
    if columns.ndim != 2 or columns.shape[1] != ORDER or np.any(~np.isfinite(columns)):
        raise ValueError("the directional action must have exactly four finite columns")
    singular = np.linalg.svd(columns, compute_uv=False)
    if singular.size < ORDER:
        return 0.0
    return float(np.prod(singular[:ORDER]))

def spectral_four_volume(matrix: np.ndarray) -> float:
    """Return ``||wedge^4 K||_2``."""
    singular = np.linalg.svd(_matrix(matrix), compute_uv=False)
    if singular.size < ORDER:
        return 0.0
    return float(np.prod(singular[:ORDER]))

def exact_frame_certificate(action: np.ndarray, leading_upper_bound: float) -> float:
    """Normalize an exact four-directional action by a valid leading upper."""
    leading = _leading(leading_upper_bound)
    return frame_volume(action) / leading**ORDER if leading else 0.0

def approximate_frame_certificate(
    approximate_action: np.ndarray,
    action_error_bound: float,
    leading_upper_bound: float,
) -> dict[str, float]:
    """Certify a frame volume from an approximate four-column action."""
    action = np.asarray(approximate_action, dtype=float)
    if action.ndim != 2 or action.shape[1] != ORDER or np.any(~np.isfinite(action)):
        raise ValueError("the approximate action must have exactly four finite columns")
    error = float(action_error_bound)
    leading = _leading(leading_upper_bound)
    if not math.isfinite(error) or error < 0.0:
        raise ValueError("the action error bound must be finite and nonnegative")
    singular = np.linalg.svd(action, compute_uv=False)
    lower_singular = np.maximum(singular[:ORDER] - error, 0.0)
    raw_lower = float(np.prod(lower_singular))
    normalized = raw_lower / leading**ORDER if leading else 0.0
    return {
        "raw_lower": raw_lower,
        "normalized_lower": normalized,
        "action_error_bound": error,
        "leading_upper_bound": leading,
    }

def capture_ratio(matrix: np.ndarray, frame: np.ndarray) -> float:
    """Return frame four-volume divided by the optimal spectral four-volume."""
    operator = _matrix(matrix)
    basis = np.asarray(frame, dtype=float)
    if basis.ndim != 2 or basis.shape != (operator.shape[1], ORDER):
        raise ValueError("frame has incompatible shape")
    gram_error = np.linalg.norm(basis.T @ basis - np.eye(ORDER), 2)
    if gram_error > 1e-9:
        raise ValueError("frame columns must be orthonormal")
    optimum = spectral_four_volume(operator)
    return frame_volume(operator @ basis) / optimum if optimum else 0.0
