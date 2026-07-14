"""Deterministic finite checks for the TPC-16 algebraic interfaces.

The script checks exact row means, cutoff drifts, Vaughan's identity,
hyperbolic divisor peeling, the 11/21 exponent ledger, and the translation
cross-spectrum convention.  It does not test any asymptotic theorem.
"""

from __future__ import annotations

import argparse
import cmath
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List


def divisors(n: int) -> List[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def mobius(n: int) -> int:
    if n == 1:
        return 1
    value = 1
    p = 2
    remaining = n
    while p * p <= remaining:
        if remaining % p == 0:
            remaining //= p
            if remaining % p == 0:
                return 0
            value = -value
            while remaining % p == 0:
                remaining //= p
        p += 1
    if remaining > 1:
        value = -value
    return value


def phi(n: int) -> int:
    result = n
    p = 2
    remaining = n
    while p * p <= remaining:
        if remaining % p == 0:
            result -= result // p
            while remaining % p == 0:
                remaining //= p
        p += 1
    if remaining > 1:
        result -= result // remaining
    return result


def ramanujan_sum(q: int, n: int) -> int:
    return sum(d * mobius(q // d) for d in divisors(math.gcd(q, abs(n))))


def lambda_model(n: int, cutoff: int) -> Fraction:
    return sum(
        (Fraction(mobius(q), phi(q)) * ramanujan_sum(q, n) for q in range(1, cutoff + 1)),
        Fraction(0),
    )


def rho_model(m: int, h: int, cutoff: int) -> Fraction:
    return sum(
        (
            Fraction(mobius(q) * ramanujan_sum(q, h), phi(q))
            for q in divisors(m)
            if q <= cutoff
        ),
        Fraction(0),
    )


def rho_prime(m: int, h: int) -> Fraction:
    return Fraction(m, phi(m)) if math.gcd(m, h) == 1 else Fraction(0)


def drift(m: int, h: int, cutoff: int) -> Fraction:
    return rho_prime(m, h) - rho_model(m, h, cutoff)


def drift_tail(m: int, h: int, cutoff: int) -> Fraction:
    return sum(
        (
            Fraction(mobius(q) * ramanujan_sum(q, h), phi(q))
            for q in divisors(m)
            if q > cutoff
        ),
        Fraction(0),
    )


def lcm_upto(n: int) -> int:
    value = 1
    for k in range(1, n + 1):
        value = math.lcm(value, k)
    return value


def von_mangoldt(n: int) -> float:
    if n < 2:
        return 0.0
    for p in range(2, n + 1):
        if all(p % d for d in range(2, int(math.sqrt(p)) + 1)):
            power = p
            while power < n:
                power *= p
            if power == n:
                return math.log(p)
    return 0.0


def beta(k: int, cutoff: int) -> int:
    return sum(mobius(d) for d in divisors(k) if d <= cutoff)


def vaughan_sides(values: Dict[int, float], u: int, v: int) -> tuple[float, float]:
    nmax = max(values, default=0)
    lhs = sum(von_mangoldt(t) * values.get(t, 0.0) for t in range(1, nmax + 1))

    rhs = sum(von_mangoldt(t) * values.get(t, 0.0) for t in range(1, min(u, nmax) + 1))
    for ell in range(1, u + 1):
        for d in range(1, v + 1):
            coeff = von_mangoldt(ell) * mobius(d)
            if coeff:
                rhs -= coeff * sum(values.get(ell * d * j, 0.0) for j in range(1, nmax // (ell * d) + 1))
    for d in range(1, v + 1):
        mu = mobius(d)
        if mu:
            rhs += mu * sum(
                math.log(j) * values.get(d * j, 0.0)
                for j in range(1, nmax // d + 1)
            )
    for ell in range(u + 1, nmax + 1):
        lam = von_mangoldt(ell)
        if not lam:
            continue
        rhs -= lam * sum(
            beta(k, v) * values.get(ell * k, 0.0)
            for k in range(2, nmax // ell + 1)
        )
    return lhs, rhs


def dft(values: Iterable[complex], length: int) -> List[complex]:
    data = list(values)
    data.extend([0j] * (length - len(data)))
    return [
        sum(data[n] * cmath.exp(-2j * math.pi * k * n / length) for n in range(length))
        for k in range(length)
    ]


def cross_spectrum_check() -> float:
    a = [0.0, 1.25, -0.5, 2.0, 0.75, -1.0, 0.0, 0.5]
    g = [0.3, -0.2, 1.1, 0.7, -0.4, 1.4, 0.2, -0.8, 0.6, 0.9, -0.1]
    h = 2
    length = 32
    direct = sum(a[n] * g[n + h] for n in range(len(a)))
    ahat = dft(a, length)
    ghat = dft(g, length)
    spectral = sum(
        ahat[k]
        * ghat[k].conjugate()
        * cmath.exp(-2j * math.pi * h * k / length)
        for k in range(length)
    ) / length
    return abs(direct - spectral)


def canonical_digest(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest().upper()


def build_certificate() -> dict:
    cutoff = 7
    h = 2
    period = lcm_upto(cutoff)
    row_checks = []
    for m in [1, 5, 7, 10, 11, 15, 22, 35]:
        average = sum((lambda_model(m * j + h, cutoff) for j in range(period)), Fraction(0)) / period
        expected = rho_model(m, h, cutoff)
        tail = drift_tail(m, h, cutoff)
        row_checks.append(
            {
                "m": m,
                "average": str(average),
                "model_mean": str(expected),
                "drift": str(drift(m, h, cutoff)),
                "tail": str(tail),
                "mean_ok": average == expected,
                "tail_ok": drift(m, h, cutoff) == tail,
            }
        )

    values = {n: math.sin(0.37 * n) + 0.1 * (n % 4) for n in range(1, 61)}
    vaughan_errors = []
    for u, v in [(3, 2), (5, 1), (4, 4), (7, 3)]:
        lhs, rhs = vaughan_sides(values, u, v)
        vaughan_errors.append({"U": u, "V": v, "error": abs(lhs - rhs)})

    peeling_checks = []
    for ell in [3, 5, 11]:
        for k in range(2, 19):
            full = beta(k, 5)
            visible = sum(mobius(d) for d in divisors(k) if d <= 5 and ell * d <= 17)
            invisible = sum(mobius(d) for d in divisors(k) if d <= 5 and ell * d > 17)
            peeling_checks.append(full == visible + invisible)

    simplified = []
    local_h = 2
    local_cutoff = 30
    for ell, d in [(31, 5), (37, 7), (41, 15), (43, 6)]:
        actual = drift(ell * d, local_h, local_cutoff)
        predicted = (
            Fraction(d, phi(d) * (ell - 1))
            if math.gcd(d, local_h) == 1
            else Fraction(0)
        )
        simplified.append(
            {"ell": ell, "d": d, "actual": str(actual), "predicted": str(predicted), "ok": actual == predicted}
        )

    sigma = Fraction(1, 200)
    delta = Fraction(1, 20)
    d_exp = Fraction(1, 21) - sigma
    l_exp = Fraction(10, 21) - sigma
    r_exp = Fraction(1, 2) - delta
    exponent_ledger = {
        "D": str(d_exp),
        "L": str(l_exp),
        "K": str(1 - l_exp),
        "DL2": str(d_exp + 2 * l_exp),
        "D12L7": str(12 * d_exp + 7 * l_exp),
        "D20L19": str(20 * d_exp + 19 * l_exp),
        "LDR": str(l_exp + d_exp + r_exp),
    }
    exponent_ok = (
        d_exp + 2 * l_exp < 1
        and 12 * d_exp + 7 * l_exp < 4
        and 20 * d_exp + 19 * l_exp < 10
        and l_exp + d_exp + r_exp < 1
        and r_exp < l_exp
    )

    payload = {
        "schema": "tpc16-square-root-gate-certificate-v1",
        "row_cutoff": cutoff,
        "row_period": period,
        "row_checks": row_checks,
        "vaughan_errors": vaughan_errors,
        "peeling_all_exact": all(peeling_checks),
        "simplified_drift_checks": simplified,
        "exponent_ledger": exponent_ledger,
        "exponent_ledger_ok": exponent_ok,
        "cross_spectrum_max_error": cross_spectrum_check(),
    }
    payload["sha256"] = canonical_digest(payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("square_root_gate_certificate.json"),
    )
    args = parser.parse_args()
    payload = build_certificate()
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
