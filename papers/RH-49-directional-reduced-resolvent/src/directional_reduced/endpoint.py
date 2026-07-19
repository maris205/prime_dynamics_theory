"""Critical-fold endpoint profiles entering the quarter-power lower bound."""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr


def _normal_density(value):
    item = np.asarray(value, dtype=np.float64)
    return np.exp(-0.5 * item * item) / math.sqrt(2.0 * math.pi)


def critical_fold_profile(xi, s, critical_coefficient: float):
    r"""Return ``phi(u xi^2-s)/Phi(u xi^2)`` on the endpoint scale."""

    u = float(critical_coefficient)
    if not np.isfinite(u) or u <= 0.0:
        raise ValueError("critical_coefficient must be positive")
    xi_value = np.asarray(xi, dtype=np.float64)
    s_value = np.asarray(s, dtype=np.float64)
    center = u * xi_value * xi_value
    return _normal_density(center - s_value) / ndtr(center)


def critical_fold_profile_derivative(xi, s, critical_coefficient: float):
    """Differentiate the endpoint profile with respect to ``s``."""

    u = float(critical_coefficient)
    xi_value = np.asarray(xi, dtype=np.float64)
    s_value = np.asarray(s, dtype=np.float64)
    center = u * xi_value * xi_value
    return (center - s_value) * _normal_density(center - s_value) / ndtr(
        center
    )


def packet_envelope(s):
    r"""A unit ``L2(0,infinity)`` packet: ``A(s)=2s exp(-s)``."""

    value = np.asarray(s, dtype=np.float64)
    return 2.0 * value * np.exp(-value)


def packet_limit_profile(xi: float, critical_coefficient: float) -> float:
    r"""Evaluate ``int A(s) partial_s q(xi,s) ds`` by adaptive quadrature."""

    value = float(xi)
    if value < 0.0 or not np.isfinite(value):
        raise ValueError("xi must be finite and nonnegative")
    result, _ = quad(
        lambda s: float(packet_envelope(s))
        * float(
            critical_fold_profile_derivative(
                value, s, critical_coefficient
            )
        ),
        0.0,
        np.inf,
        epsabs=2.0e-12,
        epsrel=2.0e-12,
        limit=200,
    )
    return float(result)
