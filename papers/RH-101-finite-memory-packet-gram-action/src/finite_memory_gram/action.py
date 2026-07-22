"""Matrix-free finite-memory actions for normalized Gram recursions."""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np


def _validated_eta(eta: float) -> float:
    value = float(eta)
    if not math.isfinite(value) or value < 0.0 or value >= 1.0:
        raise ValueError("eta must lie in [0, 1)")
    return value


def _validated_state(state: np.ndarray) -> np.ndarray:
    values = np.asarray(state, dtype=float)
    if values.ndim != 2 or values.size == 0:
        raise ValueError("state must be a nonempty matrix")
    scale = float(np.linalg.norm(values, "fro") ** 2)
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("state must have positive Frobenius norm")
    return values


def normalized_snapshot(state: np.ndarray) -> np.ndarray:
    """Return X*X / ||X||_F^2; intended for audits, not production."""
    values = _validated_state(state)
    scale = float(np.linalg.norm(values, "fro") ** 2)
    gram = values.T @ values / scale
    return (gram + gram.T) / 2.0


def normalized_snapshot_action(state: np.ndarray, packet: np.ndarray) -> np.ndarray:
    """Apply X*X / ||X||_F^2 to a packet without forming X*X."""
    values = _validated_state(state)
    trial = np.asarray(packet, dtype=float)
    if trial.ndim != 2 or trial.shape[0] != values.shape[1] or trial.shape[1] == 0:
        raise ValueError("state and packet have incompatible shapes")
    scale = float(np.linalg.norm(values, "fro") ** 2)
    return values.T @ (values @ trial) / scale


def memory_grams(states: Sequence[np.ndarray], eta: float) -> list[np.ndarray]:
    """Assemble the recursion for independent audit comparisons."""
    if not states:
        raise ValueError("at least one state is required")
    decay = _validated_eta(eta)
    first = _validated_state(states[0])
    width = first.shape[1]
    memory = np.zeros((width, width), dtype=float)
    output: list[np.ndarray] = []
    for state in states:
        values = _validated_state(state)
        if values.shape[1] != width:
            raise ValueError("all states must have the same coordinate width")
        memory = normalized_snapshot(values) + decay * memory
        output.append((memory + memory.T) / 2.0)
    return output


def packet_action(
    states: Sequence[np.ndarray],
    packet: np.ndarray,
    *,
    eta: float,
    time: int | None = None,
    depth: int | None = None,
) -> np.ndarray:
    """Apply a full or truncated normalized memory Gramian to ``packet``.

    ``depth=None`` uses the complete available history and is exact for a
    recursion initialized by G_{-1}=0.  A positive integer depth uses only
    the newest snapshots and drops the older eta-tail.
    """
    if not states:
        raise ValueError("at least one state is required")
    decay = _validated_eta(eta)
    endpoint = len(states) - 1 if time is None else int(time)
    if endpoint < 0 or endpoint >= len(states):
        raise ValueError("time is outside the available history")
    requested = endpoint + 1 if depth is None else int(depth)
    if requested <= 0:
        raise ValueError("depth must be positive")
    used = min(requested, endpoint + 1)
    trial = np.asarray(packet, dtype=float)
    first = _validated_state(states[endpoint])
    if trial.ndim != 2 or trial.shape[0] != first.shape[1] or trial.shape[1] == 0:
        raise ValueError("state and packet have incompatible shapes")
    action = np.zeros_like(trial, dtype=float)
    for age in range(used):
        action += decay**age * normalized_snapshot_action(states[endpoint - age], trial)
    return action


def truncated_memory_gram(
    states: Sequence[np.ndarray], *, eta: float, time: int | None = None, depth: int
) -> np.ndarray:
    """Assemble the recent-history sum for audit diagnostics."""
    if not states:
        raise ValueError("at least one state is required")
    endpoint = len(states) - 1 if time is None else int(time)
    if endpoint < 0 or endpoint >= len(states):
        raise ValueError("time is outside the available history")
    requested = int(depth)
    if requested <= 0:
        raise ValueError("depth must be positive")
    decay = _validated_eta(eta)
    used = min(requested, endpoint + 1)
    width = _validated_state(states[endpoint]).shape[1]
    memory = np.zeros((width, width), dtype=float)
    for age in range(used):
        memory += decay**age * normalized_snapshot(states[endpoint - age])
    return (memory + memory.T) / 2.0


def tail_trace_bound(eta: float, depth: int, past_snapshot_count: int | None = None) -> float:
    """Bound the trace of the discarded positive eta-tail."""
    decay = _validated_eta(eta)
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


def packet_action_tail_bound(
    eta: float,
    depth: int,
    packet_rank: int,
    past_snapshot_count: int | None = None,
) -> float:
    """Uniform Frobenius bound for the discarded action on an isometry."""
    rank = int(packet_rank)
    if rank <= 0:
        raise ValueError("packet rank must be positive")
    value = tail_trace_bound(eta, depth, past_snapshot_count) * math.sqrt(rank)
    return math.nextafter(value, math.inf)


def projected_cross_from_action(action: np.ndarray, packet: np.ndarray) -> np.ndarray:
    """Return (I-VV*)GV from an already computed action GV."""
    applied = np.asarray(action, dtype=float)
    trial = np.asarray(packet, dtype=float)
    if applied.ndim != 2 or trial.ndim != 2 or applied.shape != trial.shape:
        raise ValueError("action and packet must have the same shape")
    return applied - trial @ (trial.T @ applied)
