"""Exact RH-383 Euler-tail normal-form certificates.

The manuscript proves the infinite identities.  This module supplies an
independent, finite, exact-arithmetic reproduction and adversarial layer.  It
uses :class:`fractions.Fraction` throughout and keeps three compilers separate:

* the endpoint ``C/W`` partition compiler;
* the ordered-increment ``Gamma/h/e/Phi`` compiler; and
* the direct ``A_c/F_c`` telescope compiler.

Finite tails are reproduction rows, never fits and never evidence for an
asymptotic statement.  The increment coefficients ``XI`` and ``ETA`` are
deliberately distinct from the endpoint coefficients ``ALPHA`` and ``BETA``.
"""

from __future__ import annotations

from collections import Counter
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from math import factorial, isqrt


ALPHA = {2: -2, 3: 2, 4: -2, 5: 2, 6: -2, 7: 2, 8: -2}
BETA = {2: 1, 3: -2, 4: 2, 5: -2, 6: 2, 7: -2, 8: 2}

# Original RH-380/RH-381 increment channels.  These names must not be rebound
# to ALPHA/BETA: their absolute ledgers are the source of the 92/3 majorant.
XI = {4: 2, 5: -4, 6: 6, 7: -8, 8: 10}
ETA = {3: 2, 4: -4, 5: 6, 6: -8, 7: 10, 8: -12}

FINITE_TAIL_CASES = ((1, 2), (1, 4), (1, 8), (3, 12), (8, 19), (18, 19))
COFINAL_ENDPOINTS = (8, 12, 19, 32)
DIRECT_CASES = tuple((start, endpoint) for endpoint in COFINAL_ENDPOINTS for start in range(1, endpoint))
LOW_ORDER_ENDPOINTS = tuple(range(1, 34))
TAIL_TELESCOPE_STARTS = (1, 2, 3, 5, 8, 12, 18)
MAX_DEGREE = 12

EXPECTED_COUNTS = {
    "endpoint_normal_form": 67,
    "af_coefficients": 864,
    "q_signs": 432,
    "gamma_equivalence": 1084,
    "channel_equivalence": 144,
    "low_order": 33,
    "cubic_endpoint": 67,
    "cubic_symbolic": 12,
    "m2_cancellation": 1151,
    "remainder": 804,
    "terminal": 4,
    "successor_tail": 7,
    "negative_mutations": 20,
}

INCREMENT_X_ABSOLUTE_LEDGER = Fraction(35, 4)
INCREMENT_MEMORY_ABSOLUTE_LEDGER = Fraction(14)
X_HOMOGENEOUS_MAJORANT = Fraction(5, 2)
MEMORY_HOMOGENEOUS_MAJORANT = Fraction(4, 3)
GEOMETRIC_TAIL_FACTOR = 8
REMAINDER_MAJORANT_PI2 = Fraction(92, 3)
PUBLISHED_COARSE_MAJORANT_PI2 = 31
CERTIFICATE_FIXTURE_BYTES = 12245
CERTIFICATE_FIXTURE_SHA256 = "9e2742fcdb2f626909eeb528c5081c9ace5414a1e6466c15b8b6800f427b6f16"


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def payload_sha256(value: object) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("an exact Fraction is required")
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fraction_decimal(value: Fraction, places: int = 15) -> str:
    if type(value) is not Fraction or type(places) is not int or places < 1:
        raise TypeError("an exact Fraction and a positive exact integer are required")
    context = Context(prec=max(places + 20, 40), rounding=ROUND_HALF_EVEN)
    with localcontext(context):
        output = Decimal(value.numerator) / Decimal(value.denominator)
        return format(output, f".{places}f")


def _require_degree(degree: int, *, allow_zero: bool = False) -> int:
    lower = 0 if allow_zero else 1
    if type(degree) is not int or degree < lower:
        relation = "nonnegative" if allow_zero else "positive"
        raise ValueError(f"degree must be a {relation} exact integer")
    return degree


def require_truncation_degree(degree: int) -> int:
    """Accept exactly ``int >= 1``; Boolean and float aliases fail closed."""

    return _require_degree(degree)


def remainder_bound_pi2_from_rho(rho: Fraction, degree: int) -> Fraction:
    """Return the audited pi^2-scaled tail bound on its exact domain."""

    require_truncation_degree(degree)
    if type(rho) is not Fraction or rho < 0 or rho > Fraction(7, 8):
        raise ValueError("rho must be an exact Fraction in [0,7/8], not a square-clock value")
    return REMAINDER_MAJORANT_PI2 * rho ** (degree + 1)


def sieve_primes(limit: int) -> tuple[int, ...]:
    if type(limit) is not int or limit < 2:
        raise ValueError("prime cutoff must be an exact integer at least two")
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    return tuple(index for index, flag in enumerate(sieve) if flag)


@lru_cache(maxsize=None)
def first_odd_primes(count: int) -> tuple[int, ...]:
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive exact integer")
    limit = 64
    while True:
        primes = tuple(prime for prime in sieve_primes(limit) if prime != 2)
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def prime_square_weight(prime: int) -> Fraction:
    if type(prime) is not int or prime < 3 or prime % 2 == 0:
        raise ValueError("an odd prime at least three is required")
    if any(prime % divisor == 0 for divisor in range(3, isqrt(prime) + 1, 2)):
        raise ValueError("an odd prime at least three is required")
    return Fraction(1, prime * prime - 1)


def _fraction_product(values: tuple[Fraction, ...]) -> Fraction:
    if any(type(value) is not Fraction for value in values):
        raise TypeError("all factors must be exact Fractions")
    output = Fraction(1)
    for value in values:
        output *= value
    return output


def _validate_weights(weights: tuple[Fraction, ...], *, allow_empty: bool = False) -> tuple[Fraction, ...]:
    if type(weights) is not tuple or (not weights and not allow_empty):
        raise TypeError("a tuple of exact tail weights is required")
    if any(type(weight) is not Fraction or weight <= 0 or weight >= 1 for weight in weights):
        raise ValueError("tail weights must be exact Fractions in (0,1)")
    return weights


@lru_cache(maxsize=None)
def tail_weights(start_y: int, endpoint_y: int) -> tuple[Fraction, ...]:
    if type(start_y) is not int or type(endpoint_y) is not int:
        raise TypeError("tail endpoints must be exact integers")
    if start_y < 1 or endpoint_y <= start_y:
        raise ValueError("tail endpoints require 1 <= start_y < endpoint_y")
    primes = first_odd_primes(endpoint_y)
    return tuple(prime_square_weight(prime) for prime in primes[start_y:endpoint_y])


