"""Finite residue cocycle algebra."""

from __future__ import annotations

import numpy as np


def diagonal_multipliers(coarse: np.ndarray, fine: np.ndarray) -> np.ndarray:
    """Return the unique diagonal multipliers carrying nonzero residues."""

    initial = np.asarray(coarse, dtype=complex).reshape(-1)
    terminal = np.asarray(fine, dtype=complex).reshape(-1)
    if initial.shape != terminal.shape or initial.size < 1:
        raise ValueError("matching nonempty residue packets are required")
    if np.any(np.abs(initial) <= np.finfo(float).tiny):
        raise ValueError("coarse residues must be nonzero")
    return terminal / initial


def optimal_common_scalar(coarse: np.ndarray, fine: np.ndarray) -> dict[str, complex | float]:
    """Fit one complex scalar to all residue channels in least squares."""

    initial = np.asarray(coarse, dtype=complex).reshape(-1)
    terminal = np.asarray(fine, dtype=complex).reshape(-1)
    if initial.shape != terminal.shape or initial.size < 1:
        raise ValueError("matching nonempty residue packets are required")
    denominator = float(np.vdot(initial, initial).real)
    if denominator <= np.finfo(float).tiny:
        raise ValueError("coarse residue packet must be nonzero")
    scalar = complex(np.vdot(initial, terminal) / denominator)
    residual = float(
        np.linalg.norm(terminal - scalar * initial)
        / max(np.linalg.norm(terminal), np.finfo(float).tiny)
    )
    return {"scalar": scalar, "relative_residual": residual}
