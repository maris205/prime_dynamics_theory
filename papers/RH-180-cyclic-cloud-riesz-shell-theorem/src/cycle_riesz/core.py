"""Normal-cycle geometry combined with a directed Schur certificate."""

from __future__ import annotations

import math

import numpy as np


def cycle_roots(length: int, radius: float) -> np.ndarray:
    size = int(length)
    rho = float(radius)
    if size < 3 or rho <= 0.0:
        raise ValueError("length >= 3 and positive radius are required")
    return rho * np.exp(2j * np.pi * np.arange(1, size) / size)


def double_cycle_seed(length: int, radius: float) -> np.ndarray:
    roots = cycle_roots(length, radius)
    return np.diag(np.concatenate([roots, roots]))


def root_half_spacing(length: int, radius: float) -> float:
    size = int(length)
    rho = float(radius)
    if size < 3 or rho <= 0.0:
        raise ValueError("invalid cycle geometry")
    return rho * math.sin(math.pi / size)


def cycle_shell_budget(
    length: int,
    radius: float,
    contour_radius: float,
    packet_perturbation: float,
    complement_resolvent: float,
    left_coupling: float,
    right_coupling: float,
) -> dict[str, float | bool]:
    spacing = root_half_spacing(length, radius)
    delta = float(contour_radius)
    epsilon = float(packet_perturbation)
    d = float(complement_resolvent)
    b = float(left_coupling)
    c = float(right_coupling)
    if min(delta, epsilon, d, b, c) < 0.0:
        raise ValueError("budget entries must be nonnegative")
    geometry_admissible = delta < spacing
    packet_admissible = epsilon < delta
    packet_resolvent = math.inf if not packet_admissible else 1.0 / (delta - epsilon)
    schur_product = packet_resolvent * d * b * c
    return {
        "root_half_spacing": spacing,
        "contour_radius": delta,
        "packet_perturbation": epsilon,
        "packet_resolvent_bound": packet_resolvent,
        "complement_resolvent_bound": d,
        "left_coupling": b,
        "right_coupling": c,
        "directed_schur_product": schur_product,
        "geometry_admissible": geometry_admissible,
        "packet_admissible": packet_admissible,
        "schur_admissible": schur_product < 1.0,
        "certificate_admissible": geometry_admissible and packet_admissible and schur_product < 1.0,
    }
