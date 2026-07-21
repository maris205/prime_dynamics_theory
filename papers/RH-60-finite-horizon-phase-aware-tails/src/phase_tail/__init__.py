"""Finite-horizon phase-aware completion algebra for RH-60."""

from .algebra import (
    FiniteHorizonGram,
    TailCompletion,
    block_slices,
    finite_horizon_gram,
    geometric_tail_energy_upper,
    make_completion,
    normalized_power,
    packet_hybrid_upper,
    phase_aware_completion_upper,
    stein_tail_energy_upper,
)

__all__ = [
    "FiniteHorizonGram",
    "TailCompletion",
    "block_slices",
    "finite_horizon_gram",
    "geometric_tail_energy_upper",
    "make_completion",
    "normalized_power",
    "packet_hybrid_upper",
    "phase_aware_completion_upper",
    "stein_tail_energy_upper",
]
