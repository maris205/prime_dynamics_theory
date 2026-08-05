"""Exact matrix and scalar ledgers used by the RH-364 artifact."""

from __future__ import annotations

from decimal import Decimal, localcontext
from math import cos, log, pi


A = (
    (1, 0, 1, 0),
    (1, 0, 0, 0),
    (0, 1, 0, 1),
    (0, 1, 0, 0),
)

KAPPA_NUMERATOR = 773
KAPPA_DENOMINATOR = 224


def identity(size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(1 if row == column else 0 for column in range(size))
        for row in range(size)
    )


def matmul(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    size = len(left)
    return tuple(
        tuple(
            sum(left[row][index] * right[index][column] for index in range(size))
            for column in range(size)
        )
        for row in range(size)
    )


def matpow(matrix: tuple[tuple[int, ...], ...], exponent: int):
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    output = identity(len(matrix))
    base = matrix
    power = exponent
    while power:
        if power & 1:
            output = matmul(output, base)
        base = matmul(base, base)
        power >>= 1
    return output


def matrix_trace(matrix: tuple[tuple[int, ...], ...]) -> int:
    return sum(matrix[index][index] for index in range(len(matrix)))


def fixed_point_counts(maximum_order: int) -> list[int]:
    return [matrix_trace(matpow(A, order)) for order in range(1, maximum_order + 1)]


def lucas_numbers(maximum_order: int) -> list[int]:
    values = [2, 1]
    while len(values) <= maximum_order:
        values.append(values[-1] + values[-2])
    return values[1 : maximum_order + 1]


def trace_formula_counts(maximum_order: int) -> list[int]:
    lucas = lucas_numbers(maximum_order)
    return [
        lucas[order - 1] + round(2 * cos(order * pi / 2))
        for order in range(1, maximum_order + 1)
    ]


def divisors(value: int) -> list[int]:
    return [candidate for candidate in range(1, value + 1) if value % candidate == 0]


def mobius(value: int) -> int:
    if value == 1:
        return 1
    remaining = value
    prime_count = 0
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            prime_count += 1
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        prime_count += 1
    return -1 if prime_count % 2 else 1


def primitive_orbit_counts(maximum_order: int) -> list[int]:
    fixed = [0] + fixed_point_counts(maximum_order)
    return [
        sum(mobius(divisor) * fixed[order // divisor] for divisor in divisors(order))
        // order
        for order in range(1, maximum_order + 1)
    ]


def exact_polynomial_coefficients() -> list[int]:
    """Coefficients of det(I-zA), in increasing powers of z."""
    return [1, -1, 0, -1, -1]


def survivor_fixed_point_data(precision: int = 80) -> dict[str, str]:
    with localcontext() as context:
        context.prec = precision
        seven = Decimal(7)
        root_seven = context.sqrt(seven)
        x_star = -(Decimal(1) + root_seven) / Decimal(6)
        multiplier = (
            Decimal(1)
            + root_seven
            + context.sqrt(seven + Decimal(2) * root_seven)
        )
        flat_trace = Decimal(1) / (Decimal(2) * root_seven)
        return {
            "x_star": str(+x_star),
            "unstable_multiplier": str(+multiplier),
            "flat_trace_order_one": str(+flat_trace),
        }


def analytic_constants() -> dict[str, float]:
    phi = (1.0 + 5.0**0.5) / 2.0
    kappa = KAPPA_NUMERATOR / KAPPA_DENOMINATOR
    multiplier = float(survivor_fixed_point_data(50)["unstable_multiplier"])
    beta_zero = log(2.0 / phi) / log(multiplier / kappa)
    return {
        "phi": phi,
        "kappa": kappa,
        "euler_beta_one_radius": kappa / phi,
        "flat_correction_radius": kappa * kappa / phi,
        "log2_phi": log(phi, 2.0),
        "beta_zero": beta_zero,
    }


def scalar_normalization_ledger(beta: float, period_three_multiplier: float) -> dict[str, float]:
    fixed_multiplier = float(survivor_fixed_point_data(50)["unstable_multiplier"])
    scalar = fixed_multiplier**beta
    return {
        "beta": beta,
        "scalar": scalar,
        "Q1": 1.0,
        "Q2": 1.0,
        "Q3": 1.0 + 3.0 * (fixed_multiplier**3 / period_three_multiplier) ** beta,
    }


def euler_tail_bound(radius: float, beta: float, cutoff: int) -> float:
    constants = analytic_constants()
    t = radius * constants["kappa"] ** (-beta)
    q = constants["phi"] * t
    if not (0 <= t < 1 and 0 <= q < 1):
        raise ValueError("radius lies outside the certified tail domain")
    return (
        4.0
        * q ** (cutoff + 1)
        / ((cutoff + 1) * (1.0 - q) * (1.0 - t ** (cutoff + 1)))
    )
