from __future__ import annotations

from types import SimpleNamespace

import numpy as np

from directional_rouche import (
    circular_lipschitz_lower_bound,
    determinant_winding,
    exact_directional_correction,
    fom_external_solution,
    geometric_tail_majorant,
    global_scalar_majorant,
    matrix_rouche_ratio,
)


def test_exact_directional_correction_identity() -> None:
    rng = np.random.default_rng(12)
    ambient = 8
    rank = 3
    external = rng.normal(size=(ambient, ambient)) / 9.0
    reduced = rng.normal(size=(rank, rank)) / 7.0
    forcing = rng.normal(size=(ambient, rank))
    observation = rng.normal(size=(rank, ambient)) / 5.0
    approximate = rng.normal(size=(ambient, rank)) / 4.0
    result = exact_directional_correction(
        external,
        reduced,
        forcing,
        observation,
        approximate,
        0.81 + 0.27j,
    )
    assert result.identity_residual < 3.0e-15
    assert np.linalg.norm(
        result.corrected_feshbach
        - result.approximate_feshbach
        - result.feshbach_perturbation
    ) < 2.0e-15
    assert result.rouche_ratio >= 0.0


def test_global_scalar_majorant_dominates_directional_norm() -> None:
    rng = np.random.default_rng(23)
    base = np.eye(2) + 0.1 * rng.normal(size=(2, 2))
    observation = rng.normal(size=(2, 5))
    inverse = rng.normal(size=(5, 5)) / 4.0
    residual = rng.normal(size=(5, 2)) / 20.0
    perturbation = observation @ inverse @ residual
    directional = matrix_rouche_ratio(base, perturbation)
    majorant = global_scalar_majorant(
        np.linalg.norm(np.linalg.inv(base), 2),
        np.linalg.norm(observation, 2),
        np.linalg.norm(inverse, 2),
        np.linalg.norm(residual, 2),
    )
    assert directional <= majorant * (1.0 + 2.0e-14)


def test_geometric_tail_majorant_has_stated_sum() -> None:
    tail = geometric_tail_majorant(0.2, 0.05)
    assert tail.admissible
    assert abs(tail.contraction_ratio - 0.25) < 2.0e-15
    expected = 0.2 + sum(0.05 * 0.25**index for index in range(20))
    assert abs(tail.total_from_base - expected) < 2.0e-13
    assert not geometric_tail_majorant(0.1, 0.11).admissible


def test_circle_lipschitz_bound_is_valid_for_scalar_shift() -> None:
    center = 0.3 - 0.2j
    radius = 0.7
    pole = 1.15 - 0.2j
    nodes = 1024
    theta = 2.0 * np.pi * np.arange(nodes) / nodes
    points = center + radius * np.exp(1.0j * theta)
    samples = np.abs(points - pole)
    lower = circular_lipschitz_lower_bound(samples, radius)
    exact = abs(abs(pole - center) - radius)
    assert 0.0 < lower <= exact
    assert exact - lower < 3.0e-3


def test_determinant_winding_counts_one_root() -> None:
    theta = 2.0 * np.pi * np.arange(128) / 128
    values = np.exp(1.0j * theta) - 0.2
    floating, integer, maximum_step = determinant_winding(np.angle(values))
    assert abs(floating - 1.0) < 2.0e-14
    assert integer == 1
    assert maximum_step < 0.1


def test_fom_solution_reconstruction() -> None:
    first_basis = np.eye(5, 3, dtype=np.complex128)
    second_basis = np.roll(first_basis, 1, axis=0)
    first_hbar = np.zeros((4, 3), dtype=np.complex128)
    second_hbar = np.zeros((4, 3), dtype=np.complex128)
    first_hbar[:3, :3] = np.diag((0.1, 0.2, 0.3))
    second_hbar[:3, :3] = np.diag((-0.1, -0.2, -0.3))
    model = SimpleNamespace(
        retained_bases=(first_basis, second_basis),
        hessenbergs=(first_hbar, second_hbar),
        forcing_norms=np.asarray((2.0, 3.0)),
        packet_rank=2,
        maximum_depth=3,
    )
    solution = fom_external_solution(model, 0.8 + 0.1j, depth=3)
    expected_first = first_basis[:, 0] * 2.0 / (0.7 + 0.1j)
    expected_second = second_basis[:, 0] * 3.0 / (0.9 + 0.1j)
    assert np.linalg.norm(solution[:, 0] - expected_first) < 2.0e-15
    assert np.linalg.norm(solution[:, 1] - expected_second) < 2.0e-15
