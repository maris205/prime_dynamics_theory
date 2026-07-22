"""Scalar ledgers for contraction and rank-one projector validation."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class NewtonRadius:
    beta: float
    jacobian_defect: float
    inverse_norm: float
    radius: float
    contraction: float
    self_map_margin: float


def newton_contraction_radius(
    beta: float,
    jacobian_defect: float,
    inverse_norm: float,
) -> NewtonRadius:
    """Choose and verify a contraction radius for a bilinear eigenproblem."""

    b = float(beta)
    gamma = float(jacobian_defect)
    inverse = float(inverse_norm)
    if b < 0.0 or gamma < 0.0 or inverse < 0.0 or gamma >= 1.0:
        raise ValueError("invalid Newton ledger")
    radius = 2.0 * b / (1.0 - gamma)
    contraction = gamma + inverse * radius
    margin = radius - (b + gamma * radius + inverse * radius * radius)
    if contraction >= 1.0 or margin < 0.0:
        discriminant = (1.0 - gamma) ** 2 - 4.0 * inverse * b
        if inverse == 0.0 and gamma < 1.0:
            radius = b / (1.0 - gamma)
        elif discriminant > 0.0:
            radius = (
                2.0
                * b
                / (1.0 - gamma + math.sqrt(discriminant))
            )
            radius = math.nextafter(radius * (1.0 + 1.0e-10), math.inf)
        else:
            raise ValueError("Newton contraction radius does not close")
        contraction = gamma + inverse * radius
        margin = radius - (
            b + gamma * radius + inverse * radius * radius
        )
    if contraction >= 1.0 or margin < -1.0e-15 * max(1.0, radius):
        raise ValueError("Newton contraction radius does not close")
    return NewtonRadius(
        beta=b,
        jacobian_defect=gamma,
        inverse_norm=inverse,
        radius=radius,
        contraction=contraction,
        self_map_margin=margin,
    )


@dataclass(frozen=True)
class ProjectorError:
    gram_lower: float
    numerator_error: float
    normalization_error: float
    projector_error_upper: float


def parity_projector_error(
    right_norm: float,
    left_norm: float,
    right_error: float,
    left_error: float,
) -> ProjectorError:
    """Bound r l* /(l*r) against r0 l0* when r0*l0=1."""

    rn = float(right_norm)
    ln = float(left_norm)
    re = float(right_error)
    le = float(left_error)
    if min(rn, ln, re, le) < 0.0:
        raise ValueError("projector inputs must be nonnegative")
    normalization = (ln + le) * re
    gram_lower = 1.0 - normalization
    if gram_lower <= 0.0:
        raise ValueError("projector normalization is not separated from zero")
    numerator = re * (ln + le) + rn * le
    upper = (
        numerator / gram_lower
        + rn * ln * normalization / gram_lower
    )
    return ProjectorError(
        gram_lower=gram_lower,
        numerator_error=numerator,
        normalization_error=normalization,
        projector_error_upper=upper,
    )
