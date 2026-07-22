"""Finite-prefix plus block-power Hardy certificates."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BlockHardyCertificate:
    horizon: int
    finite_energy_squared: float
    source_block_squared: float
    block_power_frobenius: float
    observation_frobenius_squared: float
    tail_energy_squared_upper: float
    full_energy_squared_upper: float
    full_energy_upper: float


def _square(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be square")
    return result


def _source(value: np.ndarray, rows: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result.reshape(-1, 1)
    if result.ndim != 2 or result.shape[0] != rows:
        raise ValueError("source has incompatible shape")
    return result


def _observation(value: np.ndarray, columns: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result.reshape(1, -1)
    if result.ndim != 2 or result.shape[1] != columns:
        raise ValueError("observation has incompatible shape")
    return result


def block_hardy_certificate(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    horizon: int,
) -> BlockHardyCertificate:
    """Certify a full Hardy energy using ||A^M||_F<1."""

    a = _square(operator, "operator")
    x = _source(source, a.shape[0])
    y = _observation(observation, a.shape[0])
    length = int(horizon)
    if length <= 0:
        raise ValueError("horizon must be positive")
    state = x.copy()
    finite = 0.0
    source_block = 0.0
    for _ in range(length):
        source_block += float(np.linalg.norm(state, "fro") ** 2)
        finite += float(np.linalg.norm(y @ state, "fro") ** 2)
        state = a @ state
    power = np.linalg.matrix_power(a, length)
    q = float(np.linalg.norm(power, "fro"))
    if q >= 1.0:
        raise ValueError("block power is not Frobenius contractive")
    observation_squared = float(np.linalg.norm(y, "fro") ** 2)
    tail = observation_squared * q * q * source_block / (1.0 - q * q)
    full = finite + tail
    return BlockHardyCertificate(
        horizon=length,
        finite_energy_squared=finite,
        source_block_squared=source_block,
        block_power_frobenius=q,
        observation_frobenius_squared=observation_squared,
        tail_energy_squared_upper=tail,
        full_energy_squared_upper=full,
        full_energy_upper=float(np.sqrt(full)),
    )


def augmented_difference_system(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    comparison_operator: np.ndarray,
    comparison_source: np.ndarray,
    comparison_observation: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Realize YA^mX-Y~A~^mX~ as one augmented transfer sequence."""

    a = _square(operator, "operator")
    b = _square(comparison_operator, "comparison operator")
    if a.shape != b.shape:
        raise ValueError("operators must have equal dimensions")
    x = _source(source, a.shape[0])
    x_tilde = _source(comparison_source, b.shape[0])
    if x.shape[1] != x_tilde.shape[1]:
        raise ValueError("sources must have equal column counts")
    y = _observation(observation, a.shape[0])
    y_tilde = _observation(comparison_observation, b.shape[0])
    if y.shape[0] != y_tilde.shape[0]:
        raise ValueError("observations must have equal row counts")
    zero = np.zeros_like(a)
    augmented_operator = np.block([[a, zero], [zero, b]])
    augmented_source = np.vstack([x, x_tilde])
    augmented_observation = np.hstack([y, -y_tilde])
    return augmented_operator, augmented_source, augmented_observation
