"""High-precision boundary cycles and their time-ordered monodromy."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import mpmath as mp


@dataclass(frozen=True)
class CriticalConstants:
    """Algebraic and local constants of the first band-merging map."""

    u: mp.mpf
    r: mp.mpf
    lambda_fixed: mp.mpf
    contraction: mp.mpf
    first_interior_point: mp.mpf


@dataclass(frozen=True)
class BoundaryCycle:
    """The component-period ``k`` cycle coded by ``CA(CB)^(k-1)``.

    ``orbit`` is in forward two-step order.  Thus ``orbit[j]`` maps to
    ``orbit[(j + 1) % k]`` under ``S=f^2``.
    """

    component_period: int
    point: mp.mpf
    clearance: mp.mpf
    orbit: tuple[mp.mpf, ...]
    two_step_derivatives: tuple[mp.mpf, ...]
    multiplier: mp.mpf
    inverse_branch_derivative: mp.mpf
    lambda_fixed: mp.mpf
    decimal_digits: int

    @property
    def inverse_jacobian_radius(self) -> mp.mpf:
        """Spectral radius of the inverse-Jacobian weighted cycle."""

        with mp.workdps(self.decimal_digits):
            return +abs(self.multiplier) ** (
                -mp.mpf(1) / self.component_period
            )

    @property
    def one_step_radius(self) -> mp.mpf:
        """Radius after the canonical bipartite one-step lift."""

        with mp.workdps(self.decimal_digits):
            return +mp.sqrt(self.inverse_jacobian_radius)

    @property
    def scaled_multiplier(self) -> mp.mpf:
        """Return ``abs(M_k) / lambda^k``."""

        with mp.workdps(self.decimal_digits):
            return +abs(self.multiplier) / self.lambda_fixed**self.component_period


@lru_cache(maxsize=16)
def critical_constants(decimal_digits: int = 100) -> CriticalConstants:
    """Return high-precision constants for ``f(x)=1-u*x^2``."""

    decimal_digits = int(decimal_digits)
    if decimal_digits < 50:
        raise ValueError("decimal_digits must be at least fifty")
    with mp.workdps(decimal_digits):
        u = mp.findroot(
            lambda value: value**3 - 2 * value**2 + 2 * value - 2,
            (mp.mpf("1.5"), mp.mpf("1.6")),
        )
        r = u - 1
        lambda_fixed = 2 * u * r
        contraction = lambda_fixed**-2
        first_interior_point = 1 / mp.sqrt(u)
        return CriticalConstants(
            u=+u,
            r=+r,
            lambda_fixed=+lambda_fixed,
            contraction=+contraction,
            first_interior_point=+first_interior_point,
        )


def _maps(constants: CriticalConstants):
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

    def positive_inverse_derivative(value: mp.mpf) -> mp.mpf:
        return -1 / (2 * u * positive_inverse(value))

    def negative_inverse_derivative(value: mp.mpf) -> mp.mpf:
        return -positive_inverse_derivative(value)

    def h_derivative(value: mp.mpf) -> mp.mpf:
        return (
            positive_inverse_derivative(positive_inverse(value))
            * positive_inverse_derivative(value)
        )

    def q_derivative(value: mp.mpf) -> mp.mpf:
        return (
            positive_inverse_derivative(negative_inverse(value))
            * negative_inverse_derivative(value)
        )

    def s_map(value: mp.mpf) -> mp.mpf:
        return f_map(f_map(value))

    def s_derivative(value: mp.mpf) -> mp.mpf:
        intermediate = f_map(value)
        return 4 * u**2 * value * intermediate

    return (
        f_map,
        h_map,
        q_map,
        h_derivative,
        q_derivative,
        s_map,
        s_derivative,
    )


@lru_cache(maxsize=512)
def boundary_cycle(
    component_period: int, decimal_digits: int = 100
) -> BoundaryCycle:
    """Construct the distinguished boundary cycle by inverse contraction."""

    component_period = int(component_period)
    decimal_digits = int(decimal_digits)
    if component_period < 1:
        raise ValueError("component_period must be positive")
    if decimal_digits < 50:
        raise ValueError("decimal_digits must be at least fifty")

    with mp.workdps(decimal_digits):
        constants = critical_constants(decimal_digits)
        (
            _f_map,
            h_map,
            q_map,
            h_derivative,
            q_derivative,
            _s_map,
            s_derivative,
        ) = _maps(constants)

        def inverse_return(value: mp.mpf) -> mp.mpf:
            for _ in range(component_period - 1):
                value = h_map(value)
            return q_map(value)

        tolerance = mp.power(10, -(decimal_digits - 18))
        point = mp.mpf(1)
        for _ in range(800):
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
        derivatives = tuple(s_derivative(value) for value in orbit)
        multiplier = mp.fprod(derivatives)

        inverse_derivative = mp.mpf(1)
        value = point
        for _ in range(component_period - 1):
            inverse_derivative *= h_derivative(value)
            value = h_map(value)
        inverse_derivative *= q_derivative(value)

        return BoundaryCycle(
            component_period=component_period,
            point=+point,
            clearance=+(1 - point),
            orbit=tuple(+value for value in orbit),
            two_step_derivatives=tuple(+value for value in derivatives),
            multiplier=+multiplier,
            inverse_branch_derivative=+inverse_derivative,
            lambda_fixed=+constants.lambda_fixed,
            decimal_digits=decimal_digits,
        )


def two_step_map(value: mp.mpf, *, decimal_digits: int = 100) -> mp.mpf:
    """Evaluate ``S=f^2`` at high precision."""

    with mp.workdps(int(decimal_digits)):
        constants = critical_constants(int(decimal_digits))
        return +_maps(constants)[5](mp.mpf(value))


def h_map(value: mp.mpf, *, decimal_digits: int = 100) -> mp.mpf:
    """Evaluate the positive two-step inverse branch ``h``."""

    with mp.workdps(int(decimal_digits)):
        constants = critical_constants(int(decimal_digits))
        return +_maps(constants)[1](mp.mpf(value))


def endpoint_dictionary_gap(decimal_digits: int = 100) -> mp.mpf:
    """Return ``p_2-h(1)>0``, the direct endpoint-compression gap."""

    with mp.workdps(int(decimal_digits)):
        constants = critical_constants(int(decimal_digits))
        p_two = boundary_cycle(1, int(decimal_digits)).point
        return +(p_two - constants.first_interior_point)
