"""Exact half-line formulas for one critical folded Gaussian row."""

from __future__ import annotations

import math


SQRT_TWO = math.sqrt(2.0)
SQRT_TWO_PI = math.sqrt(2.0 * math.pi)


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


def _physical_parameters(sigma: float, clearance_ratio: float) -> tuple[float, float]:
    sigma = float(sigma)
    clearance_ratio = float(clearance_ratio)
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    if clearance_ratio < 0.0:
        raise ValueError("clearance_ratio must be nonnegative")
    scale = 1.0 / sigma
    if clearance_ratio > scale:
        raise ValueError("the Gaussian center lies outside [0, 1]")
    return scale, clearance_ratio


def direct_normalizer(sigma: float, clearance_ratio: float) -> float:
    """Mass of the direct positive Gaussian lobe retained by ``[0, 1]``."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    return normal_cdf(ratio) - normal_survival(scale - ratio)


def reflected_lobe_mass(sigma: float, clearance_ratio: float) -> float:
    """Mass contributed by folding the negative Gaussian lobe."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    return normal_survival(scale - ratio) - normal_survival(2.0 * scale - ratio)


def folded_normalizer(sigma: float, clearance_ratio: float) -> float:
    """Exact normalizer of the physical folded row on ``[0, 1]``."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    return normal_cdf(ratio) - normal_survival(2.0 * scale - ratio)


def halfline_density(value: float, clearance_ratio: float) -> float:
    """Return ``phi(v-a)/Phi(a)`` on the limiting half-line."""

    value = float(value)
    clearance_ratio = float(clearance_ratio)
    if clearance_ratio < 0.0:
        raise ValueError("clearance_ratio must be nonnegative")
    if value < 0.0:
        return 0.0
    return normal_pdf(value - clearance_ratio) / normal_cdf(clearance_ratio)


def direct_density(value: float, sigma: float, clearance_ratio: float) -> float:
    """Return the rescaled direct-lobe density on ``[0, 1/sigma]``."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    value = float(value)
    if value < 0.0 or value > scale:
        return 0.0
    return normal_pdf(value - ratio) / direct_normalizer(sigma, ratio)


def folded_density(value: float, sigma: float, clearance_ratio: float) -> float:
    """Return the rescaled density of the exact physical folded row."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    value = float(value)
    if value < 0.0 or value > scale:
        return 0.0
    numerator = normal_pdf(value - ratio) + normal_pdf(2.0 * scale - value - ratio)
    return numerator / folded_normalizer(sigma, ratio)


def exact_l1_tail(sigma: float, clearance_ratio: float) -> float:
    """Exact L1 error from either finite row to its same-ratio half-line row."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    return 2.0 * normal_survival(scale - ratio) / normal_cdf(ratio)


def exact_tv_tail(sigma: float, clearance_ratio: float) -> float:
    """Exact total variation under the convention ``TV = L1 / 2``."""

    return 0.5 * exact_l1_tail(sigma, clearance_ratio)


def l1_bound_to_limit(
    sigma: float,
    clearance_ratio: float,
    limiting_ratio: float,
) -> float:
    """Return the theorem's L1 bound to the profile with parameter ``d``."""

    limiting_ratio = float(limiting_ratio)
    if limiting_ratio < 0.0:
        raise ValueError("limiting_ratio must be nonnegative")
    return abs(float(clearance_ratio) - limiting_ratio) + exact_l1_tail(
        sigma, clearance_ratio
    )


