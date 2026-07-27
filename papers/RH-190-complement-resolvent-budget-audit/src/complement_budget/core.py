"""Norm-only complement-resolvent budgets for oblique temporal packets."""

from __future__ import annotations

import math


def root_half_spacing(length: int, radius: float) -> float:
    size = int(length)
    rho = float(radius)
    if size < 3 or rho <= 0.0:
        raise ValueError("length >= 3 and positive radius are required")
    return rho * math.sin(math.pi / size)


def norm_only_complement_budget(
    operator_norm: float,
    oblique_condition: float,
    root_radius: float,
    contour_radius: float,
    packet_resolvent_bound: float,
    left_coupling: float,
    right_coupling: float,
) -> dict[str, float | bool]:
    a_norm = float(operator_norm)
    chi = float(oblique_condition)
    rho = float(root_radius)
    delta = float(contour_radius)
    packet = float(packet_resolvent_bound)
    left = float(left_coupling)
    right = float(right_coupling)
    if min(a_norm, rho, delta, packet, left, right) < 0.0 or chi < 1.0:
        raise ValueError("invalid complement budget")
    # With an orthonormal frame Z for Ran(Q)=ker(W*), the Feshbach block is
    # D=Z*QAZ.  Thus only the output projection contributes an oblique norm:
    # ||D|| <= ||Q|| ||A|| = chi ||A||.  The ambient ||QAQ|| <= chi^2||A||
    # bound is valid but unnecessarily weaker on the invariant domain Ran(Q).
    complement_operator_bound = chi * a_norm
    minimum_contour_modulus = max(0.0, rho - delta)
    clearance = minimum_contour_modulus - complement_operator_bound
    complement_resolvent = math.inf if clearance <= 0.0 else 1.0 / clearance
    schur = math.inf if not math.isfinite(complement_resolvent) else packet * complement_resolvent * left * right
    return {
        "complement_projector_norm_bound": chi,
        "complement_operator_norm_bound": complement_operator_bound,
        "minimum_contour_modulus": minimum_contour_modulus,
        "norm_only_clearance": clearance,
        "norm_only_complement_resolvent_bound": complement_resolvent,
        "directed_schur_product": schur,
        "norm_only_resolvent_available": clearance > 0.0,
        "full_norm_only_certificate": clearance > 0.0 and schur < 1.0,
    }


def validated_inverse_bound(
    approximate_inverse_norm: float,
    nominal_inverse_defect: float,
    mesh_radius: float,
    operator_radius: float,
) -> dict[str, float | bool]:
    inverse_norm = float(approximate_inverse_norm)
    defect = float(nominal_inverse_defect)
    mesh = float(mesh_radius)
    operator = float(operator_radius)
    if min(inverse_norm, defect, mesh, operator) < 0.0:
        raise ValueError("validated inverse data must be nonnegative")
    denominator_defect = defect + inverse_norm * (mesh + operator)
    available = denominator_defect < 1.0
    bound = math.inf if not available else inverse_norm / (1.0 - denominator_defect)
    return {
        "banach_defect": denominator_defect,
        "validated_inverse_available": available,
        "validated_inverse_bound": bound,
    }