@lru_cache(maxsize=None)
def finite_euler_values(y: int) -> dict[int, Fraction]:
    if type(y) is not int or y < 1:
        raise ValueError("Euler endpoint must be a positive exact integer")
    primes = first_odd_primes(y)
    return {
        m: _fraction_product(tuple(Fraction(prime * prime - m, prime * prime) for prime in primes))
        for m in range(1, 10)
    }


@lru_cache(maxsize=None)
def normalized_euler_ratios(y: int) -> dict[int, Fraction]:
    values = finite_euler_values(y)
    return {m: values[m] / values[1] for m in range(1, 9)}


def _exact_integer(value: Fraction, label: str) -> int:
    if type(value) is not Fraction or value.denominator != 1:
        raise ArithmeticError(f"{label} is not an exact integer")
    return value.numerator


def square_run_counts(y: int) -> dict[int, int]:
    """Use second differences only through length seven; keep ``R8`` terminal."""

    primes = first_odd_primes(y)
    period = 1
    for prime in primes:
        period *= prime * prime
    euler = finite_euler_values(y)
    rows = {
        length: _exact_integer(
            Fraction(period) * (euler[length] - 2 * euler[length + 1] + euler[length + 2]),
            f"R_{length}",
        )
        for length in range(1, 8)
    }
    rows[8] = _exact_integer(Fraction(period) * euler[8], "terminal R_8")
    return rows


def reject_length_eight_second_difference(length: int) -> None:
    if type(length) is not int or length != 8:
        raise ValueError("this mutation guard is only for the length-eight terminal")
    raise ValueError("R8 is terminal P*E8; an E10 second difference is forbidden")


def c_polynomial(values: dict[int, Fraction]) -> Fraction:
    if set(values) != set(range(1, 9)):
        raise ValueError("C requires exactly V1,...,V8 (V1 is retained for typing)")
    return Fraction(1) + sum((Fraction(ALPHA[m]) * values[m] for m in range(2, 9)), Fraction(0))


def w_polynomial(values: dict[int, Fraction]) -> Fraction:
    if set(values) != set(range(1, 9)):
        raise ValueError("W requires exactly V1,...,V8 (V1 is retained for typing)")
    return sum((Fraction(BETA[m]) * values[m] for m in range(2, 9)), Fraction(0))


def normalized_x(y: int) -> Fraction:
    ratios = normalized_euler_ratios(y)
    return sum((Fraction(coefficient) * ratios[m] for m, coefficient in XI.items()), Fraction(0))


def normalized_memory(y: int) -> Fraction:
    ratios = normalized_euler_ratios(y)
    value = sum((Fraction(coefficient) * ratios[m] for m, coefficient in ETA.items()), Fraction(0))
    if not Fraction(0) <= value <= Fraction(1):
        raise AssertionError("the normalized memory statistic left [0,1]")
    return value


def finite_tail_loss(weights: tuple[Fraction, ...]) -> Fraction:
    _validate_weights(weights, allow_empty=True)
    return Fraction(1) - _fraction_product(tuple(Fraction(1) - weight for weight in weights))


def finite_increment_pi2(start_y: int, endpoint_y: int) -> Fraction:
    weights = tail_weights(start_y, endpoint_y)
    first = weights[0]
    successor_loss = finite_tail_loss(weights[1:])
    return 2 * first * normalized_x(start_y) + 4 * first * normalized_memory(start_y) * successor_loss


@lru_cache(maxsize=None)
def finite_gap_pi2(start_y: int, endpoint_y: int) -> Fraction:
    weights = tail_weights(start_y, endpoint_y)
    output = Fraction(0)
    for offset, weight in enumerate(weights):
        j = start_y + offset
        successor = weights[offset + 1 :]
        output += 2 * weight * normalized_x(j)
        output += 4 * weight * normalized_memory(j) * finite_tail_loss(successor)
    return output


def endpoint_normal_form_pi2(start_y: int, endpoint_y: int) -> Fraction:
    weights = tail_weights(start_y, endpoint_y)
    start = normalized_euler_ratios(start_y)
    endpoint = normalized_euler_ratios(endpoint_y)
    exp_minus_phi_one = _fraction_product(tuple(Fraction(1) - weight for weight in weights))
    return 2 * (c_polynomial(endpoint) - c_polynomial(start)) - 4 * w_polynomial(start) * (
        Fraction(1) - exp_minus_phi_one
    )


@lru_cache(maxsize=None)
def partitions_of(degree: int, maximum_part: int | None = None) -> tuple[tuple[int, ...], ...]:
    _require_degree(degree)
    maximum = degree if maximum_part is None else min(maximum_part, degree)
    if type(maximum) is not int or maximum < 1:
        raise ValueError("maximum partition part must be a positive exact integer")

    def build(remaining: int, cap: int) -> tuple[tuple[int, ...], ...]:
        if remaining == 0:
            return ((),)
        rows: list[tuple[int, ...]] = []
        for part in range(min(remaining, cap), 0, -1):
            rows.extend((part,) + suffix for suffix in build(remaining - part, part))
        return tuple(rows)

    return build(degree, maximum)


ALL_PARTITIONS = tuple(partition for degree in range(1, MAX_DEGREE + 1) for partition in partitions_of(degree))


def validate_partition(partition: tuple[int, ...]) -> tuple[int, ...]:
    if type(partition) is not tuple or not partition:
        raise TypeError("a nonempty integer partition tuple is required")
    if any(type(part) is not int or part < 1 for part in partition):
        raise ValueError("partition parts must be positive exact integers")
    if any(left < right for left, right in zip(partition, partition[1:])):
        raise ValueError("partition must be in nonincreasing canonical order")
    return partition


def partition_multiplicities(partition: tuple[int, ...]) -> Counter[int]:
    return Counter(validate_partition(partition))


def partition_z(partition: tuple[int, ...]) -> int:
    multiplicities = partition_multiplicities(partition)
    output = 1
    for part, count in multiplicities.items():
        output *= part**count * factorial(count)
    return output


def power_sums(weights: tuple[Fraction, ...], maximum_degree: int) -> dict[int, Fraction]:
    _validate_weights(weights)
    _require_degree(maximum_degree)
    return {
        degree: sum((weight**degree for weight in weights), Fraction(0))
        for degree in range(1, maximum_degree + 1)
    }


def power_monomial(partition: tuple[int, ...], sums: dict[int, Fraction]) -> Fraction:
    multiplicities = partition_multiplicities(partition)
    if any(part not in sums or type(sums[part]) is not Fraction for part in multiplicities):
        raise ValueError("power-sum dictionary does not cover the partition")
    return _fraction_product(tuple(sums[part] ** count for part, count in multiplicities.items()))


