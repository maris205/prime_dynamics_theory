"""Periodic Gaussian packet widths for an affine noisy cycle."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PacketTube:
    """Dimensionless periodic packet data for a two-step cycle."""

    widths: np.ndarray
    coefficients: np.ndarray
    spectral_radius: float
    balancing_diagonal: np.ndarray
    balancing_condition: float
    eigenvalue_condition: float
    recurrence_residual: float


def effective_noise_scales(points: np.ndarray, u: float) -> np.ndarray:
    r"""Return ``sqrt(1 + f'(f(x_j))^2)`` for two one-step noises."""

    values = np.asarray(points, dtype=np.float64)
    u = float(u)
    intermediate = 1.0 - u * values * values
    return np.sqrt(1.0 + (2.0 * u * np.abs(intermediate)) ** 2)


def periodic_packet_variances(
    multiplier_magnitudes: np.ndarray,
    noise_scales: np.ndarray,
) -> np.ndarray:
    r"""Solve the periodic Riccati/Lyapunov equations.

    The equations are

    ``m_j^2 v_j - v_(j+1) = beta_j^2``

    with cyclic indexing.  A unique positive solution exists when the cycle
    multiplier has magnitude greater than one.
    """

    multipliers = np.asarray(multiplier_magnitudes, dtype=np.float64)
    noise = np.asarray(noise_scales, dtype=np.float64)
    if multipliers.ndim != 1 or noise.shape != multipliers.shape:
        raise ValueError("multipliers and noise scales must be equal-length vectors")
    if multipliers.size < 1 or np.any(multipliers <= 0.0) or np.any(noise <= 0.0):
        raise ValueError("all multipliers and noise scales must be positive")
    if float(np.prod(multipliers)) <= 1.0:
        raise ValueError("the periodic orbit must be repelling")

    dimension = multipliers.size
    system = np.diag(multipliers * multipliers)
    system[np.arange(dimension), (np.arange(dimension) + 1) % dimension] -= 1.0
    variances = np.linalg.solve(system, noise * noise)
    if np.min(variances) <= 0.0:
        raise RuntimeError("periodic packet variances are not positive")
    return variances


def balancing_data(weights: np.ndarray) -> tuple[np.ndarray, float, float, float]:
    """Return radius, centered diagonal, diagonal condition, and eigen condition."""

    values = np.asarray(weights, dtype=np.float64)
    if values.ndim != 1 or values.size < 1 or np.any(values <= 0.0):
        raise ValueError("weights must be a nonempty positive vector")
    radius = float(np.exp(np.mean(np.log(values))))
    logarithms = np.zeros(values.size, dtype=np.float64)
    for index in range(values.size - 1):
        logarithms[index + 1] = (
            logarithms[index] + np.log(values[index]) - np.log(radius)
        )
    logarithms -= 0.5 * (np.max(logarithms) + np.min(logarithms))
    diagonal = np.exp(logarithms)
    condition = float(np.max(diagonal) / np.min(diagonal))
    eigen_condition = float(
        np.linalg.norm(diagonal)
        * np.linalg.norm(1.0 / diagonal)
        / diagonal.size
    )
    return diagonal, radius, condition, eigen_condition


def periodic_packet_tube(
    multiplier_magnitudes: np.ndarray,
    noise_scales: np.ndarray,
) -> PacketTube:
    """Construct the exact peak-normalized affine Gaussian packet tube."""

    multipliers = np.asarray(multiplier_magnitudes, dtype=np.float64)
    noise = np.asarray(noise_scales, dtype=np.float64)
    variances = periodic_packet_variances(multipliers, noise)
    widths = np.sqrt(variances)
    next_widths = np.roll(widths, -1)
    coefficients = next_widths / np.sqrt(next_widths**2 + noise**2)
    diagonal, radius, condition, eigen_condition = balancing_data(coefficients)
    left = multipliers**2 * variances
    right = np.roll(variances, -1) + noise**2
    residual = np.max(
        np.abs(left - right)
        / np.maximum(np.maximum(np.abs(left), np.abs(right)), 1.0)
    )
    return PacketTube(
        widths=widths,
        coefficients=coefficients,
        spectral_radius=radius,
        balancing_diagonal=diagonal,
        balancing_condition=condition,
        eigenvalue_condition=eigen_condition,
        recurrence_residual=float(residual),
    )


def fixed_boundary_width(lambda_fixed: float, u: float) -> tuple[float, float]:
    r"""Return the limiting repelling-boundary and endpoint packet widths."""

    lambda_fixed = float(lambda_fixed)
    u = float(u)
    beta_squared = 1.0 + lambda_fixed**2
    repelling_variance = beta_squared / (lambda_fixed**4 - 1.0)
    endpoint_variance = (
        repelling_variance + beta_squared
    ) / (2.0 * u * lambda_fixed) ** 2
    return float(np.sqrt(repelling_variance)), float(np.sqrt(endpoint_variance))
