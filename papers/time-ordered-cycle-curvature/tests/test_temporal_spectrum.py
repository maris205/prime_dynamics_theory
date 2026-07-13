from __future__ import annotations

import numpy as np

from temporal_spectrum.operators import (
    gaussian_markov_family,
    gaussian_markov_matrix,
    stationary_distribution,
)
from temporal_spectrum.orientation import (
    commutator,
    matched_spectrum_error,
    orientation_curvature,
    orientation_trace,
    parity_block_family,
    vandermonde,
)


def test_two_step_spectral_blindness_and_stationary_transport() -> None:
    a = gaussian_markov_matrix(120, 1.49, 0.13)
    b = gaussian_markov_matrix(120, 1.58, 0.13)
    forward = a @ b
    reverse = b @ a
    audit = matched_spectrum_error(forward, reverse, threshold=1.0e-8)
    assert audit["maximum_match_error"] < 2.0e-9
    assert np.max(np.abs(forward - reverse)) > 1.0e-5

    pi_forward = stationary_distribution(forward)
    pi_reverse = stationary_distribution(reverse)
    transported = pi_forward @ a
    assert np.max(np.abs(transported - pi_reverse)) < 2.0e-12


def test_commutator_pair_expansion() -> None:
    d = 128
    u = 1.5436890127
    sigma = 0.11
    _, matrix, first, _ = gaussian_markov_family(d, u, sigma)
    epsilon = 2.0e-4
    minus = gaussian_markov_matrix(d, u - epsilon, sigma)
    plus = gaussian_markov_matrix(d, u + epsilon, sigma)
    finite_difference = (minus @ plus - plus @ minus) / (2.0 * epsilon)
    assert np.max(np.abs(finite_difference - commutator(matrix, first))) < 2.0e-5


def test_vandermonde_curvature_and_alternation() -> None:
    d = 160
    u = 1.5436890127
    sigma = 0.10
    _, matrix, first, second = gaussian_markov_family(d, u, sigma)
    curvature = orientation_curvature(matrix, first, second)
    epsilon = 8.0e-4
    a = gaussian_markov_matrix(d, u - epsilon, sigma)
    b = gaussian_markov_matrix(d, u, sigma)
    c = gaussian_markov_matrix(d, u + epsilon, sigma)
    directed = orientation_trace(a, b, c)
    quotient = directed / vandermonde(u - epsilon, u, u + epsilon)
    assert abs(quotient - curvature) < 2.0e-4
    assert abs(orientation_trace(b, a, c) + directed) < 2.0e-13
    assert abs(orientation_trace(b, c, a) - directed) < 2.0e-13


def test_parity_block_derivatives() -> None:
    d = 112
    u = 1.51
    sigma = 0.12
    _, matrix, first, second = gaussian_markov_family(d, u, sigma)
    block, block_first, block_second = parity_block_family(matrix, first, second)
    epsilon = 2.0e-5
    plus = gaussian_markov_matrix(d, u + epsilon, sigma)
    minus = gaussian_markov_matrix(d, u - epsilon, sigma)
    plus_block = plus @ plus
    minus_block = minus @ minus
    numerical_first = (plus_block - minus_block) / (2.0 * epsilon)
    numerical_second = (plus_block - 2.0 * block + minus_block) / epsilon**2
    assert np.max(np.abs(numerical_first - block_first)) < 2.0e-7
    assert np.max(np.abs(numerical_second - block_second)) < 2.0e-5


def test_macroscopic_log_schedule_vandermonde() -> None:
    p = 2.0
    kappa = 0.5
    alphas = np.array([0.25, 0.5, 1.0])
    target = -(kappa * p) ** 3 * vandermonde(*np.log(alphas))
    values = []
    for logarithm in (100.0, 200.0, 400.0):
        parameters = kappa / (logarithm + np.log(alphas)) ** p
        values.append(logarithm ** (3.0 * p + 3.0) * vandermonde(*parameters))
    assert abs(values[-1] - target) < abs(values[0] - target)
    assert abs(values[-1] - target) / abs(target) < 0.03
