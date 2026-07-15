from __future__ import annotations

import numpy as np

from primal_dual_certificate import (
    exact_identity_residual,
    primal_dual_correction,
    primal_dual_correction_from_residuals,
    resolvent_budget,
)


def random_problem(seed: int = 17):
    rng = np.random.default_rng(seed)
    ambient = 9
    rank = 3
    shifted = np.eye(ambient) + 0.08 * (
        rng.normal(size=(ambient, ambient))
        + 1.0j * rng.normal(size=(ambient, ambient))
    )
    observation = rng.normal(size=(rank, ambient)) / 4.0
    observation = observation + 0.2j * rng.normal(size=(rank, ambient))
    base = np.eye(rank) + 0.05 * rng.normal(size=(rank, rank))
    rhs = rng.normal(size=(ambient, rank))
    primal = rng.normal(size=(ambient, rank)) / 3.0
    dual = rng.normal(size=(ambient, rank)) / 3.0
    return shifted, observation, base, rhs, primal, dual


def test_exact_primal_dual_identity() -> None:
    problem = random_problem()
    result = primal_dual_correction(*problem)
    assert exact_identity_residual(problem[0], problem[1], problem[3], result) < 3e-15


def test_exact_dual_kills_remainder() -> None:
    shifted, observation, base, rhs, primal, _ = random_problem(29)
    exact_dual = np.linalg.solve(shifted.conj().T, observation.conj().T)
    result = primal_dual_correction(
        shifted, observation, base, rhs, primal, exact_dual
    )
    assert np.linalg.norm(result.dual_residual) < 2e-15
    assert result.primal_dual_resolvent_coefficient < 2e-14
    exact = -observation @ np.linalg.solve(shifted, rhs)
    assert np.linalg.norm(result.computed_correction - exact) < 5e-15


def test_exact_primal_has_infinite_resolvent_budgets() -> None:
    shifted, observation, base, rhs, _, dual = random_problem(41)
    rhs *= 1.0e-3
    exact_primal = np.linalg.solve(shifted, rhs)
    result = primal_dual_correction(
        shifted, observation, base, rhs, exact_primal, dual
    )
    assert np.linalg.norm(result.primal_residual) < 3e-15
    assert result.one_sided_resolvent_budget > 1e13
    assert result.primal_dual_resolvent_budget > 1e13


def test_budget_edge_cases() -> None:
    assert resolvent_budget(0.2, 0.1) == 8.0
    assert np.isinf(resolvent_budget(0.2, 0.0))
    assert resolvent_budget(1.0, 0.1) == 0.0
    assert resolvent_budget(1.3, 0.1) == 0.0


def test_primal_dual_coefficient_bounds_exact_remainder() -> None:
    shifted, observation, base, rhs, primal, dual = random_problem(53)
    result = primal_dual_correction(
        shifted, observation, base, rhs, primal, dual
    )
    remainder = -result.dual_residual.conj().T @ np.linalg.solve(
        shifted, result.primal_residual
    )
    relative = np.linalg.norm(np.linalg.solve(base, remainder), 2)
    majorant = (
        result.primal_dual_resolvent_coefficient
        * np.linalg.norm(np.linalg.inv(shifted), 2)
    )
    assert relative <= majorant * (1.0 + 3e-14)


def test_matrix_free_residual_interface_matches_dense_interface() -> None:
    shifted, observation, base, rhs, primal, dual = random_problem(67)
    dense = primal_dual_correction(
        shifted, observation, base, rhs, primal, dual
    )
    residual = rhs - shifted @ primal
    dual_residual = observation.conj().T - shifted.conj().T @ dual
    matrix_free = primal_dual_correction_from_residuals(
        observation,
        base,
        primal,
        residual,
        dual,
        dual_residual,
    )
    assert np.linalg.norm(
        dense.computed_correction - matrix_free.computed_correction
    ) < 2e-15
    assert abs(
        dense.primal_dual_resolvent_coefficient
        - matrix_free.primal_dual_resolvent_coefficient
    ) < 2e-15


def test_inverse_information_no_go_example() -> None:
    first = np.asarray((1.0, 0.0), dtype=np.complex128)
    for epsilon in (1.0e-2, 1.0e-5, 1.0e-8):
        shifted = np.diag((epsilon, 1.0)).astype(np.complex128)
        remainder = np.vdot(first, np.linalg.solve(shifted, first))
        assert np.linalg.norm(shifted, 2) == 1.0
        assert abs(remainder - 1.0 / epsilon) < 1.0e-12 / epsilon
