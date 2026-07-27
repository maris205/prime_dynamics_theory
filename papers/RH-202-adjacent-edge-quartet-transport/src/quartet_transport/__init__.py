"""Finite adjacent-level transport diagnostics for spectral packets."""

from .core import (
    biorthogonal_eigenpacket,
    channel_state,
    coefficient_error,
    haar_embedding,
    matched_assignment,
    principal_data,
    relative_frobenius_defect,
)

__all__ = [
    "biorthogonal_eigenpacket",
    "channel_state",
    "coefficient_error",
    "haar_embedding",
    "matched_assignment",
    "principal_data",
    "relative_frobenius_defect",
]
