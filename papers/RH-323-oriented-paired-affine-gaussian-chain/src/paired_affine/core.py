"""Exact formulas for the RH-323 oriented paired affine Gaussian chain."""

from __future__ import annotations

import math


SQRT_TWO = math.sqrt(2.0)
SQRT_TWO_PI = math.sqrt(2.0 * math.pi)

# Repository constants from RH-14 and RH-17--RH-18.
U_C = 1.5436890126920764
LAMBDA = 1.6785735104283224
ALPHA = 2.0 * U_C
KAPPA_AFF = ALPHA * LAMBDA
BETA = math.sqrt(1.0 + LAMBDA * LAMBDA)
S1 = math.sqrt(1.0 + ALPHA * ALPHA)
S2 = math.sqrt(KAPPA_AFF * KAPPA_AFF + BETA * BETA)


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


def _clearance(clearance_ratio: float) -> float:
    clearance_ratio = float(clearance_ratio)
    if clearance_ratio < 0.0:
        raise ValueError("clearance_ratio must be nonnegative")
    return clearance_ratio


def _physical_parameters(sigma: float, clearance_ratio: float) -> tuple[float, float]:
    sigma = float(sigma)
    clearance_ratio = _clearance(clearance_ratio)
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    scale = 1.0 / sigma
    if clearance_ratio > scale:
        raise ValueError("the Gaussian center lies outside [0, 1]")
    return scale, clearance_ratio


def inverse_mills_ratio(clearance_ratio: float) -> float:
    """Return ``phi(d) / Phi(d)``."""

    clearance_ratio = _clearance(clearance_ratio)
    return normal_pdf(clearance_ratio) / normal_cdf(clearance_ratio)


def halfline_density(value: float, clearance_ratio: float) -> float:
    """Return the entrance law ``phi(v-d) / Phi(d)`` on ``v >= 0``."""

    value = float(value)
    clearance_ratio = _clearance(clearance_ratio)
    if value < 0.0:
        return 0.0
    return normal_pdf(value - clearance_ratio) / normal_cdf(clearance_ratio)


def folded_endpoint_normalizer(sigma: float, clearance_ratio: float) -> float:
    """Return the exact physical folded-row normalizer from RH-322."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    return normal_cdf(ratio) - normal_survival(2.0 * scale - ratio)


def folded_endpoint_density(
    value: float,
    sigma: float,
    clearance_ratio: float,
) -> float:
    """Return the exact finite folded endpoint density in the ``v`` coordinate."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    value = float(value)
    if value < 0.0 or value > scale:
        return 0.0
    numerator = normal_pdf(value - ratio) + normal_pdf(2.0 * scale - value - ratio)
    return numerator / folded_endpoint_normalizer(sigma, ratio)


