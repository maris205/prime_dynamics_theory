"""Finite-dimensional forms of the RH-92 Schur and block estimates."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def _factors(values: Iterable[float]) -> tuple[float, ...]:
    factors = tuple(float(value) for value in values)
    if not factors or any(not math.isfinite(value) or value < 0.0 for value in factors):
        raise ValueError("a nonempty sequence of finite nonnegative factors is required")
    return factors


def block_budget_product(values: Iterable[float]) -> float:
    """Outward-rounded product of one-step contraction budgets."""
    product = math.prod(_factors(values))
    return math.nextafter(product, math.inf)


def block_geometric_mean(values: Iterable[float]) -> float:
    """Outward-rounded geometric mean of a contraction block."""
    factors = _factors(values)
    product = math.prod(factors)
    return math.nextafter(product ** (1.0 / len(factors)), math.inf)


def block_endpoint_tail_bound(initial_tail: float, block_factor: float, blocks: int) -> float:
    """Bound E_{b+kL} by Q^k E_b."""
    initial = float(initial_tail)
    factor = float(block_factor)
    count = int(blocks)
    if initial < 0.0 or not 0.0 <= factor < 1.0 or count < 0:
        raise ValueError("invalid block-tail data")
    return math.nextafter(initial * factor**count, math.inf)


def relative_snapshot_bound(eta: float, block_factor: float, blocks: int, *, prefix_factor: float = 1.0) -> float:
    """Crude normalized-snapshot residual bound after complete blocks."""
    decay = float(eta)
    factor = float(block_factor)
    prefix = float(prefix_factor)
    count = int(blocks)
    if not 0.0 <= decay < 1.0 or not 0.0 <= factor < 1.0 or prefix < 0.0 or count < 0:
        raise ValueError("invalid block-bootstrap data")
    value = math.sqrt(prefix * factor**count / (1.0 - decay))
    return math.nextafter(value, math.inf)


def blocks_for_tolerance(eta: float, block_factor: float, tolerance: float, *, prefix_factor: float = 1.0) -> int:
    """Smallest complete-block count reaching a relative tolerance."""
    target = float(tolerance)
    if target <= 0.0:
        raise ValueError("positive tolerance required")
    blocks = 0
    while relative_snapshot_bound(eta, block_factor, blocks, prefix_factor=prefix_factor) > target:
        blocks += 1
    return blocks


def schur_trial_form(matrix: np.ndarray, coupling: np.ndarray, delta: float, trial: np.ndarray) -> float:
    """Evaluate x^* M x - 2 Re(x^* b) + delta for real arrays."""
    m = np.asarray(matrix, dtype=float)
    b = np.asarray(coupling, dtype=float).reshape(-1)
    x = np.asarray(trial, dtype=float).reshape(-1)
    gain = float(delta)
    if m.shape != (x.size, x.size) or b.size != x.size or gain < 0.0:
        raise ValueError("incompatible Schur data")
    value = float(x @ m @ x - 2.0 * x @ b + gain)
    return math.nextafter(value, math.inf)


def coercive_secular_surplus(matrix: np.ndarray, coupling: np.ndarray, delta: float) -> float:
    """Return b^* M^{-1} b - delta when M is positive definite."""
    m = np.asarray(matrix, dtype=float)
    b = np.asarray(coupling, dtype=float).reshape(-1)
    gain = float(delta)
    if m.shape != (b.size, b.size) or gain < 0.0:
        raise ValueError("incompatible secular data")
    eigenvalues = np.linalg.eigvalsh((m + m.T) / 2.0)
    if eigenvalues[0] <= 0.0:
        raise ValueError("coercive surplus requires a positive-definite matrix")
    return float(b @ np.linalg.solve(m, b) - gain)


def coercive_defect(matrix: np.ndarray, coupling: np.ndarray, trial: np.ndarray) -> float:
    """Return r^* M^{-1} r for r=Mx-b in the coercive branch."""
    m = np.asarray(matrix, dtype=float)
    b = np.asarray(coupling, dtype=float).reshape(-1)
    x = np.asarray(trial, dtype=float).reshape(-1)
    if m.shape != (x.size, x.size) or b.size != x.size:
        raise ValueError("incompatible defect data")
    eigenvalues = np.linalg.eigvalsh((m + m.T) / 2.0)
    if eigenvalues[0] <= 0.0:
        raise ValueError("coercive defect requires a positive-definite matrix")
    residual = m @ x - b
    return float(residual @ np.linalg.solve(m, residual))
