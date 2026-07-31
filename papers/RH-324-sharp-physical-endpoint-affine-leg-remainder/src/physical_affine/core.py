"""Sharp physical-to-affine formulas for the RH-324 endpoint leg."""

from __future__ import annotations

import math


SQRT_TWO = math.sqrt(2.0)
SQRT_TWO_PI = math.sqrt(2.0 * math.pi)

U_C = 1.5436890126920764
R_FIXED = U_C - 1.0
LAMBDA = 2.0 * U_C * R_FIXED
ALPHA = 2.0 * U_C
CRITICAL_PARTITION = U_C ** -0.5
CANONICAL_ETA = 0.5 * (1.0 - CRITICAL_PARTITION)
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


def _clearance(clearance_ratio: float) -> float:
    clearance_ratio = float(clearance_ratio)
    if clearance_ratio < 0.0:
        raise ValueError("clearance_ratio must be nonnegative")
    return clearance_ratio


def _physical_input(sigma: float, entrance: float) -> tuple[float, float]:
    sigma = _positive_sigma(sigma)
    entrance = float(entrance)
    if entrance < 0.0 or entrance > 1.0 / sigma:
        raise ValueError("entrance must represent a point in [0, 1]")
    return sigma, entrance


def deterministic_map(value: float) -> float:
    """Return ``1 - U_C * value**2``."""

    value = float(value)
    return 1.0 - U_C * value * value


def endpoint_source(sigma: float, entrance: float) -> float:
    """Return the physical source point ``x = 1 - sigma*v``."""

    sigma, entrance = _physical_input(sigma, entrance)
    return 1.0 - sigma * entrance


def output_coordinate_interval(sigma: float) -> tuple[float, float]:
    """Return the physical ``u=(y-r)/sigma`` state interval."""

    sigma = _positive_sigma(sigma)
    return (-R_FIXED / sigma, (1.0 - R_FIXED) / sigma)


def physical_row_normalizer(sigma: float, entrance: float) -> float:
    """Return the exact folded row normalizer for the endpoint source."""

    sigma, entrance = _physical_input(sigma, entrance)
    image = deterministic_map(1.0 - sigma * entrance)
    return (
        1.0
        - normal_survival((1.0 - image) / sigma)
        - normal_survival((1.0 + image) / sigma)
    )


def physical_row_density(output: float, sigma: float, entrance: float) -> float:
    """Return the exact rescaled folded physical first-leg density."""

    sigma, entrance = _physical_input(sigma, entrance)
    output = float(output)
    lower, upper = output_coordinate_interval(sigma)
    if output < lower or output > upper:
        return 0.0
    image = deterministic_map(1.0 - sigma * entrance)
    first = normal_pdf(output + (R_FIXED - image) / sigma)
    second = normal_pdf(output + (R_FIXED + image) / sigma)
    return (first + second) / physical_row_normalizer(sigma, entrance)


def curved_parameter(sigma: float, entrance: float) -> float:
    """Return ``alpha*v - U_C*sigma*v**2`` for the exact quadratic image."""

    sigma, entrance = _physical_input(sigma, entrance)
    return ALPHA * entrance - U_C * sigma * entrance * entrance


def curved_gaussian_density(output: float, sigma: float, entrance: float) -> float:
    """Return the full Gaussian centered at the exact curved folded image."""

    return normal_pdf(float(output) + curved_parameter(sigma, entrance))


def tangent_gaussian_density(output: float, entrance: float) -> float:
    """Return the RH-323 tangent density ``phi(u + alpha*v)``."""

    return normal_pdf(float(output) + ALPHA * float(entrance))


def endpoint_branch_margin(eta: float = CANONICAL_ETA) -> float:
    """Return the minimum folded-image distance from zero on ``sigma*v <= eta``."""

    eta = float(eta)
    if eta <= 0.0 or eta >= 1.0 - CRITICAL_PARTITION:
        raise ValueError("eta must lie strictly inside the endpoint branch")
    return U_C * (1.0 - eta) ** 2 - 1.0


def exact_curved_boundary_l1(sigma: float, entrance: float) -> float:
    """Return the exact physical-row L1 error to its full curved Gaussian."""

    sigma, entrance = _physical_input(sigma, entrance)
    source = 1.0 - sigma * entrance
    if source < CRITICAL_PARTITION:
        raise ValueError("the source has left the negative endpoint branch")
    parameter = curved_parameter(sigma, entrance)
    return 2.0 * (
        normal_survival(R_FIXED / sigma - parameter)
        + normal_survival((1.0 - R_FIXED) / sigma + parameter)
    )


def gaussian_shift_l1(displacement: float) -> float:
    """Return the exact L1 distance of unit Gaussians separated by ``displacement``."""

    displacement = abs(float(displacement))
    return 4.0 * normal_cdf(0.5 * displacement) - 2.0


def curvature_shift_l1(sigma: float, entrance: float) -> float:
    """Return the exact curved-to-tangent Gaussian L1 distance."""

    sigma = _positive_sigma(sigma)
    entrance = float(entrance)
    if entrance < 0.0:
        raise ValueError("entrance must be nonnegative")
    return gaussian_shift_l1(U_C * sigma * entrance * entrance)


def row_tangent_l1_bound(sigma: float, entrance: float) -> float:
    """Return the rowwise triangle bound from the physical row to the tangent row."""

    return exact_curved_boundary_l1(sigma, entrance) + curvature_shift_l1(
        sigma, entrance
    )


