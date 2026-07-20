from __future__ import annotations

import numpy as np
from scipy.linalg import solve_discrete_lyapunov

from hardy_tail import (
    adaptive_cutoff_multiple,
    cutoff_bound,
    deterministic_hardy_certificate,
    deterministic_main_sum,
    finite_horizon_perturbation_bound,
    full_energy_squared_perturbation_upper,
    semigroup_power_defect_upper,
    transfer_block_contraction_from_ledgers,
)


def stable_pair(seed: int = 5301):
    rng = np.random.default_rng(seed)
    operator = rng.normal(size=(7, 7)) / 4.0
    operator *= 0.61 / max(abs(np.linalg.eigvals(operator)))
    source = rng.normal(size=(7, 3))
    observation = rng.normal(size=(4, 7))
    return operator, source, observation


def exact_energy_squared(operator, source, observation):
    gramian = solve_discrete_lyapunov(operator, source @ source.T)
    return float(np.trace(observation @ gramian @ observation.T).real)


def test_deterministic_main_sum_is_the_finite_trace_identity() -> None:
    operator, source, observation = stable_pair()
    horizon = 9
    state = source.copy()
    direct = 0.0
    for _ in range(horizon):
        direct += float(np.trace(observation @ state @ state.T @ observation.T))
        state = operator @ state
    assert abs(
        deterministic_main_sum(operator, source, observation, horizon) - direct
    ) < 2.0e-12


def test_block_tail_certificate_dominates_the_infinite_energy() -> None:
    operator, source, observation = stable_pair(5302)
    certificate = deterministic_hardy_certificate(
        operator, source, observation, 12
    )
    exact = exact_energy_squared(operator, source, observation)
    assert certificate.block_power_norm < 1.0
    assert certificate.energy_squared_upper >= exact - 2.0e-10
    assert certificate.main_energy_squared <= exact + 2.0e-10
    assert certificate.simple_tail_upper >= 0.0
    assert certificate.stein_tail_upper >= 0.0


def test_finite_horizon_perturbation_bound_contains_actual_difference() -> None:
    operator, source, observation = stable_pair(5303)
    rng = np.random.default_rng(5304)
    perturbed_operator = operator + 2.0e-4 * rng.normal(size=operator.shape)
    perturbed_source = source + 3.0e-4 * rng.normal(size=source.shape)
    perturbed_observation = observation + 4.0e-4 * rng.normal(
        size=observation.shape
    )
    horizon = 8
    bound = finite_horizon_perturbation_bound(
        operator,
        source,
        observation,
        perturbed_operator,
        perturbed_source,
        perturbed_observation,
        horizon,
    )
    actual = abs(
        deterministic_main_sum(operator, source, observation, horizon)
        - deterministic_main_sum(
            perturbed_operator,
            perturbed_source,
            perturbed_observation,
            horizon,
        )
    )
    assert actual <= bound.energy_squared_difference_upper + 1.0e-11


def test_semigroup_ledger_transfers_a_block_contraction() -> None:
    operator, _, _ = stable_pair(5305)
    perturbed = operator + 1.0e-5 * np.eye(operator.shape[0])
    horizon = 7
    identity = np.eye(operator.shape[0])
    powers = [identity]
    perturbed_powers = [identity]
    for _ in range(horizon):
        powers.append(operator @ powers[-1])
        perturbed_powers.append(perturbed @ perturbed_powers[-1])
    left = [float(np.linalg.norm(value, 2)) for value in powers]
    right = [float(np.linalg.norm(value, 2)) for value in perturbed_powers]
    defect = float(np.linalg.norm(operator - perturbed, 2))
    power_defect = semigroup_power_defect_upper(
        left, right, defect, horizon
    )
    actual = float(np.linalg.norm(powers[horizon] - perturbed_powers[horizon], 2))
    transferred = transfer_block_contraction_from_ledgers(
        left[horizon], left, right, defect, horizon
    )
    assert actual <= power_defect + 1.0e-12
    assert float(np.linalg.norm(perturbed_powers[horizon], 2)) <= transferred + 1.0e-12


def test_full_energy_difference_adds_both_available_tail_budgets() -> None:
    assert full_energy_squared_perturbation_upper(0.2, 0.03, 0.05) == 0.28


def test_adaptive_cutoff_has_second_order_scale() -> None:
    ratios = []
    for dimension in (2048, 4096, 8192, 16384):
        multiple = adaptive_cutoff_multiple(1.0 / dimension)
        bound = cutoff_bound(dimension, 0.01, multiple)
        ratios.append(bound.two_norm_upper / (1.0 / dimension) ** 2)
    assert max(ratios) / min(ratios) < 1.5
    assert adaptive_cutoff_multiple(1.0 / 40960) < 8.0


def test_fixed_eight_sigma_bound_does_not_encode_asymptotic_convergence() -> None:
    values = [
        cutoff_bound(dimension, 0.01, 8.0).two_norm_upper
        for dimension in (2048, 4096, 8192)
    ]
    assert values[0] < values[1] < values[2]
