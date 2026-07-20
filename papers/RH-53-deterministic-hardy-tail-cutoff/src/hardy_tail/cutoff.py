"""Closed folded-Gaussian cutoff bounds reused by the Hardy audit."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class CutoffBound:
    dimension: int
    mesh: float
    sigma: float
    declared_multiple: float
    support_half_width: int
    effective_multiple: float
    omitted_mass_upper: float
    infinity_norm_upper: float
    two_norm_upper: float


def adaptive_cutoff_multiple(mesh: float, minimum: float = 5.0) -> float:
    """Return the RH-39 schedule ``max(minimum,2 sqrt(log(1/h)))``."""

    h = float(mesh)
    floor = float(minimum)
    if not 0.0 < h < 1.0 or floor <= 0.0:
        raise ValueError("mesh and minimum are outside their valid ranges")
    return max(floor, 2.0 * math.sqrt(math.log(1.0 / h)))


def cutoff_bound(
    dimension: int, sigma: float, declared_multiple: float
) -> CutoffBound:
    """Evaluate the analytic RH-39 full-versus-cutoff norm bound."""

    n = int(dimension)
    width = float(sigma)
    multiple = float(declared_multiple)
    h = 1.0 / n
    if n < 2 or not h < width <= 1.0 or multiple <= 0.0:
        raise ValueError("the cutoff theorem requires n>=2 and h<sigma<=1")
    half_width = int(math.ceil(multiple * width / h)) + 2
    effective = half_width * h / width
    exp_half = math.exp(-0.5 * effective * effective)
    omitted_mass = (
        2.0
        * math.sqrt(math.e)
        * exp_half
        * (h + width / effective)
        / (width - h)
    )
    if omitted_mass >= 1.0:
        raise ValueError("the omitted-mass bound is not below one")
    alpha = omitted_mass / (1.0 - omitted_mass)
    omitted_square = (
        4.0
        * math.e
        * exp_half
        * exp_half
        * (h + width / (2.0 * effective))
        / (width - h) ** 2
    )
    renormalization_square = (
        math.e
        * alpha
        * alpha
        * (4.0 * h + 2.0 * math.sqrt(math.pi) * width)
        / (width - h) ** 2
    )
    return CutoffBound(
        dimension=n,
        mesh=h,
        sigma=width,
        declared_multiple=multiple,
        support_half_width=half_width,
        effective_multiple=effective,
        omitted_mass_upper=omitted_mass,
        infinity_norm_upper=2.0 * omitted_mass,
        two_norm_upper=math.sqrt(omitted_square + renormalization_square),
    )
