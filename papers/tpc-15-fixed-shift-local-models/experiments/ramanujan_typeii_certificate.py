"""Deterministic finite certificate for TPC-15.

The certificate checks exact Ramanujan, progression-calibration, local
factor, selector, and Vaughan identities.  It does not test
Bombieri--Vinogradov, a large-sieve estimate, or any prime-pair asymptotic.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
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


def divisors(n: int) -> List[int]:
    values = [1]
    for p, exponent in prime_factorization(n).items():
        values = [d * p**j for d in values for j in range(exponent + 1)]
    return sorted(values)


def mobius(n: int) -> int:
    factors = prime_factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def totient(n: int) -> int:
    value = n
    for p in prime_factorization(n):
        value = value // p * (p - 1)
    return value


def von_mangoldt(n: int) -> float:
    if n < 2:
        return 0.0
    factors = prime_factorization(n)
    if len(factors) == 1:
        return math.log(next(iter(factors)))
    return 0.0


def ramanujan_sum(q: int, n: int) -> int:
    return sum(d * mobius(q // d) for d in divisors(math.gcd(q, abs(n))))


def hb_lambda(q_cut: int, n: int) -> Fraction:
    return sum(
        (
            Fraction(mobius(q) * ramanujan_sum(q, n), totient(q))
            for q in range(1, q_cut + 1)
        ),
        Fraction(0),
    )


def hb_divisor_coefficient(q_cut: int, e: int) -> Fraction:
    return e * sum(
        (
            Fraction(mobius(e * r) * mobius(r), totient(e * r))
            for r in range(1, q_cut // e + 1)
        ),
        Fraction(0),
    )


def hb_lambda_from_divisors(q_cut: int, n: int) -> Fraction:
    return sum(
        (hb_divisor_coefficient(q_cut, e) for e in divisors(n) if e <= q_cut),
        Fraction(0),
    )


def rho(h: int, m: int) -> Fraction:
    if math.gcd(abs(h), m) > 1:
        return Fraction(0)
    return Fraction(m, totient(m))


def lcm_range(q_cut: int) -> int:
    value = 1
    for q in range(1, q_cut + 1):
        value = math.lcm(value, q)
    return value


def progression_mean(q_cut: int, m: int, h: int) -> Fraction:
    period = lcm_range(q_cut)
    return sum(
        (hb_lambda(q_cut, m * j + h) for j in range(period)),
        Fraction(0),
    ) / period


def truncated_singular_series(q_cut: int, h: int) -> Fraction:
    return sum(
        (
            Fraction(
                mobius(q) ** 2 * ramanujan_sum(q, h),
                totient(q) ** 2,
            )
            for q in range(1, q_cut + 1)
        ),
        Fraction(0),
    )


def periodic_model_correlation(q_cut: int, h: int) -> Fraction:
    period = lcm_range(q_cut)
    return sum(
        (
            hb_lambda(q_cut, n) * hb_lambda(q_cut, n + h)
            for n in range(period)
        ),
        Fraction(0),
    ) / period


def beta_h(h: int) -> Fraction:
    value = Fraction(1)
    for p in prime_factorization(abs(h)):
        value *= Fraction((p - 1) ** 2, p * p - p + 1)
    return value


def phi_ratio(h: int) -> Fraction:
    h = abs(h)
    return Fraction(totient(h), h)


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


def selector_counts(states: Sequence[Sequence[int]]) -> Tuple[int, Dict[str, int]]:
    if not states:
        return 0, {}
    width = len(states[0])
    events = sum(sum(state) >= 2 for state in states)
    pairs = {
        f"{i},{j}": sum(state[i] * state[j] for state in states)
        for i in range(width)
        for j in range(i + 1, width)
    }
    return events, pairs


def build_certificate() -> dict:
    q_cut = 8
    h_values = [1, 2, 3, 6, 10]
    divisor_failures = []
    for n in range(1, 129):
        if hb_lambda(q_cut, n) != hb_lambda_from_divisors(q_cut, n):
            divisor_failures.append(n)

    calibration_failures = []
    for h in h_values:
        for m in range(1, q_cut + 1):
            if progression_mean(q_cut, m, h) != rho(h, m):
                calibration_failures.append([h, m])

    correlation_failures = []
    for h in h_values:
        if periodic_model_correlation(q_cut, h) != truncated_singular_series(
            q_cut, h
        ):
            correlation_failures.append(h)

    states = [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [0, 0, 0, 1],
    ]
    events, pair_counts = selector_counts(states)

    vaughan_residuals = []
    for u, v in ((3, 5), (7, 4), (10, 10)):
        for n in range(2, 257):
            vaughan_residuals.append(
                sum(vaughan_pointwise_terms(n, u, v)) - von_mangoldt(n)
            )

    boundary_q = 5
    boundary_m = 6
    boundary_h = 1

    return {
        "certificate": "TPC-15 Ramanujan and Type-II finite certificate",
        "scope": "finite algebra only; no analytic asymptotic is tested",
        "ramanujan_model": {
            "Q": q_cut,
            "period": lcm_range(q_cut),
            "divisor_expansion_failure_count": len(divisor_failures),
            "calibration_failure_count_for_m_at_most_Q": len(
                calibration_failures
            ),
            "periodic_correlation_failure_count": len(correlation_failures),
            "sample_lambda_Q_35": str(hb_lambda(q_cut, 35)),
            "sample_S_Q_2": str(truncated_singular_series(q_cut, 2)),
        },
        "calibration_boundary": {
            "Q": boundary_q,
            "m": boundary_m,
            "h": boundary_h,
            "periodic_mean": str(
                progression_mean(boundary_q, boundary_m, boundary_h)
            ),
            "full_local_density": str(rho(boundary_h, boundary_m)),
            "m_exceeds_Q": boundary_m > boundary_q,
            "values_differ": progression_mean(
                boundary_q, boundary_m, boundary_h
            )
            != rho(boundary_h, boundary_m),
        },
        "shell_local_factors": {
            "beta_2": str(beta_h(2)),
            "phi_over_h_2": str(phi_ratio(2)),
            "delta_2": str(phi_ratio(2) - beta_h(2)),
            "positive_deltas": {
                str(h): str(phi_ratio(h) - beta_h(h))
                for h in (2, 6, 10, 30)
            },
        },
        "vaughan": {
            "range": [2, 256],
            "parameter_sets": [[3, 5], [7, 4], [10, 10]],
            "max_absolute_identity_residual": max(
                abs(value) for value in vaughan_residuals
            ),
        },
        "finite_selector": {
            "state_count": len(states),
            "channel_count": len(states[0]),
            "two_or_more_events": events,
            "pair_counts": pair_counts,
            "sum_pair_counts": sum(pair_counts.values()),
            "largest_pair_count": max(pair_counts.values()),
        },
    }


def validate(data: dict) -> None:
    model = data["ramanujan_model"]
    assert model["divisor_expansion_failure_count"] == 0
    assert model["calibration_failure_count_for_m_at_most_Q"] == 0
    assert model["periodic_correlation_failure_count"] == 0
    assert data["calibration_boundary"]["m_exceeds_Q"]
    assert data["calibration_boundary"]["values_differ"]
    shell = data["shell_local_factors"]
    assert shell["beta_2"] == "1/3"
    assert shell["phi_over_h_2"] == "1/2"
    assert shell["delta_2"] == "1/6"
    assert all(Fraction(value) > 0 for value in shell["positive_deltas"].values())
    assert data["vaughan"]["max_absolute_identity_residual"] < 1.0e-12
    selector = data["finite_selector"]
    assert selector["sum_pair_counts"] >= selector["two_or_more_events"]
    assert selector["largest_pair_count"] >= math.ceil(
        selector["two_or_more_events"] / math.comb(selector["channel_count"], 2)
    )


def main() -> None:
    data = build_certificate()
    validate(data)
    output = Path(__file__).with_name("ramanujan_typeii_certificate.json")
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"TPC-15 certificate passed: {output}")


if __name__ == "__main__":
    main()