@lru_cache(maxsize=None)
def complete_homogeneous(weights: tuple[Fraction, ...], maximum_degree: int) -> tuple[Fraction, ...]:
    _validate_weights(weights, allow_empty=True)
    _require_degree(maximum_degree, allow_zero=True)
    coefficients = [Fraction(1)] + [Fraction(0)] * maximum_degree
    for weight in weights:
        updated = [Fraction(0)] * (maximum_degree + 1)
        for degree in range(maximum_degree + 1):
            updated[degree] = sum(
                (coefficients[degree - power] * weight**power for power in range(degree + 1)),
                Fraction(0),
            )
        coefficients = updated
    return tuple(coefficients)


@lru_cache(maxsize=None)
def elementary_symmetric(weights: tuple[Fraction, ...], maximum_degree: int) -> tuple[Fraction, ...]:
    _validate_weights(weights, allow_empty=True)
    _require_degree(maximum_degree, allow_zero=True)
    coefficients = [Fraction(1)] + [Fraction(0)] * maximum_degree
    for weight in weights:
        for degree in range(maximum_degree, 0, -1):
            coefficients[degree] += weight * coefficients[degree - 1]
    return tuple(coefficients)


@lru_cache(maxsize=None)
def direct_a_coefficients(weights: tuple[Fraction, ...], c: int, maximum_degree: int) -> tuple[Fraction, ...]:
    _validate_weights(weights, allow_empty=True)
    if type(c) is not int or c < 1:
        raise ValueError("c must be a positive exact integer")
    _require_degree(maximum_degree, allow_zero=True)
    coefficients = [Fraction(1)] + [Fraction(0)] * maximum_degree
    for weight in weights:
        factor = tuple((Fraction(c) * weight) ** degree for degree in range(maximum_degree + 1))
        coefficients = [
            sum((coefficients[degree - power] * factor[power] for power in range(degree + 1)), Fraction(0))
            for degree in range(maximum_degree + 1)
        ]
    return tuple(coefficients)


@lru_cache(maxsize=None)
def direct_f_coefficients(weights: tuple[Fraction, ...], c: int, maximum_degree: int) -> tuple[Fraction, ...]:
    _validate_weights(weights, allow_empty=True)
    if type(c) is not int or c < 1:
        raise ValueError("c must be a positive exact integer")
    _require_degree(maximum_degree, allow_zero=True)
    coefficients = [Fraction(1)] + [Fraction(0)] * maximum_degree
    for weight in weights:
        factor = [Fraction(1)]
        factor.extend(Fraction(c - 1) * c ** (degree - 1) * weight**degree for degree in range(1, maximum_degree + 1))
        coefficients = [
            sum((coefficients[degree - power] * factor[power] for power in range(degree + 1)), Fraction(0))
            for degree in range(maximum_degree + 1)
        ]
    return tuple(coefficients)


def h_a_coefficient(weights: tuple[Fraction, ...], c: int, degree: int) -> Fraction:
    _require_degree(degree)
    return Fraction(c**degree) * complete_homogeneous(weights, degree)[degree]


def he_f_coefficient(weights: tuple[Fraction, ...], c: int, degree: int) -> Fraction:
    _require_degree(degree)
    h = complete_homogeneous(weights, degree)
    e = elementary_symmetric(weights, degree)
    return sum(
        ((-1) ** elementary_degree * e[elementary_degree] * c ** (degree - elementary_degree) * h[degree - elementary_degree]
         for elementary_degree in range(degree + 1)),
        Fraction(0),
    )


def phi_a_coefficient(weights: tuple[Fraction, ...], c: int, degree: int) -> Fraction:
    sums = power_sums(weights, degree)
    return sum(
        (Fraction(c**degree, partition_z(partition)) * power_monomial(partition, sums) for partition in partitions_of(degree)),
        Fraction(0),
    )


def phi_f_coefficient(weights: tuple[Fraction, ...], c: int, degree: int) -> Fraction:
    sums = power_sums(weights, degree)
    output = Fraction(0)
    for partition in partitions_of(degree):
        multiplicities = partition_multiplicities(partition)
        numerator = 1
        for part, count in multiplicities.items():
            numerator *= (c**part - 1) ** count
        output += Fraction(numerator, partition_z(partition)) * power_monomial(partition, sums)
    return output


def cw_gamma_vector(partition: tuple[int, ...]) -> dict[int, Fraction]:
    multiplicities = partition_multiplicities(partition)
    degree = sum(partition)
    denominator = partition_z(partition)
    output: dict[int, Fraction] = {}
    for m in range(2, 9):
        c = m - 1
        f_numerator = 1
        for part, count in multiplicities.items():
            f_numerator *= (c**part - 1) ** count
        output[m] = (
            Fraction(-2 * ALPHA[m] * c**degree, denominator)
            - Fraction(4 * BETA[m] * (c**degree - f_numerator), denominator)
        )
    return output


def af_gamma_vector(partition: tuple[int, ...]) -> dict[int, Fraction]:
    multiplicities = partition_multiplicities(partition)
    degree = sum(partition)
    denominator = partition_z(partition)
    output = {m: Fraction(0) for m in range(2, 9)}
    for m in range(3, 9):
        c = m - 1
        f_numerator = 1
        for part, count in multiplicities.items():
            f_numerator *= (c**part - 1) ** count
        a_coefficient = Fraction(c**degree, denominator)
        f_coefficient = Fraction(f_numerator, denominator)
        output[m] = (
            Fraction(2 * XI.get(m, 0), c) * a_coefficient
            + 4 * ETA.get(m, 0) * (a_coefficient / c - f_coefficient / (c - 1))
        )
    return output


def evaluate_vector(vector: dict[int, Fraction], values: dict[int, Fraction]) -> Fraction:
    if set(vector) != set(range(2, 9)) or set(values) != set(range(1, 9)):
        raise ValueError("coefficient and Euler-ratio vectors have incompatible domains")
    return sum((vector[m] * values[m] for m in range(2, 9)), Fraction(0))


def endpoint_degree_vector(weights: tuple[Fraction, ...], degree: int) -> dict[int, Fraction]:
    """Direct ``C/W`` endpoint coefficient after scaling every weight by t."""

    _require_degree(degree)
    output: dict[int, Fraction] = {}
    for m in range(2, 9):
        c = m - 1
        a_coefficient = direct_a_coefficients(weights, c, degree)[degree]
        f_coefficient = direct_f_coefficients(weights, c, degree)[degree]
        output[m] = -2 * ALPHA[m] * a_coefficient - 4 * BETA[m] * (a_coefficient - f_coefficient)
    return output


