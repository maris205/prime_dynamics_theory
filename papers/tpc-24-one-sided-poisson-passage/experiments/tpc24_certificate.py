#!/usr/bin/env python3
"""Exact structural certificate for TPC-24.

All arithmetic identities are checked with ``Fraction``.  Logarithms
are formal variables: a polynomial is a dictionary whose monomial is a
tuple of primes.  The script audits finite algebra and rational exponent
bookkeeping only; it supplies no numerical evidence for an asymptotic
Möbius estimate or for a prime-pair theorem.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


Poly = dict[tuple[int, ...], Fraction]


def factor(n: int) -> dict[int, int]:
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
    for p, e in factor(n).items():
        out = [d * p**j for d in out for j in range(e + 1)]
    return sorted(out)


def mobius(n: int) -> int:
    fs = factor(n)
    if any(e > 1 for e in fs.values()):
        return 0
    return -1 if len(fs) % 2 else 1


def phi(n: int) -> int:
    out = n
    for p in factor(n):
        out = out // p * (p - 1)
    return out


def poly_clean(poly: defaultdict[tuple[int, ...], Fraction] | Poly) -> Poly:
    return {mon: coeff for mon, coeff in poly.items() if coeff}


def poly_add(*polys: Poly) -> Poly:
    out: defaultdict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    for poly in polys:
        for mon, coeff in poly.items():
            out[mon] += coeff
    return poly_clean(out)


def poly_scale(poly: Poly, scale: Fraction | int) -> Poly:
    q = Fraction(scale)
    return poly_clean({mon: q * coeff for mon, coeff in poly.items()})


def poly_mul(left: Poly, right: Poly) -> Poly:
    out: defaultdict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    for mon1, coeff1 in left.items():
        for mon2, coeff2 in right.items():
            out[tuple(sorted(mon1 + mon2))] += coeff1 * coeff2
    return poly_clean(out)


def constant(value: Fraction | int) -> Poly:
    q = Fraction(value)
    return {} if q == 0 else {(): q}


def formal_log(n: int) -> Poly:
    return {(p,): Fraction(e) for p, e in factor(n).items()}


def a_poly(n: int) -> Poly:
    return poly_scale(formal_log(n), -mobius(n))


def lambda_prime(r_cut: int, w: int) -> Fraction:
    if w > r_cut:
        return Fraction(0)
    total = Fraction(0)
    for b in range(1, r_cut // w + 1):
        total += Fraction(mobius(w * b) * mobius(b), phi(w * b))
    return w * total


def b_poly(r_cut: int, w: int) -> Poly:
    return poly_add(a_poly(w), constant(-lambda_prime(r_cut, w)))


def a_prefix(modulus: int, bound: int) -> Poly:
    out: Poly = {}
    for w in range(1, bound + 1):
        if math.gcd(w, modulus) == 1:
            out = poly_add(out, poly_scale(a_poly(w), Fraction(1, w)))
    return out


def model_density_check(r_cut: int, h_rad: int, d: int, ell: int) -> None:
    m = ell * d
    lhs = sum(
        (lambda_prime(r_cut, w) / w for w in range(1, r_cut + 1)
         if math.gcd(w, m * h_rad) == 1),
        Fraction(0),
    )
    rhs = Fraction(h_rad, phi(h_rad)) * Fraction(d, phi(d))
    if lhs != rhs:
        raise AssertionError(("model density", r_cut, h_rad, d, ell, lhs, rhs))


def prefix_identity_check(r_cut: int, h: int, d: int, ell: int, w_bound: int, j: int) -> None:
    h_rad = math.prod(factor(abs(h)).keys())
    m = ell * d
    modulus = m * h_rad
    rho_p = Fraction(modulus, phi(modulus))
    rho_m = Fraction(h_rad, phi(h_rad)) * Fraction(d, phi(d))
    delta = rho_p - rho_m
    e_w = poly_add(a_prefix(modulus, w_bound), constant(-rho_p))

    centered: Poly = {}
    target = m * j + h
    for w in range(1, w_bound + 1):
        if math.gcd(w, modulus) != 1:
            continue
        c_mw = Fraction(int(target % w == 0), 1) - Fraction(1, w)
        centered = poly_add(centered, poly_scale(b_poly(r_cut, w), c_mw))
    lhs = poly_add(e_w, centered)

    rhs: Poly = constant(-delta)
    for w in range(1, w_bound + 1):
        if target % w == 0:
            rhs = poly_add(rhs, b_poly(r_cut, w))
    if lhs != rhs:
        raise AssertionError(("prefix indicator", r_cut, h, d, ell, w_bound, j, lhs, rhs))

    # Exact increment P_T-P_S, with both endpoints beyond R.
    t_bound = w_bound + 7
    lhs_increment = poly_add(
        a_prefix(modulus, t_bound),
        poly_scale(a_prefix(modulus, w_bound), -1),
    )
    centered_increment: Poly = {}
    for w in range(w_bound + 1, t_bound + 1):
        if math.gcd(w, modulus) != 1:
            continue
        c_mw = Fraction(int(target % w == 0), 1) - Fraction(1, w)
        centered_increment = poly_add(
            centered_increment, poly_scale(a_poly(w), c_mw)
        )
    p_difference = poly_add(lhs_increment, centered_increment)
    divisor_shell: Poly = {}
    for w in range(w_bound + 1, t_bound + 1):
        if target % w == 0:
            divisor_shell = poly_add(divisor_shell, a_poly(w))
    if p_difference != divisor_shell:
        raise AssertionError(("prefix increment", r_cut, w_bound, t_bound, target))


def zero_kernel_direct(r_cut: int, s_cut: int, t_cut: int, m: int, n: int, h_rad: int) -> Poly:
    delta = m - n
    out: Poly = {}
    for u in range(1, s_cut + 1):
        if math.gcd(u, m * h_rad) != 1:
            continue
        for v in range(s_cut + 1, t_cut + 1):
            if math.gcd(v, n * h_rad) != 1:
                continue
            g = math.gcd(u, v)
            if delta % g:
                continue
            term = poly_mul(b_poly(r_cut, u), a_poly(v))
            out = poly_add(out, poly_scale(term, Fraction(g, u * v)))
    return out


def zero_kernel_reparam(r_cut: int, s_cut: int, t_cut: int, m: int, n: int, h_rad: int) -> Poly:
    delta = m - n
    out: Poly = {}
    for g in divisors(abs(delta)):
        if mobius(g) == 0 or math.gcd(g, m * n * h_rad) != 1:
            continue
        for c in range(1, s_cut // g + 1):
            if math.gcd(g * c, m * h_rad) != 1:
                continue
            for d in range(s_cut // g + 1, t_cut // g + 1):
                if not (s_cut < g * d <= t_cut):
                    continue
                if math.gcd(d, g * c * n * h_rad) != 1:
                    continue
                term = poly_mul(b_poly(r_cut, g * c), a_poly(g * d))
                out = poly_add(out, poly_scale(term, Fraction(1, g * c * d)))
    return out


def exponent_checks() -> int:
    checks = 0
    for bi in range(6, 15):
        beta = Fraction(bi, 20)
        for si in range(1, 9):
            s = Fraction(si, 20)
            for ti in range(si, 11):
                t = Fraction(ti, 20)
                eta_star = min(
                    1 - Fraction(3, 2) * beta,
                    (beta + 1 - 2 * s - 2 * t) / 2,
                    (3 - beta - s - 5 * t) / 4,
                )
                for f1i in range(si + 1):
                    f1 = Fraction(f1i, 20)
                    for f2i in range(ti + 1):
                        f2 = Fraction(f2i, 20)
                        k1 = max(f1, beta - f1)
                        k2 = max(f2, beta - f2)
                        for y in (Fraction(0), (s + t) / 2, s + t):
                            eta_a = (beta + 1 - y - k1 - k2) / 2
                            eta_b = 1 - f1 - f2 - (k1 + k2) / 2
                            if max(eta_a, eta_b) < eta_star:
                                raise AssertionError(
                                    ("ledger", beta, s, t, f1, f2, y,
                                     eta_a, eta_b, eta_star)
                                )
                            checks += 1
    return checks


def special_ledger_checks() -> int:
    checks = 0
    samples = (
        (Fraction(3, 20), Fraction(31, 50), Fraction(1, 25)),
        (Fraction(1, 8), Fraction(3, 5), Fraction(1, 100)),
        (Fraction(1, 5), Fraction(13, 20), Fraction(1, 50)),
    )
    for delta, beta, xi in samples:
        s = Fraction(1, 2) - delta
        t = s + xi
        general = (
            1 - Fraction(3, 2) * beta,
            (beta + 1 - 2 * s - 2 * t) / 2,
            (3 - beta - s - 5 * t) / 4,
        )
        special = (
            1 - Fraction(3, 2) * beta,
            (beta + 4 * delta - 1) / 2 - xi,
            (6 * delta - beta - 5 * xi) / 4,
        )
        if general != special:
            raise AssertionError(("specialization", delta, beta, xi, general, special))
        checks += 1

    delta, beta, xi = samples[0]
    values = (
        Fraction(1, 2) - delta,
        1 - beta,
        Fraction(1, 2) - delta + xi,
        min(
            1 - Fraction(3, 2) * beta,
            (beta + 4 * delta - 1) / 2 - xi,
            (6 * delta - beta - 5 * xi) / 4,
        ),
    )
    expected = (Fraction(7, 20), Fraction(19, 50), Fraction(39, 100), Fraction(1, 50))
    if values != expected:
        raise AssertionError(("passage sample", values, expected))
    checks += 1
    return checks


def fixed_modulus_failure_check() -> None:
    r_cut = 30
    p = 29
    response: Poly = {}
    for u in range(1, r_cut + 1):
        g = math.gcd(u, p)
        bracket = g * int(p % g == 0) - 1
        response = poly_add(
            response,
            poly_scale(b_poly(r_cut, u), Fraction(bracket, u)),
        )
    expected = {(): Fraction(1), (p,): Fraction(p - 1, p)}
    if response != expected:
        raise AssertionError(("fixed modulus response", response, expected))


def main() -> None:
    checks = 0

    row_samples = (
        (12, 2, 1, 29, 3),
        (18, 6, 1, 37, 5),
        (30, 2, 3, 61, 3),
        (30, 6, 5, 61, 5),
    )
    for r_cut, h_rad, d, ell, j in row_samples:
        if math.gcd(d, h_rad) != 1 or d * h_rad > r_cut or ell <= 2 * r_cut:
            raise AssertionError(("bad row sample", r_cut, h_rad, d, ell))
        model_density_check(r_cut, h_rad, d, ell)
        checks += 1
        prefix_identity_check(r_cut, h_rad, d, ell, r_cut + 5, j)
        checks += 2

    zero_samples = (
        (8, 12, 24, 35, 55, 2),
        (10, 15, 30, 77, 119, 6),
        (12, 18, 36, 143, 187, 2),
        (14, 20, 40, 221, 299, 6),
    )
    for sample in zero_samples:
        direct = zero_kernel_direct(*sample)
        reparam = zero_kernel_reparam(*sample)
        if direct != reparam:
            raise AssertionError(("zero reparametrization", sample, direct, reparam))
        checks += 1

    # Check the coefficient split a(gd)=mu(g)a(d)-mu(g)log(g)mu(d).
    for g in range(1, 18):
        for d in range(1, 24):
            if math.gcd(g, d) != 1 or mobius(g * d) == 0:
                continue
            rhs = poly_add(
                poly_scale(a_poly(d), mobius(g)),
                poly_scale(formal_log(g), -mobius(g) * mobius(d)),
            )
            if a_poly(g * d) != rhs:
                raise AssertionError(("a(gd) split", g, d))
            checks += 1

    fixed_modulus_failure_check()
    checks += 1

    ledger_checks = exponent_checks()
    checks += ledger_checks
    checks += special_ledger_checks()

    source_path = Path(__file__).resolve()
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    payload = {
        "certificate": "TPC-24 one-sided Poisson passage",
        "exact_checks": checks,
        "ledger_checks": ledger_checks,
        "source_sha256": source_hash,
        "fixed_modulus_calibration_failure_detected": True,
        "mass_sensitive_zero_mode_retained": True,
        "polylog_projective_mass_is_explicit_hypothesis": True,
        "asymptotic_evidence": False,
        "full_residual_closure": False,
        "hardy_littlewood_asymptotic": False,
        "twin_prime_result": False,
        "general_parity_breakthrough": False,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_digest"] = hashlib.sha256(canonical).hexdigest()

    output_path = source_path.with_suffix(".json")
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
