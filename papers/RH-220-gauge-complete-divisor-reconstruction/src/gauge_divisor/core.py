"""Affine gauge completion of the normalized quartet shape."""

from __future__ import annotations

import math

import numpy as np


def shape_roots(u: float, eta: float) -> np.ndarray:
    axial = float(u)
    asymmetry = float(eta)
    if not (0.0 <= axial <= 1.0 and -1.0 <= asymmetry <= 1.0):
        raise ValueError("coordinates lie outside the shape rectangle")
    a = math.sqrt(axial)
    b = math.sqrt(max(0.0, (1.0 - axial) * (1.0 + asymmetry)))
    d = math.sqrt(max(0.0, (1.0 - axial) * (1.0 - asymmetry)))
    return np.asarray([a + 1j * b, a - 1j * b, -a + 1j * d, -a - 1j * d])


def shape_coefficients(u: float, eta: float) -> np.ndarray:
    axial = float(u)
    asymmetry = float(eta)
    return np.asarray([
        1.0,
        0.0,
        2.0 - 4.0 * axial,
        4.0 * math.sqrt(axial) * (1.0 - axial) * asymmetry,
        1.0 - asymmetry**2 * (1.0 - axial) ** 2,
    ])


def raw_roots(center: complex, radius: float, u: float, eta: float) -> np.ndarray:
    scale = float(radius)
    if scale <= 0.0:
        raise ValueError("the RMS radius must be positive")
    return complex(center) + scale * shape_roots(u, eta)


def raw_coefficients(center: complex, radius: float, u: float, eta: float) -> np.ndarray:
    """Expand r^4 Q((z-mu)/r) without numerical root finding."""

    scale = float(radius)
    if scale <= 0.0:
        raise ValueError("the RMS radius must be positive")
    mu = complex(center)
    shape = shape_coefficients(u, eta)
    x = np.poly1d([1.0, -mu])
    polynomial = x**4 + shape[2] * scale**2 * x**2 + shape[3] * scale**3 * x + shape[4] * scale**4
    return np.asarray(polynomial.c, dtype=complex)


def gauge_shape_parameters(roots: np.ndarray) -> dict[str, float | complex]:
    values = np.asarray(roots, dtype=complex).reshape(-1)
    if values.size != 4:
        raise ValueError("a quartet is required")
    center = complex(np.mean(values))
    centered = values - center
    radius = float(np.sqrt(np.mean(np.abs(centered) ** 2)))
    normalized = centered / radius
    upper = normalized[np.argsort(-normalized.imag)[:2]]
    positive = upper[int(np.argmax(upper.real))]
    negative = upper[int(np.argmin(upper.real))]
    a = 0.5 * (positive.real - negative.real)
    b2 = positive.imag**2
    d2 = negative.imag**2
    return {
        "center": center,
        "radius": radius,
        "u": float(a**2),
        "eta": float((b2 - d2) / (b2 + d2)),
    }


def coefficient_path_decomposition(
    first: tuple[complex, float, float, float],
    second: tuple[complex, float, float, float],
) -> dict[str, float]:
    """Change gauge first and shape second, yielding an exact telescoping path."""

    mu0, r0, u0, eta0 = first
    mu1, r1, u1, eta1 = second
    start = raw_coefficients(mu0, r0, u0, eta0)
    corner = raw_coefficients(mu1, r1, u0, eta0)
    finish = raw_coefficients(mu1, r1, u1, eta1)
    gauge = corner - start
    shape = finish - corner
    total = finish - start
    return {
        "total_norm": float(np.linalg.norm(total)),
        "gauge_leg_norm": float(np.linalg.norm(gauge)),
        "shape_leg_norm": float(np.linalg.norm(shape)),
        "telescoping_residual": float(np.linalg.norm(total - gauge - shape)),
    }


def route_coordinate(statuses: dict[str, bool]) -> str:
    required = (
        "shape_manifold_exact",
        "gauge_reconstruction_exact",
        "simple_recurrence_rejected",
        "fixed_quartic_counting_rejected",
    )
    if not all(bool(statuses.get(key)) for key in required):
        return "quartet_shape_frontier_incomplete"
    if statuses.get("rank_growing_divisor_constructed"):
        return "rank_growing_divisor_open_local_uniform_limit"
    return "finite_gauge_complete_shape_flow_open_rank_growing_divisor"