def endpoint_increment_channel_vectors(weights: tuple[Fraction, ...], degree: int) -> dict[str, dict[int, Fraction]]:
    """The direct A/F telescope split matching the original increment split."""

    _require_degree(degree)
    numerator = {m: Fraction(0) for m in range(2, 9)}
    memory = {m: Fraction(0) for m in range(2, 9)}
    for m in range(3, 9):
        c = m - 1
        a_coefficient = direct_a_coefficients(weights, c, degree)[degree]
        f_coefficient = direct_f_coefficients(weights, c, degree)[degree]
        numerator[m] = Fraction(2 * XI.get(m, 0), c) * a_coefficient
        memory[m] = 4 * ETA.get(m, 0) * (a_coefficient / c - f_coefficient / (c - 1))
    return {"numerator": numerator, "memory": memory}


def ordered_increment_channel_vectors(weights: tuple[Fraction, ...], degree: int) -> dict[str, dict[int, Fraction]]:
    """Independent ordered-tail compiler using complete/elementary functions.

    The memory loss is on the strict successor suffix.  Replacing it by the
    current suffix is the forbidden mutation that changes the quadratic
    ``P_2`` sign.
    """

    _validate_weights(weights)
    _require_degree(degree)
    numerator = {m: Fraction(0) for m in range(2, 9)}
    memory = {m: Fraction(0) for m in range(2, 9)}
    for index, weight in enumerate(weights):
        current = weights[index:]
        successor = weights[index + 1 :]
        h_current = complete_homogeneous(current, degree - 1)
        e_successor = elementary_symmetric(successor, degree - 1)
        for m in range(3, 9):
            c = m - 1
            numerator[m] += 2 * XI.get(m, 0) * weight * c ** (degree - 1) * h_current[degree - 1]
            memory_piece = Fraction(0)
            for h_degree in range(0, degree - 1):
                loss_degree = degree - 1 - h_degree
                loss = Fraction((-1) ** (loss_degree + 1)) * e_successor[loss_degree]
                memory_piece += c**h_degree * h_current[h_degree] * loss
            memory[m] += 4 * ETA.get(m, 0) * weight * memory_piece
    return {"numerator": numerator, "memory": memory}


def partition_degree_value(weights: tuple[Fraction, ...], degree: int, endpoint_values: dict[int, Fraction]) -> Fraction:
    sums = power_sums(weights, degree)
    return sum(
        (
            evaluate_vector(cw_gamma_vector(partition), endpoint_values)
            * power_monomial(partition, sums)
            for partition in partitions_of(degree)
        ),
        Fraction(0),
    )


def endpoint_degree_value(weights: tuple[Fraction, ...], degree: int, endpoint_values: dict[int, Fraction]) -> Fraction:
    return evaluate_vector(endpoint_degree_vector(weights, degree), endpoint_values)


def truncation_value(weights: tuple[Fraction, ...], degree: int, endpoint_values: dict[int, Fraction]) -> Fraction:
    require_truncation_degree(degree)
    return sum((partition_degree_value(weights, current, endpoint_values) for current in range(1, degree + 1)), Fraction(0))


def low_order_expected_vectors() -> dict[tuple[int, ...], dict[int, Fraction]]:
    first = {m: Fraction(2 * XI.get(m, 0)) for m in range(2, 9)}
    y_variation = {m: Fraction(XI.get(m, 0) * (m - 1)) for m in range(2, 9)}
    square = {m: y_variation[m] + 2 * ETA.get(m, 0) for m in range(2, 9)}
    independent = {m: y_variation[m] - 2 * ETA.get(m, 0) for m in range(2, 9)}
    return {(1,): first, (1, 1): square, (2,): independent}


CUBIC_VECTORS = {
    (1, 1, 1): {2: 0, 3: 4, 4: Fraction(-22, 3), 5: Fraction(20, 3), 6: 2, 7: Fraction(-68, 3), 8: Fraction(178, 3)},
    (2, 1): {2: 0, 3: 4, 4: 10, 5: -52, 6: 134, 7: -268, 8: 466},
    (3,): {2: 0, 3: -8, 4: Fraction(100, 3), 5: Fraction(-248, 3), 6: 164, 7: Fraction(-856, 3), 8: Fraction(1364, 3)},
}


def remainder_ledger() -> dict[str, object]:
    x_terms = {
        str(m): Fraction(abs(XI[m]) * (9 - m), 8)
        for m in XI
    }
    memory_terms = {
        str(m): Fraction(abs(ETA[m]) * (9 - m), 8)
        for m in ETA
    }
    x_sum = sum(x_terms.values(), Fraction(0))
    memory_sum = sum(memory_terms.values(), Fraction(0))
    x_homogeneous = 2 * x_sum / 7
    # The loss has s>=1.  The audited Phi/h/e sum contributes at most 1/42;
    # four times the ETA ledger gives the homogeneous 4/3 coefficient.
    phi_loss_factor = Fraction(1, 42)
    memory_homogeneous = 4 * memory_sum * phi_loss_factor
    x_tail = GEOMETRIC_TAIL_FACTOR * x_homogeneous
    memory_tail = GEOMETRIC_TAIL_FACTOR * memory_homogeneous
    total = x_tail + memory_tail
    all_pass = (
        x_sum == INCREMENT_X_ABSOLUTE_LEDGER
        and memory_sum == INCREMENT_MEMORY_ABSOLUTE_LEDGER
        and x_homogeneous == X_HOMOGENEOUS_MAJORANT
        and memory_homogeneous == MEMORY_HOMOGENEOUS_MAJORANT
        and x_tail == 20
        and memory_tail == Fraction(32, 3)
        and total == REMAINDER_MAJORANT_PI2
        and total < PUBLISHED_COARSE_MAJORANT_PI2
        and tuple(XI) != tuple(ALPHA)
        and tuple(ETA) != tuple(BETA)
    )
    return {
        "increment_x_coefficients": {str(key): value for key, value in XI.items()},
        "increment_memory_coefficients": {str(key): value for key, value in ETA.items()},
        "endpoint_alpha_coefficients": {str(key): value for key, value in ALPHA.items()},
        "endpoint_beta_coefficients": {str(key): value for key, value in BETA.items()},
        "nomenclature_firewall": "35/4 and 14 belong only to increment XI/ETA, never endpoint ALPHA/BETA",
        "x_absolute_terms": {key: fraction_text(value) for key, value in x_terms.items()},
        "x_absolute_sum": fraction_text(x_sum),
        "memory_absolute_terms": {key: fraction_text(value) for key, value in memory_terms.items()},
        "memory_absolute_sum": fraction_text(memory_sum),
        "x_homogeneous": fraction_text(x_homogeneous),
        "memory_phi_loss_factor": fraction_text(phi_loss_factor),
        "memory_homogeneous": fraction_text(memory_homogeneous),
        "geometric_tail_factor": GEOMETRIC_TAIL_FACTOR,
        "x_tail": fraction_text(x_tail),
        "memory_tail": fraction_text(memory_tail),
        "total_pi2": fraction_text(total),
        "published_coarse_pi2": PUBLISHED_COARSE_MAJORANT_PI2,
        "all_pass": all_pass,
    }


