"""Boundary, discriminant, and quantitative collapse of quartet shapes."""

from __future__ import annotations

import itertools
import math

import numpy as np


BOUNDARY_ROOTS = np.asarray([1.0, 1.0, -1.0, -1.0], dtype=complex)
BOUNDARY_COEFFICIENTS = np.asarray([1.0, 0.0, -2.0, 0.0, 1.0])


def canonical_roots(u: float, eta: float) -> np.ndarray:
    axial = float(u)
    asymmetry = float(eta)
    if not (0.0 <= axial <= 1.0 and -1.0 <= asymmetry <= 1.0):
        raise ValueError("coordinates lie outside the shape rectangle")
    a = math.sqrt(axial)
    b = math.sqrt(max(0.0, (1.0 - axial) * (1.0 + asymmetry)))
    d = math.sqrt(max(0.0, (1.0 - axial) * (1.0 - asymmetry)))
    return np.asarray([a + 1j * b, a - 1j * b, -a + 1j * d, -a - 1j * d])


def discriminant_formula(u: float, eta: float) -> float:
    axial = float(u)
    asymmetry = float(eta)
    if not (0.0 <= axial <= 1.0 and -1.0 <= asymmetry <= 1.0):
        raise ValueError("coordinates lie outside the shape rectangle")
    return float(
        256.0
        * (1.0 - axial) ** 2
        * (1.0 - asymmetry**2)
        * (4.0 * axial + (1.0 - axial) ** 2 * asymmetry**2) ** 2
    )


def root_discriminant(roots: np.ndarray) -> complex:
    values = np.asarray(roots, dtype=complex).reshape(-1)
    if values.size != 4:
        raise ValueError("a quartet is required")
    result = 1.0 + 0.0j
    for first, second in itertools.combinations(values, 2):
        result *= (first - second) ** 2
    return complex(result)


def boundary_root_distance(u: float, eta: float) -> float:
    roots = canonical_roots(u, eta)
    assignments = itertools.permutations(BOUNDARY_ROOTS)
    return float(min(max(abs(value - target) for value, target in zip(roots, assignment)) for assignment in assignments))


def uniform_boundary_root_bound(u: float) -> float:
    axial = float(u)
    if not 0.0 <= axial <= 1.0:
        raise ValueError("u must belong to [0,1]")
    return float(math.sqrt(2.0 * (1.0 - axial)) + (1.0 - axial) / (1.0 + math.sqrt(axial)))


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


def coefficient_boundary_distance(u: float, eta: float) -> float:
    return float(np.max(np.abs(shape_coefficients(u, eta) - BOUNDARY_COEFFICIENTS)))


def degeneracy_labels(u: float, eta: float, tolerance: float = 1.0e-12) -> list[str]:
    axial = float(u)
    asymmetry = float(eta)
    labels = []
    if abs(axial - 1.0) <= tolerance:
        labels.append("axial_double_pair")
    if abs(abs(asymmetry) - 1.0) <= tolerance:
        labels.append("one_real_double_pair")
    if abs(axial) <= tolerance and abs(asymmetry) <= tolerance:
        labels.append("coincident_imaginary_pairs")
    return labels
