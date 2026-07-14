"""Conditioned-Gaussian Hellinger affinities and endpoint resolution ranks."""

from __future__ import annotations

import numpy as np
from scipy.special import ndtr

from .boundary import LAMBDA_FIXED


HALF_ENERGY_THRESHOLD = 1.0 / np.sqrt(2.0)


def conditioned_gaussian_affinity(
    first: np.ndarray | float,
    second: np.ndarray | float,
    *,
    power: float = 0.5,
) -> np.ndarray:
    r"""Return the exact affinity of normalized powered Gaussian rows.

    The arguments are the dimensionless endpoint clearances ``delta/sigma``.
    ``power=1/2`` gives Hellinger fingerprints; ``power=1`` gives normalized
    linear kernel rows. Inputs are broadcast in the NumPy sense.
    """

    first_array = np.asarray(first, dtype=np.float64)
    second_array = np.asarray(second, dtype=np.float64)
    power = float(power)
    if np.any(first_array < 0.0) or np.any(second_array < 0.0):
        raise ValueError("dimensionless clearances must be nonnegative")
    if power <= 0.0:
        raise ValueError("power must be positive")
    root_two_power = np.sqrt(2.0 * power)
    numerator = ndtr(np.sqrt(power / 2.0) * (first_array + second_array))
    denominator = np.sqrt(
        ndtr(root_two_power * first_array)
        * ndtr(root_two_power * second_array)
    )
    separation = np.exp(-0.25 * power * (first_array - second_array) ** 2)
    return separation * numerator / denominator


def endpoint_residual_energy(
    clearance_ratio: np.ndarray | float, *, power: float = 0.5
) -> np.ndarray:
    r"""Return ``||(I-|psi_0><psi_0|) psi_t||_2^2`` for ``t=delta/sigma``."""

    values = np.asarray(clearance_ratio, dtype=np.float64)
    overlap = conditioned_gaussian_affinity(values, 0.0, power=power)
    return np.clip(1.0 - overlap * overlap, 0.0, 1.0)


def projected_gram_matrix(
    clearances: np.ndarray,
    sigma: float,
    *,
    tail_ratio: float = 1.0e-12,
    power: float = 0.5,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the finite projected Gram matrix and retained dimensionless ladder."""

    values = np.asarray(clearances, dtype=np.float64)
    sigma = float(sigma)
    tail_ratio = float(tail_ratio)
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    if tail_ratio <= 0.0:
        raise ValueError("tail_ratio must be positive")
    if np.any(values <= 0.0) or np.any(values[1:] >= values[:-1]):
        raise ValueError("clearances must be positive and strictly decreasing")

    dimensionless = values / sigma
    retained = dimensionless[dimensionless >= tail_ratio]
    affinity = conditioned_gaussian_affinity(
        retained[:, None], retained[None, :], power=power
    )
    endpoint = conditioned_gaussian_affinity(retained, 0.0, power=power)
    gram = affinity - np.outer(endpoint, endpoint)
    gram = 0.5 * (gram + gram.T)
    return gram, retained


def resolution_singular_values(
    clearances: np.ndarray,
    sigma: float,
    *,
    tail_ratio: float = 1.0e-12,
    power: float = 0.5,
) -> np.ndarray:
    """Return singular values of the endpoint-projected resolution operator."""

    gram, _ = projected_gram_matrix(
        clearances, sigma, tail_ratio=tail_ratio, power=power
    )
    eigenvalues = np.linalg.eigvalsh(gram)
    eigenvalues = np.clip(eigenvalues, 0.0, None)
    return np.sqrt(eigenvalues[::-1])


def threshold_rank(
    clearances: np.ndarray,
    sigma: float,
    *,
    threshold: float = HALF_ENERGY_THRESHOLD,
    tail_ratio: float = 1.0e-12,
    power: float = 0.5,
) -> int:
    """Count singular values strictly above a fixed resolution threshold."""

    threshold = float(threshold)
    if not 0.0 < threshold < 1.0:
        raise ValueError("threshold must lie strictly between zero and one")
    singular_values = resolution_singular_values(
        clearances, sigma, tail_ratio=tail_ratio, power=power
    )
    return int(np.count_nonzero(singular_values > threshold))


def hilbert_schmidt_energy(
    clearances: np.ndarray, sigma: float, *, power: float = 0.5
) -> float:
    """Return the squared Hilbert--Schmidt norm from a sufficiently long ladder."""

    values = np.asarray(clearances, dtype=np.float64)
    sigma = float(sigma)
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    return float(np.sum(endpoint_residual_energy(values / sigma, power=power)))


def half_logarithmic_clock(sigma: np.ndarray | float) -> np.ndarray:
    r"""Return ``log(1/sigma)/(2 log(lambda))``."""

    values = np.asarray(sigma, dtype=np.float64)
    if np.any(values <= 0.0):
        raise ValueError("sigma must be positive")
    return np.log(1.0 / values) / (2.0 * np.log(LAMBDA_FIXED))