def _digest_rows(rows: list[dict[str, object]]) -> str:
    return payload_sha256(rows)


def _fraction_vector_text(vector: dict[int, Fraction]) -> dict[str, str]:
    return {str(m): fraction_text(vector[m]) for m in sorted(vector)}


def endpoint_normal_form_certificate() -> dict[str, object]:
    rows = []
    for start, endpoint in DIRECT_CASES:
        increment = finite_gap_pi2(start, endpoint)
        normal = endpoint_normal_form_pi2(start, endpoint)
        rows.append({"start": start, "endpoint": endpoint, "pass": increment == normal})
    return {
        "count": len(rows),
        "row_digest": _digest_rows(rows),
        "samples": rows[:2] + rows[-2:],
        "all_pass": len(rows) == EXPECTED_COUNTS["endpoint_normal_form"] and all(row["pass"] for row in rows),
    }


def af_coefficient_certificate() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    q_rows: list[dict[str, object]] = []
    for start, endpoint in FINITE_TAIL_CASES:
        weights = tail_weights(start, endpoint)
        for c in range(2, 8):
            direct_a = direct_a_coefficients(weights, c, MAX_DEGREE)
            direct_f = direct_f_coefficients(weights, c, MAX_DEGREE)
            for degree in range(1, MAX_DEGREE + 1):
                a_h = h_a_coefficient(weights, c, degree)
                a_phi = phi_a_coefficient(weights, c, degree)
                f_he = he_f_coefficient(weights, c, degree)
                f_phi = phi_f_coefficient(weights, c, degree)
                rows.append({
                    "kind": "A",
                    "start": start,
                    "endpoint": endpoint,
                    "c": c,
                    "degree": degree,
                    "pass": direct_a[degree] == a_h == a_phi,
                })
                rows.append({
                    "kind": "F",
                    "start": start,
                    "endpoint": endpoint,
                    "c": c,
                    "degree": degree,
                    "pass": direct_f[degree] == f_he == f_phi,
                })
                sums = power_sums(weights, degree)
                q_partition = sum(
                    (
                        Fraction((-1) ** len(partition), partition_z(partition))
                        * power_monomial(partition, sums)
                        for partition in partitions_of(degree)
                    ),
                    Fraction(0),
                )
                q_elementary = Fraction((-1) ** degree) * elementary_symmetric(weights, degree)[degree]
                loss_partition = -q_partition
                q_rows.append({
                    "start": start,
                    "endpoint": endpoint,
                    "c_label": c,
                    "degree": degree,
                    "c_label_is_redundant": True,
                    "q_partition": fraction_text(q_partition),
                    "q_elementary": fraction_text(q_elementary),
                    "a_minus_f_nonnegative_separate_check": direct_a[degree] - direct_f[degree] >= 0,
                    "pass": (
                        q_partition == q_elementary
                        and Fraction((-1) ** degree) * q_partition >= 0
                        and Fraction((-1) ** (degree + 1)) * loss_partition >= 0
                    ),
                })
    return {
        "coefficient_count": len(rows),
        "coefficient_digest": _digest_rows(rows),
        "coefficient_samples": rows[:2] + rows[-2:],
        "q_sign_count": len(q_rows),
        "q_sign_digest": _digest_rows(q_rows),
        "q_sign_redundancy_note": "432 labeled rows repeat 72 tail/degree Q identities under six inert c labels; Q is independent of c, and the repetitions are not 432 different theorems",
        "q_sign_samples": q_rows[:2] + q_rows[-2:],
        "all_pass": (
            len(rows) == EXPECTED_COUNTS["af_coefficients"]
            and len(q_rows) == EXPECTED_COUNTS["q_signs"]
            and all(row["pass"] for row in rows)
            and all(row["pass"] for row in q_rows)
        ),
    }


def gamma_equivalence_certificate() -> dict[str, object]:
    rows = []
    m2_rows = []
    for endpoint in COFINAL_ENDPOINTS:
        values = normalized_euler_ratios(endpoint)
        for partition in ALL_PARTITIONS:
            cw = cw_gamma_vector(partition)
            af = af_gamma_vector(partition)
            rows.append({
                "endpoint": endpoint,
                "partition": list(partition),
                "pass": cw == af and evaluate_vector(cw, values) == evaluate_vector(af, values),
            })
            m2_rows.append({
                "endpoint": endpoint,
                "partition": list(partition),
                "pass": cw[2] == af[2] == 0,
            })
    direct_rows = []
    for start, endpoint in DIRECT_CASES:
        weights = tail_weights(start, endpoint)
        a_one = _fraction_product(tuple(Fraction(1, 1 - weight) for weight in weights))
        f_one = Fraction(1)
        u2 = normalized_euler_ratios(endpoint)[2]
        c_piece = -2 * ALPHA[2] * u2 * (a_one - 1)
        w_piece = -4 * BETA[2] * u2 * (a_one - f_one)
        direct_rows.append({"start": start, "endpoint": endpoint, "pass": c_piece + w_piece == 0})
    return {
        "gamma_count": len(rows),
        "gamma_digest": _digest_rows(rows),
        "gamma_redundancy_note": "1084=271 unique symbolic partitions times four endpoint labels; these are labeled exact evaluations, not 1084 different identities",
        "gamma_samples": rows[:2] + rows[-2:],
        "m2_partition_count": len(m2_rows),
        "m2_partition_digest": _digest_rows(m2_rows),
        "m2_direct_count": len(direct_rows),
        "m2_direct_digest": _digest_rows(direct_rows),
        "m2_total_count": len(m2_rows) + len(direct_rows),
        "m2_redundancy_note": "1151=271 unique symbolic cancellations times four endpoint labels, plus 67 direct finite telescopes; this is not 1151 distinct all-order theorems",
        "all_pass": (
            len(rows) == EXPECTED_COUNTS["gamma_equivalence"]
            and len(m2_rows) + len(direct_rows) == EXPECTED_COUNTS["m2_cancellation"]
            and all(row["pass"] for row in rows + m2_rows + direct_rows)
        ),
    }


def channel_equivalence_certificate() -> dict[str, object]:
    rows = []
    for start, endpoint in FINITE_TAIL_CASES:
        weights = tail_weights(start, endpoint)
        for degree in range(1, MAX_DEGREE + 1):
            ordered = ordered_increment_channel_vectors(weights, degree)
            telescoped = endpoint_increment_channel_vectors(weights, degree)
            for channel in ("numerator", "memory"):
                rows.append({
                    "start": start,
                    "endpoint": endpoint,
                    "degree": degree,
                    "channel": channel,
                    "pass": ordered[channel] == telescoped[channel],
                })
    return {
        "count": len(rows),
        "row_digest": _digest_rows(rows),
        "samples": rows[:2] + rows[-2:],
        "all_pass": len(rows) == EXPECTED_COUNTS["channel_equivalence"] and all(row["pass"] for row in rows),
    }


