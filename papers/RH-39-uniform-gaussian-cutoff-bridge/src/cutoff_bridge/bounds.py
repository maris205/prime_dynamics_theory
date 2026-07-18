"""Explicit tail and Euclidean cutoff bounds for the folded Gaussian model."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class CutoffBound:
    """Finite-grid bounds for one row-normalized folded Gaussian matrix."""

    dimension: int
    mesh: float
    sigma: float
    declared_multiple: float
    support_half_width: int
    effective_multiple: float
    omitted_mass_upper: float
    infinity_norm_upper: float
    omitted_frobenius_square_upper: float
    renormalization_frobenius_square_upper: float
    two_norm_upper: float


@dataclass(frozen=True)
class HaarCutoffDefect:
    """Cutoff contributions to the four dyadic Haar blocks."""

    coarse_consistency: float
    coarse_to_detail: float
    detail_to_coarse: float
    detail_block: float


def _positive(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def support_half_width(
    dimension: int, sigma: float, declared_multiple: float
) -> int:
    """Return the exact half-width used by the archived sparse builder."""

    n = int(dimension)
    if n < 2:
        raise ValueError("dimension must be at least two")
    width = _positive(sigma, "sigma")
    multiple = _positive(declared_multiple, "declared_multiple")
    return int(math.ceil(multiple * width * n)) + 2


def cutoff_bound(
    dimension: int,
    sigma: float,
    declared_multiple: float,
) -> CutoffBound:
    """Evaluate the Mills-ratio cutoff theorem in binary64.

    The formulas themselves are analytic.  The publication certificate also
    evaluates them with Arb interval arithmetic; this helper is intended for
    tests, schedules, and diagnostics.
    """

    n = int(dimension)
    width = _positive(sigma, "sigma")
    multiple = _positive(declared_multiple, "declared_multiple")
    h = 1.0 / n
    if width > 1.0:
        raise ValueError("sigma must not exceed the unit folded interval")
    if h >= width:
        raise ValueError("the theorem requires mesh < sigma")
    half_width = support_half_width(n, width, multiple)
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
        raise ValueError("the tail upper is not smaller than one")
    alpha = omitted_mass / (1.0 - omitted_mass)
    exp_square = exp_half * exp_half
    denominator_square = (width - h) ** 2
    omitted_square = (
        4.0
        * math.e
        * exp_square
        * (h + width / (2.0 * effective))
        / denominator_square
    )
    renormalization_square = (
        alpha
        * alpha
        * math.e
        * (4.0 * h + 2.0 * math.sqrt(math.pi) * width)
        / denominator_square
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
        omitted_frobenius_square_upper=omitted_square,
        renormalization_frobenius_square_upper=renormalization_square,
        two_norm_upper=math.sqrt(omitted_square + renormalization_square),
    )


def haar_cutoff_defect(coarse: CutoffBound, fine: CutoffBound) -> HaarCutoffDefect:
    """Propagate full-versus-cutoff errors through exact Haar coordinates."""

    if fine.dimension != 2 * coarse.dimension:
        raise ValueError("fine dimension must be twice the coarse dimension")
    if fine.sigma != coarse.sigma:
        raise ValueError("coarse and fine widths must agree")
    return HaarCutoffDefect(
        coarse_consistency=coarse.two_norm_upper + fine.two_norm_upper,
        coarse_to_detail=fine.two_norm_upper,
        detail_to_coarse=fine.two_norm_upper,
        detail_block=fine.two_norm_upper,
    )


def adaptive_cutoff_multiple(mesh: float, minimum: float = 5.0) -> float:
    """Return ``max(minimum, sqrt(4 log(1/h)))``."""

    h = _positive(mesh, "mesh")
    floor = _positive(minimum, "minimum")
    if h >= 1.0:
        raise ValueError("mesh must be smaller than one")
    return max(floor, math.sqrt(4.0 * math.log(1.0 / h)))
