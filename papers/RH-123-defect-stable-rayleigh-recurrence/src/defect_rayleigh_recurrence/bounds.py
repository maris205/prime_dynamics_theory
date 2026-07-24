"""Affine relative-Rayleigh recurrence with additive Loewner defects."""

from __future__ import annotations

import math
import numpy as np


def _nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def defect_gamma_squared_bound(
    source_gamma_squared: float,
    gram_factor: float,
    tail_factor: float,
    gram_defect_fraction: float,
    additive_tail_defect: float,
) -> float:
    """Return ``(b*x + delta)/(a*(1-eta))``."""
    x = _nonnegative(source_gamma_squared, "source gamma squared")
    a = float(gram_factor)
    b = _nonnegative(tail_factor, "tail factor")
    eta = float(gram_defect_fraction)
    delta = _nonnegative(additive_tail_defect, "additive tail defect")
    if not math.isfinite(a) or a <= 0.0:
        raise ValueError("gram factor must be finite and positive")
    if not math.isfinite(eta) or not 0.0 <= eta < 1.0:
        raise ValueError("gram defect fraction must lie in [0,1)")
    return (b * x + delta) / (a * (1.0 - eta))


def iterate_affine_upper(initial: float, rho: float, forcing: float, steps: int) -> list[float]:
    """Iterate ``x[n+1] = rho*x[n] + forcing`` including the initial value."""
    value = _nonnegative(initial, "initial value")
    multiplier = _nonnegative(rho, "rho")
    source = _nonnegative(forcing, "forcing")
    count = int(steps)
    if count < 0:
        raise ValueError("steps must be nonnegative")
    values = [value]
    for _ in range(count):
        value = multiplier * value + source
        values.append(value)
    return values


def _spd(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    value = (value + value.T) / 2.0
    if np.linalg.eigvalsh(value)[0] <= 0.0:
        raise ValueError(f"{name} must be positive definite")
    return value


def _gamma_squared(gram: np.ndarray, tail: np.ndarray) -> float:
    values, vectors = np.linalg.eigh(gram)
    inverse = (vectors * values**-0.5) @ vectors.T
    return float(np.linalg.eigvalsh(inverse @ tail @ inverse)[-1])


def defect_transfer_certificate(
    source_gram: np.ndarray,
    source_tail: np.ndarray,
    target_gram: np.ndarray,
    target_tail: np.ndarray,
    gauge: np.ndarray,
    gram_factor: float,
    tail_factor: float,
    gram_defect_fraction: float,
    additive_tail_defect: float,
) -> dict[str, float | bool]:
    g = _spd(source_gram, "source gram")
    d = _spd(source_tail, "source tail")
    gp = _spd(target_gram, "target gram")
    dp = _spd(target_tail, "target tail")
    s = np.asarray(gauge, dtype=float)
    if s.shape != g.shape or abs(np.linalg.det(s)) < 1e-15:
        raise ValueError("gauge must be invertible and have matching shape")
    a = float(gram_factor); b = float(tail_factor); eta = float(gram_defect_fraction); delta = float(additive_tail_defect)
    h = s.T @ g @ s
    gram_slack = float(np.linalg.eigvalsh(gp - a * (1.0 - eta) * h)[0])
    tail_slack = float(np.linalg.eigvalsh(b * s.T @ d @ s + delta * h - dp)[0])
    source = _gamma_squared(g, d)
    target = _gamma_squared(gp, dp)
    upper = defect_gamma_squared_bound(source, a, b, eta, delta)
    tolerance = 5e-10 * max(1.0, np.linalg.norm(gp, 2), np.linalg.norm(dp, 2))
    return {
        "source_gamma_squared": source, "target_gamma_squared": target, "target_gamma_squared_upper": upper,
        "gram_minimum_slack": gram_slack, "tail_minimum_slack": tail_slack,
        "gram_hypothesis_holds": bool(gram_slack >= -tolerance),
        "tail_hypothesis_holds": bool(tail_slack >= -tolerance),
        "conclusion_holds": bool(target <= upper + tolerance),
    }