def low_order_certificate() -> dict[str, object]:
    expected = low_order_expected_vectors()
    rows = []
    for endpoint in LOW_ORDER_ENDPOINTS:
        values = normalized_euler_ratios(endpoint)
        checks = {
            str(partition): cw_gamma_vector(partition) == vector
            and evaluate_vector(cw_gamma_vector(partition), values) == evaluate_vector(vector, values)
            for partition, vector in expected.items()
        }
        rows.append({"endpoint": endpoint, "checks": checks, "pass": all(checks.values())})
    return {
        "count": len(rows),
        "row_digest": _digest_rows(rows),
        "statement": "gamma_(1)=2X; gamma_(1,1)=Y+2m; gamma_(2)=Y-2m, retaining the independent P2 sign",
        "redundancy_note": "33 endpoint-labeled bundles repeat the same three symbolic coefficient identities; these are not 33 different theorems",
        "samples": rows[:2] + rows[-2:],
        "all_pass": len(rows) == EXPECTED_COUNTS["low_order"] and all(row["pass"] for row in rows),
    }


def cubic_certificate() -> dict[str, object]:
    symbolic_rows = []
    for endpoint in COFINAL_ENDPOINTS:
        values = normalized_euler_ratios(endpoint)
        for partition, expected in CUBIC_VECTORS.items():
            expected_fraction = {m: Fraction(coefficient) for m, coefficient in expected.items()}
            actual = cw_gamma_vector(partition)
            symbolic_rows.append({
                "endpoint": endpoint,
                "partition": list(partition),
                "pass": actual == expected_fraction and evaluate_vector(actual, values) == evaluate_vector(expected_fraction, values),
            })
    endpoint_rows = []
    for start, endpoint in DIRECT_CASES:
        weights = tail_weights(start, endpoint)
        values = normalized_euler_ratios(endpoint)
        partition_value = partition_degree_value(weights, 3, values)
        direct_value = endpoint_degree_value(weights, 3, values)
        endpoint_rows.append({"start": start, "endpoint": endpoint, "pass": partition_value == direct_value})
    return {
        "symbolic_count": len(symbolic_rows),
        "symbolic_digest": _digest_rows(symbolic_rows),
        "endpoint_count": len(endpoint_rows),
        "endpoint_digest": _digest_rows(endpoint_rows),
        "frozen_vectors": {str(key): _fraction_vector_text({m: Fraction(value) for m, value in vector.items()}) for key, vector in CUBIC_VECTORS.items()},
        "all_pass": (
            len(symbolic_rows) == EXPECTED_COUNTS["cubic_symbolic"]
            and len(endpoint_rows) == EXPECTED_COUNTS["cubic_endpoint"]
            and all(row["pass"] for row in symbolic_rows + endpoint_rows)
        ),
    }


def remainder_certificate() -> dict[str, object]:
    rows = []
    for start, endpoint in DIRECT_CASES:
        weights = tail_weights(start, endpoint)
        values = normalized_euler_ratios(endpoint)
        exact = endpoint_normal_form_pi2(start, endpoint)
        total = sum(weights, Fraction(0))
        rho = 7 * total
        if rho > Fraction(7, 8):
            raise AssertionError("the finite square-prime tail exceeded rho=7/8")
        cumulative = Fraction(0)
        for degree in range(1, MAX_DEGREE + 1):
            cumulative += partition_degree_value(weights, degree, values)
            remainder = exact - cumulative
            bound = REMAINDER_MAJORANT_PI2 * rho ** (degree + 1)
            rows.append({
                "start": start,
                "endpoint": endpoint,
                "D": degree,
                "pass": abs(remainder) <= bound,
            })
    return {
        "count": len(rows),
        "row_digest": _digest_rows(rows),
        "samples": rows[:2] + rows[-2:],
        "bound": "abs(pi^2 R_D)<=92*rho^(D+1)/3, hence abs(R_D)<=92*rho^(D+1)/(3*pi^2)",
        "all_pass": len(rows) == EXPECTED_COUNTS["remainder"] and all(row["pass"] for row in rows),
    }


def terminal_certificate() -> dict[str, object]:
    rows = []
    for y in (1, 2, 3, 6):
        euler = finite_euler_values(y)
        primes = first_odd_primes(y)
        period = 1
        for prime in primes:
            period *= prime * prime
        runs = square_run_counts(y)
        terminal = _exact_integer(Fraction(period) * euler[8], "terminal R8")
        rows.append({
            "y": y,
            "E9": fraction_text(euler[9]),
            "R8": runs[8],
            "P_E8": terminal,
            "E10_constructed": False,
            "pass": euler[9] == 0 and runs[8] == terminal,
        })
    return {
        "count": len(rows),
        "rows": rows,
        "construction": "R_l=P(E_l-2E_(l+1)+E_(l+2)) only for l<=7; R8=P*E8 separately; E9=0; no E10",
        "all_pass": len(rows) == EXPECTED_COUNTS["terminal"] and all(row["pass"] for row in rows),
    }


def successor_tail_certificate() -> dict[str, object]:
    endpoint = 32
    rows = []
    for start in TAIL_TELESCOPE_STARTS:
        left = finite_gap_pi2(start, endpoint) - finite_gap_pi2(start + 1, endpoint)
        right = finite_increment_pi2(start, endpoint)
        rows.append({"start": start, "endpoint": endpoint, "pass": left == right})
    return {
        "count": len(rows),
        "row_digest": _digest_rows(rows),
        "indexing": "the memory loss begins at j+1, the strict successor suffix",
        "rows": rows,
        "all_pass": len(rows) == EXPECTED_COUNTS["successor_tail"] and all(row["pass"] for row in rows),
    }


def _loss_partition_sign(partition: tuple[int, ...]) -> int:
    validate_partition(partition)
    return (-1) ** (len(partition) + 1)


def _wrong_degree_loss_sign(partition: tuple[int, ...]) -> int:
    validate_partition(partition)
    return (-1) ** (sum(partition) + 1)


def _exact_json_value(value: object) -> object:
    if type(value) is Fraction:
        return fraction_text(value)
    if type(value) is dict:
        return {str(key): _exact_json_value(item) for key, item in value.items()}
    if type(value) in (tuple, list):
        return [_exact_json_value(item) for item in value]
    if type(value) in (str, int, bool) or value is None:
        return value
    raise TypeError(f"unsupported exact mutation payload: {type(value).__name__}")


