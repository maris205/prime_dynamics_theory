import numpy as np
import pytest

from lag_reset_bridge import (
    centered_action_radius,
    choose_adaptive_candidate,
    path_overlap_lower,
    singular_interval,
)


def top_projector(matrix: np.ndarray, rank: int) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2.0)
    frame = vectors[:, np.argsort(values)[::-1][:rank]]
    return frame @ frame.T


def cross(matrix: np.ndarray, projector: np.ndarray) -> np.ndarray:
    return (np.eye(matrix.shape[0]) - projector) @ matrix @ projector


def test_scalar_centered_projector_bound() -> None:
    matrix = np.diag([4.0, 2.0, 1.0, -1.0])
    projector = np.diag([1.0, 1.0, 0.0, 0.0])
    theta = 0.03
    rotation = np.eye(4)
    rotation[[1, 1, 2, 2], [1, 2, 1, 2]] = [np.cos(theta), -np.sin(theta), np.sin(theta), np.cos(theta)]
    moved = rotation @ projector @ rotation.T
    epsilon = float(np.linalg.norm(moved - projector, 2))
    spread = float(np.linalg.eigvalsh(matrix)[-1] - np.linalg.eigvalsh(matrix)[0])
    error = float(np.linalg.norm(cross(matrix, moved) - cross(matrix, projector), 2))
    assert error <= centered_action_radius(0.0, spread, epsilon) * (1.0 + 1e-12)


def test_lagged_innovation_identity() -> None:
    rng = np.random.default_rng(4)
    eta = 0.3
    snapshots = []
    for _ in range(5):
        values = rng.normal(size=(5, 3))
        snapshots.append(values @ values.T)
    memory = [snapshots[0]]
    for snapshot in snapshots[1:]:
        memory.append(snapshot + eta * memory[-1])
    target, lag, depth = 4, 2, 3
    projector = top_projector(memory[target - lag], 2)
    tail = eta**depth * memory[target - depth]
    recent = memory[target] - tail
    innovation = sum(eta**age * snapshots[target - age] for age in range(lag))
    assert np.allclose(cross(recent, projector), cross(innovation, projector) - cross(tail, projector))


def test_singular_interval_and_path_product() -> None:
    assert singular_interval(0.5, 0.2) == pytest.approx((0.3, 0.7))
    assert singular_interval(0.1, 0.2)[0] == 0.0
    assert path_overlap_lower([0.5, 0.25, 0.8]) == pytest.approx(0.1)


def test_adaptive_tie_breaks_toward_short_lag() -> None:
    selected = choose_adaptive_candidate([
        {"lag": 3, "normalized_base_lower": 0.2},
        {"lag": 1, "normalized_base_lower": 0.2},
        {"lag": 2, "normalized_base_lower": 0.1},
    ])
    assert selected["lag"] == 1


def test_invalid_bounds() -> None:
    with pytest.raises(ValueError):
        centered_action_radius(0.0, 1.0, 1.1)
    with pytest.raises(ValueError):
        path_overlap_lower([0.5, -0.1])
    with pytest.raises(ValueError):
        choose_adaptive_candidate([])
