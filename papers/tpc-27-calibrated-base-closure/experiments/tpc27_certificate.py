#!/usr/bin/env python3
"""Exact finite certificate for TPC-27.

Only the Python standard library is used.  Rational terms are represented
by ``Fraction`` and logarithms by formal prime-log variables.  The script
checks the new Ramanujan-square factorization, the exact model-multiple
density, the centered-to-calibrated bridge, and the rational exponent
sample.  It is regression control for finite algebra, not numerical
evidence for an asymptotic Mobius estimate or for twin primes.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


Monomial = tuple[int, ...]
Poly = dict[Monomial, Fraction]


def require(condition: bool, label: str, *details: object) -> None:
    """Raise in ordinary and optimized Python when a check fails."""
    if not condition:
        raise RuntimeError((label,) + details)


def factor(n: int) -> dict[int, int]:
    require(n >= 1, "factor-positive", n)
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def divisors(n: int) -> list[int]:
    out = [1]
    for p, exponent in factor(n).items():
        old = tuple(out)
        power = 1
        for _ in range(exponent):
            power *= p
            out.extend(value * power for value in old)
    return sorted(out)


def mobius(n: int) -> int:
    data = factor(n)
    if any(exponent > 1 for exponent in data.values()):
        return 0
    return -1 if len(data) % 2 else 1


def phi(n: int) -> int:
    out = n
    for p in factor(n):
        out = out // p * (p - 1)
    return out


def radical(n: int) -> int:
    out = 1
    for p in factor(abs(n)):
        out *= p
    return out


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True


def next_prime(n: int) -> int:
    candidate = max(2, n + 1)
    while not is_prime(candidate):
        candidate += 1
    return candidate


def clean(poly: defaultdict[Monomial, Fraction] | Poly) -> Poly:
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def add(*polys: Poly) -> Poly:
    out: defaultdict[Monomial, Fraction] = defaultdict(Fraction)
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] += coefficient
    return clean(out)


def scale(poly: Poly, scalar: int | Fraction) -> Poly:
    value = Fraction(scalar)
    return clean({monomial: value * coefficient
                  for monomial, coefficient in poly.items()})


def multiply(left: Poly, right: Poly) -> Poly:
    out: defaultdict[Monomial, Fraction] = defaultdict(Fraction)
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(sorted(monomial_left + monomial_right))
            out[monomial] += coefficient_left * coefficient_right
    return clean(out)


def constant(value: int | Fraction) -> Poly:
    coefficient = Fraction(value)
    return {} if not coefficient else {(): coefficient}


def formal_log(n: int) -> Poly:
    return {(p,): Fraction(exponent)
            for p, exponent in factor(n).items()}


def a_poly(n: int) -> Poly:
    return scale(formal_log(n), -mobius(n))


def lambda_prime(r_cut: int, u: int) -> Fraction:
    if u > r_cut:
        return Fraction(0)
    total = Fraction(0)
    for b in range(1, r_cut // u + 1):
        total += Fraction(mobius(u * b) * mobius(b), phi(u * b))
    return u * total


def b_poly(r_cut: int, u: int) -> Poly:
    return add(a_poly(u), constant(-lambda_prime(r_cut, u)))


def ramanujan(k: int, delta: int) -> int:
    return sum(e * mobius(k // e)
               for e in divisors(math.gcd(k, abs(delta))))


def serialize_poly(poly: Poly) -> dict[str, str]:
    return {
        "1" if not monomial else "*".join(
            f"log({p})" for p in monomial): str(coefficient)
        for monomial, coefficient in sorted(poly.items())
    }


def rho_model(h_rad: int, d_row: int) -> Fraction:
    return Fraction(h_rad, phi(h_rad)) * Fraction(d_row, phi(d_row))


def rho_prime(h_rad: int, ell: int, d_row: int) -> Fraction:
    return Fraction(ell * d_row * h_rad, phi(ell * d_row * h_rad))


def delta_h(h_rad: int, ell: int, d_row: int) -> Fraction:
    return rho_prime(h_rad, ell, d_row) - rho_model(h_rad, d_row)


def check_ramanujan_resolution() -> tuple[int, list[dict[str, int]]]:
    checks = 0
    samples: list[dict[str, int]] = []
    for g in range(1, 61):
        for delta in range(-100, 101):
            left = g * int(delta % g == 0) - 1
            right = sum(ramanujan(k, delta)
                        for k in divisors(g) if k > 1)
            require(left == right, "ramanujan-resolution", g, delta,
                    left, right)
            checks += 1
        if g in (1, 6, 30, 60):
            samples.append({
                "g": g,
                "delta": 30,
                "value": g * int(30 % g == 0) - 1,
            })
    return checks, samples


def direct_model_multiple(r_cut: int, k: int, m: int,
                          h_rad: int) -> Fraction:
    return sum((lambda_prime(r_cut, u) / u
                for u in range(1, r_cut + 1)
                if u % k == 0 and math.gcd(u, m * h_rad) == 1),
               Fraction())


def predicted_model_multiple(r_cut: int, k: int,
                             d_row: int, h_rad: int) -> Fraction:
    m0 = d_row * h_rad
    return Fraction(mobius(k), phi(k)) * sum(
        (Fraction(1, phi(a)) for a in divisors(m0) if a * k <= r_cut),
        Fraction(),
    )


def check_model_multiple_identity() -> tuple[int, int, list[dict[str, object]]]:
    checks = 0
    complete_checks = 0
    samples: list[dict[str, object]] = []
    for r_cut in range(3, 43):
        ell = next_prime(2 * r_cut)
        for h_rad in (1, 2, 6):
            for d_row in range(1, min(12, r_cut) + 1):
                if mobius(d_row) == 0 or math.gcd(d_row, h_rad) != 1:
                    continue
                m = ell * d_row
                for k in range(1, r_cut + 1):
                    if mobius(k) == 0 or math.gcd(k, m * h_rad) != 1:
                        continue
                    direct = direct_model_multiple(r_cut, k, m, h_rad)
                    predicted = predicted_model_multiple(
                        r_cut, k, d_row, h_rad)
                    require(direct == predicted, "model-multiple-truncated",
                            r_cut, ell, d_row, h_rad, k,
                            direct, predicted)
                    checks += 1
                    if k * d_row * h_rad <= r_cut:
                        complete = (Fraction(mobius(k), phi(k))
                                    * rho_model(h_rad, d_row))
                        require(direct == complete, "model-multiple-complete",
                                r_cut, ell, d_row, h_rad, k,
                                direct, complete)
                        checks += 1
                        complete_checks += 1
    for case in ((30, 2, 1, 3), (36, 6, 5, 1), (42, 2, 5, 3)):
        r_cut, h_rad, d_row, k = case
        ell = next_prime(2 * r_cut)
        m = ell * d_row
        direct = direct_model_multiple(r_cut, k, m, h_rad)
        samples.append({
            "R": r_cut,
            "H": h_rad,
            "ell": ell,
            "d_row": d_row,
            "k": k,
            "direct": str(direct),
            "predicted": str(predicted_model_multiple(
                r_cut, k, d_row, h_rad)),
        })
    return checks, complete_checks, samples


def check_a_multiple_identity() -> tuple[int, list[dict[str, object]]]:
    checks = 0
    samples: list[dict[str, object]] = []
    for k in range(1, 31):
        if mobius(k) == 0:
            continue
        for w in range(1, 41):
            if math.gcd(k, w) != 1:
                continue
            left = a_poly(k * w)
            right = add(
                scale(a_poly(w), mobius(k)),
                scale(formal_log(k), -mobius(k) * mobius(w)),
            )
            require(left == right, "a-multiple-formal", k, w,
                    serialize_poly(left), serialize_poly(right))
            checks += 1
    for k, w in ((2, 15), (5, 14), (30, 7)):
        samples.append({
            "k": k,
            "w": w,
            "a_kw": serialize_poly(a_poly(k * w)),
        })
    return checks, samples


def direct_zero_kernel(r_cut: int, s_cut: int, m: int,
                       n: int, h_rad: int) -> Poly:
    out: Poly = {}
    delta = m - n
    for u in range(1, s_cut + 1):
        if math.gcd(u, m * h_rad) != 1:
            continue
        for v in range(1, s_cut + 1):
            if math.gcd(v, n * h_rad) != 1:
                continue
            g = math.gcd(u, v)
            multiplier = g * int(delta % g == 0) - 1
            if multiplier:
                out = add(out, scale(
                    multiply(b_poly(r_cut, u), b_poly(r_cut, v)),
                    Fraction(multiplier, u * v),
                ))
    return out


def multiple_density_poly(r_cut: int, s_cut: int, k: int,
                          m: int, h_rad: int) -> Poly:
    out: Poly = {}
    for u in range(1, s_cut + 1):
        if u % k == 0 and math.gcd(u, m * h_rad) == 1:
            out = add(out, scale(b_poly(r_cut, u), Fraction(1, u)))
    return out


def factored_zero_kernel(r_cut: int, s_cut: int, m: int,
                         n: int, h_rad: int) -> Poly:
    out: Poly = {}
    for k in range(2, s_cut + 1):
        left = multiple_density_poly(r_cut, s_cut, k, m, h_rad)
        right = multiple_density_poly(r_cut, s_cut, k, n, h_rad)
        out = add(out, scale(multiply(left, right),
                             ramanujan(k, m - n)))
    return out


def check_zero_factorization() -> tuple[int, list[dict[str, object]], Poly]:
    cases = (
        (5, 8, 1, (11, 13, 17, 19)),
        (7, 11, 2, (13, 15, 17, 21)),
        (9, 14, 6, (17, 25, 29, 35)),
    )
    checks = 0
    samples: list[dict[str, object]] = []
    sample_poly: Poly = {}
    for r_cut, s_cut, h_rad, rows in cases:
        for m in rows:
            for n in rows:
                if math.gcd(m, h_rad) != 1 or math.gcd(n, h_rad) != 1:
                    continue
                direct = direct_zero_kernel(r_cut, s_cut, m, n, h_rad)
                factored = factored_zero_kernel(
                    r_cut, s_cut, m, n, h_rad)
                require(direct == factored, "zero-factorization",
                        r_cut, s_cut, h_rad, m, n,
                        serialize_poly(direct), serialize_poly(factored))
                checks += 1
                if m != n and len(samples) < 5:
                    samples.append({
                        "R": r_cut,
                        "S": s_cut,
                        "H": h_rad,
                        "m": m,
                        "n": n,
                        "polynomial": serialize_poly(direct),
                    })
                    sample_poly = direct
    return checks, samples, sample_poly


def centered_signal(r_cut: int, s_cut: int, m: int,
                    h: int, j: int) -> Poly:
    h_rad = radical(h)
    target = m * j + h
    out: Poly = {}
    for u in range(1, s_cut + 1):
        if math.gcd(u, m * h_rad) != 1:
            continue
        coefficient = Fraction(int(target % u == 0), 1) - Fraction(1, u)
        out = add(out, scale(b_poly(r_cut, u), coefficient))
    return out


def calibrated_prefix(r_cut: int, s_cut: int, ell: int,
                      d_row: int, h: int, j: int) -> Poly:
    h_rad = radical(h)
    m = ell * d_row
    target = m * j + h
    out: Poly = constant(-delta_h(h_rad, ell, d_row))
    for u in range(1, s_cut + 1):
        if target % u == 0:
            out = add(out, b_poly(r_cut, u))
    return out


def calibration_error(s_cut: int, m: int, h_rad: int) -> Poly:
    out: Poly = constant(-Fraction(m * h_rad, phi(m * h_rad)))
    for u in range(1, s_cut + 1):
        if math.gcd(u, m * h_rad) == 1:
            out = add(out, scale(a_poly(u), Fraction(1, u)))
    return out


def check_prefix_bridge() -> tuple[int, list[dict[str, object]]]:
    cases = (
        (6, 10, 13, 1, 1, range(0, 13)),
        (10, 15, 23, 3, 2, range(1, 18, 2)),
        # Keep d*rad(h) <= R, the finite-model completeness condition
        # that is automatic in the asymptotic opened-row range.
        (30, 36, 61, 5, 6, (1, 5, 7, 11, 13, 17)),
    )
    checks = 0
    samples: list[dict[str, object]] = []
    for r_cut, s_cut, ell, d_row, h, j_values in cases:
        require(ell > r_cut and is_prime(ell), "bridge-row-prime", ell)
        h_rad = radical(h)
        require(math.gcd(d_row, h_rad) == 1, "bridge-row-coprime")
        m = ell * d_row
        error = calibration_error(s_cut, m, h_rad)
        for j in j_values:
            left = calibrated_prefix(r_cut, s_cut, ell, d_row, h, j)
            right = add(centered_signal(r_cut, s_cut, m, h, j), error)
            require(left == right, "prefix-Z-plus-E", r_cut, s_cut,
                    ell, d_row, h, j,
                    serialize_poly(left), serialize_poly(right))
            checks += 1
        samples.append({
            "R": r_cut,
            "S": s_cut,
            "ell": ell,
            "d_row": d_row,
            "h": h,
            "E_polynomial": serialize_poly(error),
        })
    return checks, samples


def check_scalar_four_channel_algebra() -> int:
    values = tuple(Fraction(n, d)
                   for d in range(1, 9) for n in range(-5, 6))
    checks = 0
    for index in range(0, len(values) - 3, 4):
        z1, z2, e1, e2 = values[index:index + 4]
        left = (z1 + e1) * (z2 + e2)
        right = z1 * z2 + e1 * z2 + z1 * e2 + e1 * e2
        require(left == right, "ZZ-EZ-ZE-EE", z1, z2, e1, e2)
        checks += 1
    return checks


def sharp_eta(beta: Fraction, t: Fraction) -> Fraction:
    if t <= (1 - beta) / 2:
        return 1 - beta - t
    if t <= beta / 2:
        return (3 - 3 * beta - 2 * t) / 4
    if t <= (3 * beta - 1) / 2:
        return (3 - beta - 6 * t) / 4
    return (beta + 1 - 4 * t) / 2


def check_parameter_samples() -> tuple[int, dict[str, object], dict[str, object]]:
    delta = Fraction(3, 20)
    beta = Fraction(31, 50)
    s = Fraction(1, 2) - delta
    j_exp = 1 - beta
    t = Fraction(39, 100)
    base_faces = (
        1 - Fraction(3, 2) * beta,
        (beta + 1 - 4 * s) / 2,
        (3 - beta - 6 * s) / 4,
    )
    require((s, j_exp, t) ==
            (Fraction(7, 20), Fraction(19, 50), Fraction(39, 100)),
            "strict-scales", s, j_exp, t)
    require(s < j_exp < t, "strict-crossing", s, j_exp, t)
    require(j_exp - s == Fraction(3, 100),
            "strict-poisson-margin", j_exp - s)
    require(base_faces == (Fraction(7, 100), Fraction(11, 100),
                           Fraction(7, 100)),
            "strict-base-faces", base_faces)
    require(sharp_eta(beta, t) == Fraction(1, 100),
            "strict-annular-saving", sharp_eta(beta, t))

    beta_high = Fraction(267, 400)
    s_high = Fraction(23, 60)
    j_high = 1 - beta_high
    t_high = Fraction(193, 500)
    require(s_high - j_high == Fraction(61, 1200),
            "high-base-beyond-J", s_high, j_high)
    require(s_high > j_high, "high-poisson-short-fails")
    require(sharp_eta(beta_high, t_high) == Fraction(33, 8000),
            "high-annular-saving", sharp_eta(beta_high, t_high))
    checks = 8
    return checks, {
        "delta": str(delta),
        "beta": str(beta),
        "S_exponent": str(s),
        "J_exponent": str(j_exp),
        "T_exponent": str(t),
        "base_faces": [str(value) for value in base_faces],
        "base_saving": "7/100",
        "poisson_short_margin": "3/100",
        "annular_saving": "1/100",
        "selected_base_closed": True,
    }, {
        "beta": str(beta_high),
        "S_exponent": str(s_high),
        "J_exponent": str(j_high),
        "T_exponent": str(t_high),
        "S_beyond_J_margin": "61/1200",
        "annular_saving": "33/8000",
        "selected_base_closed": False,
        "cutoff_stability_only": True,
    }


def main() -> None:
    checks = 0
    subcounts: dict[str, int] = {}

    count, ramanujan_samples = check_ramanujan_resolution()
    checks += count
    subcounts["ramanujan_compatibility_resolution"] = count

    count, complete_count, model_samples = check_model_multiple_identity()
    checks += count
    subcounts["exact_model_multiple_density"] = count

    count, a_samples = check_a_multiple_identity()
    checks += count
    subcounts["formal_prime_multiple_identity"] = count

    count, zero_samples, sample_zero = check_zero_factorization()
    checks += count
    subcounts["ramanujan_square_zero_factorization"] = count

    count, bridge_samples = check_prefix_bridge()
    checks += count
    subcounts["centered_to_calibrated_bridge"] = count

    count = check_scalar_four_channel_algebra()
    checks += count
    subcounts["ZZ_EZ_ZE_EE_algebra"] = count

    count, strict_sample, high_sample = check_parameter_samples()
    checks += count
    subcounts["rational_parameter_samples"] = count

    source_path = Path(__file__)
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    payload = {
        "paper": "TPC-27",
        "certificate": "calibrated base closure and Ramanujan-square zero mode",
        "exact_check_count": checks,
        "subcheck_counts": subcounts,
        "complete_model_multiple_checks": complete_count,
        "ramanujan_samples": ramanujan_samples,
        "model_multiple_samples": model_samples,
        "formal_prime_multiple_samples": a_samples,
        "zero_factorization_samples": zero_samples,
        "prefix_bridge_samples": bridge_samples,
        "sample_zero_polynomial": serialize_poly(sample_zero),
        "strict_crossing_sample": strict_sample,
        "high_beta_boundary_sample": high_sample,
        "source_sha256": source_hash,
        "claims": {
            "finite_ramanujan_resolution": True,
            "finite_ramanujan_square_factorization": True,
            "exact_model_multiple_density": True,
            "exact_centered_to_calibrated_bridge": True,
            "strict_sample_ledger": True,
            "asymptotic_mobius_evidence": False,
            "full_residual_closure": False,
            "high_beta_base_closed": False,
            "ultra_long_complement_closed": False,
            "hardy_littlewood": False,
            "positivity": False,
            "twin_primes": False,
            "general_parity_breakthrough": False,
            "riemann_hypothesis": False,
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_digest"] = hashlib.sha256(
        canonical.encode("utf-8")).hexdigest()
    output_path = source_path.with_suffix(".json")
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
