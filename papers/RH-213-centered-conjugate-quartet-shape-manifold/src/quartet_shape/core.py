"""Exact two-coordinate geometry of centered conjugate quartets."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class ShapeCoordinates:
    u: float
    eta: float
    axial_coordinate: float
    positive_imaginary_height: float
    negative_imaginary_height: float


def shape_roots(u: float, eta: float) -> np.ndarray:
    """Canonical roots with center zero and mean square modulus one."""

    axial = float(u)
    asymmetry = float(eta)
    if not (0.0 <= axial <= 1.0):
        raise ValueError("u must belong to [0,1]")
    if not (-1.0 <= asymmetry <= 1.0):
        raise ValueError("eta must belong to [-1,1]")
    a = math.sqrt(axial)
    b = math.sqrt(max(0.0, (1.0 - axial) * (1.0 + asymmetry)))
    d = math.sqrt(max(0.0, (1.0 - axial) * (1.0 - asymmetry)))
    return np.asarray([a + 1j * b, a - 1j * b, -a + 1j * d, -a - 1j * d])


def shape_coefficients(u: float, eta: float) -> np.ndarray:
    """Monic coefficients in descending order for the canonical quartet."""

    axial = float(u)
    asymmetry = float(eta)
    if not (0.0 <= axial <= 1.0 and -1.0 <= asymmetry <= 1.0):
        raise ValueError("coordinates are outside the compact shape rectangle")
    c2 = 2.0 - 4.0 * axial
    c3 = 4.0 * math.sqrt(axial) * (1.0 - axial) * asymmetry
    c4 = 1.0 - asymmetry**2 * (1.0 - axial) ** 2
    return np.asarray([1.0, 0.0, c2, c3, c4], dtype=float)


def coordinates_from_roots(roots: np.ndarray, tolerance: float = 1.0e-8) -> ShapeCoordinates:
    """Recover ``(u, eta)`` from a canonical numerical root multiset."""

    values = np.asarray(roots, dtype=complex).reshape(-1)
    if values.size != 4:
        raise ValueError("a quartet is required")
    if abs(np.mean(values)) > tolerance:
        raise ValueError("the quartet is not centered")
    if abs(np.mean(np.abs(values) ** 2) - 1.0) > tolerance:
        raise ValueError("the quartet is not RMS normalized")
    upper = values[values.imag >= -tolerance]
    if upper.size != 2:
        # Select one representative from each conjugate pair under tiny noise.
        upper = values[np.argsort(-values.imag)[:2]]
    positive = upper[int(np.argmax(upper.real))]
    negative = upper[int(np.argmin(upper.real))]
    a = 0.5 * (positive.real - negative.real)
    b2 = float(positive.imag**2)
    d2 = float(negative.imag**2)
    denominator = b2 + d2
    eta = 0.0 if denominator <= np.finfo(float).tiny else (b2 - d2) / denominator
    return ShapeCoordinates(
        u=float(a**2),
        eta=float(eta),
        axial_coordinate=float(a),
        positive_imaginary_height=float(abs(positive.imag)),
        negative_imaginary_height=float(abs(negative.imag)),
    )


def coordinates_from_coefficients(coefficients: np.ndarray) -> tuple[float, float]:
    coeff = np.asarray(coefficients, dtype=complex).reshape(-1)
    if coeff.size != 5 or abs(coeff[0] - 1.0) > 1.0e-10 or abs(coeff[1]) > 1.0e-8:
        raise ValueError("a centered monic quartic is required")
    u = float(((2.0 - coeff[2].real) / 4.0))
    denominator = 4.0 * math.sqrt(max(u, 0.0)) * (1.0 - u)
    if abs(denominator) <= 1.0e-14:
        eta = 0.0
    else:
        eta = float(coeff[3].real / denominator)
    return u, eta


def coefficient_manifold_residual(coefficients: np.ndarray) -> float:
    """Residual in c3^2 = 4(2-c2)(1-c4), including realness defects."""

    coeff = np.asarray(coefficients, dtype=complex).reshape(-1)
    if coeff.size != 5:
        raise ValueError("five monic coefficients are required")
    algebraic = coeff[3] ** 2 - 4.0 * (2.0 - coeff[2]) * (1.0 - coeff[4])
    defects = [abs(coeff[0] - 1.0), abs(coeff[1]), abs(algebraic), float(np.max(np.abs(coeff.imag)))]
    return float(max(defects))


def root_geometry_residual(roots: np.ndarray) -> float:
    values = np.asarray(roots, dtype=complex).reshape(-1)
    coefficients = np.poly(values)
    return float(max(
        abs(np.mean(values)),
        abs(np.mean(np.abs(values) ** 2) - 1.0),
        coefficient_manifold_residual(coefficients),
    ))
