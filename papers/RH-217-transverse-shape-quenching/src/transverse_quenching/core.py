"""Anisotropic sensitivity of the quartet coefficient map."""

from __future__ import annotations

import math

import numpy as np


def coefficient_map(u: float, eta: float) -> np.ndarray:
    axial = float(u)
    asymmetry = float(eta)
    if not (0.0 < axial <= 1.0 and -1.0 <= asymmetry <= 1.0):
        raise ValueError("use u in (0,1] and eta in [-1,1]")
    return np.asarray([
        2.0 - 4.0 * axial,
        4.0 * math.sqrt(axial) * (1.0 - axial) * asymmetry,
        1.0 - asymmetry**2 * (1.0 - axial) ** 2,
    ])


def coefficient_jacobian(u: float, eta: float) -> np.ndarray:
    axial = float(u)
    asymmetry = float(eta)
    if not (0.0 < axial <= 1.0 and -1.0 <= asymmetry <= 1.0):
        raise ValueError("use u in (0,1] and eta in [-1,1]")
    du = np.asarray([
        -4.0,
        2.0 * asymmetry * (1.0 - 3.0 * axial) / math.sqrt(axial),
        2.0 * asymmetry**2 * (1.0 - axial),
    ])
    deta = np.asarray([
        0.0,
        4.0 * math.sqrt(axial) * (1.0 - axial),
        -2.0 * asymmetry * (1.0 - axial) ** 2,
    ])
    return np.column_stack((du, deta))


def transverse_lipschitz_bound(u: float) -> float:
    """Uniform Euclidean Lipschitz constant in eta at fixed u."""

    axial = float(u)
    if not 0.0 <= axial <= 1.0:
        raise ValueError("u must belong to [0,1]")
    return float(2.0 * (1.0 - axial) * math.sqrt(4.0 * axial + (1.0 - axial) ** 2))


def transverse_difference(u: float, eta_first: float, eta_second: float) -> float:
    first = coefficient_map(u, eta_first)
    second = coefficient_map(u, eta_second)
    return float(np.linalg.norm(first - second))


def axial_transverse_path_decomposition(
    u_first: float,
    eta_first: float,
    u_second: float,
    eta_second: float,
) -> dict[str, float]:
    """Exact telescoping along an axial leg followed by a transverse leg."""

    start = coefficient_map(u_first, eta_first)
    corner = coefficient_map(u_second, eta_first)
    finish = coefficient_map(u_second, eta_second)
    axial = corner - start
    transverse = finish - corner
    total = finish - start
    return {
        "total_norm": float(np.linalg.norm(total)),
        "axial_leg_norm": float(np.linalg.norm(axial)),
        "transverse_leg_norm": float(np.linalg.norm(transverse)),
        "telescoping_residual": float(np.linalg.norm(total - axial - transverse)),
    }
