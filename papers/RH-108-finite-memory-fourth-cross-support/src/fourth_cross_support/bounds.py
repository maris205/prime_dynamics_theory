"""Weyl support bounds and an exact normalized-memory barrier family."""

from __future__ import annotations

import math

import numpy as np


def _eta(value: float) -> float:
    eta = float(value)
    if not math.isfinite(eta) or eta < 0.0 or eta >= 1.0:
        raise ValueError("eta must lie in [0, 1)")
    return eta


def _nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def _singular_values(values: list[float] | tuple[float, ...] | np.ndarray) -> np.ndarray:
    singular = np.asarray(values, dtype=float)
    if singular.ndim != 1 or singular.size < 4 or np.any(~np.isfinite(singular)) or np.any(singular < 0.0):
        raise ValueError("at least four finite nonnegative singular values are required")
    singular = np.sort(singular)[::-1]
    if singular[0] <= 0.0:
        raise ValueError("the leading singular value must be positive")
    return singular


def finite_tail_operator_bound(
    eta: float,
    depth: int,
    past_snapshot_count: int | None = None,
) -> float:
    """Trace/operator bound for the positive tail eta^m G_{t-m}."""
    decay = _eta(eta)
    memory = int(depth)
    if memory <= 0:
        raise ValueError("depth must be positive")
    if past_snapshot_count is None:
        value = decay**memory / (1.0 - decay)
    else:
        count = int(past_snapshot_count)
        if count < 0:
            raise ValueError("past snapshot count must be nonnegative")
        if count == 0:
            return 0.0
        value = decay**memory * (1.0 - decay**count) / (1.0 - decay)
    return math.nextafter(value, math.inf)


def weyl_ratio_lower_bound(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    tail_operator_bound: float,
) -> float:
    """Lower-bound s_4(K)/s_1(K) from a recent cross and an operator error."""
    singular = _singular_values(recent_singular_values)
    delta = _nonnegative(tail_operator_bound, "tail operator bound")
    numerator = max(0.0, math.nextafter(float(singular[3]) - delta, -math.inf))
    denominator = math.nextafter(float(singular[0]) + delta, math.inf)
    if numerator == 0.0:
        return 0.0
    return max(0.0, math.nextafter(numerator / denominator, -math.inf))


def support_margin(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    tail_operator_bound: float,
    threshold: float,
) -> float:
    """Return shat_4 - tau shat_1 - (1+tau) delta."""
    singular = _singular_values(recent_singular_values)
    delta = _nonnegative(tail_operator_bound, "tail operator bound")
    cutoff = float(threshold)
    if not math.isfinite(cutoff) or cutoff <= 0.0:
        raise ValueError("threshold must be finite and positive")
    value = float(singular[3]) - cutoff * float(singular[0]) - (1.0 + cutoff) * delta
    return math.nextafter(value, -math.inf)


def fourth_support_certificate(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    tail_operator_bound: float,
    threshold: float,
) -> dict[str, float | bool]:
    """Package the fourth-mode ratio lower bound and support decision."""
    singular = _singular_values(recent_singular_values)
    cutoff = float(threshold)
    lower = weyl_ratio_lower_bound(singular, tail_operator_bound)
    margin = support_margin(singular, tail_operator_bound, cutoff)
    return {
        "recent_leading_singular_value": float(singular[0]),
        "recent_fourth_singular_value": float(singular[3]),
        "tail_operator_bound": float(tail_operator_bound),
        "ratio_lower_bound": lower,
        "additive_support_margin": margin,
        "support_certified": bool(margin >= 0.0 and lower >= cutoff),
    }


def normalized_gram(state: np.ndarray) -> np.ndarray:
    values = np.asarray(state, dtype=float)
    if values.ndim != 2 or values.size == 0:
        raise ValueError("state must be a nonempty matrix")
    gram = values.T @ values
    scale = float(np.trace(gram))
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("state must have positive Frobenius norm")
    gram = gram / scale
    return (gram + gram.T) / 2.0


def barrier_snapshot(epsilon: float) -> np.ndarray:
    """Return X_e with trace-normalized cross singulars (4,3,2,e)/34."""
    value = float(epsilon)
    if not math.isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError("epsilon must lie in [0, 1]")
    state = np.zeros((5, 8), dtype=float)
    state[0, 0], state[0, 4] = 1.0, 4.0
    state[1, 1], state[1, 5] = 1.0, 3.0
    state[2, 2], state[2, 6] = 1.0, 2.0
    state[3, 3], state[3, 7] = 1.0, value
    state[4, 7] = math.sqrt(max(0.0, 1.0 - value * value))
    return state


def source_seed_gram() -> np.ndarray:
    """A trace-one source Gramian whose unique top rank-four packet is V."""
    return np.diag([2.0] * 4 + [1.0] * 4) / 12.0


def source_seeded_barrier_data(epsilon: float, eta: float = 1.0 / 512.0) -> dict[str, np.ndarray | float]:
    """Build the one-update source-seeded memory barrier exactly."""
    decay = _eta(eta)
    value = float(epsilon)
    snapshot = normalized_gram(barrier_snapshot(value))
    source = source_seed_gram()
    gram = snapshot + decay * source
    packet = np.eye(8, 4)
    complement = np.eye(8)[:, 4:]
    cross = gram @ packet - packet @ (packet.T @ gram @ packet)
    singular = np.linalg.svd(cross, compute_uv=False)
    return {
        "snapshot": snapshot,
        "source_gram": source,
        "memory_gram": gram,
        "packet": packet,
        "complement": complement,
        "cross": cross,
        "singular_values": singular,
        "ratio": float(singular[3] / singular[0]),
        "packet_block": packet.T @ gram @ packet,
        "complement_block": complement.T @ gram @ complement,
        "trace_clock": float(np.trace(gram)),
        "operator_norm": float(np.linalg.norm(gram, 2)),
    }
