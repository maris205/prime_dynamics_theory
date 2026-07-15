from __future__ import annotations

import numpy as np

from physical_feshbach import (
    bright_history_trial,
    critical_bright_trial,
    dense_feshbach_data,
    eigenmode_closure,
    external_project,
    label_resolved_trial,
    packet_project,
    single_label_trial,
)


def random_pair(seed: int = 4) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    trial = rng.normal(size=(7, 3))
    test_raw = rng.normal(size=(7, 3))
    gram = test_raw.T @ trial
    test = np.linalg.solve(gram, test_raw.T)
    return trial, test


def test_packet_and_external_are_complementary_projectors() -> None:
    trial, test = random_pair()
    rng = np.random.default_rng(8)
    values = rng.normal(size=(7, 2))
    packet = packet_project(values, trial, test)
    external = external_project(values, trial, test)
    assert np.linalg.norm(packet + external - values) < 2.0e-14
    assert np.linalg.norm(packet_project(packet, trial, test) - packet) < 2.0e-14
    assert np.linalg.norm(packet_project(external, trial, test)) < 2.0e-14


def test_dense_feshbach_determinant_identity() -> None:
    trial, test = random_pair()
    rng = np.random.default_rng(9)
    matrix = rng.normal(size=(7, 7)) / 5.0
    data = dense_feshbach_data(matrix, trial, test, 0.43 + 0.27j)
    assert data.determinant_residual < 2.0e-13
    compressed_resolvent = test @ np.linalg.solve(
        (0.43 + 0.27j) * np.eye(7) - matrix,
        trial,
    )
    assert np.linalg.norm(compressed_resolvent - np.linalg.inv(data.feshbach)) < 3.0e-12


def test_eigenmode_block_closure_is_exact() -> None:
    trial, test = random_pair()
    rng = np.random.default_rng(11)
    matrix = rng.normal(size=(7, 7)) / 4.0
    values, vectors = np.linalg.eig(matrix)
    index = int(np.argmax(np.abs(values)))
    closure = eigenmode_closure(
        lambda vector: matrix @ vector,
        trial,
        test,
        values[index],
        vectors[:, index],
    )
    assert closure.packet_closure_residual < 2.0e-13
    assert closure.external_equation_residual < 2.0e-13
    assert closure.resolvent_lower_bound > 0.0
    packet = trial @ test
    external = np.eye(7) - packet
    external_operator = (
        values[index] * np.eye(7) - external @ matrix @ external
    )
    inverse_norm = np.linalg.norm(np.linalg.inv(external_operator), ord=2)
    assert closure.resolvent_lower_bound <= inverse_norm * (1.0 + 2.0e-13)


def test_eigenmode_closure_is_packet_gauge_covariant() -> None:
    trial, test = random_pair()
    rng = np.random.default_rng(13)
    matrix = rng.normal(size=(7, 7)) / 6.0
    values, vectors = np.linalg.eig(matrix)
    index = 2
    first = eigenmode_closure(
        lambda vector: matrix @ vector,
        trial,
        test,
        values[index],
        vectors[:, index],
    )
    gauge = np.asarray(((1.2, 0.1, -0.2), (0.3, 0.9, 0.1), (0.0, -0.2, 1.1)))
    second = eigenmode_closure(
        lambda vector: matrix @ vector,
        trial @ gauge,
        np.linalg.solve(gauge, test),
        values[index],
        vectors[:, index],
    )
    assert np.linalg.norm(first.packet_component - second.packet_component) < 3.0e-14
    assert np.linalg.norm(first.external_component - second.external_component) < 3.0e-14
    assert abs(first.resolvent_lower_bound - second.resolvent_lower_bound) < 3.0e-13


def test_bright_history_trial_retains_two_critical_columns() -> None:
    first = np.asarray(((1.0, 0.9), (0.2, 0.1), (0.0, 0.0), (0.0, 0.0)))
    critical = np.asarray(((0.0, 0.0), (0.0, 0.0), (0.8, 0.0), (0.0, 0.6)))
    trial = bright_history_trial((first, critical))
    assert trial.shape == (4, 3)
    assert abs(np.linalg.norm(trial[:, 0]) - 1.0) < 2.0e-15
    assert np.vdot(trial[:, 1], trial[:, 2]) == 0.0


def test_packet_trial_variants_have_expected_ranks() -> None:
    regular = np.asarray(
        ((1.0, 0.8), (0.2, 0.1), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0))
    )
    middle = np.asarray(
        ((0.0, 0.0), (0.0, 0.0), (0.9, 0.7), (0.1, 0.2), (0.0, 0.0), (0.0, 0.0))
    )
    critical = np.asarray(
        ((0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.6, 0.0), (0.0, 0.5))
    )
    histories = (regular, middle, critical)
    assert bright_history_trial(histories).shape == (6, 4)
    assert critical_bright_trial(histories).shape == (6, 3)
    assert label_resolved_trial(histories).shape == (6, 6)
    assert single_label_trial(histories, 0).shape == (6, 3)
    assert single_label_trial(histories, 1).shape == (6, 3)
