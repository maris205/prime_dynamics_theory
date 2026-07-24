"""Finite-dimensional outward guards for a directional support candidate."""

from __future__ import annotations

import math

import numpy as np


def _sym(value, name):
    matrix = np.asarray(value, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or np.any(~np.isfinite(matrix)):
        raise ValueError(f"{name} must be a finite square matrix")
    return (matrix + matrix.T) / 2.0


def _nn(value, name):
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def outward_two_residual_certificate(
    source_gram_hat,
    source_tail_hat,
    target_gram_hat,
    target_tail_hat,
    forcing_hat,
    gauge,
    raw_factor,
    source_tail_bound,
    target_tail_bound,
    source_gram_radius,
    source_tail_radius,
    target_gram_radius,
    target_tail_radius,
    forcing_radius,
):
    """Certify raw recurrence and normalized bridge from spectral-norm radii."""
    g = _sym(source_gram_hat, "source gram")
    d = _sym(source_tail_hat, "source tail")
    gp = _sym(target_gram_hat, "target gram")
    dp = _sym(target_tail_hat, "target tail")
    forcing = _sym(forcing_hat, "forcing")
    orthogonal = np.asarray(gauge, dtype=float)
    if orthogonal.shape != g.shape or np.any(~np.isfinite(orthogonal)):
        raise ValueError("gauge has incompatible shape")
    raw = _nn(raw_factor, "raw factor")
    source_bound = _nn(source_tail_bound, "source tail bound")
    target_bound = _nn(target_tail_bound, "target tail bound")
    rg = _nn(source_gram_radius, "source gram radius")
    rd = _nn(source_tail_radius, "source tail radius")
    rgp = _nn(target_gram_radius, "target gram radius")
    rdp = _nn(target_tail_radius, "target tail radius")
    rf = _nn(forcing_radius, "forcing radius")
    norm2 = float(np.linalg.norm(orthogonal, 2)) ** 2
    raw_numeric = float(np.linalg.eigvalsh(raw * orthogonal.T @ d @ orthogonal + forcing - dp)[0])
    raw_guard = raw * norm2 * rd + rf + rdp
    bridge_numeric = float(np.linalg.eigvalsh(target_bound * gp - raw * source_bound * orthogonal.T @ g @ orthogonal - forcing)[0])
    bridge_guard = target_bound * rgp + raw * source_bound * norm2 * rg + rf
    return {
        "raw_numeric_slack": raw_numeric,
        "raw_required_guard": raw_guard,
        "raw_outward_slack": raw_numeric - raw_guard,
        "bridge_numeric_slack": bridge_numeric,
        "bridge_required_guard": bridge_guard,
        "bridge_outward_slack": bridge_numeric - bridge_guard,
        "raw_certified": bool(raw_numeric >= raw_guard),
        "bridge_certified": bool(bridge_numeric >= bridge_guard),
        "both_certified": bool(raw_numeric >= raw_guard and bridge_numeric >= bridge_guard),
    }


def outward_base_lower(gram_hat, gram_radius):
    """Lower-bound sqrt(lambda_min(G)/lambda_max(G)) from a norm enclosure."""
    gram = _sym(gram_hat, "gram")
    radius = _nn(gram_radius, "gram radius")
    values = np.linalg.eigvalsh(gram)
    lower = max(0.0, float(values[0]) - radius)
    upper = float(values[-1]) + radius
    if upper <= 0.0:
        raise ValueError("Gram upper eigenvalue must be positive")
    return math.sqrt(lower / upper)


def directional_lower(tail_squared_upper, normalized_base_lower):
    tail = _nn(tail_squared_upper, "tail squared upper")
    base = _nn(normalized_base_lower, "normalized base lower")
    return max(0.0, 1.0 - math.sqrt(tail)) ** 4 * base