def _oracle_mutation_row(name: str, expected: object, wrong: object) -> dict[str, object]:
    expected_payload = _exact_json_value(expected)
    wrong_payload = _exact_json_value(wrong)
    return {
        "mutation": name,
        "expected_digest": payload_sha256(expected_payload),
        "wrong_digest": payload_sha256(wrong_payload),
        "pass": expected_payload != wrong_payload,
    }


def _gamma_with_denominator(partition: tuple[int, ...], denominator: int) -> dict[int, Fraction]:
    multiplicities = partition_multiplicities(partition)
    degree = sum(partition)
    if type(denominator) is not int or denominator < 1:
        raise ValueError("mutated denominator must remain a positive exact integer")
    output: dict[int, Fraction] = {}
    for m in range(2, 9):
        c = m - 1
        f_numerator = 1
        for part, count in multiplicities.items():
            f_numerator *= (c**part - 1) ** count
        output[m] = (
            Fraction(-2 * ALPHA[m] * c**degree, denominator)
            - Fraction(4 * BETA[m] * (c**degree - f_numerator), denominator)
        )
    return output


def _wrong_current_tail_gap_pi2(start_y: int, endpoint_y: int) -> Fraction:
    weights = tail_weights(start_y, endpoint_y)
    output = Fraction(0)
    for offset, weight in enumerate(weights):
        j = start_y + offset
        current_loss = finite_tail_loss(weights[offset:])
        output += 2 * weight * normalized_x(j)
        output += 4 * weight * normalized_memory(j) * current_loss
    return output


def _mutated_endpoint_prefactors(start_y: int, endpoint_y: int, c_factor: int, memory_factor: int) -> Fraction:
    weights = tail_weights(start_y, endpoint_y)
    start = normalized_euler_ratios(start_y)
    endpoint = normalized_euler_ratios(endpoint_y)
    product = _fraction_product(tuple(Fraction(1) - weight for weight in weights))
    return c_factor * (c_polynomial(endpoint) - c_polynomial(start)) - memory_factor * w_polynomial(start) * (
        Fraction(1) - product
    )


def _mutated_m2_coefficient(partition: tuple[int, ...], alpha2: int, beta2: int) -> Fraction:
    multiplicities = partition_multiplicities(partition)
    denominator = partition_z(partition)
    degree = sum(partition)
    f_numerator = 1
    for part, count in multiplicities.items():
        f_numerator *= (1**part - 1) ** count
    return Fraction(-2 * alpha2 * 1**degree, denominator) - Fraction(
        4 * beta2 * (1**degree - f_numerator), denominator
    )


def _gamma_with_memory_plus_f(partition: tuple[int, ...]) -> dict[int, Fraction]:
    multiplicities = partition_multiplicities(partition)
    degree = sum(partition)
    denominator = partition_z(partition)
    output: dict[int, Fraction] = {}
    for m in range(2, 9):
        c = m - 1
        f_numerator = 1
        for part, count in multiplicities.items():
            f_numerator *= (c**part - 1) ** count
        output[m] = Fraction(-2 * ALPHA[m] * c**degree, denominator) - Fraction(
            4 * BETA[m] * (c**degree + f_numerator), denominator
        )
    return output


def _gamma_with_plus_one_factors(partition: tuple[int, ...]) -> dict[int, Fraction]:
    multiplicities = partition_multiplicities(partition)
    degree = sum(partition)
    denominator = partition_z(partition)
    output: dict[int, Fraction] = {}
    for m in range(2, 9):
        c = m - 1
        wrong_f = 1
        for part, count in multiplicities.items():
            wrong_f *= (c**part + 1) ** count
        output[m] = Fraction(-2 * ALPHA[m] * c**degree, denominator) - Fraction(
            4 * BETA[m] * (c**degree - wrong_f), denominator
        )
    return output


def _mutated_finite_increment_pi2(
    start_y: int,
    endpoint_y: int,
    *,
    xi_override: dict[int, int] | None = None,
    eta_override: dict[int, int] | None = None,
) -> Fraction:
    weights = tail_weights(start_y, endpoint_y)
    first = weights[0]
    ratios = normalized_euler_ratios(start_y)
    xi = XI if xi_override is None else xi_override
    eta = ETA if eta_override is None else eta_override
    x_value = sum((Fraction(coefficient) * ratios[m] for m, coefficient in xi.items()), Fraction(0))
    memory_value = sum((Fraction(coefficient) * ratios[m] for m, coefficient in eta.items()), Fraction(0))
    return 2 * first * x_value + 4 * first * memory_value * finite_tail_loss(weights[1:])


