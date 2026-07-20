"""Strong--weak cutoff and Riesz-transfer ledgers for RH-55."""

from __future__ import annotations

from dataclasses import dataclass
import math


def _nonnegative(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def _positive(value: float, name: str) -> float:
    result = _nonnegative(value, name)
    if result == 0.0:
        raise ValueError(f"{name} must be positive")
    return result


@dataclass(frozen=True)
class SandwichDefect:
    """Three-term perturbation bound for ``T R_T(z) T``."""

    outer_left: float
    resolvent: float
    outer_right: float
    total: float


@dataclass(frozen=True)
class RieszDefect:
    """Projector and weighted-Riesz defects on one contour."""

    sandwich: SandwichDefect
    projector: float
    weighted: float


@dataclass(frozen=True)
class CutoffLedger:
    """Strong and weak norms induced by one row-tail upper."""

    omitted_mass: float
    weak_l1_to_l1: float
    strong_l1_to_bv: float
    strong_bv_to_bv: float
    weak_l1_to_l2: float


@dataclass(frozen=True)
class AdaptiveEnvelope:
    """Asymptotic cutoff envelope for one ``(h, sigma, kappa)`` triple."""

    mesh: float
    sigma: float
    kappa: float
    logarithm: float
    omitted_mass_envelope: float
    riesz_envelope: float
    normalized_by_sqrt_sigma: float


@dataclass(frozen=True)
class GaussianShapeEnvelope:
    """Shape-aware folded-Gaussian cutoff envelope."""

    mesh: float
    sigma: float
    kappa: float
    exponential_tail: float
    riesz_envelope: float
    normalized_by_sqrt_sigma: float


@dataclass(frozen=True)
class MidpointUlamLedger:
    """Second-order midpoint-to-Ulam comparison scales."""

    mesh: float
    sigma: float
    row_l1: float
    strong_bv: float
    inside_bulk_square_regime: bool


def sandwich_defect_upper(
    *,
    outer_weak_defect: float,
    reference_resolvent: float,
    reference_smoothing: float,
    perturbed_smoothing: float,
    perturbed_resolvent: float,
    strong_defect: float,
    strong_input_defect: float,
) -> SandwichDefect:
    """Bound ``||T R_T T - Ttilde R_Ttilde Ttilde||_(L1->L2)``.

    The decomposition changes, in order, the left outer operator, the
    resolvent, and the right outer operator.  Resolvents act on the strong
    space; the left outer factors provide the final L1-to-L2 smoothing.
    """

    rho = _nonnegative(outer_weak_defect, "outer_weak_defect")
    m = _nonnegative(reference_resolvent, "reference_resolvent")
    r = _nonnegative(reference_smoothing, "reference_smoothing")
    s = _nonnegative(perturbed_smoothing, "perturbed_smoothing")
    mt = _nonnegative(perturbed_resolvent, "perturbed_resolvent")
    tau1 = _nonnegative(strong_defect, "strong_defect")
    tau0 = _nonnegative(strong_input_defect, "strong_input_defect")
    left = rho * m * r
    resolvent = s * m * mt * tau1 * r
    right = s * mt * tau0
    return SandwichDefect(left, resolvent, right, left + resolvent + right)


def riesz_defect_upper(
    *,
    contour_length: float,
    minimum_modulus: float,
    sandwich: SandwichDefect,
) -> RieszDefect:
    """Integrate the sandwich defect for projector and weighted terms."""

    length = _positive(contour_length, "contour_length")
    radius = _positive(minimum_modulus, "minimum_modulus")
    base = length * sandwich.total / (2.0 * math.pi)
    return RieszDefect(
        sandwich=sandwich,
        projector=base / (radius * radius),
        weighted=base / radius,
    )


def cutoff_norm_ledger(mesh: float, omitted_mass: float) -> CutoffLedger:
    """Convert the exact twice-the-tail row identity into weak/BV norms.

    A cellwise-constant density with row L1 mass at most ``2 Q`` has L2 norm
    at most ``2 Q/sqrt(h)``.  The piecewise-BV inflation uses the conservative
    total-variation upper ``4 Q/h``.
    """

    h = _positive(mesh, "mesh")
    q = _nonnegative(omitted_mass, "omitted_mass")
    weak = 2.0 * q
    strong = weak + 4.0 * q / h
    return CutoffLedger(
        omitted_mass=q,
        weak_l1_to_l1=weak,
        strong_l1_to_bv=strong,
        strong_bv_to_bv=strong,
        weak_l1_to_l2=weak / math.sqrt(h),
    )


def adaptive_tail_envelope(
    mesh: float,
    sigma: float,
    kappa: float,
    *,
    constant: float = 1.0,
) -> AdaptiveEnvelope:
    """Evaluate ``Q <= C h^kappa/sqrt(log(1/h))`` and its Riesz envelope."""

    h = _positive(mesh, "mesh")
    width = _positive(sigma, "sigma")
    power = _positive(kappa, "kappa")
    coefficient = _positive(constant, "constant")
    if h >= 1.0:
        raise ValueError("mesh must be smaller than one")
    logarithm = math.log(1.0 / h)
    omitted = coefficient * h**power / math.sqrt(logarithm)
    riesz = omitted / (h * width**1.5)
    return AdaptiveEnvelope(
        mesh=h,
        sigma=width,
        kappa=power,
        logarithm=logarithm,
        omitted_mass_envelope=omitted,
        riesz_envelope=riesz,
        normalized_by_sqrt_sigma=riesz / math.sqrt(width),
    )


def critical_kappa_for_mesh_power(mesh_power: float) -> float:
    """Return the generic mass-only threshold ``1 + 3/(2p)``."""

    power = _positive(mesh_power, "mesh_power")
    return 1.0 + 1.5 / power


def gaussian_shape_envelope(
    mesh: float,
    sigma: float,
    kappa: float,
    *,
    constant: float = 1.0,
) -> GaussianShapeEnvelope:
    """Evaluate the shape-aware envelope ``C h^kappa sigma^(-5/2)``.

    For ``L_kappa=sqrt(2 kappa log(1/h))``, the Gaussian boundary height is
    exactly ``exp(-L_kappa^2/2)=h^kappa``.  Target variation, rather than a
    distribution-free cell jump estimate, removes the artificial ``1/h``.
    """

    h = _positive(mesh, "mesh")
    width = _positive(sigma, "sigma")
    power = _positive(kappa, "kappa")
    coefficient = _positive(constant, "constant")
    if h >= 1.0:
        raise ValueError("mesh must be smaller than one")
    tail = h**power
    riesz = coefficient * tail / width**2.5
    return GaussianShapeEnvelope(
        mesh=h,
        sigma=width,
        kappa=power,
        exponential_tail=tail,
        riesz_envelope=riesz,
        normalized_by_sqrt_sigma=riesz / math.sqrt(width),
    )


def gaussian_shape_critical_kappa(mesh_power: float) -> float:
    """Return the Gaussian shape-aware threshold ``5/(2p)``."""

    power = _positive(mesh_power, "mesh_power")
    return 2.5 / power


def rh39_omitted_mass_upper(
    mesh: float,
    sigma: float,
    declared_multiple: float,
) -> float:
    """Evaluate the exact RH-39 Mills-ratio row-tail upper."""

    h = _positive(mesh, "mesh")
    width = _positive(sigma, "sigma")
    multiple = _positive(declared_multiple, "declared_multiple")
    if h >= width:
        raise ValueError("the RH-39 bound requires mesh < sigma")
    half_width = math.ceil(multiple * width / h) + 2
    effective = half_width * h / width
    return (
        2.0
        * math.sqrt(math.e)
        * math.exp(-0.5 * effective * effective)
        * (h + width / effective)
        / (width - h)
    )


def midpoint_ulam_ledger(
    mesh: float,
    sigma: float,
    *,
    row_constant: float = 1.0,
    strong_constant: float = 1.0,
) -> MidpointUlamLedger:
    """Record the midpoint quadrature scales ``h^2 sigma^-2`` and ``h sigma^-2``."""

    h = _positive(mesh, "mesh")
    width = _positive(sigma, "sigma")
    row = _positive(row_constant, "row_constant") * h * h / (width * width)
    strong = _positive(strong_constant, "strong_constant") * h / (
        width * width
    )
    return MidpointUlamLedger(
        mesh=h,
        sigma=width,
        row_l1=row,
        strong_bv=strong,
        inside_bulk_square_regime=h / (width * width) < 1.0,
    )
