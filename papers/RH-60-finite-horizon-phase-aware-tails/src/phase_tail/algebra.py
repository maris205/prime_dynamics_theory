"""Finite-horizon packet Grams and positive Stein tail completions."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np


def _square_matrix(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be square")
    return result


def _source_matrix(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[:, None]
    if result.ndim != 2 or result.shape[0] != dimension:
        raise ValueError("source has incompatible shape")
    return result


def _observation_matrix(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[None, :]
    if result.ndim != 2 or result.shape[1] != dimension:
        raise ValueError("observation has incompatible shape")
    return result


def block_slices(sizes: Sequence[int]) -> tuple[slice, ...]:
    result = []
    position = 0
    for item in sizes:
        width = int(item)
        if width <= 0:
            raise ValueError("block sizes must be positive")
        result.append(slice(position, position + width))
        position += width
    return tuple(result)


@dataclass(frozen=True)
class FiniteHorizonGram:
    """Finite response Gram and its exact fused energy."""

    horizon: int
    gram: np.ndarray
    packet_energy_squared: np.ndarray
    fused_energy_squared: float

    @property
    def fused_energy(self) -> float:
        return math.sqrt(max(0.0, self.fused_energy_squared))


def finite_horizon_gram(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    horizon: int,
    *,
    packet_slices: Sequence[slice] | None = None,
) -> FiniteHorizonGram:
    r"""Compute the exact Gram of responses for times ``0 <= m < horizon``.

    If packet slices are supplied, each source packet is propagated separately
    and the returned Gram retains all finite-horizon cross phases.
    """

    a = _square_matrix(operator, "operator")
    x = _source_matrix(source, a.shape[0])
    y = _observation_matrix(observation, a.shape[0])
    count = int(horizon)
    if count < 0:
        raise ValueError("horizon must be nonnegative")
    if packet_slices is None:
        slices = (slice(0, a.shape[0]),)
    else:
        slices = tuple(packet_slices)
        if not slices:
            raise ValueError("packet_slices must not be empty")
        for block_slice in slices:
            if block_slice.start is None or block_slice.stop is None:
                raise ValueError("packet slices must have explicit endpoints")
            if block_slice.start < 0 or block_slice.stop > a.shape[0]:
                raise ValueError("packet slice is outside the state space")
    states = []
    for block_slice in slices:
        packet = np.zeros_like(x)
        packet[block_slice, :] = x[block_slice, :]
        states.append(packet)
    gram = np.zeros((len(states), len(states)), dtype=np.complex128)
    for _ in range(count):
        responses = [y @ state for state in states]
        for row, response_left in enumerate(responses):
            for column, response_right in enumerate(responses):
                gram[row, column] += np.trace(
                    response_left @ response_right.conjugate().T
                )
        states = [a @ state for state in states]
    gram = 0.5 * (gram + gram.conjugate().T)
    diagonal = np.maximum(np.real(np.diag(gram)), 0.0)
    fused = float(np.real(np.sum(gram)))
    if fused < -1.0e-10 * max(1.0, float(np.sum(diagonal))):
        raise ValueError("finite-horizon fused Gram is not positive")
    return FiniteHorizonGram(
        horizon=count,
        gram=gram,
        packet_energy_squared=diagonal,
        fused_energy_squared=max(0.0, fused),
    )


def normalized_power(
    normalized_operator: np.ndarray,
    weighted_source: np.ndarray,
    horizon: int,
) -> np.ndarray:
    """Apply a normalized operator power to a weighted source."""

    s = _square_matrix(normalized_operator, "normalized_operator")
    state = _source_matrix(weighted_source, s.shape[0])
    count = int(horizon)
    if count < 0:
        raise ValueError("horizon must be nonnegative")
    for _ in range(count):
        state = s @ state
    return state


def stein_tail_energy_upper(
    normalized_operator: np.ndarray,
    weighted_source: np.ndarray,
    kappa: float,
    horizon: int,
) -> float:
    r"""Return ``sqrt(kappa) ||S^L P^(1/2) X||_HS``."""

    multiplier = float(kappa)
    if not math.isfinite(multiplier) or multiplier < 0.0:
        raise ValueError("kappa must be finite and nonnegative")
    state = normalized_power(normalized_operator, weighted_source, horizon)
    return math.sqrt(max(0.0, multiplier)) * float(np.linalg.norm(state, "fro"))


def geometric_tail_energy_upper(
    normalized_operator: np.ndarray,
    weighted_source: np.ndarray,
    kappa: float,
    horizon: int,
) -> float:
    """Use a one-number contraction rate to upper-bound the Stein tail."""

    s = _square_matrix(normalized_operator, "normalized_operator")
    q = float(np.linalg.norm(s, 2))
    if q >= 1.0:
        raise ValueError("normalized operator is not contractive")
    source_norm = float(np.linalg.norm(weighted_source, "fro"))
    return math.sqrt(max(0.0, float(kappa))) * q ** int(horizon) * source_norm


def packet_hybrid_upper(
    finite_packet_energy: float, tail_energy: float
) -> float:
    """Combine orthogonal-in-time finite and tail packet energies."""

    short = float(finite_packet_energy)
    tail = float(tail_energy)
    if short < 0.0 or tail < 0.0:
        raise ValueError("packet energies must be nonnegative")
    return math.hypot(short, tail)


def phase_aware_completion_upper(
    finite_fused_energy: float, tail_energies: Sequence[float]
) -> float:
    r"""Minkowski completion preserving all finite-horizon cross phases.

    The finite part is fused before applying a triangle inequality; only the
    separate tails are summed absolutely.
    """

    finite = float(finite_fused_energy)
    tails = tuple(float(value) for value in tail_energies)
    if finite < 0.0 or any(value < 0.0 for value in tails):
        raise ValueError("completion terms must be nonnegative")
    return finite + sum(tails)


@dataclass(frozen=True)
class TailCompletion:
    """Stored components of a phase-aware finite-horizon completion."""

    horizon: int
    finite_fused_energy: float
    tail_energies: tuple[float, ...]
    phase_aware_upper: float
    packet_hybrid_uppers: tuple[float, ...]


def make_completion(
    finite: FiniteHorizonGram,
    tail_energies: Sequence[float],
) -> TailCompletion:
    tails = tuple(float(value) for value in tail_energies)
    if len(tails) != len(finite.packet_energy_squared):
        raise ValueError("one tail is required per finite-horizon packet")
    packet_uppers = tuple(
        packet_hybrid_upper(math.sqrt(max(0.0, energy)), tail)
        for energy, tail in zip(finite.packet_energy_squared, tails)
    )
    return TailCompletion(
        horizon=finite.horizon,
        finite_fused_energy=finite.fused_energy,
        tail_energies=tails,
        phase_aware_upper=phase_aware_completion_upper(
            finite.fused_energy, tails
        ),
        packet_hybrid_uppers=packet_uppers,
    )
