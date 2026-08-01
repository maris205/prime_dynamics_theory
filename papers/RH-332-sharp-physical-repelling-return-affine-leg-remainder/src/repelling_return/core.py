"""Exact formulas for the RH-332 physical repelling-return row."""

from __future__ import annotations

import math
from collections.abc import Callable


SQRT_TWO = math.sqrt(2.0)
SQRT_TWO_PI = math.sqrt(2.0 * math.pi)

U_C = 1.5436890126920764
R_FIXED = U_C - 1.0
LAMBDA = 2.0 * U_C * R_FIXED
ALPHA = 2.0 * U_C
CRITICAL_PARTITION = U_C**-0.5
CURVATURE_L1_SLOPE = math.sqrt(2.0 / math.pi) * U_C
TRACE_RADIUS = 1.4


def normal_pdf(value: float) -> float:
    """Return the standard normal density."""

    value = float(value)
    return math.exp(-0.5 * value * value) / SQRT_TWO_PI


def normal_cdf(value: float) -> float:
    """Return the standard normal distribution function."""

    return 0.5 * math.erfc(-float(value) / SQRT_TWO)


def normal_survival(value: float) -> float:
    """Return the standard normal upper-tail probability."""

    return 0.5 * math.erfc(float(value) / SQRT_TWO)


def _positive_sigma(sigma: float) -> float:
    sigma = float(sigma)
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    return sigma


def _nonnegative_phase(phase: float) -> float:
    phase = float(phase)
    if phase < 0.0:
        raise ValueError("the clearance phase must be nonnegative")
    return phase


def deterministic_map(value: float) -> float:
    """Return the quadratic map ``f(x)=1-U_C*x**2``."""

    value = float(value)
    return 1.0 - U_C * value * value


def state_interval(sigma: float) -> tuple[float, float]:
    """Return the scaled physical interval about the repelling point."""

    sigma = _positive_sigma(sigma)
    return (-R_FIXED / sigma, (1.0 - R_FIXED) / sigma)


def _physical_repelling_coordinate(sigma: float, source: float) -> tuple[float, float]:
    sigma = _positive_sigma(sigma)
    source = float(source)
    lower, upper = state_interval(sigma)
    if source < lower or source > upper:
        raise ValueError("source must represent a physical point in [0, 1]")
    return sigma, source


def physical_row_normalizer_at_x(sigma: float, source_x: float) -> float:
    """Return the exact folded-row state normalizer at a physical source."""

    sigma = _positive_sigma(sigma)
    source_x = float(source_x)
    if source_x < 0.0 or source_x > 1.0:
        raise ValueError("source_x must lie in [0, 1]")
    image = deterministic_map(source_x)
    return (
        1.0
        - normal_survival((1.0 - image) / sigma)
        - normal_survival((1.0 + image) / sigma)
    )


def repelling_displacement(sigma: float, source: float) -> float:
    """Return ``d_sigma(u)=lambda*u+U_C*sigma*u**2``."""

    sigma, source = _physical_repelling_coordinate(sigma, source)
    return LAMBDA * source + U_C * sigma * source * source


def physical_second_row_density(output: float, sigma: float, source: float) -> float:
    """Return ``sigma*P_sigma(r+sigma*u,r+sigma*w)`` exactly."""

    sigma, source = _physical_repelling_coordinate(sigma, source)
    output = float(output)
    lower, upper = state_interval(sigma)
    if output < lower or output > upper:
        return 0.0
    displacement = repelling_displacement(sigma, source)
    normalizer = physical_row_normalizer_at_x(sigma, R_FIXED + sigma * source)
    return (
        normal_pdf(output + displacement)
        + normal_pdf(output + 2.0 * R_FIXED / sigma - displacement)
    ) / normalizer


def curved_second_density(output: float, sigma: float, source: float) -> float:
    """Return the full-line Gaussian at the exact quadratic image."""

    displacement = repelling_displacement(sigma, source)
    return normal_pdf(float(output) + displacement)


def tangent_second_density(output: float, source: float) -> float:
    """Return the RH-323 tangent row ``phi(w+lambda*u)``."""

    return normal_pdf(float(output) + LAMBDA * float(source))


