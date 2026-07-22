from __future__ import annotations

import numpy as np
import pytest

from finite_memory_gram import (
    memory_grams,
    normalized_snapshot,
    normalized_snapshot_action,
    packet_action,
    packet_action_tail_bound,
    projected_cross_from_action,
    tail_trace_bound,
    truncated_memory_gram,
)


def test_snapshot_action_avoids_gram_without_changing_result() -> None:
    state = np.arange(1.0, 21.0).reshape(5, 4)
    packet, _ = np.linalg.qr(np.arange(1.0, 9.0).reshape(4, 2))
    expected = normalized_snapshot(state) @ packet
    assert np.linalg.norm(normalized_snapshot_action(state, packet) - expected) < 1e-14


def test_exact_history_action_and_truncation_identity() -> None:
    rng = np.random.default_rng(101)
    states = [rng.normal(size=(7, 5)) for _ in range(6)]
    packet, _ = np.linalg.qr(rng.normal(size=(5, 3)))
    eta = 0.125
    grams = memory_grams(states, eta)
    exact = packet_action(states, packet, eta=eta, time=5)
    assert np.linalg.norm(exact - grams[5] @ packet) < 1e-14
    depth = 2
    recent = packet_action(states, packet, eta=eta, time=5, depth=depth)
    assert np.linalg.norm(recent - truncated_memory_gram(states, eta=eta, time=5, depth=depth) @ packet) < 1e-14
    remainder = exact - recent
    assert np.linalg.norm(remainder - eta**depth * grams[3] @ packet) < 1e-14
    bound = packet_action_tail_bound(eta, depth, packet.shape[1], past_snapshot_count=4)
    assert np.linalg.norm(remainder, "fro") <= bound


def test_cross_projection_is_nonexpansive() -> None:
    rng = np.random.default_rng(102)
    packet, _ = np.linalg.qr(rng.normal(size=(8, 3)))
    error = rng.normal(size=(8, 3))
    projected = projected_cross_from_action(error, packet)
    assert np.linalg.norm(projected, "fro") <= np.linalg.norm(error, "fro") + 1e-14


def test_tail_bounds_and_validation() -> None:
    eta = 1.0 / 512.0
    assert tail_trace_bound(eta, 4, 0) == 0.0
    assert tail_trace_bound(eta, 4, 10) <= tail_trace_bound(eta, 4)
    with pytest.raises(ValueError):
        tail_trace_bound(1.0, 2)
    with pytest.raises(ValueError):
        packet_action([], np.eye(2), eta=eta)
    with pytest.raises(ValueError):
        normalized_snapshot(np.zeros((2, 2)))
