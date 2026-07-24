"""Loewner transfer of relative Gramians under an invertible frame gauge."""

from __future__ import annotations

import math
import numpy as np


def _symmetric(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    return (value + value.T) / 2.0


def _positive(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return number


def _inverse_root(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    if values[0] <= 0.0:
        raise ValueError("the reference Gramian must be positive definite")
    return (vectors * values**-0.5) @ vectors.T


def relative_gamma(gram: np.ndarray, tail_upper: np.ndarray) -> float:
    """Return the least ``gamma`` such that ``tail_upper <= gamma^2 gram``."""
    g = _symmetric(gram, "gram")
    d = _symmetric(tail_upper, "tail upper")
    if np.linalg.eigvalsh(d)[0] < -1e-11:
        raise ValueError("the tail upper must be positive semidefinite")
    inverse = _inverse_root(g)
    relative = inverse @ d @ inverse
    relative = (relative + relative.T) / 2.0
    return math.sqrt(max(0.0, float(np.linalg.eigvalsh(relative)[-1])))


def frame_volume(gram: np.ndarray) -> float:
    """Return ``sqrt(det gram)`` with a stable eigenvalue product."""
    g = _symmetric(gram, "gram")
    values = np.linalg.eigvalsh(g)
    if values[0] < -1e-11:
        raise ValueError("the Gramian must be positive semidefinite")
    return float(np.sqrt(np.prod(np.maximum(values, 0.0))))


def transfer_gamma_bound(source_gamma: float, gram_factor: float, tail_factor: float) -> float:
    """Return ``sqrt(tail_factor / gram_factor) * source_gamma``."""
    gamma = float(source_gamma)
    if not math.isfinite(gamma) or gamma < 0.0:
        raise ValueError("source gamma must be finite and nonnegative")
    a = _positive(gram_factor, "gram factor")
    b = float(tail_factor)
    if not math.isfinite(b) or b < 0.0:
        raise ValueError("tail factor must be finite and nonnegative")
    return math.sqrt(b / a) * gamma


def gauge_transfer_certificate(
    source_gram: np.ndarray,
    source_tail: np.ndarray,
    target_gram: np.ndarray,
    target_tail: np.ndarray,
    gauge: np.ndarray,
    gram_factor: float,
    tail_factor: float,
) -> dict[str, float | bool]:
    """Audit the exact gauge-covariant transfer theorem.

    The hypotheses are ``G' >= a S.T G S`` and ``D' <= b S.T D S``.
    """
    g = _symmetric(source_gram, "source gram")
    d = _symmetric(source_tail, "source tail")
    gp = _symmetric(target_gram, "target gram")
    dp = _symmetric(target_tail, "target tail")
    s = np.asarray(gauge, dtype=float)
    if s.shape != g.shape or np.any(~np.isfinite(s)) or abs(np.linalg.det(s)) <= 1e-15:
        raise ValueError("the gauge must be a finite invertible matrix of matching size")
    a = _positive(gram_factor, "gram factor")
    b = float(tail_factor)
    if not math.isfinite(b) or b < 0.0:
        raise ValueError("tail factor must be finite and nonnegative")
    pulled_g = s.T @ g @ s
    pulled_d = s.T @ d @ s
    gram_slack = float(np.linalg.eigvalsh(gp - a * pulled_g)[0])
    tail_slack = float(np.linalg.eigvalsh(b * pulled_d - dp)[0])
    source = relative_gamma(g, d)
    target = relative_gamma(gp, dp)
    bound = transfer_gamma_bound(source, a, b)
    source_volume = frame_volume(g)
    target_volume = frame_volume(gp)
    volume_lower = a ** (g.shape[0] / 2.0) * abs(float(np.linalg.det(s))) * source_volume
    tolerance = 3e-10 * max(1.0, np.linalg.norm(gp, 2), np.linalg.norm(dp, 2))
    return {
        "source_gamma": source,
        "target_gamma": target,
        "gamma_upper": bound,
        "source_volume": source_volume,
        "target_volume": target_volume,
        "target_volume_lower": volume_lower,
        "gram_minimum_slack": gram_slack,
        "tail_minimum_slack": tail_slack,
        "gram_hypothesis_holds": bool(gram_slack >= -tolerance),
        "tail_hypothesis_holds": bool(tail_slack >= -tolerance),
        "gamma_conclusion_holds": bool(target <= bound + tolerance),
        "volume_conclusion_holds": bool(target_volume + tolerance >= volume_lower),
    }
