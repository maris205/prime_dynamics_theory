#!/usr/bin/env python3
"""Exact certificate for the zero-Mellin prime-residual identities.

The program uses integers, fractions, and formal logarithm symbols only.
It does not numerically approximate the von Mangoldt logarithms and it does
not certify the analytic Titchmarsh or Bombieri--Vinogradov inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Mapping, MutableMapping, Tuple


LinearKey = Tuple[str, int]
QuadraticKey = Tuple[str, int, int]
FormalKey = LinearKey | QuadraticKey
FormalExpression = Dict[FormalKey, int]


def prime_factorization(n: int) -> Dict[int, int]:
    if n < 1:
        raise ValueError("factorization requires n >= 1")
    factors: Dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def divisors(n: int) -> List[int]:
    values = [1]
    for p, exponent in prime_factorization(n).items():
        old = list(values)
        power = 1
        for _ in range(exponent):
            power *= p
            values.extend(d * power for d in old)
    return sorted(values)


def tau(n: int) -> int:
    result = 1
    for exponent in prime_factorization(n).values():
        result *= exponent + 1
    return result


def lambda_prime(n: int) -> int | None:
    """Return p if n is a positive prime power p^k, and None otherwise."""
    if n <= 1:
        return None
    factors = prime_factorization(n)
    if len(factors) != 1:
        return None
    return next(iter(factors))


def primes_up_to(limit: int) -> List[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def add_term(expr: MutableMapping[FormalKey, int], key: FormalKey, value: int) -> None:
    if value:
        expr[key] = expr.get(key, 0) + value
        if expr[key] == 0:
            del expr[key]


def add_source_target(expr: MutableMapping[FormalKey, int], source: int, target: int) -> None:
    """Add (Lambda(source)-1)*Lambda(target) in a formal log-prime basis."""
    target_prime = lambda_prime(target)
    if target_prime is None:
        return
    source_prime = lambda_prime(source)
    if source_prime is not None:
        p, q = sorted((source_prime, target_prime))
        add_term(expr, ("LL", p, q), 1)
    add_term(expr, ("L", target_prime), -1)


def direct_expression(r0: int, r1: int, h: int, divisor_test=None) -> FormalExpression:
    expr: DefaultDict[FormalKey, int] = defaultdict(int)
    for r in range(r0, r1 + 1):
        for n in divisors(r):
            if divisor_test is None or divisor_test(n):
                add_source_target(expr, n, r + h)
    return dict(expr)


def collapsed_expression(r0: int, r1: int, h: int) -> FormalExpression:
    expr: DefaultDict[FormalKey, int] = defaultdict(int)
    for r in range(r0, r1 + 1):
        target_prime = lambda_prime(r + h)
        if target_prime is None:
            continue
        for p, exponent in prime_factorization(r).items():
            a, b = sorted((p, target_prime))
            add_term(expr, ("LL", a, b), exponent)
        add_term(expr, ("L", target_prime), -tau(r))
    return dict(expr)


def expression_rows(expr: Mapping[FormalKey, int]) -> List[dict]:
    rows = []
    for key in sorted(expr, key=lambda item: (len(item), item)):
        if key[0] == "L":
            rows.append({"basis": f"log({key[1]})", "coefficient": expr[key]})
        else:
            rows.append(
                {
                    "basis": f"log({key[1]})*log({key[2]})",
                    "coefficient": expr[key],
                }
            )
    return rows


def verify_divisor_identity(r0: int, r1: int) -> bool:
    for r in range(r0, r1 + 1):
        log_coefficients: DefaultDict[int, int] = defaultdict(int)
        constant = 0
        for n in divisors(r):
            p = lambda_prime(n)
            if p is not None:
                log_coefficients[p] += 1
            constant -= 1
        if constant != -tau(r):
            return False
        if dict(log_coefficients) != prime_factorization(r):
            return False
    return True


def verify_target_reindexing(r0: int, r1: int, h: int, d: int) -> bool:
    direct = [(m, d * m + h) for m in range(1, r1 // d + 1) if r0 <= d * m <= r1]
    progression = [
        ((t - h) // d, t)
        for t in range(r0 + h, r1 + h + 1)
        if t % d == h % d and (t - h) // d >= 1
    ]
    return direct == progression


def finite_c2(prime_limit: int) -> Fraction:
    value = Fraction(1, 2)
    for p in primes_up_to(prime_limit):
        if p > 2:
            value *= Fraction(p * (p - 1) + 1, p * (p - 1))
    return value


def euler_factor_checks(prime_limit: int, h: int) -> List[dict]:
    rows = []
    h_primes = set(prime_factorization(abs(h)).keys()) if h else set()
    for p in primes_up_to(prime_limit):
        if p in h_primes:
            factor = Fraction(p - 1, p)
            expected = Fraction(p - 1, p)
            kind = "excluded"
        else:
            # (1-1/p) * sum_{k>=0} 1/phi(p^k)
            factor = Fraction(p - 1, p) * (
                1 + Fraction(p, (p - 1) * (p - 1))
            )
            expected = 1 + Fraction(1, p * (p - 1))
            kind = "ordinary"
        rows.append(
            {
                "prime": p,
                "kind": kind,
                "factor": f"{factor.numerator}/{factor.denominator}",
                "expected": f"{expected.numerator}/{expected.denominator}",
                "equal": factor == expected,
            }
        )
    return rows


def canonical_json_bytes(payload: Mapping) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "ascii"
    )


def build_certificate(r0: int = 1000, r1: int = 2000, h: int = 2, d: int = 31) -> dict:
    if not (1 <= r0 <= r1 and 1 <= d < r1):
        raise ValueError("require 1 <= r0 <= r1 and 1 <= d < r1")
    if h == 0:
        raise ValueError("the paper and certificate require h != 0")
    full_direct = direct_expression(r0, r1, h)
    full_collapsed = collapsed_expression(r0, r1, h)
    small = direct_expression(r0, r1, h, lambda n: n <= d)
    large = direct_expression(r0, r1, h, lambda n: n > d)
    recombined: Dict[FormalKey, int] = dict(small)
    for key, value in large.items():
        add_term(recombined, key, value)

    c2 = finite_c2(43)
    euler_checks = euler_factor_checks(19, h)
    payload = {
        "schema": "tpc9-zero-mellin-exact-certificate-v2",
        "parameters": {"r0": r0, "r1": r1, "h": h, "D": d},
        "counts": {
            "product_values": r1 - r0 + 1,
            "factor_pairs": sum(tau(r) for r in range(r0, r1 + 1)),
            "small_factor_pairs": sum(
                sum(1 for n in divisors(r) if n <= d) for r in range(r0, r1 + 1)
            ),
            "large_factor_pairs": sum(
                sum(1 for n in divisors(r) if n > d) for r in range(r0, r1 + 1)
            ),
            "formal_terms": len(full_direct),
        },
        "checks": {
            "divisor_identity_every_r": verify_divisor_identity(r0, r1),
            "direct_equals_collapsed": full_direct == full_collapsed,
            "small_plus_large_equals_full": recombined == full_direct,
            "target_reindexing_all_d_le_D": all(
                verify_target_reindexing(r0, r1, h, modulus)
                for modulus in range(1, d + 1)
            ),
            "all_local_euler_factors_at_s0": all(row["equal"] for row in euler_checks),
        },
        "reference_finite_C2_product_p_le_43": {
            "numerator": c2.numerator,
            "denominator": c2.denominator,
            "decimal_display_only": format(float(c2), ".12f"),
        },
        "local_euler_checks_at_s0_p_le_19": euler_checks,
        "formal_complete_expression": expression_rows(full_direct),
    }
    payload_hash = hashlib.sha256(canonical_json_bytes(payload)).hexdigest().upper()
    return {"canonical_payload_sha256": payload_hash, **payload}


def write_certificate(path: Path, certificate: Mapping) -> None:
    text = json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r0", type=int, default=1000)
    parser.add_argument("--r1", type=int, default=2000)
    parser.add_argument("--h", type=int, default=2)
    parser.add_argument("--D", type=int, default=31)
    parser.add_argument(
        "--output", type=Path, default=Path("data/exact-zero-mellin-certificate.json")
    )
    args = parser.parse_args()
    certificate = build_certificate(args.r0, args.r1, args.h, args.D)
    write_certificate(args.output, certificate)


if __name__ == "__main__":
    main()
