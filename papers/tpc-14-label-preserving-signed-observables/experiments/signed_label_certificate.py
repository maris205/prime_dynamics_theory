"""Deterministic finite certificate for TPC-14.

The script checks only finite algebraic identities.  It is not a numerical
test of the imported asymptotic prime theorems.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


def prime_factorization(n: int) -> Dict[int, int]:
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


def is_prime(n: int) -> bool:
    return n >= 2 and prime_factorization(n) == {n: 1}


def von_mangoldt(n: int) -> float:
    if n < 2:
        return 0.0
    factors = prime_factorization(n)
    if len(factors) == 1:
        return math.log(next(iter(factors)))
    return 0.0


def mobius(n: int) -> int:
    factors = prime_factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def liouville(n: int) -> int:
    return -1 if sum(prime_factorization(n).values()) % 2 else 1


def divisors(n: int) -> List[int]:
    answer = [1]
    for p, exponent in prime_factorization(n).items():
        answer = [d * p**j for d in answer for j in range(exponent + 1)]
    return sorted(answer)


def unitary_divisors(n: int) -> List[int]:
    blocks = [p**exponent for p, exponent in prime_factorization(n).items()]
    answer = [1]
    for block in blocks:
        answer += [d * block for d in answer]
    return sorted(answer)


def radical(n: int) -> int:
    return math.prod(prime_factorization(n))


def shell_coefficient_direct(n: int) -> float:
    return sum(von_mangoldt(d) - 1.0 for d in unitary_divisors(n) if d > 1)


def shell_coefficient_closed(n: int) -> float:
    omega = len(prime_factorization(n))
    return math.log(radical(n)) - 2**omega + 1.0


def factor_coordinates(n: int, m: int) -> Tuple[int, int, int]:
    k = math.gcd(n, m)
    return n // k, m // k, k


def product_coordinate_ledger(r: int) -> List[Tuple[int, int, int]]:
    return [factor_coordinates(n, r // n) for n in divisors(r)]


def beta_v(k: int, v: int) -> int:
    return sum(mobius(d) for d in divisors(k) if d <= v)


def vaughan_pointwise_terms(n: int, u: int, v: int) -> Tuple[float, ...]:
    term_1 = von_mangoldt(n) if n <= u else 0.0
    term_2 = -sum(
        von_mangoldt(ell) * mobius(d)
        for ell in divisors(n)
        if ell <= u
        for d in divisors(n // ell)
        if d <= v
    )
    term_3 = sum(
        mobius(d) * math.log(n // d) for d in divisors(n) if d <= v
    )
    term_4 = -sum(
        von_mangoldt(ell) * beta_v(n // ell, v)
        for ell in divisors(n)
        if ell > u and n // ell > 1
    )
    return term_1, term_2, term_3, term_4


def hard_packet(n: int, u: int, v: int) -> float:
    return -sum(
        von_mangoldt(ell) * beta_v(n // ell, v)
        for ell in divisors(n)
        if ell > u and n // ell > v
    )


def divisor_signature(n: int, r: int) -> Tuple[int, ...]:
    return tuple(int(d < n and n % d == 0) for d in range(2, r + 1))


def fiber_minimax(values: Dict[int, float], signatures: Dict[int, tuple]) -> float:
    fibers: Dict[tuple, List[float]] = {}
    for index, value in values.items():
        fibers.setdefault(signatures[index], []).append(value)
    return 0.5 * max(max(fiber) - min(fiber) for fiber in fibers.values())


def shift_coordinate_radius(weights: Sequence[float], index: int, ball: float) -> float:
    norm_sq = sum(weight * weight for weight in weights)
    return ball * math.sqrt(1.0 - weights[index] ** 2 / norm_sq)


def build_certificate() -> dict:
    shell_residuals = {
        n: shell_coefficient_direct(n) - shell_coefficient_closed(n)
        for n in range(2, 257)
    }
    coordinate_failures = []
    for r in range(1, 257):
        coordinates = product_coordinate_ledger(r)
        if len(coordinates) != len(divisors(r)):
            coordinate_failures.append(r)
        for a, b, k in coordinates:
            if math.gcd(a, b) != 1 or a * b * k * k != r:
                coordinate_failures.append(r)

    u = v = 10
    vaughan_residuals = {}
    for n in range(2, 257):
        terms = vaughan_pointwise_terms(n, u, v)
        vaughan_residuals[n] = sum(terms) - von_mangoldt(n)

    p, q_1, q_2, r_cut = 101, 11, 13, 10
    semiprime = q_1 * q_2
    interval = range(101, 201)
    signatures = {n: divisor_signature(n, r_cut) for n in interval}
    prime_values = {n: float(is_prime(n)) for n in interval}
    liouville_values = {n: float(liouville(n)) for n in interval}
    lambda_values = {n: von_mangoldt(n) for n in interval}

    weights = [1.0, 2.0, 3.0, 2.0, 1.0]
    shift_index = 2
    shift_ball = 7.0

    return {
        "certificate": "TPC-14 signed label finite certificate",
        "scope": "finite algebra only; no asymptotic theorem is tested",
        "shell": {
            "range": [2, 256],
            "max_absolute_residual": max(abs(x) for x in shell_residuals.values()),
            "beta_2": 1.0 - 2.0 / (4.0 - 2.0 + 1.0),
            "h2_leading_coefficient": 6.0 / math.pi**2 - 1.0 / 3.0,
        },
        "coordinates": {
            "range": [1, 256],
            "failure_count": len(coordinate_failures),
            "endpoint_for_101": list(factor_coordinates(101, 1)),
            "radial_example": list(factor_coordinates(12, 18)),
        },
        "vaughan": {
            "U": u,
            "V": v,
            "range": [2, 256],
            "max_absolute_identity_residual": max(
                abs(x) for x in vaughan_residuals.values()
            ),
            "hard_packet_prime": hard_packet(p, u, v),
            "hard_packet_semiprime": hard_packet(semiprime, u, v),
            "expected_semiprime_value": -math.log(semiprime),
        },
        "local_null_witness": {
            "R": r_cut,
            "prime": p,
            "semiprime": semiprime,
            "factors": [q_1, q_2],
            "same_signature": signatures[p] == signatures[semiprime],
            "prime_zero_at_R_150": not any(divisor_signature(p, 150)),
            "semiprime_detected_at_R_150": any(divisor_signature(semiprime, 150)),
            "signature": list(signatures[p]),
            "same_residue_mod_7": p % 7 == semiprime % 7,
            "residue_mod_7": p % 7,
            "type_II_prime_value": 0,
            "type_II_semiprime_value": 1,
            "prime_indicator_minimax": fiber_minimax(prime_values, signatures),
            "liouville_minimax": fiber_minimax(liouville_values, signatures),
            "lambda_minimax_lower_bound": 0.5 * math.log(p),
            "lambda_minimax_computed": fiber_minimax(lambda_values, signatures),
        },
        "shift_minimax": {
            "weights": weights,
            "selected_index": shift_index,
            "ball_radius": shift_ball,
            "exact_radius": shift_coordinate_radius(weights, shift_index, shift_ball),
        },
    }


def validate(certificate: dict) -> None:
    tolerance = 1.0e-12
    assert certificate["shell"]["max_absolute_residual"] < tolerance
    assert certificate["coordinates"]["failure_count"] == 0
    assert certificate["coordinates"]["endpoint_for_101"] == [101, 1, 1]
    assert certificate["coordinates"]["radial_example"] == [2, 3, 6]
    assert certificate["vaughan"]["max_absolute_identity_residual"] < tolerance
    assert abs(certificate["vaughan"]["hard_packet_prime"]) < tolerance
    assert abs(
        certificate["vaughan"]["hard_packet_semiprime"]
        - certificate["vaughan"]["expected_semiprime_value"]
    ) < tolerance
    witness = certificate["local_null_witness"]
    assert witness["same_signature"]
    assert witness["prime_zero_at_R_150"]
    assert witness["semiprime_detected_at_R_150"]
    assert witness["same_residue_mod_7"]
    assert witness["prime_indicator_minimax"] == 0.5
    assert witness["liouville_minimax"] == 1.0
    assert witness["lambda_minimax_computed"] >= witness["lambda_minimax_lower_bound"]


def main() -> None:
    certificate = build_certificate()
    validate(certificate)
    output = Path(__file__).with_name("signed_label_certificate.json")
    output.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"TPC-14 certificate passed: {output}")


if __name__ == "__main__":
    main()
