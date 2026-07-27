"""Multiplicity identities for left multiplication on matrix Hilbert space."""

from __future__ import annotations

import numpy as np


def left_multiply(operator: np.ndarray, state: np.ndarray) -> np.ndarray:
    """Apply X -> AX after checking the physical matrix-state type."""

    dynamics = np.asarray(operator)
    values = np.asarray(state)
    if dynamics.ndim != 2 or dynamics.shape[0] != dynamics.shape[1]:
        raise ValueError("operator must be square")
    if values.ndim != 2 or values.shape[0] != dynamics.shape[0]:
        raise ValueError("state must have one row per operator coordinate")
    return dynamics @ values


def vectorized_left_operator(operator: np.ndarray, columns: int) -> np.ndarray:
    """Return the column-major matrix of X -> AX, namely I_m tensor A."""

    dynamics = np.asarray(operator)
    width = int(columns)
    if dynamics.ndim != 2 or dynamics.shape[0] != dynamics.shape[1]:
        raise ValueError("operator must be square")
    if width < 1:
        raise ValueError("columns must be positive")
    return np.kron(np.eye(width, dtype=dynamics.dtype), dynamics)


def riesz_rank(base_rank: int, columns: int) -> int:
    """Rank of P_Gamma(A) acting by left multiplication on n by m matrices."""

    rank = int(base_rank)
    width = int(columns)
    if rank < 0 or width < 1:
        raise ValueError("invalid rank or column count")
    return rank * width


def characteristic_power(base_determinant: complex, columns: int) -> complex:
    """Evaluate det(zI-L_A)=det(zI-A)^m from the base determinant."""

    width = int(columns)
    if width < 1:
        raise ValueError("columns must be positive")
    return complex(base_determinant) ** width


def complement_count(base_count: int, packet_count: int, columns: int) -> int:
    """Complement count forced by N_L=m N_A=N_K+N_D.

    A negative answer means that the proposed Schur homotopy/count identity
    cannot hold for those counts.
    """

    base = int(base_count)
    packet = int(packet_count)
    width = int(columns)
    if base < 0 or packet < 0 or width < 1:
        raise ValueError("counts must be nonnegative and columns positive")
    return width * base - packet


def complement_free_compatible(packet_count: int, columns: int) -> bool:
    """Whether a packet count can equal a full Frobenius Riesz count."""

    packet = int(packet_count)
    width = int(columns)
    if packet < 0 or width < 1:
        raise ValueError("invalid packet count or column count")
    return packet % width == 0


def resolvent_norm_identity(operator: np.ndarray, z: complex) -> tuple[float, float]:
    """Numerically compare base and one repeated Frobenius resolvent norm."""

    dynamics = np.asarray(operator, dtype=complex)
    base = np.linalg.inv(complex(z) * np.eye(dynamics.shape[0]) - dynamics)
    repeated = vectorized_left_operator(dynamics, 2)
    ambient = np.linalg.inv(complex(z) * np.eye(repeated.shape[0]) - repeated)
    return float(np.linalg.norm(base, 2)), float(np.linalg.norm(ambient, 2))
