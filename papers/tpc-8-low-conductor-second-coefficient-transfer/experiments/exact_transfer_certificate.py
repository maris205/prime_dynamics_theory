#!/usr/bin/env python3
"""Exact finite certificate for low-conductor second-coefficient transfer.

Every calculation in this module uses Python integers or ``Fraction``.
The certificate verifies the finite CRT operator, its arithmetic-involution
resolution, exact real conductor modes, and progression reindexing.  It does
not evaluate a Bombieri--Vinogradov error and contains no floating-point
evidence for an asymptotic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Callable, Dict, Iterable, Mapping, Sequence, Tuple


PRIMES: Tuple[int, ...] = (5, 7, 11)
Q = math.prod(PRIMES)
SHIFT = 2


def factor_integer(value: int) -> Dict[int, int]:
    """Return the exact prime factorization of a positive integer."""

    if value <= 0:
        raise ValueError("factorization is defined only for positive integers")
    result: Dict[int, int] = {}
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            result[divisor] = result.get(divisor, 0) + 1
            remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        result[remaining] = result.get(remaining, 0) + 1
    return result


def squarefree_primes(modulus: int) -> Tuple[int, ...]:
    factors = factor_integer(modulus)
    if any(exponent != 1 for exponent in factors.values()):
        raise ValueError("the transfer modulus must be squarefree")
    return tuple(sorted(factors))


def euler_phi(value: int) -> int:
    result = value
    for prime in factor_integer(value):
        result -= result // prime
    return result


def squarefree_divisors(primes: Sequence[int]) -> Tuple[int, ...]:
    values = [1]
    for prime in primes:
        values += [prime * value for value in values]
    return tuple(sorted(values))


def mobius_squarefree(value: int) -> int:
    return -1 if len(factor_integer(value)) % 2 else 1


def units(modulus: int) -> Tuple[int, ...]:
    if modulus == 1:
        return (0,)
    return tuple(value for value in range(modulus) if math.gcd(value, modulus) == 1)


def kappa(modulus: int) -> Fraction:
    value = Fraction(1)
    for prime in squarefree_primes(modulus):
        value *= Fraction(prime - 2, prime - 1)
    return value


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def canonical_hash(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest().upper()


def vector_hash(values: Iterable[object]) -> str:
    encoded = json.dumps(list(values), sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest().upper()


def arithmetic_involution(value: int, modulus: int, h: int = SHIFT) -> int:
    """Return J_{h,d}(x)=-h*x^{-1} modulo d."""

    if modulus == 1:
        return 0
    if math.gcd(value, modulus) != 1 or math.gcd(h, modulus) != 1:
        raise ValueError("the involution is defined on units with (h,d)=1")
    return (-h * pow(value, -1, modulus)) % modulus


def involution_record(modulus: int, h: int = SHIFT) -> Dict[str, object]:
    group = units(modulus)
    permutation = [arithmetic_involution(value, modulus, h) for value in group]
    if any(arithmetic_involution(image, modulus, h) != value for value, image in zip(group, permutation)):
        raise AssertionError("the arithmetic map is not an involution")
    fixed = sum(value == image for value, image in zip(group, permutation))
    if (len(group) - fixed) % 2:
        raise AssertionError("an involution must have an even nonfixed part")
    two_cycles = (len(group) - fixed) // 2
    return {
        "modulus": modulus,
        "group_size": len(group),
        "fixed_points": fixed,
        "two_cycles": two_cycles,
        "plus_eigenspace_dimension": fixed + two_cycles,
        "minus_eigenspace_dimension": two_cycles,
        "permutation_sha256": vector_hash(permutation),
    }


def deterministic_beta(modulus: int) -> Dict[int, int]:
    """A signed integer observable on the unit group."""

    values = {
        residue: ((residue * residue + 3 * residue + 1) % 13) - 6
        for residue in units(modulus)
    }
    return {residue: value for residue, value in values.items() if value}


def beta_summary(beta: Mapping[int, int]) -> Dict[str, int]:
    return {
        "support_size": len(beta),
        "sum": sum(beta.values()),
        "l1": sum(abs(value) for value in beta.values()),
        "l2_squared": sum(value * value for value in beta.values()),
    }


def transfer_residue_sum(
    beta: Mapping[int, int], m: int, modulus: int, h: int = SHIFT
) -> int:
    if math.gcd(m * h, modulus) != 1:
        raise ValueError("the row coordinate and shift must be modulus units")
    return sum(
        beta.get(residue, 0)
        for residue in units(modulus)
        if math.gcd(m * residue + h, modulus) == 1
    )


def transfer_average(
    beta: Mapping[int, int], m: int, modulus: int, h: int = SHIFT
) -> Fraction:
    return Fraction(transfer_residue_sum(beta, m, modulus, h), euler_phi(modulus))


def survivor_inclusion_exclusion(
    m: int, residue: int, modulus: int, h: int = SHIFT
) -> tuple[int, int]:
    """Return both sides of the pointwise squarefree survivor identity."""

    if math.gcd(m * residue * h, modulus) != 1:
        raise ValueError("the pointwise kernel is evaluated on unit coordinates")
    left = int(math.gcd(m * residue + h, modulus) == 1)
    right = sum(
        mobius_squarefree(divisor)
        for divisor in squarefree_divisors(squarefree_primes(modulus))
        if (m * residue + h) % divisor == 0
    )
    return left, right


def fiber_average(
    beta: Mapping[int, int], ambient: int, divisor: int, residue: int
) -> Fraction:
    """Conditional average from G_ambient to one residue in G_divisor."""

    selected = [
        beta.get(value, 0)
        for value in units(ambient)
        if value % divisor == residue % divisor
    ]
    expected = euler_phi(ambient) // euler_phi(divisor)
    if len(selected) != expected:
        raise AssertionError("the CRT fiber has the wrong cardinality")
    return Fraction(sum(selected), len(selected))


def involution_bundle_average(
    beta: Mapping[int, int], m: int, modulus: int, h: int = SHIFT
) -> Fraction:
    """Resolve the survivor transfer into CRT fiber/involution layers."""

    result = Fraction(0)
    for divisor in squarefree_divisors(squarefree_primes(modulus)):
        image = arithmetic_involution(m % divisor, divisor, h)
        result += Fraction(mobius_squarefree(divisor), euler_phi(divisor)) * fiber_average(
            beta, modulus, divisor, image
        )
    return result


def legendre_symbol(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        return 0
    residue = pow(value, (prime - 1) // 2, prime)
    if residue == 1:
        return 1
    if residue == prime - 1:
        return -1
    raise AssertionError("Euler's criterion returned an invalid value")


def quadratic_mode_value(value: int, conductor: int) -> int:
    result = 1
    for prime in squarefree_primes(conductor):
        result *= legendre_symbol(value, prime)
    return result


def quadratic_mode(modulus: int, conductor: int) -> Dict[int, int]:
    if modulus % conductor:
        raise ValueError("the exact conductor must divide the ambient modulus")
    return {
        residue: quadratic_mode_value(residue, conductor)
        for residue in units(modulus)
    }


def predicted_quadratic_residue_sum(
    m: int, modulus: int, conductor: int, h: int = SHIFT
) -> int:
    active = squarefree_primes(conductor)
    inactive = [prime for prime in squarefree_primes(modulus) if conductor % prime]
    return (
        (-1) ** len(active)
        * quadratic_mode_value(-h, conductor)
        * quadratic_mode_value(m, conductor)
        * math.prod(prime - 2 for prime in inactive)
    )


def mode_record(modulus: int, conductor: int, h: int = SHIFT) -> Dict[str, object]:
    beta = quadratic_mode(modulus, conductor)
    group = units(modulus)
    observed = [transfer_residue_sum(beta, m, modulus, h) for m in group]
    predicted = [
        predicted_quadratic_residue_sum(m, modulus, conductor, h) for m in group
    ]
    if observed != predicted:
        raise AssertionError(f"the quadratic mode formula failed at conductor {conductor}")
    active_product = math.prod(
        prime - 2 for prime in squarefree_primes(conductor)
    )
    counts = {str(value): observed.count(value) for value in sorted(set(observed))}
    return {
        "exact_conductor": conductor,
        "support_primes": list(squarefree_primes(conductor)),
        "unnormalized_residue_sum_counts": counts,
        "normalized_multiplier_absolute_value": fraction_text(
            Fraction(1, active_product)
        ),
        "formula_holds_on_all_rows": True,
        "residue_sum_vector_sha256": vector_hash(observed),
    }


def first_progression_value(lower_exclusive: int, residue: int, modulus: int) -> int:
    first_allowed = lower_exclusive + 1
    return first_allowed + (residue - first_allowed) % modulus


def direct_weighted_row(
    m: int,
    n_scale: int,
    modulus: int,
    h: int,
    beta: Mapping[int, int],
    target_weight: Callable[[int], int],
) -> int:
    return sum(
        beta.get(n % modulus, 0) * target_weight(m * n + h)
        for n in range(n_scale + 1, 2 * n_scale + 1)
    )


def progression_weighted_row(
    m: int,
    n_scale: int,
    modulus: int,
    h: int,
    beta: Mapping[int, int],
    target_weight: Callable[[int], int],
) -> int:
    total = 0
    lower = m * n_scale + h
    upper = 2 * m * n_scale + h
    progression_modulus = m * modulus
    for residue, coefficient in beta.items():
        target_residue = (m * residue + h) % progression_modulus
        first = first_progression_value(lower, target_residue, progression_modulus)
        total += coefficient * sum(
            target_weight(target)
            for target in range(first, upper + 1, progression_modulus)
        )
    return total


def prime_power_base(value: int) -> int | None:
    factors = factor_integer(value)
    if len(factors) != 1:
        return None
    return next(iter(factors))


def add_formal_lambda(record: Dict[int, int], target: int, coefficient: int) -> None:
    prime = prime_power_base(target)
    if prime is not None and coefficient:
        record[prime] = record.get(prime, 0) + coefficient
        if record[prime] == 0:
            del record[prime]


def direct_symbolic_lambda_row(
    m: int, n_scale: int, modulus: int, h: int, beta: Mapping[int, int]
) -> Dict[int, int]:
    result: Dict[int, int] = {}
    for n in range(n_scale + 1, 2 * n_scale + 1):
        add_formal_lambda(result, m * n + h, beta.get(n % modulus, 0))
    return result


def progression_symbolic_lambda_row(
    m: int, n_scale: int, modulus: int, h: int, beta: Mapping[int, int]
) -> Dict[int, int]:
    result: Dict[int, int] = {}
    lower = m * n_scale + h
    upper = 2 * m * n_scale + h
    progression_modulus = m * modulus
    for residue, coefficient in beta.items():
        target_residue = (m * residue + h) % progression_modulus
        first = first_progression_value(lower, target_residue, progression_modulus)
        for target in range(first, upper + 1, progression_modulus):
            add_formal_lambda(result, target, coefficient)
    return result


def exact_progression_record() -> Dict[str, object]:
    modulus = 35
    h = SHIFT
    m_scale = 17
    n_scale = 257
    beta = {
        residue: ((3 * residue * residue + 2 * residue + 1) % 9) - 4
        for residue in units(modulus)
    }
    m_values = [
        m
        for m in range(m_scale + 1, 2 * m_scale + 1)
        if math.gcd(m, modulus * h) == 1
    ]
    target_weight = lambda target: ((target * target + 3 * target + 7) % 17) - 8
    direct_rows = [
        direct_weighted_row(m, n_scale, modulus, h, beta, target_weight)
        for m in m_values
    ]
    progression_rows = [
        progression_weighted_row(m, n_scale, modulus, h, beta, target_weight)
        for m in m_values
    ]
    if direct_rows != progression_rows:
        raise AssertionError("integer target-weight progression reindexing failed")

    direct_lambda = [
        direct_symbolic_lambda_row(m, n_scale, modulus, h, beta)
        for m in m_values
    ]
    progression_lambda = [
        progression_symbolic_lambda_row(m, n_scale, modulus, h, beta)
        for m in m_values
    ]
    if direct_lambda != progression_lambda:
        raise AssertionError("formal von Mangoldt progression reindexing failed")
    lambda_vectors = [
        [[prime, coefficient] for prime, coefficient in sorted(row.items())]
        for row in direct_lambda
    ]
    return {
        "modulus": modulus,
        "shift": h,
        "m_interval": {"start_exclusive": m_scale, "end_inclusive": 2 * m_scale},
        "n_interval": {"start_exclusive": n_scale, "end_inclusive": 2 * n_scale},
        "eligible_rows": len(m_values),
        "integer_weight_rows_sha256": vector_hash(direct_rows),
        "integer_reindexing_exact": True,
        "formal_lambda_basis": "independent symbols log(p)",
        "formal_lambda_nonzero_coefficients": sum(len(row) for row in direct_lambda),
        "formal_lambda_rows_sha256": vector_hash(lambda_vectors),
        "formal_lambda_reindexing_exact": True,
    }


def build_payload() -> Dict[str, object]:
    modulus = Q
    h = SHIFT
    group = units(modulus)
    divisors = squarefree_divisors(PRIMES)
    beta = deterministic_beta(modulus)

    direct = [transfer_average(beta, m, modulus, h) for m in group]
    bundled = [involution_bundle_average(beta, m, modulus, h) for m in group]
    if direct != bundled:
        raise AssertionError("the CRT involution bundle does not reconstruct transfer")

    survivor_counts = [
        sum(math.gcd(m * residue + h, modulus) == 1 for residue in group)
        for m in group
    ]
    expected_survivors = math.prod(prime - 2 for prime in PRIMES)
    if set(survivor_counts) != {expected_survivors}:
        raise AssertionError("the local survivor row count is not constant")

    pointwise_values = []
    for m in group:
        for residue in group:
            left, right = survivor_inclusion_exclusion(m, residue, modulus, h)
            if left != right:
                raise AssertionError("pointwise survivor inclusion-exclusion failed")
            pointwise_values.append(left)

    main_scale = 997
    residue_main = []
    operator_main = []
    main_rows = [m for m in group if math.gcd(m, h) == 1]
    for m in main_rows:
        residue_sum = transfer_residue_sum(beta, m, modulus, h)
        residue_main.append(Fraction(m * main_scale * residue_sum, euler_phi(m * modulus)))
        operator_main.append(
            Fraction(m * main_scale, euler_phi(m))
            * transfer_average(beta, m, modulus, h)
        )
    if residue_main != operator_main:
        raise AssertionError("the BV row-main normalization is inconsistent")

    return {
        "schema": "tpc8-exact-low-conductor-transfer-v1",
        "modulus": modulus,
        "primes": list(PRIMES),
        "shift": h,
        "group_size": len(group),
        "normalization": {
            "kappa": fraction_text(kappa(modulus)),
            "survivors_per_row": expected_survivors,
            "transfer_average_denominator": euler_phi(modulus),
            "normalized_operator_sends_one_to_one": True,
        },
        "pointwise_inclusion_exclusion": {
            "checked_unit_pairs": len(pointwise_values),
            "all_pairs_equal": True,
            "survivor_indicator_sha256": vector_hash(pointwise_values),
        },
        "arithmetic_involutions": {
            str(divisor): involution_record(divisor, h) for divisor in divisors
        },
        "signed_observable": beta_summary(beta),
        "involution_bundle": {
            "formula": "K=sum_(d|q) mu(d)/phi(d) U_(h,d) E_(q,d)",
            "all_rows_equal": True,
            "direct_vector_sha256": vector_hash(
                [fraction_text(value) for value in direct]
            ),
            "bundle_vector_sha256": vector_hash(
                [fraction_text(value) for value in bundled]
            ),
        },
        "quadratic_exact_conductor_modes": {
            str(conductor): mode_record(modulus, conductor, h)
            for conductor in divisors
        },
        "bv_main_normalization": {
            "test_scale_N": main_scale,
            "eligible_rows_with_gcd_m_h_equal_one": len(main_rows),
            "identity": "m*N*S_beta(m)/phi(mq)=(m*N/phi(m))*K_beta(m)",
            "all_rows_equal": True,
            "row_main_vector_sha256": vector_hash(
                [fraction_text(value) for value in residue_main]
            ),
        },
        "exact_progression_reindexing": exact_progression_record(),
        "interpretation_boundary": (
            "All entries above are finite integer or rational identities. "
            "They do not estimate a Bombieri--Vinogradov error, verify an "
            "asymptotic range, or approximate Lambda-1 by periodic data."
        ),
    }


def build_certificate() -> Dict[str, object]:
    payload = build_payload()
    return {**payload, "canonical_payload_sha256": canonical_hash(payload)}


def validate_certificate(certificate: Mapping[str, object]) -> None:
    if certificate.get("schema") != "tpc8-exact-low-conductor-transfer-v1":
        raise AssertionError("the certificate schema is incorrect")
    payload = dict(certificate)
    recorded_hash = payload.pop("canonical_payload_sha256", None)
    if recorded_hash != canonical_hash(payload):
        raise AssertionError("the canonical payload hash is incorrect")
    rebuilt = build_certificate()
    if dict(certificate) != rebuilt:
        raise AssertionError("the certificate does not match exact recomputation")


def render_certificate(certificate: Mapping[str, object]) -> bytes:
    return (json.dumps(certificate, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_certificate(path: Path) -> None:
    certificate = build_certificate()
    validate_certificate(certificate)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(render_certificate(certificate))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = build_certificate()
    validate_certificate(certificate)
    rendered = render_certificate(certificate)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(rendered)
    else:
        print(rendered.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