def gaussian_shift_l1(displacement: float) -> float:
    """Return the unhalved L1 distance between shifted unit Gaussians."""

    return 4.0 * normal_cdf(0.5 * abs(float(displacement))) - 2.0


def exact_curved_boundary_l1(sigma: float, source: float) -> float:
    """Return the exact physical-second-row distance to its curved Gaussian."""

    sigma, source = _physical_repelling_coordinate(sigma, source)
    displacement = repelling_displacement(sigma, source)
    return 2.0 * (
        normal_survival(R_FIXED / sigma - displacement)
        + normal_survival((1.0 - R_FIXED) / sigma + displacement)
    )


def exact_curvature_shift_l1(sigma: float, source: float) -> float:
    """Return the exact curved-to-tangent second-row L1 distance."""

    sigma, source = _physical_repelling_coordinate(sigma, source)
    return gaussian_shift_l1(U_C * sigma * source * source)


def physical_tangent_triangle_bounds(sigma: float, source: float) -> tuple[float, float]:
    """Return reverse/forward triangle bounds for the physical tangent error."""

    boundary = exact_curved_boundary_l1(sigma, source)
    curvature = exact_curvature_shift_l1(sigma, source)
    return (max(0.0, curvature - boundary), min(2.0, curvature + boundary))


def fixed_row_linear_coefficient(source: float) -> float:
    """Return the sharp fixed-source coefficient of the second-row error."""

    source = float(source)
    return CURVATURE_L1_SLOPE * source * source


def endpoint_curved_parameter(sigma: float, entrance: float) -> float:
    """Return the RH-324 first-leg curved parameter."""

    sigma = _positive_sigma(sigma)
    entrance = float(entrance)
    if entrance < 0.0 or entrance > 1.0 / sigma:
        raise ValueError("entrance must represent a physical point in [0, 1]")
    return ALPHA * entrance - U_C * sigma * entrance * entrance


def folded_seed_normalizer(sigma: float, phase: float) -> float:
    """Return the exact RH-322/RH-324 finite entrance normalizer."""

    sigma = _positive_sigma(sigma)
    phase = _nonnegative_phase(phase)
    scale = 1.0 / sigma
    if phase > scale:
        raise ValueError("phase must lie inside the finite entrance interval")
    return normal_cdf(phase) - normal_survival(2.0 * scale - phase)


def folded_seed_density(entrance: float, sigma: float, phase: float) -> float:
    """Return the exact finite RH-324 entrance density."""

    sigma = _positive_sigma(sigma)
    phase = _nonnegative_phase(phase)
    scale = 1.0 / sigma
    if phase > scale:
        raise ValueError("phase must lie inside the finite entrance interval")
    entrance = float(entrance)
    if entrance < 0.0 or entrance > scale:
        return 0.0
    return (
        normal_pdf(entrance - phase)
        + normal_pdf(2.0 * scale - entrance - phase)
    ) / folded_seed_normalizer(sigma, phase)


def physical_first_row_density(output: float, sigma: float, entrance: float) -> float:
    """Return the exact RH-324 endpoint-to-repelling physical row."""

    sigma = _positive_sigma(sigma)
    entrance = float(entrance)
    if entrance < 0.0 or entrance > 1.0 / sigma:
        raise ValueError("entrance must represent a physical point in [0, 1]")
    output = float(output)
    lower, upper = state_interval(sigma)
    if output < lower or output > upper:
        return 0.0
    source_x = 1.0 - sigma * entrance
    image = deterministic_map(source_x)
    return (
        normal_pdf(output + (R_FIXED - image) / sigma)
        + normal_pdf(output + (R_FIXED + image) / sigma)
    ) / physical_row_normalizer_at_x(sigma, source_x)


def limiting_intermediate_density(source: float, phase: float) -> float:
    """Return the RH-323 affine U-marginal density ``p_d``."""

    source = float(source)
    phase = _nonnegative_phase(phase)
    scale = math.sqrt(1.0 + ALPHA * ALPHA)
    return (
        normal_pdf((source + ALPHA * phase) / scale)
        * normal_cdf((phase - ALPHA * source) / scale)
        / (scale * normal_cdf(phase))
    )


