"""Exact finite-prefix formulas for the RH-333 raw affine escape obstruction."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math

import mpmath as mp


# The ordinary decimals below reproduce archived evaluations.  The theorem
# keeps C_b and C_M symbolic and does not use these as interval certificates.
U_C = 1.5436890126920764
R_FIXED = U_C - 1.0
LAMBDA = 2.0 * U_C * R_FIXED
C_B_REPRODUCTION = 0.4608051492217
C_M_REPRODUCTION = 1.946342905200967
TRACE_RADIUS = 1.4


@dataclass(frozen=True)
class CriticalConstants:
    """High-precision constants for ``f(x)=1-u*x**2``."""

    u: mp.mpf
    r: mp.mpf
    lambda_fixed: mp.mpf


@dataclass(frozen=True)
class BoundaryCycle:
    """The RH-17 component-time boundary cycle in forward ``S=f**2`` order."""

    component_period: int
    physical_period: int
    point: mp.mpf
    clearance: mp.mpf
    orbit: tuple[mp.mpf, ...]
    signed_slopes: tuple[mp.mpf, ...]
    noise_standard_deviations: tuple[mp.mpf, ...]
    multiplier: mp.mpf
    decimal_digits: int


@lru_cache(maxsize=16)
def critical_constants(decimal_digits: int = 100) -> CriticalConstants:
    """Return the algebraic map constants at controlled working precision."""

    decimal_digits = int(decimal_digits)
    if decimal_digits < 50:
        raise ValueError("decimal_digits must be at least fifty")
    with mp.workdps(decimal_digits):
        u = mp.findroot(
            lambda value: value**3 - 2 * value**2 + 2 * value - 2,
            (mp.mpf("1.5"), mp.mpf("1.6")),
        )
        r = u - 1
        return CriticalConstants(u=+u, r=+r, lambda_fixed=+(2 * u * r))


def _cycle_maps(constants: CriticalConstants):
    u = constants.u

    def f_map(value: mp.mpf) -> mp.mpf:
        return 1 - u * value**2

    def positive_inverse(value: mp.mpf) -> mp.mpf:
        return mp.sqrt((1 - value) / u)

    def negative_inverse(value: mp.mpf) -> mp.mpf:
        return -positive_inverse(value)

    def h_map(value: mp.mpf) -> mp.mpf:
        return positive_inverse(positive_inverse(value))

    def q_map(value: mp.mpf) -> mp.mpf:
        return positive_inverse(negative_inverse(value))

    def s_map(value: mp.mpf) -> mp.mpf:
        return f_map(f_map(value))

    def s_derivative(value: mp.mpf) -> mp.mpf:
        return 4 * u**2 * value * f_map(value)

    def beta(value: mp.mpf) -> mp.mpf:
        intermediate = f_map(value)
        return mp.sqrt(1 + (-2 * u * intermediate) ** 2)

    return f_map, h_map, q_map, s_map, s_derivative, beta


@lru_cache(maxsize=256)
def boundary_cycle(
    component_period: int, decimal_digits: int = 100
) -> BoundaryCycle:
    """Construct the distinguished RH-17 orbit by inverse contraction."""

    component_period = int(component_period)
    decimal_digits = int(decimal_digits)
    if component_period < 2:
        raise ValueError("the preclosing prefix requires component_period >= 2")
    if decimal_digits < 50:
        raise ValueError("decimal_digits must be at least fifty")

    with mp.workdps(decimal_digits):
        constants = critical_constants(decimal_digits)
        _f_map, h_map, q_map, _s_map, s_derivative, beta = _cycle_maps(
            constants
        )

        def inverse_return(value: mp.mpf) -> mp.mpf:
            for _ in range(component_period - 1):
                value = h_map(value)
            return q_map(value)

        tolerance = mp.power(10, -(decimal_digits - 18))
        point = mp.mpf(1)
        for _ in range(1000):
            updated = inverse_return(point)
            if abs(updated - point) <= tolerance:
                point = updated
                break
            point = updated
        else:
            raise RuntimeError(
                f"boundary fixed-point iteration failed for k={component_period}"
            )

        h_powers = [point]
        for _ in range(component_period - 1):
            h_powers.append(h_map(h_powers[-1]))
        orbit = (point,) + tuple(reversed(h_powers[1:]))
        slopes = tuple(s_derivative(value) for value in orbit)
        betas = tuple(beta(value) for value in orbit)
        multiplier = mp.fprod(slopes)
        return BoundaryCycle(
            component_period=component_period,
            physical_period=2 * component_period,
            point=+point,
            clearance=+(1 - point),
            orbit=tuple(+value for value in orbit),
            signed_slopes=tuple(+value for value in slopes),
            noise_standard_deviations=tuple(+value for value in betas),
            multiplier=+multiplier,
            decimal_digits=decimal_digits,
        )


def deterministic_map(value: mp.mpf | float) -> mp.mpf:
    """Evaluate ``f`` using the precision carried by ``value`` when possible."""

    constants = critical_constants(100)
    with mp.workdps(100):
        value = mp.mpf(value)
        return +(1 - constants.u * value**2)


def two_step_map(value: mp.mpf | float, decimal_digits: int = 100) -> mp.mpf:
    """Evaluate ``S=f**2`` at high precision."""

    with mp.workdps(int(decimal_digits)):
        constants = critical_constants(int(decimal_digits))
        return +_cycle_maps(constants)[3](mp.mpf(value))


def raw_prefix_expansion_coefficients(
    cycle: BoundaryCycle,
) -> tuple[mp.mpf, tuple[mp.mpf, ...]]:
    """Return the entrance and innovation coefficients in exact forward order.

    The recurrence uses rows ``j=0,...,k-2`` and stops at the preclosing
    coordinate.  Innovation ``0`` is the noise injected by row ``j=0``.
    """

    with mp.workdps(cycle.decimal_digits):
        slopes = cycle.signed_slopes
        betas = cycle.noise_standard_deviations
        entrance = mp.fprod(slopes[:-1])
        innovations = []
        for ell in range(cycle.component_period - 1):
            tail = mp.fprod(slopes[ell + 1 : -1])
            innovations.append(betas[ell] * tail)
        return +entrance, tuple(+value for value in innovations)


def first_innovation_standard_deviation(cycle: BoundaryCycle) -> mp.mpf:
    """Return ``beta_0 prod_{j=1}^{k-2}|a_j|``."""

    with mp.workdps(cycle.decimal_digits):
        return +abs(raw_prefix_expansion_coefficients(cycle)[1][0])


def first_innovation_standard_deviation_via_multiplier(
    cycle: BoundaryCycle,
) -> mp.mpf:
    """Return the identical multiplier quotient for the first innovation."""

    with mp.workdps(cycle.decimal_digits):
        slopes = cycle.signed_slopes
        return +(
            cycle.noise_standard_deviations[0]
            * abs(cycle.multiplier)
            / (abs(slopes[0]) * abs(slopes[-1]))
        )


def forward_variance_step(
    variance: mp.mpf | float,
    signed_slope: mp.mpf | float,
    beta_squared: mp.mpf | float,
) -> mp.mpf:
    """Apply the mass-one forward variance recurrence with a plus noise term."""

    variance = mp.mpf(variance)
    signed_slope = mp.mpf(signed_slope)
    beta_squared = mp.mpf(beta_squared)
    if variance < 0 or beta_squared <= 0:
        raise ValueError("variance must be nonnegative and beta_squared positive")
    return +(signed_slope**2 * variance + beta_squared)


def forward_prefix_variance(
    cycle: BoundaryCycle, entrance_variance: mp.mpf | float
) -> mp.mpf:
    """Propagate a finite entrance variance through the ``k-1`` raw rows."""

    with mp.workdps(cycle.decimal_digits):
        variance = mp.mpf(entrance_variance)
        for slope, beta in zip(
            cycle.signed_slopes[:-1], cycle.noise_standard_deviations[:-1]
        ):
            variance = forward_variance_step(variance, slope, beta**2)
        return +variance


def expanded_prefix_variance(
    cycle: BoundaryCycle, entrance_variance: mp.mpf | float
) -> mp.mpf:
    """Evaluate the same forward variance from the exact affine expansion."""

    with mp.workdps(cycle.decimal_digits):
        entrance, innovations = raw_prefix_expansion_coefficients(cycle)
        return +(
            entrance**2 * mp.mpf(entrance_variance)
            + mp.fsum(coefficient**2 for coefficient in innovations)
        )


def normal_cdf(value: float) -> float:
    """Return the standard normal distribution function."""

    return 0.5 * math.erfc(-float(value) / math.sqrt(2.0))


def normal_survival(value: float) -> float:
    """Return the standard normal survival probability."""

    return 0.5 * math.erfc(float(value) / math.sqrt(2.0))


def gaussian_maximum_interval_mass(length: float, standard_deviation: float) -> float:
    """Maximum Gaussian mass of an interval of the given length, over all means."""

    length = float(length)
    standard_deviation = float(standard_deviation)
    if length < 0 or standard_deviation <= 0:
        raise ValueError("length must be nonnegative and standard_deviation positive")
    return 2.0 * normal_cdf(length / (2.0 * standard_deviation)) - 1.0


def finite_unhalved_l1_lower_bound(sigma: float, propagated_sd: float) -> float:
    """Return the exact factor-four support/escape lower bound."""

    sigma = float(sigma)
    propagated_sd = float(propagated_sd)
    if sigma <= 0 or propagated_sd <= 0:
        raise ValueError("sigma and propagated_sd must be positive")
    return 4.0 * normal_survival(1.0 / (2.0 * sigma * propagated_sd))


def reproduction_C_s() -> float:
    """Evaluate the symbolic ``C_s`` formula with archived ordinary decimals."""

    return (
        C_M_REPRODUCTION
        * math.sqrt(1.0 + LAMBDA**2)
        / (
            8.0
            * U_C**2
            * LAMBDA
            * math.sqrt(C_B_REPRODUCTION)
        )
    )


def phase_clearance(eta: float) -> float:
    """Return the non-certified reproduction value ``d=C_b lambda^(-2 eta)``."""

    return C_B_REPRODUCTION * LAMBDA ** (-2.0 * float(eta))


def phase_propagated_scale(eta: float) -> float:
    """Return the non-certified reproduction value ``c_eta=C_s lambda^(2 eta)``."""

    return reproduction_C_s() * LAMBDA ** (2.0 * float(eta))


def phase_l1_lower_bound(eta: float) -> float:
    """Return ``4 barPhi(1/(2 c_eta))`` using reproduction decimals."""

    scale = phase_propagated_scale(eta)
    return 4.0 * normal_survival(1.0 / (2.0 * scale))


def natural_clock_sigma(component_period: int, eta: float) -> float:
    """Return the exact clock sample satisfying ``eta_sigma=eta``."""

    component_period = int(component_period)
    if component_period < 1:
        raise ValueError("component_period must be positive")
    return LAMBDA ** (-2.0 * (component_period - float(eta)))


def natural_target_scale(component_period: int) -> float:
    """Return ``H_k=k R^(-2k)``."""

    component_period = int(component_period)
    if component_period < 1:
        raise ValueError("component_period must be positive")
    return component_period * TRACE_RADIUS ** (-2 * component_period)


def finite_orbit_row(component_period: int, decimal_digits: int = 110) -> dict[str, object]:
    """Build one deterministic, non-certified orbit reproduction row."""

    cycle = boundary_cycle(component_period, decimal_digits)
    constants = critical_constants(decimal_digits)
    with mp.workdps(decimal_digits):
        direct = first_innovation_standard_deviation(cycle)
        quotient = first_innovation_standard_deviation_via_multiplier(cycle)
        relative_error = abs(direct - quotient) / direct
        return {
            "component_period": component_period,
            "physical_one_step_period": 2 * component_period,
            "boundary_point": float(cycle.point),
            "boundary_clearance": float(cycle.clearance),
            "signed_first_slope": float(cycle.signed_slopes[0]),
            "signed_last_slope": float(cycle.signed_slopes[-1]),
            "absolute_multiplier": float(abs(cycle.multiplier)),
            "absolute_multiplier_over_lambda_k": float(
                abs(cycle.multiplier) / constants.lambda_fixed**component_period
            ),
            "first_innovation_sd_direct": float(direct),
            "first_innovation_sd_via_multiplier": float(quotient),
            "product_identity_relative_error": float(relative_error),
            "sd_over_lambda_2k": float(
                direct / constants.lambda_fixed ** (2 * component_period)
            ),
            "certification_status": "noncertified_reproduction",
        }


def phase_row(eta: float) -> dict[str, object]:
    """Build one limiting-phase reproduction row."""

    eta = float(eta)
    clearance = phase_clearance(eta)
    scale = phase_propagated_scale(eta)
    return {
        "eta": eta,
        "clearance_d": clearance,
        "propagated_scale_c_eta": scale,
        "unhalved_l1_liminf_lower_bound": phase_l1_lower_bound(eta),
        "c_eta_via_C_s_C_b_over_d": (
            reproduction_C_s() * C_B_REPRODUCTION / clearance
        ),
        "certification_status": "noncertified_reproduction",
    }
