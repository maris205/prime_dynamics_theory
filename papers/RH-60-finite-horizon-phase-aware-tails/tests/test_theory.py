import math

import numpy as np
import pytest
from scipy.linalg import solve_discrete_lyapunov

from phase_tail import (
    finite_horizon_gram,
    geometric_tail_energy_upper,
    make_completion,
    packet_hybrid_upper,
    phase_aware_completion_upper,
    stein_tail_energy_upper,
)


def example():
    operator = np.asarray(
        [[0.2, 0.35], [0.0, 0.65]], dtype=np.complex128
    )
    source = np.asarray([[0.4], [0.7]])
    observation = np.asarray([[0.8, -0.3]])
    return operator, source, observation


def test_finite_horizon_gram_is_positive_and_fuses_packets_exactly() -> None:
    operator, source, observation = example()
    finite = finite_horizon_gram(
        operator,
        source,
        observation,
        5,
        packet_slices=(slice(0, 1), slice(1, 2)),
    )
    assert np.min(np.linalg.eigvalsh(finite.gram)) > -1.0e-12
    fused = finite.gram.sum().real
    direct = finite_horizon_gram(operator, source, observation, 5)
    assert fused == pytest.approx(direct.fused_energy_squared, rel=2.0e-13)
    assert finite.fused_energy_squared >= 0.0


def test_stein_tail_and_geometric_tail_are_valid_upper_forms() -> None:
    operator, source, observation = example()
    observability = solve_discrete_lyapunov(
        operator.conjugate().T,
        observation.conjugate().T @ observation,
    )
    metric = solve_discrete_lyapunov(
        operator.conjugate().T, np.eye(2)
    )
    eigenvalues, vectors = np.linalg.eigh(metric)
    root = (vectors * np.sqrt(eigenvalues)) @ vectors.conjugate().T
    inverse = (vectors * (1.0 / np.sqrt(eigenvalues))) @ vectors.conjugate().T
    normalized = root @ operator @ inverse
    residual = metric - operator.conjugate().T @ metric @ operator
    kappa = float(
        np.linalg.eigvalsh(
            observation @ np.linalg.solve(residual, observation.conjugate().T)
        )[-1]
    )
    horizon = 4
    exact_tail = float(
        np.trace(
            (np.linalg.matrix_power(operator, horizon) @ source).conjugate().T
            @ observability
            @ (np.linalg.matrix_power(operator, horizon) @ source)
        ).real
    )
    weighted = root @ source
    tail = stein_tail_energy_upper(normalized, weighted, kappa, horizon)
    geometric = geometric_tail_energy_upper(
        normalized, weighted, kappa, horizon
    )
    assert tail * tail >= exact_tail * (1.0 - 1.0e-11)
    assert geometric >= tail * (1.0 - 1.0e-11)


def test_phase_aware_completion_preserves_the_finite_fusion() -> None:
    finite = finite_horizon_gram(
        *example(), 3, packet_slices=(slice(0, 1), slice(1, 2))
    )
    completion = make_completion(finite, (0.2, 0.3))
    assert completion.phase_aware_upper == pytest.approx(
        finite.fused_energy + 0.5
    )
    assert completion.packet_hybrid_uppers[0] == pytest.approx(
        packet_hybrid_upper(math.sqrt(finite.packet_energy_squared[0]), 0.2)
    )
    assert phase_aware_completion_upper(finite.fused_energy, (0.2, 0.3)) == (
        completion.phase_aware_upper
    )


def test_invalid_horizons_and_negative_completion_terms_are_rejected() -> None:
    operator, source, observation = example()
    with pytest.raises(ValueError):
        finite_horizon_gram(operator, source, observation, -1)
    with pytest.raises(ValueError):
        packet_hybrid_upper(-1.0, 0.2)
    with pytest.raises(ValueError):
        phase_aware_completion_upper(1.0, (0.2, -0.1))
