"""Outer resonance-cloud fitting and the canonical geometric scattering model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .deterministic import LAMBDA_FIXED


@dataclass(frozen=True)
class CloudFit:
    effective_degree: int
    selected_positive: np.ndarray
    expected_positive: np.ndarray
    phase_rms: float
    radial_mean: float
    radial_rms_from_threshold: float
    radial_gap: float

    @property
    def selected_full(self) -> np.ndarray:
        return np.concatenate((self.selected_positive, np.conjugate(self.selected_positive)))


def fit_outer_cloud(
    bulk: np.ndarray,
    *,
    maximum_degree: int = 12,
    imaginary_tolerance: float = 1.0e-7,
) -> CloudFit:
    """Select the outer conjugate ring at the largest radial spectral gap."""

    values = np.asarray(bulk, dtype=np.complex128)
    positive = values[values.imag > float(imaginary_tolerance)]
    positive = positive[np.argsort(-np.abs(positive))]
    if positive.size < 3:
        raise ValueError("at least three positive-imaginary bulk values are required")
    window = positive[: min(int(maximum_degree) + 1, positive.size)]
    radii = np.abs(window)
    gaps = radii[:-1] - radii[1:]
    degree = int(np.argmax(gaps) + 1)
    if degree < 2:
        degree = 2
    selected = positive[:degree]
    selected = selected[np.argsort(np.angle(selected))]
    expected_angles = np.arange(1, degree + 1) * np.pi / (degree + 1)
    threshold = LAMBDA_FIXED ** -0.5
    expected = threshold * np.exp(1j * expected_angles)
    phase_error = np.angle(selected) - expected_angles
    radius_error = np.abs(selected) - threshold
    return CloudFit(
        effective_degree=degree,
        selected_positive=selected,
        expected_positive=expected,
        phase_rms=float(np.sqrt(np.mean(phase_error**2))),
        radial_mean=float(np.mean(np.abs(selected))),
        radial_rms_from_threshold=float(np.sqrt(np.mean(radius_error**2))),
        radial_gap=float(gaps[degree - 1]) if degree - 1 < gaps.size else float("nan"),
    )


def geometric_cloud(degree: int) -> np.ndarray:
    """Return the ``2N`` eigenvalue proxies resolving ``1/(1-z^2/lambda)``."""

    degree = int(degree)
    if degree < 1:
        raise ValueError("degree must be positive")
    angles = np.arange(1, degree + 1) * np.pi / (degree + 1)
    positive = LAMBDA_FIXED ** -0.5 * np.exp(1j * angles)
    return np.concatenate((positive, np.conjugate(positive)))


def geometric_section(degree: int, q: complex) -> complex:
    """Return ``1+q+...+q**N`` without cancellation at ``q=1``."""

    degree = int(degree)
    q = complex(q)
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    if abs(q - 1.0) < 1.0e-10:
        return complex(degree + 1)
    return complex((1.0 - q ** (degree + 1)) / (1.0 - q))


def scattering_profile(s: complex) -> complex:
    """Return the universal pole-resolution profile ``(exp(s)-1)/s``."""

    s = complex(s)
    if abs(s) < 1.0e-10:
        return 1.0 + 0.5 * s + s * s / 6.0
    return complex(np.expm1(s) / s)


def scaled_geometric_profile(degree: int, s: complex) -> complex:
    """Evaluate the normalized geometric section in the scattering coordinate."""

    degree = int(degree)
    q = np.exp(complex(s) / (degree + 1))
    return geometric_section(degree, q) / (degree + 1)


def cloud_det2(values: np.ndarray, z: complex) -> complex:
    """Return the second-regularized product over a finite resonance cloud."""

    values = np.asarray(values, dtype=np.complex128)
    z = complex(z)
    return complex(np.prod((1.0 - z * values) * np.exp(z * values)))