def inverse_mills_ratio(phase: float) -> float:
    """Return ``phi(d)/Phi(d)`` for a nonnegative phase."""

    phase = _nonnegative_phase(phase)
    return normal_pdf(phase) / normal_cdf(phase)


def entrance_second_moment(phase: float) -> float:
    """Return the second moment of the half-line entrance variable V."""

    phase = _nonnegative_phase(phase)
    return phase * phase + 1.0 + phase * inverse_mills_ratio(phase)


def total_intermediate_second_moment(phase: float) -> float:
    """Return ``E[U**2]`` in the RH-323 affine first-leg law."""

    return 1.0 + ALPHA * ALPHA * entrance_second_moment(phase)


def total_transported_linear_coefficient(phase: float) -> float:
    """Return the sharp total second-hybrid-row coefficient."""

    return CURVATURE_L1_SLOPE * total_intermediate_second_moment(phase)


def composite_simpson(
    function: Callable[[float], float], lower: float, upper: float, intervals: int = 20000
) -> float:
    """Integrate a scalar function by deterministic composite Simpson quadrature."""

    if intervals <= 0:
        raise ValueError("intervals must be positive")
    if intervals % 2:
        intervals += 1
    step = (upper - lower) / intervals
    total = function(lower) + function(upper)
    total += 4.0 * sum(function(lower + step * j) for j in range(1, intervals, 2))
    total += 2.0 * sum(function(lower + step * j) for j in range(2, intervals, 2))
    return total * step / 3.0


def sector_intermediate_second_moment(
    phase: float, *, positive: bool, cutoff: float = 32.0, intervals: int = 32000
) -> float:
    """Quadrature for ``int_{+/- u>0} u**2 p_d(u) du``."""

    phase = _nonnegative_phase(phase)
    cutoff = float(cutoff)
    if cutoff <= 0.0:
        raise ValueError("cutoff must be positive")
    lower, upper = (0.0, cutoff) if positive else (-cutoff, 0.0)
    return composite_simpson(
        lambda source: source
        * source
        * limiting_intermediate_density(source, phase),
        lower,
        upper,
        intervals,
    )


def sector_transported_linear_coefficient(
    phase: float, *, positive: bool, cutoff: float = 32.0, intervals: int = 32000
) -> float:
    """Return the positive/negative-orientation sharp coefficient."""

    return CURVATURE_L1_SLOPE * sector_intermediate_second_moment(
        phase, positive=positive, cutoff=cutoff, intervals=intervals
    )


def sector_curvature_proxy(
    sigma: float,
    phase: float,
    *,
    positive: bool,
    cutoff: float = 32.0,
    intervals: int = 32000,
) -> float:
    """Average the exact curved-to-tangent distance against ``p_d``."""

    sigma = _positive_sigma(sigma)
    phase = _nonnegative_phase(phase)
    lower, upper = (0.0, cutoff) if positive else (-cutoff, 0.0)
    return composite_simpson(
        lambda source: limiting_intermediate_density(source, phase)
        * gaussian_shift_l1(U_C * sigma * source * source),
        lower,
        upper,
        intervals,
    )


def critical_partition_source(sigma: float) -> float:
    """Return the repelling coordinate whose physical point is ``x=b``."""

    sigma = _positive_sigma(sigma)
    return (CRITICAL_PARTITION - R_FIXED) / sigma


def critical_partition_obstruction_lower_bound(sigma: float) -> float:
    """Return the reverse-triangle lower bound at the global source ``x=b``."""

    source = critical_partition_source(sigma)
    return physical_tangent_triangle_bounds(sigma, source)[0]


def alias_scale_exponent(radius: float = TRACE_RADIUS) -> float:
    """Return ``log(radius)/log(lambda)`` on the first-alias clock."""

    radius = float(radius)
    if radius <= 1.0:
        raise ValueError("radius must exceed one")
    return math.log(radius) / math.log(LAMBDA)
