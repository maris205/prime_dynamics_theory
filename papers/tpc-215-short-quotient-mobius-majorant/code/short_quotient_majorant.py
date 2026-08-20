"""Exact finite support for the TPC-215 short-quotient majorant."""

from __future__ import annotations

import hashlib
import math
from fractions import Fraction
from math import gcd
from typing import Iterable


Q_VALUES = (11, 13, 17)
HEIGHT = 40
LOWER_CUTOFF = 2
UPPER_CUTOFF = 35


class AuditFailure(RuntimeError):
    """Raised when an exact release invariant fails."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise AuditFailure(message)


def squarefree_factors(value: int) -> tuple[int, ...]:
    """Return the prime factors of a positive squarefree integer."""

    require(type(value) is int and value >= 1, "positive integer required")
    factors: list[int] = []
    remainder = value
    candidate = 2
    while candidate * candidate <= remainder:
        if remainder % candidate == 0:
            factors.append(candidate)
            remainder //= candidate
            if remainder % candidate == 0:
                raise ValueError("squarefree integer required")
        candidate += 1
    if remainder > 1:
        factors.append(remainder)
    return tuple(factors)


def is_squarefree(value: int) -> bool:
    try:
        squarefree_factors(value)
    except (AuditFailure, ValueError):
        return False
    return True


def mobius(value: int) -> int:
    if not is_squarefree(value):
        return 0
    return -1 if len(squarefree_factors(value)) % 2 else 1


def positive_divisors(value: int) -> tuple[int, ...]:
    return tuple(divisor for divisor in range(1, value + 1) if value % divisor == 0)


def divisor_family(
    lower_cutoff: int = LOWER_CUTOFF,
    upper_cutoff: int = UPPER_CUTOFF,
    q_values: tuple[int, ...] = Q_VALUES,
) -> tuple[int, ...]:
    return tuple(
        divisor
        for divisor in range(lower_cutoff + 1, upper_cutoff + 1)
        if is_squarefree(divisor) and all(gcd(divisor, q) == 1 for q in q_values)
    )


def psi(value: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + value * value) ** 2


def emitter_row(
    modulus: int,
    q_values: tuple[int, ...] = Q_VALUES,
    height: int = HEIGHT,
) -> tuple[Fraction, ...]:
    require(type(modulus) is int and modulus >= 1, "positive modulus")
    require(type(height) is int and height >= 1, "positive height")
    row = [Fraction(0, 1) for _ in range(modulus)]
    for q in q_values:
        require(gcd(q, modulus) == 1, "q must be a unit modulo the row modulus")
        limit = modulus * q // height
        for m in range(-limit, limit + 1):
            if m == 0:
                continue
            residue = (m * pow(q, -1, modulus)) % modulus
            row[residue] += psi(Fraction(height * m, modulus * q))
    return tuple(row)


def row_hash(row: tuple[Fraction, ...]) -> str:
    payload = "|".join(str(value) for value in row).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def fraction_hash(value: Fraction) -> str:
    return hashlib.sha256(str(value).encode("ascii")).hexdigest()


def row_norm(row: tuple[Fraction, ...]) -> Fraction:
    return sum((value * value for value in row), Fraction(0, 1))


def primitive_row_norm(row: tuple[Fraction, ...]) -> Fraction:
    modulus = len(row)
    return sum(
        (row[residue] * row[residue] for residue in range(modulus) if gcd(residue, modulus) == 1),
        Fraction(0, 1),
    )


def reduced_denominators(divisors: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted({h for divisor in divisors for h in positive_divisors(divisor)}))


def active_denominators(
    divisors: tuple[int, ...],
    q_values: tuple[int, ...] = Q_VALUES,
    height: int = HEIGHT,
) -> tuple[int, ...]:
    return tuple(
        h
        for h in reduced_denominators(divisors)
        if any(emitter_row(h, q_values, height))
    )


def coefficient_polynomial(divisor: int) -> dict[str, Fraction]:
    scale = Fraction(mobius(divisor), divisor)
    return {f"log({prime})": scale for prime in squarefree_factors(divisor)}


def add_linear_polynomials(
    left: dict[str, Fraction], right: dict[str, Fraction]
) -> dict[str, Fraction]:
    result = dict(left)
    for variable, coefficient in right.items():
        result[variable] = result.get(variable, Fraction(0, 1)) + coefficient
        if result[variable] == 0:
            del result[variable]
    return result


def tail_polynomial(divisors: tuple[int, ...], denominator: int) -> dict[str, Fraction]:
    result: dict[str, Fraction] = {}
    for divisor in divisors:
        if divisor % denominator == 0:
            result = add_linear_polynomials(result, coefficient_polynomial(divisor))
    return result


def polynomial_json(polynomial: dict[str, Fraction]) -> dict[str, str]:
    return {variable: str(polynomial[variable]) for variable in sorted(polynomial)}


def evaluate_linear(polynomial: dict[str, Fraction]) -> float:
    return sum(
        float(coefficient) * math.log(int(variable[4:-1]))
        for variable, coefficient in polynomial.items()
    )


def coefficient_value(divisor: int) -> float:
    return mobius(divisor) * math.log(divisor) / divisor


def harmonic(number: int) -> Fraction:
    require(type(number) is int and number >= 0, "nonnegative harmonic index")
    return sum((Fraction(1, value) for value in range(1, number + 1)), Fraction(0, 1))


def exponent_ledger() -> dict[str, str]:
    height_exponent = Fraction(21, 32)
    q_exponent = Fraction(1, 3)
    upper_exponent = Fraction(133, 400)
    activation_exponent = height_exponent - q_exponent
    quotient_exponent = upper_exponent + q_exponent - height_exponent
    require(activation_exponent == Fraction(31, 96), "activation exponent")
    require(quotient_exponent == Fraction(23, 2400), "quotient exponent")
    return {
        "H": str(height_exponent),
        "Q": str(q_exponent),
        "U": str(upper_exponent),
        "Y0": str(activation_exponent),
        "UQ_over_H": str(quotient_exponent),
    }


def finite_audit() -> dict[str, object]:
    divisors = divisor_family()
    denominators = reduced_denominators(divisors)
    active = active_denominators(divisors)
    q_max = max(Q_VALUES)
    activation_floor = (HEIGHT + q_max - 1) // q_max
    uniform_quotient_bound = UPPER_CUTOFF * q_max // HEIGHT

    require(all(h >= activation_floor for h in active), "activation floor")
    require(all(LOWER_CUTOFF < h <= UPPER_CUTOFF for h in active), "active row in band")
    require(all(h in divisors for h in active), "full-band diagonal anchor")
    require(emitter_row(1)[0] == 0, "zero axis")

    dilation_checks = 0
    decomposition_rows: list[str] = []
    for divisor in divisors:
        large_row = emitter_row(divisor)
        for denominator in positive_divisors(divisor):
            small_row = emitter_row(denominator)
            scale = divisor // denominator
            for residue, value in enumerate(small_row):
                require(large_row[scale * residue] == value, "dilation covariance")
                dilation_checks += 1
        lhs = row_norm(large_row)
        rhs = sum(
            (primitive_row_norm(emitter_row(h)) for h in positive_divisors(divisor)),
            Fraction(0, 1),
        )
        require(lhs == rhs, "row norm decomposition")
        decomposition_rows.append(f"{divisor}:{lhs}:{rhs}")

    tail_rows: list[dict[str, object]] = []
    actual_max_quotient = 1
    cluster_energy = 0.0
    for denominator in active:
        multiples = tuple(divisor for divisor in divisors if divisor % denominator == 0)
        quotients = tuple(divisor // denominator for divisor in multiples)
        actual_max_quotient = max(actual_max_quotient, *quotients)
        require(1 in quotients, "k=1 diagonal anchor")
        require(max(quotients) <= uniform_quotient_bound, "uniform quotient bound")
        tail_poly = tail_polynomial(divisors, denominator)
        tail_value = evaluate_linear(tail_poly)
        direct_mass = sum(coefficient_value(divisor) ** 2 for divisor in multiples)
        ratio = tail_value * tail_value / direct_mass
        harmonic_index = UPPER_CUTOFF // denominator
        majorant = (
            math.log(UPPER_CUTOFF) / math.log(denominator)
        ) ** 2 * float(harmonic(harmonic_index)) ** 2
        require(ratio <= majorant * (1 + 1e-13), "harmonic majorant")
        top_shell = 2 * denominator > UPPER_CUTOFF
        if top_shell:
            require(multiples == (denominator,), "top-shell unique multiple")
            require(tail_poly == coefficient_polynomial(denominator), "top-shell polynomial")
            require(abs(ratio - 1.0) <= 1e-14, "top-shell ratio")
        primitive_norm = primitive_row_norm(emitter_row(denominator))
        cluster_energy += primitive_norm.numerator / primitive_norm.denominator * tail_value * tail_value
        tail_rows.append(
            {
                "denominator": denominator,
                "multiples": list(multiples),
                "quotients": list(quotients),
                "tail_polynomial": polynomial_json(tail_poly),
                "tail_value": format(tail_value, ".17g"),
                "direct_coefficient_mass": format(direct_mass, ".17g"),
                "tail_to_direct_ratio": format(ratio, ".17g"),
                "harmonic_index": harmonic_index,
                "harmonic_majorant": format(majorant, ".17g"),
                "top_shell": top_shell,
                "row_hash": row_hash(emitter_row(denominator)),
                "primitive_norm_hash": fraction_hash(primitive_norm),
            }
        )

    direct_energy = sum(
        coefficient_value(divisor) ** 2
        * float(row_norm(emitter_row(divisor)))
        for divisor in divisors
    )
    global_ratio = cluster_energy / direct_energy
    top_shell = tuple(h for h in active if 2 * h > UPPER_CUTOFF)
    require(bool(top_shell), "nonempty top shell")
    require(actual_max_quotient <= uniform_quotient_bound, "actual quotient bound")

    decomposition_hash = hashlib.sha256(
        "|".join(decomposition_rows).encode("ascii")
    ).hexdigest()
    return {
        "q_values": list(Q_VALUES),
        "H": HEIGHT,
        "Y0": LOWER_CUTOFF,
        "U": UPPER_CUTOFF,
        "psi": "(1+t^2)^(-2)",
        "divisors": list(divisors),
        "reduced_denominators": list(denominators),
        "active_denominators": list(active),
        "activation_floor": activation_floor,
        "uniform_quotient_bound": uniform_quotient_bound,
        "actual_max_quotient": actual_max_quotient,
        "top_shell_denominators": list(top_shell),
        "dilation_checks": dilation_checks,
        "row_decomposition_hash": decomposition_hash,
        "tail_rows": tail_rows,
        "cluster_energy": format(cluster_energy, ".17g"),
        "direct_sum_energy": format(direct_energy, ".17g"),
        "cluster_to_direct_ratio": format(global_ratio, ".17g"),
        "numeric_classification": "NUMERICAL_OBSERVATION",
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "TPC215_SHORT_QUOTIENT_MOBIUS_MAJORANT_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_SHORT_QUOTIENT_CLUSTER_MAJORANT",
        "source_exponents": exponent_ledger(),
        "source_relations": {
            "Y0": "H/(4Q)",
            "q_shell": "Q<q<=2Q",
            "activation": "h>=H/q_max>=H/(2Q)=2Y0",
            "quotient": "k<=Uq_max/H<=2UQ/H=2x^(23/2400+o(1))",
            "majorant": "A_x=O((log x)^2)=x^(o(1))",
        },
        "claim_firewall": {
            "route_advance": "YES",
            "structural_threshold_a": "PASS",
            "activation_floor": "PROVED_EXACT",
            "active_denominator_in_full_band": "PROVED_EXACT",
            "short_quotient_normal_form": "PROVED_EXACT",
            "quotient_length_exponent": "PROVED_23_OVER_2400",
            "row_norm_divisor_decomposition": "PROVED_EXACT",
            "cluster_to_direct_majorant": "PROVED_O_LOG_X_SQUARED",
            "fixed_power_cluster_amplification": "EXCLUDED",
            "top_shell_ratio_one": "PROVED_EXACT",
            "uniform_rowwise_power_saving": "REFUTED_SCOPED",
            "finite_ratios": "NUMERICAL_OBSERVATION",
            "direct_sum_arithmetic_energy_bound": "OPEN",
            "finite_window_off_frequency_gram": "OPEN",
            "prime_shell_reassembly": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b_strict_1_over_400": "UNPAID",
        },
        "finite_fixture": finite_audit(),
    }