def negative_mutation_certificate() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    sign_weights = tail_weights(1, 4)
    for degree in (2, 3, 4):
        sums = power_sums(sign_weights, degree)
        correct = Fraction((-1) ** degree) * elementary_symmetric(sign_weights, degree)[degree]
        wrong = sum(
            (
                Fraction((-1) ** degree, partition_z(partition))
                * power_monomial(partition, sums)
                for partition in partitions_of(degree)
            ),
            Fraction(0),
        )
        rows.append(_oracle_mutation_row(f"Q_length_parity_replaced_by_total_degree_{degree}", correct, wrong))

    denominator_cases = (
        ((1, 1, 1), 1, "omit_multiplicity_factorial"),
        ((2,), 1, "omit_part_power"),
        ((2, 1), factorial(3), "replace_z_by_degree_factorial"),
    )
    for partition, wrong_denominator, label in denominator_cases:
        rows.append(_oracle_mutation_row(
            f"gamma_{label}_{partition}",
            af_gamma_vector(partition),
            _gamma_with_denominator(partition, wrong_denominator),
        ))

    rows.append(_oracle_mutation_row(
        "successor_tail_replaced_by_current_in_full_gap",
        endpoint_normal_form_pi2(18, 19),
        _wrong_current_tail_gap_pi2(18, 19),
    ))
    rows.append(_oracle_mutation_row(
        "endpoint_C_prefactor_2_replaced_by_1",
        finite_gap_pi2(1, 8),
        _mutated_endpoint_prefactors(1, 8, 1, 4),
    ))
    rows.append(_oracle_mutation_row(
        "endpoint_memory_prefactor_4_replaced_by_2",
        finite_gap_pi2(1, 8),
        _mutated_endpoint_prefactors(1, 8, 2, 2),
    ))

    m2_partition = (5, 3, 2, 1)
    rows.append(_oracle_mutation_row(
        "m2_endpoint_alpha_minus2_replaced_by_minus1",
        af_gamma_vector(m2_partition)[2],
        _mutated_m2_coefficient(m2_partition, -1, 1),
    ))
    rows.append(_oracle_mutation_row(
        "m2_endpoint_beta_1_replaced_by_2",
        af_gamma_vector(m2_partition)[2],
        _mutated_m2_coefficient(m2_partition, -2, 2),
    ))

    rows.append(_oracle_mutation_row(
        "cubic_memory_A_minus_F_replaced_by_A_plus_F",
        af_gamma_vector((1, 1, 1)),
        _gamma_with_memory_plus_f((1, 1, 1)),
    ))
    rows.append(_oracle_mutation_row(
        "cubic_factor_c_power_minus1_replaced_by_c_power_plus1",
        af_gamma_vector((2, 1)),
        _gamma_with_plus_one_factors((2, 1)),
    ))

    wrong_xi = dict(XI)
    wrong_xi[4] = 1
    rows.append(_oracle_mutation_row(
        "increment_xi_m4_2_replaced_by_1",
        finite_increment_pi2(3, 12),
        _mutated_finite_increment_pi2(3, 12, xi_override=wrong_xi),
    ))
    wrong_eta = dict(ETA)
    wrong_eta[4] = 2
    rows.append(_oracle_mutation_row(
        "increment_eta_m4_minus4_replaced_by_2",
        finite_increment_pi2(3, 12),
        _mutated_finite_increment_pi2(3, 12, eta_override=wrong_eta),
    ))

    for label, value in (("D_bool", True), ("D_float", 1.0), ("D_zero", 0)):
        rejected = False
        try:
            require_truncation_degree(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            rejected = True
        rows.append({"mutation": label, "rejected_exception": "ValueError", "pass": rejected})

    terminal_rejected = False
    try:
        reject_length_eight_second_difference(8)
    except ValueError:
        terminal_rejected = True
    rows.append({"mutation": "terminal_R8_second_difference_E10", "rejected_exception": "ValueError", "pass": terminal_rejected})

    rho_weights = tail_weights(1, 8)
    rho_values = normalized_euler_ratios(8)
    rho_degree = 3
    rho_exact = endpoint_normal_form_pi2(1, 8)
    rho_truncation = truncation_value(rho_weights, rho_degree, rho_values)
    rho_residual = abs(rho_exact - rho_truncation)
    rho_total = sum(rho_weights, Fraction(0))
    correct_rho_bound = remainder_bound_pi2_from_rho(7 * rho_total, rho_degree)
    wrong_rho_bound = REMAINDER_MAJORANT_PI2 * rho_total ** (rho_degree + 1)
    rows.append({
        "mutation": "rho_7T_replaced_by_T_in_remainder_bound",
        "expected_digest": payload_sha256(_exact_json_value(correct_rho_bound)),
        "wrong_digest": payload_sha256(_exact_json_value(wrong_rho_bound)),
        "wrong_residual_to_bound": fraction_text(rho_residual / wrong_rho_bound),
        "pass": rho_residual <= correct_rho_bound and rho_residual > wrong_rho_bound,
    })

    return {
        "count": len(rows),
        "rejected": sum(bool(row["pass"]) for row in rows),
        "rows": rows,
        "all_pass": len(rows) == EXPECTED_COUNTS["negative_mutations"] and all(row["pass"] for row in rows),
    }


def proof_ledger() -> dict[str, object]:
    return {
        "absolute_convergence": "for c<=7, sum_r c^r P_r/r converges absolutely because c*a_(j+1)<=7/24 and sum a_(j+1)<infinity",
        "endpoint_products": "A_c=exp(Phi_c)=product(1-ca)^(-1), F_c=exp(Phi_c-Phi_1)=product(1-a)/(1-ca)",
        "partition_sign": "exp(-Phi_1) uses (-1)^length(lambda); 1-exp(-Phi_1) uses (-1)^(length(lambda)+1)",
        "m2": "for every nonempty partition, the endpoint alpha_2 and beta_2 terms cancel exactly",
        "increment_x_bound": "sum_(m=4)^8 |xi_m|u_m<=35/4 gives |Gamma_X,n|<=5*rho^n/2",
        "increment_memory_bound": "sum_(m=3)^8 |eta_m|u_m<=14 and the successor loss s>=1 give |Gamma_M,n|<=4*rho^n/3",
        "tail_bound": "rho<=7/8 and sum_(n>D)rho^n<=8*rho^(D+1), hence 20+32/3=92/3",
        "general_vs_special": "the 92/3 arbitrary-order ledger does not inherit the sharper RH-381 or RH-382 special-purpose constants",
        "finite_rows_are_reproduction_only": True,
    }


@lru_cache(maxsize=1)
def build_certificate() -> dict[str, object]:
    if len(ALL_PARTITIONS) != 271 or len(DIRECT_CASES) != 67:
        raise AssertionError("the frozen partition or endpoint grid drifted")
    sections = {
        "endpoint_normal_form": endpoint_normal_form_certificate(),
        "af_coefficients": af_coefficient_certificate(),
        "gamma_equivalence": gamma_equivalence_certificate(),
        "channel_equivalence": channel_equivalence_certificate(),
        "low_order": low_order_certificate(),
        "cubic": cubic_certificate(),
        "remainder": remainder_certificate(),
        "remainder_ledger": remainder_ledger(),
        "terminal": terminal_certificate(),
        "successor_tail": successor_tail_certificate(),
        "negative_mutations": negative_mutation_certificate(),
    }
    all_pass = all(section["all_pass"] for section in sections.values())
    return {
        "status": "RH-383_exact_euler_tail_partition_certificate",
        "counts": EXPECTED_COUNTS,
        "partition_count_degrees_1_through_12": len(ALL_PARTITIONS),
        "sections": sections,
        "proof_ledger": proof_ledger(),
        "claim_boundary": {
            "fixed_finite_q_before_N_limit": True,
            "universally_safe_phasewise_c11_zero_only": True,
            "finite_rows_are_reproduction_only": True,
            "rho_is_not_square_clock_q": True,
            "no_PNT_or_p_y_rewrite": True,
            "no_growing_clock_or_adaptive_capacity": True,
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "no_operator_trace_zeros_or_RH": True,
            "gates_A_through_E": [False, False, False, False, False],
        },
        "all_pass": all_pass,
    }


def verify_certificate() -> dict[str, object]:
    certificate = build_certificate()
    if not certificate["all_pass"]:
        raise AssertionError("the exact RH-383 certificate has a failed section")
    if len(canonical_json_bytes(certificate)) != CERTIFICATE_FIXTURE_BYTES:
        raise AssertionError("the canonical RH-383 certificate byte count drifted")
    if payload_sha256(certificate) != CERTIFICATE_FIXTURE_SHA256:
        raise AssertionError("the canonical RH-383 certificate digest drifted")
    return certificate
