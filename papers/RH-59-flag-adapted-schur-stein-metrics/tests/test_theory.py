import math

import numpy as np
import pytest
from scipy.linalg import solve_discrete_lyapunov

from flag_stein import (
    build_flag_metric,
    comparison_contraction_log_upper,
    evaluate_packet_certificate,
    packet_log_upper_objective,
    scaled_comparison_prefix,
    scaled_normalized_prefix,
)


def example():
    triangular = np.asarray(
        [[0.15, 0.65, -0.20], [0.0, 0.48, 0.55], [0.0, 0.0, -0.72]],
        dtype=np.complex128,
    )
    source = np.asarray([[0.4, -0.1], [0.2, 0.5], [-0.3, 0.6]])
    observation = np.asarray([[0.7, 0.1, -0.4], [0.2, -0.5, 0.6]])
    return triangular, source, observation


def test_local_metrics_normalize_each_diagonal_block() -> None:
    triangular, _, _ = example()
    family = build_flag_metric(triangular, (1, 1, 1))
    assert family.strict_lower_relative_defect == 0.0
    assert max(block.residual_relative for block in family.blocks) < 1.0e-13
    assert max(block.contraction for block in family.blocks) < 1.0
    assert np.diag(family.comparison_matrix) == pytest.approx(
        [block.contraction for block in family.blocks]
    )


def test_hierarchical_scaling_makes_the_full_flag_dissipative() -> None:
    triangular, _, _ = example()
    family = build_flag_metric(triangular, (1, 1, 1))
    log_scales = (-5.0, -2.5, 0.0)
    normalized = scaled_normalized_prefix(family, 2, log_scales)
    comparison = scaled_comparison_prefix(family, 2, log_scales)
    assert np.linalg.norm(normalized, 2) <= np.linalg.norm(comparison, 2)
    assert np.linalg.norm(comparison, 2) < 1.0


def test_packet_supersolution_bounds_the_exact_packet_energy() -> None:
    triangular, source, observation = example()
    family = build_flag_metric(triangular, (1, 1, 1))
    log_scales = (-5.0, -2.5, 0.0)
    certificate = evaluate_packet_certificate(
        source, observation, family, 2, log_scales
    )

    observability = solve_discrete_lyapunov(
        triangular.conjugate().T,
        observation.conjugate().T @ observation,
    )
    packet = np.zeros_like(source)
    packet[2, :] = source[2, :]
    exact_squared = float(
        np.trace(packet.conjugate().T @ observability @ packet).real
    )
    assert certificate.energy_squared_upper >= exact_squared * (1.0 - 1.0e-12)
    assert certificate.minimum_dissipation_eigenvalue > 0.0
    assert certificate.minimum_supersolution_eigenvalue > -1.0e-11
    assert math.exp(
        packet_log_upper_objective(
            source, observation, family, 2, log_scales
        )
    ) == pytest.approx(certificate.energy_upper, rel=2.0e-13)
    assert certificate.energy_upper <= certificate.contraction_energy_upper


def test_exact_dissipation_is_no_worse_than_scalar_comparison_upper() -> None:
    triangular, source, observation = example()
    family = build_flag_metric(triangular, (1, 1, 1))
    log_scales = (-5.0, -2.5, 0.0)
    exact = evaluate_packet_certificate(
        source, observation, family, 2, log_scales
    )
    comparison = math.exp(
        comparison_contraction_log_upper(
            source, observation, family, 2, log_scales
        )
    )
    assert exact.energy_upper <= exact.contraction_energy_upper
    assert exact.contraction_energy_upper <= comparison * (1.0 + 1.0e-12)


def test_invalid_flags_and_nondissipative_scalings_are_rejected() -> None:
    triangular, source, observation = example()
    with pytest.raises(ValueError):
        build_flag_metric(triangular, (1, 1))
    family = build_flag_metric(triangular, (1, 1, 1))
    with pytest.raises(ValueError):
        evaluate_packet_certificate(source, observation, family, 2, (0.0, 0.0))
    with pytest.raises(ValueError):
        evaluate_packet_certificate(source, observation, family, 2, (5.0, 2.5, 0.0))