def exact_endpoint_l1_tail(sigma: float, clearance_ratio: float) -> float:
    """Return the exact RH-322 same-clearance entrance-row L1 error."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    return 2.0 * normal_survival(scale - ratio) / normal_cdf(ratio)


def first_leg_density(intermediate: float, entrance: float) -> float:
    """Return the density of ``U = -ALPHA * V - Z1`` conditional on ``V``."""

    return normal_pdf(float(intermediate) + ALPHA * float(entrance))


def second_leg_density(output: float, intermediate: float) -> float:
    """Return the density of ``W = -LAMBDA * U + Z2`` conditional on ``U``."""

    return normal_pdf(float(output) + LAMBDA * float(intermediate))


def collapsed_output_density(output: float, entrance: float) -> float:
    """Return the density of ``W = KAPPA_AFF * V + BETA * Z`` conditional on ``V``."""

    standardized = (float(output) - KAPPA_AFF * float(entrance)) / BETA
    return normal_pdf(standardized) / BETA


def oriented_joint_density(
    entrance: float,
    intermediate: float,
    output: float,
    clearance_ratio: float,
) -> float:
    """Return the limiting oriented joint density ``J_d(v,u,w)``."""

    return (
        halfline_density(entrance, clearance_ratio)
        * first_leg_density(intermediate, entrance)
        * second_leg_density(output, intermediate)
    )


def finite_oriented_joint_density(
    entrance: float,
    intermediate: float,
    output: float,
    sigma: float,
    clearance_ratio: float,
) -> float:
    """Return the affine chain seeded by the exact finite RH-322 entrance row."""

    return (
        folded_endpoint_density(entrance, sigma, clearance_ratio)
        * first_leg_density(intermediate, entrance)
        * second_leg_density(output, intermediate)
    )


def intermediate_density(intermediate: float, clearance_ratio: float) -> float:
    """Return the explicit extended-skew-normal marginal of ``U``."""

    clearance_ratio = _clearance(clearance_ratio)
    intermediate = float(intermediate)
    gaussian = normal_pdf((intermediate + ALPHA * clearance_ratio) / S1) / S1
    selection = normal_cdf((clearance_ratio - ALPHA * intermediate) / S1)
    return gaussian * selection / normal_cdf(clearance_ratio)


def output_density(output: float, clearance_ratio: float) -> float:
    """Return the explicit extended-skew-normal marginal of ``W``."""

    clearance_ratio = _clearance(clearance_ratio)
    output = float(output)
    gaussian = normal_pdf((output - KAPPA_AFF * clearance_ratio) / S2) / S2
    selection_argument = (
        KAPPA_AFF * output + BETA * BETA * clearance_ratio
    ) / (BETA * S2)
    return gaussian * normal_cdf(selection_argument) / normal_cdf(clearance_ratio)


def output_gaussian_reference_density(output: float, clearance_ratio: float) -> float:
    """Return the unconditioned Gaussian convolution used as a tail reference."""

    clearance_ratio = _clearance(clearance_ratio)
    return normal_pdf((float(output) - KAPPA_AFF * clearance_ratio) / S2) / S2


def output_reference_ratio(output: float, clearance_ratio: float) -> float:
    """Return ``q_d`` divided by its unconditioned Gaussian reference."""

    clearance_ratio = _clearance(clearance_ratio)
    argument = (
        KAPPA_AFF * float(output) + BETA * BETA * clearance_ratio
    ) / (BETA * S2)
    return normal_cdf(argument) / normal_cdf(clearance_ratio)


def output_tail_ratio_limit(clearance_ratio: float) -> float:
    """Return the positive-tail limit of ``q_d`` over its Gaussian reference."""

    clearance_ratio = _clearance(clearance_ratio)
    return 1.0 / normal_cdf(clearance_ratio)


def entrance_mean(clearance_ratio: float) -> float:
    """Return the mean of the half-line entrance law."""

    clearance_ratio = _clearance(clearance_ratio)
    return clearance_ratio + inverse_mills_ratio(clearance_ratio)


def entrance_variance(clearance_ratio: float) -> float:
    """Return the variance of the half-line entrance law."""

    clearance_ratio = _clearance(clearance_ratio)
    ratio = inverse_mills_ratio(clearance_ratio)
    return 1.0 - clearance_ratio * ratio - ratio * ratio


def mean_vector(clearance_ratio: float) -> tuple[float, float, float]:
    """Return ``E(V,U,W)`` for the oriented chain."""

    mean = entrance_mean(clearance_ratio)
    return (mean, -ALPHA * mean, KAPPA_AFF * mean)


def covariance_matrix(
    clearance_ratio: float,
) -> tuple[tuple[float, float, float], ...]:
    """Return the exact covariance matrix of ``(V,U,W)``."""

    variance = entrance_variance(clearance_ratio)
    vv = variance
    uu = ALPHA * ALPHA * variance + 1.0
    ww = KAPPA_AFF * KAPPA_AFF * variance + BETA * BETA
    vu = -ALPHA * variance
    vw = KAPPA_AFF * variance
    uw = -LAMBDA * uu
    return ((vv, vu, vw), (vu, uu, uw), (vw, uw, ww))


def conditioning_bias(clearance_ratio: float) -> tuple[float, float, float]:
    """Return the mean shift from centers ``(d,-ALPHA*d,KAPPA_AFF*d)``."""

    ratio = inverse_mills_ratio(clearance_ratio)
    return (ratio, -ALPHA * ratio, KAPPA_AFF * ratio)


def joint_l1_bound(
    sigma: float,
    clearance_ratio: float,
    limiting_ratio: float,
) -> float:
    """Return the RH-323 joint-chain L1 bound to phase ``limiting_ratio``."""

    limiting_ratio = _clearance(limiting_ratio)
    return abs(float(clearance_ratio) - limiting_ratio) + exact_endpoint_l1_tail(
        sigma, clearance_ratio
    )


def intermediate_positive_probability_at_zero() -> float:
    """Return ``P(U > 0)`` at clearance phase ``d = 0``."""

    return math.atan(1.0 / ALPHA) / math.pi


def output_negative_probability_at_zero() -> float:
    """Return ``P(W < 0)`` at clearance phase ``d = 0``."""

    return math.atan(BETA / KAPPA_AFF) / math.pi
