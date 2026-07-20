import math

import numpy as np
import pytest

from intrinsic_transfer import (
    ContourComponent,
    contour_riesz_defect_upper,
    factor_aware_left_defects,
    factor_aware_right_defects,
    finite_directional_perturbation_bound,
    growing_horizon_energy_upper,
    identification_budget,
    nonnormal_projector_example,
    normalized_hilbert_schmidt_defect_upper,
    semigroup_power_defect_upper,
    transfer_block_contraction,
)


def power_norms(operator, horizon):
    powers = [np.eye(operator.shape[0])]
    for _ in range(1, horizon):
        powers.append(operator @ powers[-1])
    return [float(np.linalg.norm(value, 2)) for value in powers]


def test_normalized_coupling_bound_dominates_actual_difference():
    rng = np.random.default_rng(5401)
    reference = rng.normal(size=(7, 4))
    perturbed = reference + 1.0e-3 * rng.normal(size=(7, 4))
    norm = float(np.linalg.norm(reference, "fro"))
    defect = float(np.linalg.norm(reference - perturbed, "fro"))
    actual = np.linalg.norm(
        reference / np.linalg.norm(reference, "fro")
        - perturbed / np.linalg.norm(perturbed, "fro"),
        "fro",
    )
    assert actual <= normalized_hilbert_schmidt_defect_upper(norm, defect)
    with pytest.raises(ValueError):
        normalized_hilbert_schmidt_defect_upper(1.0, 1.0)


def test_contour_riesz_formulas():
    projector, weighted = contour_riesz_defect_upper(
        0.01,
        [
            ContourComponent(2.0 * math.pi * 0.1, 1.1, 4.0, 5.0),
            ContourComponent(2.0 * math.pi * 0.2, 0.9, 3.0, 6.0),
        ],
    )
    assert projector == pytest.approx(0.056)
    assert weighted == pytest.approx(0.0544)


def test_factor_aware_compositions_match_theorem():
    left = factor_aware_left_defects(
        hardy_radius=0.8,
        markov_defect=0.01,
        weighted_riesz_defect=0.02,
        projector_defect=0.03,
        coupling_norm=2.0,
        coupling_defect=0.1,
        perturbed_complement_norm=1.5,
    )
    assert left.operator == pytest.approx(0.0375)
    assert left.normalized_coupling == pytest.approx(0.1)
    assert left.source == pytest.approx(0.18)
    assert left.observation == 0.0
    right = factor_aware_right_defects(
        hardy_radius=0.8,
        markov_defect=0.01,
        weighted_riesz_defect=0.02,
        projector_defect=0.03,
        coupling_norm=2.0,
        coupling_defect=0.1,
    )
    assert right.operator == pytest.approx(0.0375)
    assert right.source == pytest.approx(0.1)
    assert right.observation == pytest.approx(0.03)


def test_semigroup_ledger_bound_and_contraction_transfer():
    rng = np.random.default_rng(5402)
    a = rng.normal(size=(5, 5)) / 5.0
    b = a + 1.0e-4 * rng.normal(size=(5, 5))
    horizon = 7
    left = power_norms(a, horizon)
    right = power_norms(b, horizon)
    defect = float(np.linalg.norm(a - b, 2))
    upper = semigroup_power_defect_upper(left, right, defect, horizon)
    actual = float(
        np.linalg.norm(
            np.linalg.matrix_power(a, horizon)
            - np.linalg.matrix_power(b, horizon),
            2,
        )
    )
    assert actual <= upper * (1.0 + 1.0e-12)
    q = float(np.linalg.norm(np.linalg.matrix_power(a, horizon), 2))
    assert transfer_block_contraction(q, left, right, defect, horizon) == pytest.approx(
        q + upper
    )


