"""Exact and outward-rounded certificates for RH-381.

The theorem is symbolic.  This module supplies a deterministic reproduction
layer: exact finite Euler/run identities, exact finite tail-sum identities,
and rational enclosures obtained from directed ``Decimal`` arithmetic.  It
does not infer an all-order statement from the finite diagnostic rows.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from math import isqrt


CUTOFF = 100_000
PRECISION = 60
X_LIPSCHITZ = 170
REMAINDER_CONSTANT = 342
DIAGNOSTIC_Y = (1, 2, 3, 5, 10, 25)
X_COEFFICIENTS = {4: 2, 5: -4, 6: 6, 7: -8, 8: 10}
CANONICAL_FIXTURE_SHA256 = (
    "d55fd48071eb5b88c054f3d34329f274f792f2bbd859b4ab98e31b5b7020beb8"
)
NUMERIC_PLAN_INTERVAL_SHA256 = (
    "e0342f871b1f952039da2b1025fa7598771b9fa089295f07cb60b11f70cee15c"
)


def fraction_text(value: Fraction) -> str:
    """Return a reduced, stable rational string."""

    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def canonical_json_bytes(value: object) -> bytes:
    """Return the compact canonical JSON encoding used for fixture hashes."""

    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def payload_sha256(value: object) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def sieve_primes(limit: int) -> tuple[int, ...]:
    if type(limit) is not int or limit < 2:
        raise ValueError("prime cutoff must be an integer at least two")
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    return tuple(index for index, flag in enumerate(sieve) if flag)


def first_odd_primes(count: int) -> tuple[int, ...]:
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer")
    limit = 32
    while True:
        primes = tuple(prime for prime in sieve_primes(limit) if prime != 2)
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def integer_square_tail_bound(cutoff: int) -> Fraction:
    """Return ``sum_(n>cutoff) 1/(n^2-1)`` in telescoped form."""

    if type(cutoff) is not int or cutoff < 2:
        raise ValueError("tail cutoff must be an integer at least two")
    return Fraction(1, 2) * (Fraction(1, cutoff) + Fraction(1, cutoff + 1))


def prime_square_weight(prime: int) -> Fraction:
    if type(prime) is not int or prime < 3 or prime % 2 == 0:
        raise ValueError("an odd prime at least three is required")
    if any(prime % divisor == 0 for divisor in range(3, isqrt(prime) + 1, 2)):
        raise ValueError("an odd prime at least three is required")
    return Fraction(1, prime * prime - 1)


def _fraction_product(values: tuple[Fraction, ...]) -> Fraction:
    output = Fraction(1)
    for value in values:
        output *= value
    return output


def _exact_integer(value: Fraction, label: str) -> int:
    if value.denominator != 1:
        raise ArithmeticError(f"{label} is not integral: {fraction_text(value)}")
    return value.numerator


def square_parameters(y: int) -> dict[str, object]:
    primes = first_odd_primes(y)
    p_product = 1
    a_product = 1
    d_product = 1
    for prime in primes:
        p_product *= prime * prime
        a_product *= prime * prime - 1
        d_product *= prime * prime - 2
    return {
        "y": y,
        "primes": primes,
        "p_y": primes[-1],
        "P": p_product,
        "q": 4 * p_product,
        "A": a_product,
        "D": d_product,
    }


def finite_euler_values(y: int) -> dict[int, Fraction]:
    primes = first_odd_primes(y)
    return {
        m: _fraction_product(tuple(Fraction(prime * prime - m, prime * prime) for prime in primes))
        for m in range(1, 10)
    }


def normalized_euler_ratios(y: int) -> dict[int, Fraction]:
    values = finite_euler_values(y)
    return {m: values[m] / values[1] for m in range(1, 9)}


def square_run_counts(y: int) -> dict[int, int]:
    parameters = square_parameters(y)
    p_product = parameters["P"]
    if not isinstance(p_product, int):
        raise TypeError("square period product is not an integer")
    euler = finite_euler_values(y)
    output = {
        length: _exact_integer(
            p_product * (euler[length] - 2 * euler[length + 1] + euler[length + 2]),
            f"R_{length}({y})",
        )
        for length in range(1, 8)
    }
    output[8] = _exact_integer(p_product * euler[8], f"R_8({y})")
    return output


def run_statistics(y: int) -> dict[str, int]:
    runs = square_run_counts(y)
    even_runs = sum(runs[length] for length in (2, 4, 6, 8))
    even_sites = sum(length * runs[length] for length in (2, 4, 6, 8))
    return {
        "O": sum(runs[length] for length in (1, 3, 5, 7)),
        "E": even_runs,
        "L": even_sites,
        "M": sum((length - 1) * runs[length] for length in (1, 3, 5, 7)),
        "X": even_sites - 2 * even_runs,
    }


def normalized_x(y: int) -> Fraction:
    ratios = normalized_euler_ratios(y)
    euler_form = sum(
        (coefficient * ratios[m] for m, coefficient in X_COEFFICIENTS.items()),
        Fraction(0),
    )
    parameters = square_parameters(y)
    statistics = run_statistics(y)
    a_product = parameters["A"]
    if not isinstance(a_product, int):
        raise TypeError("A_y is not an integer")
    run_form = Fraction(statistics["X"], a_product)
    if euler_form != run_form:
        raise AssertionError("Euler and run forms of X_y disagree")
    return euler_form


@dataclass(frozen=True)
class EulerValue:
    inv_pi2: Fraction = Fraction(0)
    kappa2: Fraction = Fraction(0)

    def __add__(self, other: object) -> "EulerValue":
        if not isinstance(other, EulerValue):
            return NotImplemented
        return EulerValue(self.inv_pi2 + other.inv_pi2, self.kappa2 + other.kappa2)

    def __sub__(self, other: object) -> "EulerValue":
        if not isinstance(other, EulerValue):
            return NotImplemented
        return EulerValue(self.inv_pi2 - other.inv_pi2, self.kappa2 - other.kappa2)

    def exact_dict(self) -> dict[str, str]:
        return {"inv_pi2": fraction_text(self.inv_pi2), "kappa2": fraction_text(self.kappa2)}


def square_increment(y: int) -> EulerValue:
    parameters = square_parameters(y)
    following = square_parameters(y + 1)
    statistics = run_statistics(y)
    a_product = parameters["A"]
    d_product = parameters["D"]
    next_prime = following["p_y"]
    if not isinstance(a_product, int) or not isinstance(d_product, int) or not isinstance(next_prime, int):
        raise TypeError("square increment parameters have invalid types")
    s = next_prime * next_prime
    return EulerValue(
        Fraction(2 * statistics["X"] + 4 * statistics["M"], a_product * (s - 1)),
        Fraction(-statistics["M"], d_product * (s - 2)),
    )


def canonical_fixture() -> dict[str, object]:
    """Return the six-row exact fixture independently frozen by numeric audit."""

    rows: list[dict[str, object]] = []
    increments: list[EulerValue] = []
    for y in range(1, 7):
        parameters = square_parameters(y)
        runs = square_run_counts(y)
        statistics = run_statistics(y)
        ratios = normalized_euler_ratios(y)
        a_product = parameters["A"]
        d_product = parameters["D"]
        p_y = parameters["p_y"]
        if not isinstance(a_product, int) or not isinstance(d_product, int) or not isinstance(p_y, int):
            raise TypeError("canonical fixture parameters have invalid types")
        increment = square_increment(y)
        increments.append(increment)
        rows.append(
            {
                "A": a_product,
                "D": d_product,
                "E": statistics["E"],
                "L": statistics["L"],
                "M": statistics["M"],
                "M_over_A": fraction_text(Fraction(statistics["M"], a_product)),
                "O": statistics["O"],
                "R": {str(length): runs[length] for length in range(1, 9)},
                "U4_8": {str(m): fraction_text(ratios[m]) for m in range(4, 9)},
                "X_integer": statistics["X"],
                "X_normalized": fraction_text(normalized_x(y)),
                "a_next": fraction_text(prime_square_weight(first_odd_primes(y + 1)[-1])),
                "increment": increment.exact_dict(),
                "p_y": p_y,
                "y": y,
            }
        )
    one_to_three = EulerValue()
    one_to_six = EulerValue()
    for index, increment in enumerate(increments, start=1):
        one_to_six += increment
        if index <= 3:
            one_to_three += increment
    payload = {
        "rows": rows,
        "telescoping": {
            "1_to_3": one_to_three.exact_dict(),
            "1_to_6": one_to_six.exact_dict(),
        },
    }
    if payload_sha256(payload) != CANONICAL_FIXTURE_SHA256:
        raise AssertionError("canonical six-row fixture drifted")
    return payload


def finite_tail_identity(weights: tuple[Fraction, ...]) -> dict[str, object]:
    """Certify both exact tail-sum identities for a finite nonnegative list."""

    if not weights or any(type(weight) is not Fraction for weight in weights):
        raise TypeError("a nonempty sequence of exact Fraction weights is required")
    if any(weight < 0 for weight in weights):
        raise ValueError("tail weights must be nonnegative")
    suffix = Fraction(0)
    left_current = Fraction(0)
    left_next = Fraction(0)
    square_sum = sum((weight * weight for weight in weights), Fraction(0))
    for weight in reversed(weights):
        left_next += weight * suffix
        suffix += weight
        left_current += weight * suffix
    current_rhs = (suffix * suffix + square_sum) / 2
    next_rhs = (suffix * suffix - square_sum) / 2
    return {
        "count": len(weights),
        "T": fraction_text(suffix),
        "S": fraction_text(square_sum),
        "current_identity_pass": left_current == current_rhs,
        "next_identity_pass": left_next == next_rhs,
        "current_upper_pass": left_current <= suffix * suffix,
        "next_upper_pass": left_next <= suffix * suffix / 2,
        "all_pass": (
            left_current == current_rhs
            and left_next == next_rhs
            and left_current <= suffix * suffix
            and left_next <= suffix * suffix / 2
        ),
    }


def exact_identity_rows() -> list[dict[str, object]]:
    primes = tuple(prime for prime in sieve_primes(400) if prime != 2)
    rows = []
    for start, count in ((0, 16), (1, 24), (5, 32), (12, 40)):
        weights = tuple(prime_square_weight(prime) for prime in primes[start : start + count])
        row = finite_tail_identity(weights)
        row.update({"start_index": start, "end_index": start + count})
        rows.append(row)
    return rows


def coefficient_ledger() -> dict[str, object]:
    contributions = {
        str(m): abs(coefficient) * (m - 1)
        for m, coefficient in X_COEFFICIENTS.items()
    }
    x_total = sum(contributions.values())
    main_remainder = 2 * x_total
    memory_remainder = 2
    return {
        "x_contributions": contributions,
        "x_lipschitz": x_total,
        "main_remainder": main_remainder,
        "memory_remainder": memory_remainder,
        "total_remainder": main_remainder + memory_remainder,
        "pass": x_total == X_LIPSCHITZ and main_remainder + memory_remainder == REMAINDER_CONSTANT,
    }


def certify_upper_le_lower(
    upper: Decimal, lower: Decimal, label: str, low_context: Context
) -> Decimal:
    """Fail closed unless an outward upper endpoint is below a lower endpoint."""

    if upper > lower:
        raise ArithmeticError(f"{label} is not certified by the outward intervals")
    with localcontext(low_context):
        return lower - upper


def _contexts(precision: int) -> tuple[Context, Context]:
    return (
        Context(prec=precision, rounding=ROUND_FLOOR),
        Context(prec=precision, rounding=ROUND_CEILING),
    )


def _fraction_decimal(value: Fraction, context: Context) -> Decimal:
    with localcontext(context):
        return Decimal(value.numerator) / Decimal(value.denominator)


@dataclass(frozen=True)
class DecimalInterval:
    lower: Decimal
    upper: Decimal

    def __post_init__(self) -> None:
        if self.lower > self.upper:
            raise ArithmeticError("reversed interval")

    def as_list(self) -> list[str]:
        return [str(self.lower), str(self.upper)]


def _fraction_interval(value: Fraction, low: Context, high: Context) -> DecimalInterval:
    return DecimalInterval(_fraction_decimal(value, low), _fraction_decimal(value, high))


def _add(left: DecimalInterval, right: DecimalInterval, low: Context, high: Context) -> DecimalInterval:
    with localcontext(low):
        lower = left.lower + right.lower
    with localcontext(high):
        upper = left.upper + right.upper
    return DecimalInterval(lower, upper)


def _subtract(left: DecimalInterval, right: DecimalInterval, low: Context, high: Context) -> DecimalInterval:
    with localcontext(low):
        lower = left.lower - right.upper
    with localcontext(high):
        upper = left.upper - right.lower
    return DecimalInterval(lower, upper)


def _scale(value: DecimalInterval, scalar: int, low: Context, high: Context) -> DecimalInterval:
    if scalar >= 0:
        with localcontext(low):
            lower = value.lower * Decimal(scalar)
        with localcontext(high):
            upper = value.upper * Decimal(scalar)
    else:
        with localcontext(low):
            lower = value.upper * Decimal(scalar)
        with localcontext(high):
            upper = value.lower * Decimal(scalar)
    return DecimalInterval(lower, upper)


def _multiply_positive(
    left: DecimalInterval, right: DecimalInterval, low: Context, high: Context
) -> DecimalInterval:
    if left.lower < 0 or right.lower < 0:
        raise ValueError("positive interval multiplication received a negative endpoint")
    with localcontext(low):
        lower = left.lower * right.lower
    with localcontext(high):
        upper = left.upper * right.upper
    return DecimalInterval(lower, upper)


def _square_positive(value: DecimalInterval, low: Context, high: Context) -> DecimalInterval:
    return _multiply_positive(value, value, low, high)


def _abs_upper(value: DecimalInterval) -> Decimal:
    return max(value.lower.copy_abs(), value.upper.copy_abs())


def _decimal_product_ratio(
    primes: tuple[int, ...], coefficient: int, low: Context, high: Context
) -> DecimalInterval:
    lower = Decimal(1)
    upper = Decimal(1)
    for prime in primes:
        denominator = prime * prime - 1
        factor = _fraction_interval(
            Fraction(denominator - coefficient, denominator), low, high
        )
        product_interval = _multiply_positive(
            DecimalInterval(lower, upper), factor, low, high
        )
        lower, upper = product_interval.lower, product_interval.upper
    return DecimalInterval(lower, upper)


def _decimal_weight_sum(
    primes: tuple[int, ...], low: Context, high: Context
) -> DecimalInterval:
    lower = Decimal(0)
    upper = Decimal(0)
    for prime in primes:
        denominator = Decimal(prime * prime - 1)
        with localcontext(low):
            term_low = Decimal(1) / denominator
            lower = lower + term_low
        with localcontext(high):
            term_high = Decimal(1) / denominator
            upper = upper + term_high
    return DecimalInterval(lower, upper)


def _linear_combination(
    terms: tuple[tuple[int, DecimalInterval], ...], low: Context, high: Context
) -> DecimalInterval:
    output = DecimalInterval(Decimal(0), Decimal(0))
    for coefficient, interval in terms:
        output = _add(output, _scale(interval, coefficient, low, high), low, high)
    return output


@lru_cache(maxsize=2, typed=True)
def interval_fixture(cutoff: int = CUTOFF, precision: int = PRECISION) -> dict[str, object]:
    """Build proof-grade outward finite diagnostics at the frozen cutoff."""

    if type(cutoff) is not int or type(precision) is not int:
        raise TypeError("RH-381 cutoff and precision must be exact integers")
    if cutoff != CUTOFF or precision != PRECISION:
        raise ValueError("RH-381 release intervals require the frozen cutoff and precision")
    low, high = _contexts(precision)
    primes_all = sieve_primes(cutoff)
    odd_primes = tuple(prime for prime in primes_all if prime != 2)
    tail_fraction = integer_square_tail_bound(cutoff)
    tail = _fraction_interval(tail_fraction, low, high)
    one = DecimalInterval(Decimal(1), Decimal(1))

    u: dict[int, DecimalInterval] = {}
    for m in range(2, 9):
        partial = _decimal_product_ratio(odd_primes, m - 1, low, high)
        tail_factor = _fraction_interval(
            Fraction(1) - (m - 1) * tail_fraction, low, high
        )
        lower_product = _multiply_positive(partial, tail_factor, low, high)
        u[m] = DecimalInterval(lower_product.lower, partial.upper)

    c_infinity = _linear_combination(
        ((1, one), (-2, u[2]), (2, u[3]), (-2, u[4]), (2, u[5]), (-2, u[6]), (2, u[7]), (-2, u[8])),
        low,
        high,
    )
    x_infinity = _linear_combination(
        tuple((coefficient, u[m]) for m, coefficient in X_COEFFICIENTS.items()),
        low,
        high,
    )
    if x_infinity.lower <= 0:
        raise ArithmeticError("numeric X_infinity enclosure did not certify positivity")

    diagnostic_rows: list[dict[str, object]] = []
    for y in DIAGNOSTIC_Y:
        p_y = first_odd_primes(y)[-1]
        later = tuple(prime for prime in odd_primes if prime > p_y)
        t_partial = _decimal_weight_sum(later, low, high)
        with localcontext(high):
            t_upper = t_partial.upper + tail.upper
        t_interval = DecimalInterval(t_partial.lower, t_upper)

        p_partial = _decimal_product_ratio(later, 1, low, high)
        p_tail_factor = _fraction_interval(Fraction(1) - tail_fraction, low, high)
        p_lower = _multiply_positive(p_partial, p_tail_factor, low, high).lower
        p_interval = DecimalInterval(p_lower, p_partial.upper)

        parameters = square_parameters(y)
        stats = run_statistics(y)
        a_product = parameters["A"]
        if not isinstance(a_product, int):
            raise TypeError("diagnostic A_y is not an integer")
        odd_ratio = _fraction_interval(Fraction(stats["O"], a_product), low, high)
        even_ratio = _fraction_interval(Fraction(stats["E"], a_product), low, high)
        gap_pi2 = _subtract(
            _scale(_subtract(c_infinity, odd_ratio, low, high), 2, low, high),
            _scale(_multiply_positive(even_ratio, _subtract(one, p_interval, low, high), low, high), 4, low, high),
            low,
            high,
        )
        leading_pi2 = _scale(_multiply_positive(x_infinity, t_interval, low, high), 2, low, high)
        residual_pi2 = _subtract(gap_pi2, leading_pi2, low, high)
        residual_abs_upper = _abs_upper(residual_pi2)
        t_squared = _square_positive(t_interval, low, high)
        with localcontext(low):
            bound342_lower = Decimal(REMAINDER_CONSTANT) * t_squared.lower
        bound_margin = certify_upper_le_lower(
            residual_abs_upper, bound342_lower, f"342-bound y={y}", low
        )

        x_y = _fraction_interval(normalized_x(y), low, high)
        x_error = _subtract(x_y, x_infinity, low, high)
        x_error_abs_upper = _abs_upper(x_error)
        with localcontext(low):
            bound170_lower = Decimal(X_LIPSCHITZ) * t_interval.lower
        certify_upper_le_lower(
            x_error_abs_upper, bound170_lower, f"170-bound y={y}", low
        )
        diagnostic_rows.append(
            {
                "y": y,
                "T": t_interval.as_list(),
                "gap_pi2": gap_pi2.as_list(),
                "residual_pi2": residual_pi2.as_list(),
                "residual_abs_upper": str(residual_abs_upper),
                "bound342_lower": str(bound342_lower),
                "bound_margin": str(bound_margin),
                "bound_pass": True,
                "x_error_abs_upper": str(x_error_abs_upper),
                "bound170_lower": str(bound170_lower),
                "x_bound_pass": True,
            }
        )

    prime_hash = sha256(canonical_json_bytes(list(primes_all))).hexdigest()
    payload = {
        "cutoff": cutoff,
        "precision": precision,
        "prime_count": len(primes_all),
        "last_prime": primes_all[-1],
        "prime_json_sha256": prime_hash,
        "integer_tail_bound": fraction_text(tail_fraction),
        "u_m": {str(m): u[m].as_list() for m in range(2, 9)},
        "C_infinity": c_infinity.as_list(),
        "X_infinity": x_infinity.as_list(),
        "rows": diagnostic_rows,
        "all_pass": all(row["bound_pass"] and row["x_bound_pass"] for row in diagnostic_rows),
    }
    return payload


def verify_certificate(
    x_lipschitz: int = X_LIPSCHITZ,
    remainder_constant: int = REMAINDER_CONSTANT,
    cutoff: int = CUTOFF,
    precision: int = PRECISION,
) -> dict[str, object]:
    """Run the bounded RH-381 certificate suite and reject rebinding."""

    if type(x_lipschitz) is not int:
        raise TypeError("the RH-381 X Lipschitz constant must be an exact integer")
    if type(remainder_constant) is not int:
        raise TypeError("the RH-381 remainder constant must be an exact integer")
    if type(cutoff) is not int or type(precision) is not int:
        raise TypeError("the RH-381 interval parameters must be exact integers")
    if x_lipschitz != X_LIPSCHITZ:
        raise ValueError("the RH-381 X Lipschitz constant was rebound")
    if remainder_constant != REMAINDER_CONSTANT:
        raise ValueError("the RH-381 remainder constant was rebound")
    if cutoff != CUTOFF or precision != PRECISION:
        raise ValueError("the RH-381 interval protocol was rebound")
    fixture = canonical_fixture()
    intervals = interval_fixture(cutoff, precision)
    identity_rows = exact_identity_rows()
    ledger = coefficient_ledger()
    interval_digest = payload_sha256(intervals)
    all_pass = (
        payload_sha256(fixture) == CANONICAL_FIXTURE_SHA256
        and interval_digest == NUMERIC_PLAN_INTERVAL_SHA256
        and bool(intervals["all_pass"])
        and all(row["all_pass"] for row in identity_rows)
        and bool(ledger["pass"])
    )
    if interval_digest != NUMERIC_PLAN_INTERVAL_SHA256:
        raise ArithmeticError("outward interval fixture differs from the independent frozen audit")
    return {
        "canonical_fixture": fixture,
        "canonical_fixture_bytes": len(canonical_json_bytes(fixture)),
        "canonical_fixture_sha256": payload_sha256(fixture),
        "interval_fixture": intervals,
        "interval_fixture_bytes": len(canonical_json_bytes(intervals)),
        "interval_fixture_sha256": interval_digest,
        "numeric_plan_interval_sha256": NUMERIC_PLAN_INTERVAL_SHA256,
        "interval_digest_matches_independent_plan": interval_digest == NUMERIC_PLAN_INTERVAL_SHA256,
        "exact_tail_identity_rows": identity_rows,
        "coefficient_ledger": ledger,
        "claim_boundary": {
            "fixed_finite_q_before_N_limit": True,
            "phasewise_c11_zero_only": True,
            "finite_rows_are_reproduction_only": True,
            "no_PNT": True,
            "no_second_order_coefficient_claim": True,
            "no_p_y_asymptotic": True,
            "no_growing_clock": True,
            "no_adaptive_capacity_convergence": True,
            "gates_A_through_E": [False, False, False, False, False],
        },
        "all_pass": all_pass,
    }
