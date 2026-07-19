from __future__ import annotations

import numpy as np

from two_pole_hardy import (
    controllability_gramian,
    hardy_energy,
    hardy_resolvent_upper,
    lyapunov_supersolution_certificate,
    observability_gramian,
    two_pole_bulk_matrix,
)


def test_two_pole_deflation_removes_both_eigenchannels() -> None:
    rng = np.random.default_rng(5001)
    basis = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    inverse = np.linalg.inv(basis)
    values = np.asarray((1.0, -0.94, 0.63, -0.52, 0.31, -0.2, 0.1j, -0.1j))
    operator = basis @ np.diag(values) @ inverse
    right = basis[:, :2]
    left = np.conjugate(inverse[:2, :].T)
    bulk, projection, corrected_left = two_pole_bulk_matrix(
        operator, right, left, values[:2]
    )
    assert np.linalg.norm(projection @ projection - projection) < 3.0e-12
    assert np.linalg.norm(corrected_left.conjugate().T @ right - np.eye(2)) < 3.0e-12
    assert np.linalg.norm(bulk @ right) < 5.0e-12


def test_hardy_energy_bounds_every_resolvent_node() -> None:
    rng = np.random.default_rng(5002)
    operator = rng.normal(size=(7, 7)) / 8.0
    operator *= 0.55 / max(abs(np.linalg.eigvals(operator)))
    source = rng.normal(size=(7, 3))
    radius = 0.72
    sequence = []
    state = source.copy()
    for _ in range(180):
        sequence.append(np.linalg.norm(state, "fro"))
        state = operator @ state
    energy = hardy_energy(sequence, radius)
    for theta in np.linspace(0.0, 2.0 * np.pi, 31, endpoint=False):
        z = 0.9 * np.exp(1j * theta)
        exact = np.linalg.solve(z * np.eye(7) - operator, source)
        upper = hardy_resolvent_upper(energy, radius, abs(z))
        assert np.linalg.norm(exact, "fro") <= (
            upper.resolvent_action_upper * (1.0 + 2.0e-12)
        )


def test_stein_gramians_equal_weighted_power_energies() -> None:
    rng = np.random.default_rng(5003)
    operator = rng.normal(size=(6, 6)) / 10.0
    operator *= 0.5 / max(abs(np.linalg.eigvals(operator)))
    source = rng.normal(size=(6, 2))
    observation = rng.normal(size=(3, 6))
    radius = 0.75
    controllability = controllability_gramian(operator, source, radius)
    observability = observability_gramian(operator, observation, radius)
    state = source.copy()
    left_sum = 0.0
    right_state = np.eye(6)
    right_sum = 0.0
    for power in range(250):
        left_sum += np.linalg.norm(state, "fro") ** 2 / radius ** (2 * power)
        right_sum += np.linalg.norm(observation @ right_state, "fro") ** 2 / radius ** (2 * power)
        state = operator @ state
        right_state = operator @ right_state
    assert np.isclose(np.trace(controllability).real, left_sum, rtol=2.0e-11)
    assert np.isclose(np.trace(observability).real, right_sum, rtol=2.0e-11)


def test_exact_gramian_is_an_admissible_lyapunov_supersolution() -> None:
    rng = np.random.default_rng(5004)
    operator = rng.normal(size=(5, 5)) / 12.0
    operator *= 0.45 / max(abs(np.linalg.eigvals(operator)))
    source = rng.normal(size=(5, 2))
    radius = 0.7
    gramian = controllability_gramian(operator, source, radius)
    certificate = lyapunov_supersolution_certificate(
        operator, source, gramian + 1.0e-10 * np.eye(5), radius
    )
    assert certificate.admissible
    assert certificate.residual_minimum_eigenvalue > -1.0e-11
    assert certificate.trace_upper >= np.trace(gramian).real