def test_finite_directional_bound_dominates_actual_main_sum_change():
    rng = np.random.default_rng(5403)
    a = rng.normal(size=(6, 6)) / 6.0
    at = a + 2.0e-4 * rng.normal(size=(6, 6))
    x = rng.normal(size=(6, 3)) / 3.0
    xt = x + 1.0e-4 * rng.normal(size=(6, 3))
    y = rng.normal(size=(4, 6)) / 3.0
    yt = y + 1.0e-4 * rng.normal(size=(4, 6))
    horizon = 9
    result = finite_directional_perturbation_bound(
        a,
        x,
        y,
        at,
        xt,
        yt,
        horizon,
        operator_defect_upper=np.linalg.norm(a - at, 2),
        source_defect_upper=np.linalg.norm(x - xt, "fro"),
        observation_defect_upper=np.linalg.norm(y - yt, 2),
    )

    def energy_squared(operator, source, observation):
        state = source.copy()
        total = 0.0
        for _ in range(horizon):
            total += np.linalg.norm(observation @ state, "fro") ** 2
            state = operator @ state
        return total

    actual = abs(energy_squared(a, x, y) - energy_squared(at, xt, yt))
    assert actual <= result.energy_squared_difference_upper * (1.0 + 1.0e-12)


def test_growing_horizon_upper_dominates_perturbed_lyapunov_energy():
    rng = np.random.default_rng(5404)
    a = rng.normal(size=(5, 5)) / 6.0
    at = a + 1.0e-5 * rng.normal(size=(5, 5))
    x = rng.normal(size=(5, 2)) / 4.0
    xt = x + 1.0e-5 * rng.normal(size=(5, 2))
    y = rng.normal(size=(3, 5)) / 4.0
    yt = y + 1.0e-5 * rng.normal(size=(3, 5))
    horizon = 6
    left_norms = power_norms(a, horizon)
    right_norms = power_norms(at, horizon)
    finite_bound = finite_directional_perturbation_bound(
        a,
        x,
        y,
        at,
        xt,
        yt,
        horizon,
        operator_defect_upper=np.linalg.norm(a - at, 2),
        source_defect_upper=np.linalg.norm(x - xt, "fro"),
        observation_defect_upper=np.linalg.norm(y - yt, 2),
        reference_power_norms=left_norms,
        perturbed_power_norms=right_norms,
    )
    state = x.copy()
    reference_finite_squared = 0.0
    for _ in range(horizon):
        reference_finite_squared += np.linalg.norm(y @ state, "fro") ** 2
        state = a @ state
    defect = float(np.linalg.norm(a - at, 2))
    d_horizon = semigroup_power_defect_upper(
        left_norms, right_norms, defect, horizon
    )
    result = growing_horizon_energy_upper(
        reference_finite_energy=math.sqrt(reference_finite_squared),
        finite_sequence_difference_upper=finite_bound.sequence_difference_upper,
        reference_block_norm=np.linalg.norm(np.linalg.matrix_power(a, horizon), 2),
        power_defect_upper=d_horizon,
        perturbed_source_norm_upper=np.linalg.norm(xt, "fro"),
        perturbed_observation_norm_upper=np.linalg.norm(yt, 2),
        perturbed_power_norms=right_norms,
        horizon=horizon,
    )
    from scipy.linalg import solve_discrete_lyapunov

    gramian = solve_discrete_lyapunov(at, xt @ xt.T)
    actual_squared = float(np.trace(yt @ gramian @ yt.T).real)
    assert actual_squared <= result.perturbed_full_energy_squared_upper


def test_identification_exponent_threshold():
    polylog = identification_budget(0.0, 0.0)
    assert polylog.hardy_product_exponent == 0.0
    assert polylog.mixed_gain_exponent == pytest.approx(0.25)
    assert polylog.identification_sigma_exponent == pytest.approx(3.25)
    assert polylog.preserves_all_strict_bulk_square_schedules
    threshold = identification_budget(0.1, 0.15)
    assert threshold.preserves_all_strict_bulk_square_schedules
    assert identification_budget(0.1, 0.151).preserves_all_strict_bulk_square_schedules is False


def test_nonnormal_example_has_vanishing_input_but_fixed_projector_change():
    values = [nonnormal_projector_example(k, 0.25) for k in (10.0, 100.0, 1000.0)]
    defects = [item["operator_defect"] for item in values]
    projector_defects = [item["projector_defect"] for item in values]
    assert defects == pytest.approx([0.025, 0.0025, 0.00025])
    assert min(projector_defects) > 0.08
    assert projector_defects[-1] / defects[-1] > 300.0
    for item in values:
        assert item["eigenvalues"][0] < 0.0 < 1.0 < item["eigenvalues"][1]
