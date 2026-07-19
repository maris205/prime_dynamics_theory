"""Algebra and endpoint scaling for RH-49 directional resolvents."""

from .algebra import (
    DirectionalResidualUpper,
    StableRankTransfer,
    deflated_shift_dense,
    directional_residual_upper,
    mixed_gain_from_hilbert_schmidt,
    rank_one_projection,
    reduced_resolvent_dense,
)
from .endpoint import (
    critical_fold_profile,
    critical_fold_profile_derivative,
    packet_envelope,
    packet_limit_profile,
)

__all__ = [
    "DirectionalResidualUpper",
    "StableRankTransfer",
    "critical_fold_profile",
    "critical_fold_profile_derivative",
    "deflated_shift_dense",
    "directional_residual_upper",
    "mixed_gain_from_hilbert_schmidt",
    "packet_envelope",
    "packet_limit_profile",
    "rank_one_projection",
    "reduced_resolvent_dense",
]