def halfline_density(value: float, clearance_ratio: float) -> float:
    """Return the RH-322 limiting endpoint density."""

    value = float(value)
    clearance_ratio = _clearance(clearance_ratio)
    if value < 0.0:
        return 0.0
    return normal_pdf(value - clearance_ratio) / normal_cdf(clearance_ratio)


def folded_seed_normalizer(sigma: float, clearance_ratio: float) -> float:
    """Return the exact RH-322 folded entrance-row normalizer."""

    sigma = _positive_sigma(sigma)
    clearance_ratio = _clearance(clearance_ratio)
    scale = 1.0 / sigma
    if clearance_ratio > scale:
        raise ValueError("the Gaussian center lies outside [0, 1]")
    return normal_cdf(clearance_ratio) - normal_survival(2.0 * scale - clearance_ratio)


def folded_seed_density(value: float, sigma: float, clearance_ratio: float) -> float:
    """Return the exact finite RH-322 entrance density."""

    sigma = _positive_sigma(sigma)
    clearance_ratio = _clearance(clearance_ratio)
    scale = 1.0 / sigma
    if clearance_ratio > scale:
        raise ValueError("the Gaussian center lies outside [0, 1]")
    value = float(value)
    if value < 0.0 or value > scale:
        return 0.0
    numerator = normal_pdf(value - clearance_ratio) + normal_pdf(
        2.0 * scale - value - clearance_ratio
    )
    return numerator / folded_seed_normalizer(sigma, clearance_ratio)


def exact_seed_l1_tail(sigma: float, clearance_ratio: float) -> float:
    """Return the exact finite entrance-row L1 error from RH-322."""

    sigma = _positive_sigma(sigma)
    clearance_ratio = _clearance(clearance_ratio)
    scale = 1.0 / sigma
    if clearance_ratio > scale:
        raise ValueError("the Gaussian center lies outside [0, 1]")
    return 2.0 * normal_survival(scale - clearance_ratio) / normal_cdf(
        clearance_ratio
    )


def inverse_mills_ratio(clearance_ratio: float) -> float:
    """Return ``phi(a)/Phi(a)``."""

    clearance_ratio = _clearance(clearance_ratio)
    return normal_pdf(clearance_ratio) / normal_cdf(clearance_ratio)


def entrance_second_moment(clearance_ratio: float) -> float:
    """Return the second moment of the RH-322 half-line entrance law."""

    clearance_ratio = _clearance(clearance_ratio)
    return (
        clearance_ratio * clearance_ratio
        + 1.0
        + clearance_ratio * inverse_mills_ratio(clearance_ratio)
    )


def remainder_components(
    sigma: float,
    clearance_ratio: float,
    *,
    eta: float = CANONICAL_ETA,
) -> dict[str, float]:
    """Return the explicit finite-seed physical-to-affine joint bound components."""

    sigma = _positive_sigma(sigma)
    clearance_ratio = _clearance(clearance_ratio)
    if clearance_ratio > 1.0 / sigma:
        raise ValueError("the Gaussian center lies outside [0, 1]")
    margin = endpoint_branch_margin(eta)
    curvature = CURVATURE_L1_SLOPE * sigma * entrance_second_moment(
        clearance_ratio
    )
    boundary = 2.0 * (
        normal_survival(margin / sigma)
        + normal_survival((1.0 - R_FIXED) / sigma)
    )
    bad_branch = (
        2.0
        * normal_survival(float(eta) / sigma - clearance_ratio)
        / normal_cdf(clearance_ratio)
    )
    seed = exact_seed_l1_tail(sigma, clearance_ratio)
    return {
        "curvature": curvature,
        "physical_boundary": boundary,
        "bad_branch": bad_branch,
        "finite_seed": seed,
    }


def finite_joint_l1_bound(
    sigma: float,
    clearance_ratio: float,
    limiting_ratio: float,
    *,
    eta: float = CANONICAL_ETA,
) -> float:
    """Return the RH-324 physical first-leg joint L1 bound."""

    limiting_ratio = _clearance(limiting_ratio)
    components = remainder_components(sigma, clearance_ratio, eta=eta)
    return abs(float(clearance_ratio) - limiting_ratio) + sum(components.values())


def sharp_linear_coefficient(clearance_ratio: float) -> float:
    """Return the positive coefficient of the phase-matched joint L1 remainder."""

    return CURVATURE_L1_SLOPE * entrance_second_moment(clearance_ratio)


def alias_scale_exponent(radius: float = TRACE_RADIUS) -> float:
    """Return ``log(radius)/log(lambda)`` at the first-alias clock."""

    radius = float(radius)
    if radius <= 1.0:
        raise ValueError("radius must exceed one")
    return math.log(radius) / math.log(LAMBDA)


def physical_joint_density(
    entrance: float,
    output: float,
    sigma: float,
    clearance_ratio: float,
) -> float:
    """Return the exact finite physical first-leg joint density."""

    return folded_seed_density(entrance, sigma, clearance_ratio) * physical_row_density(
        output, sigma, entrance
    )


def affine_joint_density(
    entrance: float,
    output: float,
    clearance_ratio: float,
) -> float:
    """Return the limiting phase-indexed affine first-leg joint density."""

    return halfline_density(entrance, clearance_ratio) * tangent_gaussian_density(
        output, entrance
    )
