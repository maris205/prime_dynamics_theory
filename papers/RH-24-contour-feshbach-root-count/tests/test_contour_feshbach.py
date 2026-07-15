from __future__ import annotations

import numpy as np

from contour_feshbach import (
    BatchedArnoldiFeshbach,
    build_batched_arnoldi_feshbach,
    circle_contour_audit,
    determinant_newton_root,
    sampled_rouche_audit,
)


def random_arnoldi_model(seed: int = 17):
    rng = np.random.default_rng(seed)
    ambient = 28
    rank = 2
    external = rng.normal(size=(ambient, ambient)) / 13.0
    observation = rng.normal(size=(rank, ambient)) / 7.0
    forcing = rng.normal(size=(ambient, rank))
    reduced = rng.normal(size=(rank, rank)) / 6.0

    def action(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        return external @ values, observation @ values

    model = build_batched_arnoldi_feshbach(
        action,
        forcing,
        reduced,
        steps=7,
        retain_bases=True,
    )
    return model, external, observation, forcing


def test_batched_arnoldi_evaluation_has_exact_projected_residual() -> None:
    model, external, observation, forcing = random_arnoldi_model()
    zeta = 0.71 + 0.29j
    depth = 6
    evaluation = model.evaluate(zeta, depth=depth)
    approximate = np.empty_like(forcing, dtype=np.complex128)
    for column in range(model.packet_rank):
        basis = model.retained_bases[column][:, :depth]
        hessenberg = model.hessenbergs[column][:depth, :depth]
        right_hand_side = np.zeros(depth, dtype=np.complex128)
        right_hand_side[0] = model.forcing_norms[column]
        coordinates = np.linalg.solve(
            zeta * np.eye(depth) - hessenberg,
            right_hand_side,
        )
        approximate[:, column] = basis @ coordinates
    residual = (zeta * np.eye(external.shape[0]) - external) @ approximate - forcing
    exact_relative_columns = np.linalg.norm(residual, axis=0) / np.linalg.norm(
        forcing, axis=0
    )
    assert np.linalg.norm(
        exact_relative_columns - evaluation.relative_column_residuals
    ) < 2.0e-14
    assert np.all(
        exact_relative_columns
        <= evaluation.relative_column_residual_bounds + 2.0e-14
    )
    assert np.linalg.norm(evaluation.self_energy - observation @ approximate) < 2.0e-13
    assert max(model.arnoldi_orthogonality_errors) < 2.0e-13


def test_feshbach_derivative_matches_centered_difference() -> None:
    model, _, _, _ = random_arnoldi_model(23)
    zeta = 0.64 - 0.31j
    step = 2.0e-6
    center = model.evaluate(zeta, depth=6)
    plus = model.evaluate(zeta + step, depth=6).feshbach
    minus = model.evaluate(zeta - step, depth=6).feshbach
    finite_difference = (plus - minus) / (2.0 * step)
    assert np.linalg.norm(center.derivative - finite_difference) < 3.0e-9


def test_projected_augmented_determinant_identity() -> None:
    model, _, _, _ = random_arnoldi_model(29)
    residual = model.determinant_factorization_residual(0.83 + 0.21j, depth=5)
    assert residual < 2.0e-12


def scalar_rational_model(coupling: float = 0.4) -> BatchedArnoldiFeshbach:
    return BatchedArnoldiFeshbach(
        reduced=np.asarray(((0.5,),), dtype=np.complex128),
        forcing_norms=np.asarray((1.2,)),
        hessenbergs=(np.asarray(((0.2,), (0.03,)), dtype=np.complex128),),
        output_couplings=(np.asarray(((coupling,),), dtype=np.complex128),),
        arnoldi_orthogonality_errors=np.asarray((0.0,)),
        arnoldi_relation_defect_norms=(np.asarray((0.0,)),),
    )


def test_argument_principle_counts_zeros_and_poles() -> None:
    model = scalar_rational_model()
    augmented_roots = np.linalg.eigvals(model.augmented_matrix())
    positive_root = augmented_roots[np.argmax(augmented_roots.real)]
    isolated = circle_contour_audit(
        model,
        positive_root + 0.015,
        0.12,
        nodes=256,
    )
    assert isolated.winding_integer == 1
    assert isolated.projected_pole_count == 0
    assert isolated.projected_zero_count == 1
    assert abs(isolated.cauchy_count - 1.0) < 2.0e-11
    assert abs(isolated.cauchy_centroid - positive_root) < 2.0e-11

    zero_and_pole = circle_contour_audit(model, 0.0, 0.45, nodes=256)
    assert zero_and_pole.winding_integer == 0
    assert zero_and_pole.projected_pole_count == 1
    assert zero_and_pole.projected_zero_count == 1


def test_log_derivative_newton_refines_simple_root() -> None:
    model = scalar_rational_model()
    target = np.max(np.linalg.eigvals(model.augmented_matrix()).real)
    result = determinant_newton_root(model, 0.9 + 0.08j, trust_radius=0.4)
    assert result.converged
    assert abs(result.root - target) < 3.0e-12
    assert result.relative_smallest_singular_value < 2.0e-11


def test_sampled_rouche_audit_distinguishes_small_and_large_changes() -> None:
    base = scalar_rational_model(0.4)
    nearby = scalar_rational_model(0.4001)
    distant = scalar_rational_model(0.9)
    center = 1.06
    radius = 0.15
    small = sampled_rouche_audit(base, nearby, center, radius, nodes=128)
    large = sampled_rouche_audit(base, distant, center, radius, nodes=128)
    assert small.criterion_satisfied_on_mesh
    assert small.maximum_relative_perturbation < 0.01
    assert large.maximum_relative_perturbation > 1.0