def compact_mills_l1_bound(
    sigma: float,
    clearance_ratio: float,
    *,
    minimum_ratio: float,
    maximum_ratio: float,
) -> float:
    """Uniform Mills upper bound for a prescribed compact ratio interval."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    minimum_ratio = float(minimum_ratio)
    maximum_ratio = float(maximum_ratio)
    if not 0.0 <= minimum_ratio <= ratio <= maximum_ratio:
        raise ValueError("clearance_ratio is outside the prescribed interval")
    gap = scale - maximum_ratio
    if gap <= 0.0:
        raise ValueError("the ratio interval must lie below 1/sigma")
    return 2.0 * normal_pdf(gap) / (normal_cdf(minimum_ratio) * gap)


def inverse_mills_ratio(clearance_ratio: float) -> float:
    """Return ``phi(a) / Phi(a)`` for a physical clearance ratio."""

    clearance_ratio = float(clearance_ratio)
    if clearance_ratio < 0.0:
        raise ValueError("clearance_ratio must be nonnegative")
    return normal_pdf(clearance_ratio) / normal_cdf(clearance_ratio)


def limit_mean(clearance_ratio: float) -> float:
    """Return the first moment of the limiting half-line profile."""

    clearance_ratio = float(clearance_ratio)
    return clearance_ratio + inverse_mills_ratio(clearance_ratio)


def limit_second_moment(clearance_ratio: float) -> float:
    """Return the second raw moment of the limiting half-line profile."""

    clearance_ratio = float(clearance_ratio)
    ratio = inverse_mills_ratio(clearance_ratio)
    return clearance_ratio * clearance_ratio + 1.0 + clearance_ratio * ratio


def limit_variance(clearance_ratio: float) -> float:
    """Return the variance of the limiting half-line profile."""

    clearance_ratio = float(clearance_ratio)
    ratio = inverse_mills_ratio(clearance_ratio)
    return 1.0 - clearance_ratio * ratio - ratio * ratio


def limit_moments(clearance_ratio: float, maximum_order: int) -> tuple[float, ...]:
    """Return raw moments through ``maximum_order`` using the exact recurrence."""

    clearance_ratio = float(clearance_ratio)
    maximum_order = int(maximum_order)
    if clearance_ratio < 0.0:
        raise ValueError("clearance_ratio must be nonnegative")
    if maximum_order < 0:
        raise ValueError("maximum_order must be nonnegative")
    moments = [1.0]
    if maximum_order == 0:
        return tuple(moments)
    moments.append(limit_mean(clearance_ratio))
    for order in range(1, maximum_order):
        moments.append(clearance_ratio * moments[order] + order * moments[order - 1])
    return tuple(moments)


def limit_cdf(value: float, clearance_ratio: float) -> float:
    """Return the distribution function of a limiting half-line profile."""

    value = float(value)
    clearance_ratio = float(clearance_ratio)
    if clearance_ratio < 0.0:
        raise ValueError("clearance_ratio must be nonnegative")
    if value <= 0.0:
        return 0.0
    numerator = normal_cdf(value - clearance_ratio) - normal_survival(clearance_ratio)
    return min(1.0, max(0.0, numerator / normal_cdf(clearance_ratio)))


def limit_l1_distance(first_ratio: float, second_ratio: float) -> float:
    """Return the exact L1 distance between two limiting profiles."""

    first_ratio = float(first_ratio)
    second_ratio = float(second_ratio)
    if first_ratio < 0.0 or second_ratio < 0.0:
        raise ValueError("clearance ratios must be nonnegative")
    if first_ratio == second_ratio:
        return 0.0
    crossing = 0.5 * (first_ratio + second_ratio) + (
        math.log(normal_cdf(first_ratio)) - math.log(normal_cdf(second_ratio))
    ) / (first_ratio - second_ratio)
    return 2.0 * abs(
        limit_cdf(crossing, first_ratio) - limit_cdf(crossing, second_ratio)
    )


def direct_mean(sigma: float, clearance_ratio: float) -> float:
    """Return the exact first moment of the finite direct-lobe row."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    gap = scale - ratio
    return ratio + (normal_pdf(ratio) - normal_pdf(gap)) / direct_normalizer(
        sigma, ratio
    )


def direct_second_moment(sigma: float, clearance_ratio: float) -> float:
    """Return the exact second raw moment of the finite direct-lobe row."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    gap = scale - ratio
    correction = ratio * normal_pdf(ratio) - (scale + ratio) * normal_pdf(gap)
    return ratio * ratio + 1.0 + correction / direct_normalizer(sigma, ratio)


def direct_wasserstein_tail(sigma: float, clearance_ratio: float) -> float:
    """Return the exact W1 distance to the same-ratio half-line profile."""

    scale, ratio = _physical_parameters(sigma, clearance_ratio)
    gap = scale - ratio
    tail = normal_survival(gap)
    numerator = normal_pdf(gap) - inverse_mills_ratio(ratio) * tail
    return numerator / direct_normalizer(sigma, ratio)
