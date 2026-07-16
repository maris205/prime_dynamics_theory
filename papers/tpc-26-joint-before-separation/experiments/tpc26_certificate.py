#!/usr/bin/env python3
"""Exact finite certificate for TPC-26.

Only the Python standard library is used.  Arithmetic scale parameters are
``Fraction`` objects, and logarithms are formal prime-log variables.  The
certificate checks finite algebra, CRT counts, and a rational conductor
ledger.  It is not numerical evidence for an asymptotic Mobius estimate,
Hardy--Littlewood, or twin primes.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Iterable


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


def mobius(n: int) -> int:
    factors = factor(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


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
    return {} if coefficient == 0 else {(): coefficient}


def formal_log(n: int) -> Poly:
    return {(p,): Fraction(exponent)
            for p, exponent in factor(n).items()}


def a_poly(n: int) -> Poly:
    return scale(formal_log(n), -mobius(n))


def lambda_prime(r_cut: int, w: int) -> Fraction:
    if w > r_cut:
        return Fraction(0)
    total = Fraction(0)
    for b in range(1, r_cut // w + 1):
        total += Fraction(mobius(w * b) * mobius(b), phi(w * b))
    return w * total


def b_poly(r_cut: int, w: int) -> Poly:
    return add(a_poly(w), constant(-lambda_prime(r_cut, w)))


def serialize_poly(poly: Poly) -> dict[str, str]:
    return {
        "1" if not monomial else "*".join(
            f"log({p})" for p in monomial): str(coefficient)
        for monomial, coefficient in sorted(poly.items())
    }


def delta_h(h_rad: int, ell: int, d: int) -> Fraction:
    require(is_prime(ell), "delta-source-prime", ell)
    require(mobius(d) != 0 and math.gcd(d, h_rad) == 1,
            "delta-opened-row", h_rad, d)
    return Fraction(h_rad, phi(h_rad)) * Fraction(d, phi(d) * (ell - 1))


def divisibility_prefix(r_cut: int, w_cut: int, m: int, h: int,
                        j: int) -> Poly:
    h_rad = radical(h)
    out: Poly = {}
    target = m * j + h
    for w in range(1, w_cut + 1):
        if target % w == 0 and math.gcd(w, m * h_rad) == 1:
            out = add(out, b_poly(r_cut, w))
    return out


def shell_signal(s_cut: int, t_cut: int, m: int, h: int, j: int) -> Poly:
    h_rad = radical(h)
    out: Poly = {}
    target = m * j + h
    for w in range(s_cut + 1, t_cut + 1):
        if target % w == 0 and math.gcd(w, m * h_rad) == 1:
            out = add(out, a_poly(w))
    return out


def annular_orbit_sum(r_cut: int, s_cut: int, t_cut: int,
                      m: int, n: int, h: int, j: int,
                      region: str = "annulus") -> Poly:
    """Raw joint divisor sum in one selected support region."""
    h_rad = radical(h)
    target_m = m * j + h
    target_n = n * j + h
    out: Poly = {}
    for u in range(1, t_cut + 1):
        if target_m % u or math.gcd(u, m * h_rad) != 1:
            continue
        for v in range(1, t_cut + 1):
            if target_n % v or math.gcd(v, n * h_rad) != 1:
                continue
            selected = {
                "annulus": max(u, v) > s_cut,
                "forward": u <= s_cut < v,
                "transpose": v <= s_cut < u,
                "both": s_cut < u and s_cut < v,
            }.get(region)
            require(selected is not None, "unknown-orbit-region", region)
            if selected:
                out = add(out, multiply(b_poly(r_cut, u),
                                        b_poly(r_cut, v)))
    return out


def check_annular_prefix_identity() -> tuple[int, list[dict[str, object]]]:
    cases = (
        {
            "r": 7, "s": 8, "t": 15, "h": 2,
            "left": (17, 1), "right": (19, 3),
            "j_values": (1, 3, 5, 7, 9, 11),
        },
        {
            "r": 6, "s": 7, "t": 13, "h": 6,
            "left": (17, 1), "right": (19, 1),
            "j_values": (1, 5, 7, 11, 13),
        },
        {
            "r": 10, "s": 11, "t": 19, "h": 4,
            "left": (23, 1), "right": (29, 5),
            "j_values": (1, 3, 5, 7, 9),
        },
    )
    checks = 0
    summaries: list[dict[str, object]] = []
    for case in cases:
        r_cut = int(case["r"])
        s_cut = int(case["s"])
        t_cut = int(case["t"])
        h = int(case["h"])
        h_rad = radical(h)
        ell_m, d_m = case["left"]  # type: ignore[misc]
        ell_n, d_n = case["right"]  # type: ignore[misc]
        m = ell_m * d_m
        n = ell_n * d_n
        require(r_cut <= s_cut < t_cut, "prefix-cut-order", case)
        require(ell_m > 2 * r_cut and ell_n > 2 * r_cut,
                "prefix-source-separation", case)
        require(d_m * h_rad <= r_cut and d_n * h_rad <= r_cut,
                "prefix-opened-support", case)
        drift_m = delta_h(h_rad, ell_m, d_m)
        drift_n = delta_h(h_rad, ell_n, d_n)
        local_checks = 0
        for j in case["j_values"]:  # type: ignore[assignment]
            require(math.gcd(j, h_rad) == 1, "prefix-primitive-j", case, j)
            b_ms = divisibility_prefix(r_cut, s_cut, m, h, j)
            b_mt = divisibility_prefix(r_cut, t_cut, m, h, j)
            b_ns = divisibility_prefix(r_cut, s_cut, n, h, j)
            b_nt = divisibility_prefix(r_cut, t_cut, n, h, j)
            l_m = shell_signal(s_cut, t_cut, m, h, j)
            l_n = shell_signal(s_cut, t_cut, n, h, j)

            require(add(b_mt, scale(b_ms, -1)) == l_m,
                    "prefix-shell-left", case, j)
            require(add(b_nt, scale(b_ns, -1)) == l_n,
                    "prefix-shell-right", case, j)
            local_checks += 2

            p_ms = add(b_ms, constant(-drift_m))
            p_mt = add(b_mt, constant(-drift_m))
            p_ns = add(b_ns, constant(-drift_n))
            p_nt = add(b_nt, constant(-drift_n))
            left = add(multiply(p_mt, p_nt),
                       scale(multiply(p_ms, p_ns), -1))
            raw_annulus = annular_orbit_sum(
                r_cut, s_cut, t_cut, m, n, h, j, "annulus")
            right = add(raw_annulus, scale(l_n, -drift_m),
                        scale(l_m, -drift_n))
            require(left == right, "annular-prefix-drift", case, j,
                    serialize_poly(left), serialize_poly(right))
            local_checks += 1

            partition = add(
                annular_orbit_sum(r_cut, s_cut, t_cut, m, n, h, j,
                                  "forward"),
                annular_orbit_sum(r_cut, s_cut, t_cut, m, n, h, j,
                                  "transpose"),
                annular_orbit_sum(r_cut, s_cut, t_cut, m, n, h, j,
                                  "both"),
            )
            require(raw_annulus == partition, "annulus-orbit-partition",
                    case, j)
            local_checks += 1
        checks += local_checks
        summaries.append({
            "R": r_cut,
            "S": s_cut,
            "T": t_cut,
            "h": h,
            "rows": [m, n],
            "j_count": len(case["j_values"]),  # type: ignore[arg-type]
            "checks": local_checks,
        })
    return checks, summaries


def zero_kernel(r_cut: int, s_cut: int, t_cut: int, m: int, n: int,
                h_rad: int, region: str) -> Poly:
    delta = m - n
    out: Poly = {}
    for u in range(1, t_cut + 1):
        if math.gcd(u, m * h_rad) != 1:
            continue
        for v in range(1, t_cut + 1):
            if math.gcd(v, n * h_rad) != 1:
                continue
            selected = {
                "annulus": max(u, v) > s_cut,
                "forward": u <= s_cut < v,
                "transpose": v <= s_cut < u,
                "both": s_cut < u and s_cut < v,
            }.get(region)
            require(selected is not None, "unknown-zero-region", region)
            if not selected:
                continue
            g = math.gcd(u, v)
            if delta % g:
                continue
            left_coefficient = (a_poly(u) if u > s_cut
                                else b_poly(r_cut, u))
            right_coefficient = (a_poly(v) if v > s_cut
                                 else b_poly(r_cut, v))
            term = multiply(left_coefficient, right_coefficient)
            out = add(out, scale(term, Fraction(g, u * v)))
    return out


def both_zero_gcd(s_cut: int, t_cut: int, m: int, n: int,
                  h_rad: int) -> Poly:
    delta = m - n
    out: Poly = {}
    for g in range(1, t_cut + 1):
        if delta % g or mobius(g) == 0 or math.gcd(g, m * n * h_rad) != 1:
            continue
        for c in range(1, t_cut // g + 1):
            if not (s_cut < g * c <= t_cut):
                continue
            if math.gcd(c, g * m * h_rad) != 1:
                continue
            inner: Poly = {}
            for d in range(1, t_cut // g + 1):
                if not (s_cut < g * d <= t_cut):
                    continue
                if math.gcd(d, g * c * n * h_rad) != 1:
                    continue
                inner = add(inner, scale(a_poly(g * d), Fraction(1, d)))
            out = add(out, scale(multiply(a_poly(g * c), inner),
                                 Fraction(1, g * c)))
    return out


def check_zero_kernels() -> tuple[int, list[dict[str, object]], Poly]:
    cases = (
        (4, 4, 12, 1, 11, 17),
        (7, 7, 15, 2, 17, 57),
        (6, 6, 16, 6, 17, 19),
        (8, 9, 20, 2, 35, 77),
    )
    checks = 0
    summaries: list[dict[str, object]] = []
    sample_poly: Poly = {}
    for r_cut, s_cut, t_cut, h_rad, m, n in cases:
        require(r_cut <= s_cut < t_cut and m != n,
                "zero-case-shape", (r_cut, s_cut, t_cut, h_rad, m, n))
        require(math.gcd(m * n, h_rad) == 1,
                "zero-case-primitivity", h_rad, m, n)
        direct = zero_kernel(r_cut, s_cut, t_cut, m, n, h_rad, "both")
        gcd_form = both_zero_gcd(s_cut, t_cut, m, n, h_rad)
        require(direct == gcd_form, "both-zero-gcd", r_cut, s_cut,
                t_cut, h_rad, m, n, serialize_poly(direct),
                serialize_poly(gcd_form))
        checks += 1

        annulus = zero_kernel(r_cut, s_cut, t_cut, m, n, h_rad,
                              "annulus")
        partition = add(
            zero_kernel(r_cut, s_cut, t_cut, m, n, h_rad, "forward"),
            zero_kernel(r_cut, s_cut, t_cut, m, n, h_rad, "transpose"),
            direct,
        )
        require(annulus == partition, "zero-annulus-partition", r_cut,
                s_cut, t_cut, h_rad, m, n)
        checks += 1
        sample_poly = direct
        summaries.append({
            "R": r_cut, "S": s_cut, "T": t_cut, "H": h_rad,
            "rows": [m, n], "monomial_count": len(direct),
            "checks": 2,
        })
    return checks, summaries, sample_poly


def check_a_product_identity() -> tuple[int, int]:
    checks = 0
    tested_pairs = 0
    for g in range(1, 31):
        for d in range(1, 41):
            if mobius(g) == 0 or mobius(d) == 0 or math.gcd(g, d) != 1:
                continue
            right = add(
                scale(a_poly(d), mobius(g)),
                scale(formal_log(g), -mobius(g) * mobius(d)),
            )
            require(a_poly(g * d) == right, "a-gd-formal-identity", g, d,
                    serialize_poly(a_poly(g * d)), serialize_poly(right))
            checks += 1
            tested_pairs += 1
    return checks, tested_pairs


def lcm(left: int, right: int) -> int:
    return left // math.gcd(left, right) * right


def check_crt_case(h: int, m: int, n: int, max_modulus: int) -> tuple[int, int]:
    h_rad = radical(h)
    require(math.gcd(m * n, h_rad) == 1, "crt-row-primitivity", h, m, n)
    checks = 0
    pairs = 0
    for u in range(1, max_modulus + 1):
        if math.gcd(u, m * h_rad) != 1:
            continue
        for v in range(1, max_modulus + 1):
            if math.gcd(v, n * h_rad) != 1:
                continue
            q = lcm(u, v)
            g = math.gcd(u, v)
            compatible = (m - n) % g == 0
            q_residues = [
                j for j in range(q)
                if (m * j + h) % u == 0 and (n * j + h) % v == 0
            ]
            require(len(q_residues) == (1 if compatible else 0),
                    "crt-compatible-class-count", h, m, n, u, v,
                    compatible, q_residues)
            checks += 1
            if compatible:
                require(math.gcd(q_residues[0], q) == 1,
                        "crt-joint-class-unit", h, m, n, u, v,
                        q_residues[0], q)
                checks += 1

            period = h_rad * q
            count = sum(
                1 for j in range(period)
                if math.gcd(j, h_rad) == 1
                and (m * j + h) % u == 0
                and (n * j + h) % v == 0
            )
            expected_count = phi(h_rad) if compatible else 0
            require(count == expected_count, "crt-period-count", h, m, n,
                    u, v, period, count, expected_count)
            checks += 1
            density = Fraction(count, period)
            expected_density = (Fraction(phi(h_rad), h_rad * q)
                                if compatible else Fraction(0))
            require(density == expected_density, "crt-joint-density", h,
                    m, n, u, v, density, expected_density)
            checks += 1
            pairs += 1
    return checks, pairs


def check_crt_density() -> tuple[int, list[dict[str, int]]]:
    cases = (
        (1, 11, 17, 10),
        (4, 17, 57, 12),
        (12, 17, 19, 12),
        (18, 35, 77, 11),
    )
    checks = 0
    summaries: list[dict[str, int]] = []
    for h, m, n, max_modulus in cases:
        local_checks, pairs = check_crt_case(h, m, n, max_modulus)
        checks += local_checks
        summaries.append({
            "h": h, "h_radical": radical(h), "m": m, "n": n,
            "max_modulus": max_modulus, "modulus_pairs": pairs,
            "checks": local_checks,
        })
    return checks, summaries


def k_exponent(beta: Fraction, conductor: Fraction) -> Fraction:
    return max(conductor, beta - conductor)


def cell_savings(beta: Fraction, t: Fraction, y: Fraction,
                 f1: Fraction, f2: Fraction) -> tuple[Fraction, Fraction]:
    k1 = k_exponent(beta, f1)
    k2 = k_exponent(beta, f2)
    eta_a = (beta + 1 - y - k1 - k2) / 2
    eta_b = 1 - f1 - f2 - (k1 + k2) / 2
    return eta_a, eta_b


def sharp_eta(beta: Fraction, t: Fraction) -> Fraction:
    require(t > 1 - beta, "sharp-crossing", beta, t)
    if t <= beta / 2:
        return (3 * (1 - beta) - 2 * t) / 4
    return min((beta + 1 - 4 * t) / 2,
               (3 - beta - 6 * t) / 4)


def fraction_grid(limit: Fraction, denominator: int) -> Iterable[Fraction]:
    for numerator in range(denominator + 1):
        yield limit * Fraction(numerator, denominator)


def check_sharp_grid(beta: Fraction, t: Fraction,
                     f_denominator: int = 24,
                     y_denominator: int = 12) -> tuple[int, int]:
    eta = sharp_eta(beta, t)
    checks = 0
    points = 0
    for f1 in fraction_grid(t, f_denominator):
        for f2 in fraction_grid(t, f_denominator):
            for y in fraction_grid(2 * t, y_denominator):
                eta_a, eta_b = cell_savings(beta, t, y, f1, f2)
                require(max(eta_a, eta_b) >= eta,
                        "sharp-grid-lower-bound", beta, t, y, f1, f2,
                        eta_a, eta_b, eta)
                checks += 1
                points += 1
    return checks, points


def check_sharp_ledger() -> tuple[int, list[dict[str, str]], int]:
    grid_cases = (
        (Fraction(4, 5), Fraction(1, 4)),
        (Fraction(31, 50), Fraction(39, 100)),
        (Fraction(7, 10), Fraction(9, 25)),
        (Fraction(267, 400), Fraction(193, 500)),
    )
    checks = 0
    total_points = 0
    summaries: list[dict[str, str]] = []
    for beta, t in grid_cases:
        local_checks, points = check_sharp_grid(beta, t)
        checks += local_checks
        total_points += points
        eta = sharp_eta(beta, t)
        if t <= beta / 2:
            sigma_star = (1 - beta + 2 * t) / 2
            f1 = sigma_star / 2
            f2 = sigma_star / 2
            eta_a, eta_b = cell_savings(beta, t, 2 * t, f1, f2)
            require(eta_a == eta_b == eta, "low-low-sharp-witness",
                    beta, t, f1, f2, eta_a, eta_b, eta)
            witness = "low-low"
        else:
            high_face = (beta + 1 - 4 * t) / 2
            mixed_face = (3 - beta - 6 * t) / 4
            high_a, high_b = cell_savings(beta, t, 2 * t, t, t)
            require(max(high_a, high_b) == high_face,
                    "high-high-face-witness", beta, t, high_a, high_b,
                    high_face)
            low = (1 - beta) / 2
            mixed_a, mixed_b = cell_savings(beta, t, 2 * t, low, t)
            require(mixed_a == mixed_b == mixed_face,
                    "mixed-face-witness", beta, t, low, mixed_a, mixed_b,
                    mixed_face)
            require(min(high_face, mixed_face) == eta,
                    "high-region-minimum", beta, t, high_face,
                    mixed_face, eta)
            checks += 2
            witness = "mixed/high-high"
        checks += 1
        summaries.append({
            "beta": str(beta), "t": str(t), "eta": str(eta),
            "region": "low" if t <= beta / 2 else "high-mixed",
            "witness": witness, "grid_points": str(points),
        })

    beta_join = Fraction(7, 10)
    t_join = beta_join / 2
    low_join = (3 * (1 - beta_join) - 2 * t_join) / 4
    high_join = min((beta_join + 1 - 4 * t_join) / 2,
                    (3 - beta_join - 6 * t_join) / 4)
    require(low_join == high_join == Fraction(1, 20),
            "sharp-branch-join", low_join, high_join)
    checks += 1

    beta_low_boundary = Fraction(4, 5)
    t_low_boundary = 3 * (1 - beta_low_boundary) / 2
    require(sharp_eta(beta_low_boundary, t_low_boundary) == 0,
            "sharp-low-zero-boundary", beta_low_boundary, t_low_boundary)
    checks += 1

    beta_mixed_boundary = Fraction(31, 50)
    t_mixed_boundary = (3 - beta_mixed_boundary) / 6
    require((3 - beta_mixed_boundary - 6 * t_mixed_boundary) / 4 == 0,
            "sharp-mixed-zero-boundary", beta_mixed_boundary,
            t_mixed_boundary)
    checks += 1

    beta_high_boundary = Fraction(31, 50)
    t_high_boundary = (beta_high_boundary + 1) / 4
    require((beta_high_boundary + 1 - 4 * t_high_boundary) / 2 == 0,
            "sharp-high-zero-boundary", beta_high_boundary,
            t_high_boundary)
    checks += 1

    beta_cross_boundary = Fraction(3, 5)
    t_cross_boundary = 1 - beta_cross_boundary
    mixed_at_cross = (3 - beta_cross_boundary - 6 * t_cross_boundary) / 4
    require(mixed_at_cross == 0, "sharp-three-fifths-boundary",
            beta_cross_boundary, t_cross_boundary, mixed_at_cross)
    checks += 1

    return checks, summaries, total_points


def check_old_sample() -> tuple[int, dict[str, object]]:
    delta = Fraction(3, 20)
    beta = Fraction(31, 50)
    xi = Fraction(1, 25)
    s = Fraction(1, 2) - delta
    j_exponent = 1 - beta
    t = s + xi
    coarse_faces = (
        1 - Fraction(3, 2) * beta,
        (beta + 1 - 4 * t) / 2,
        (3 - beta - 6 * t) / 4,
    )
    require((s, j_exponent, t) ==
            (Fraction(7, 20), Fraction(19, 50), Fraction(39, 100)),
            "old-sample-scales", s, j_exponent, t)
    require(s < j_exponent < t, "old-sample-crossing", s, j_exponent, t)
    require(coarse_faces == (Fraction(7, 100), Fraction(3, 100),
                             Fraction(1, 100)),
            "old-sample-faces", coarse_faces)
    require(sharp_eta(beta, t) == Fraction(1, 100),
            "old-sample-sharp-eta", sharp_eta(beta, t))
    return 4, {
        "delta": str(delta), "beta": str(beta), "xi": str(xi),
        "S_exponent": str(s), "J_exponent": str(j_exponent),
        "T_exponent": str(t),
        "coarse_faces": [str(value) for value in coarse_faces],
        "sharp_eta": "1/100",
    }


def check_high_beta_sample() -> tuple[int, dict[str, object]]:
    sigma = Fraction(1, 10000)
    source_lambda = Fraction(10, 21) - sigma
    delta = Fraction(7, 60)
    v_exponent = Fraction(1, 4) - delta / 2
    beta = Fraction(267, 400)
    d_exponent = beta - source_lambda
    s = Fraction(1, 2) - delta
    j_exponent = 1 - beta
    t = Fraction(193, 500)
    high_face = (beta + 1 - 4 * t) / 2
    mixed_face = (3 - beta - 6 * t) / 4
    margins = {
        "beta_above_two_thirds": beta - Fraction(2, 3),
        "delta_above_one_ninth": delta - Fraction(1, 9),
        "delta_below_profile_ceiling":
            Fraction(5, 42) - 2 * sigma - delta,
        "delta_above_profile_floor":
            delta - (Fraction(1, 42) + 3 * sigma),
        "delta_below_one_quarter": Fraction(1, 4) - delta,
        "source_above_R": source_lambda - s,
        "D_below_V": v_exponent - d_exponent,
        "T_above_S": t - s,
        "T_above_J": t - j_exponent,
    }
    for name, margin in margins.items():
        require(margin > 0, "high-beta-positive-margin", name, margin)
    require(source_lambda == Fraction(99979, 210000),
            "high-beta-source-lambda", source_lambda)
    require(v_exponent == Fraction(23, 120),
            "high-beta-V-exponent", v_exponent)
    require(d_exponent == Fraction(10049, 52500),
            "high-beta-D-exponent", d_exponent)
    require(margins["D_below_V"] == Fraction(9, 35000),
            "high-beta-D-margin", margins["D_below_V"])
    require(margins["T_above_S"] == Fraction(1, 375),
            "high-beta-shell-margin", margins["T_above_S"])
    require(j_exponent == Fraction(133, 400),
            "high-beta-J-exponent", j_exponent)
    require(t >= beta / 2, "high-beta-ledger-region", beta, t)
    require(high_face == Fraction(247, 4000),
            "high-beta-high-face", high_face)
    require(mixed_face == Fraction(33, 8000),
            "high-beta-mixed-face", mixed_face)
    require(sharp_eta(beta, t) == Fraction(33, 8000),
            "high-beta-sharp-eta", sharp_eta(beta, t))
    checks = len(margins) + 10
    return checks, {
        "sigma": str(sigma),
        "delta": str(delta),
        "source_lambda": str(source_lambda),
        "V_exponent": str(v_exponent),
        "beta": str(beta),
        "D_exponent": str(d_exponent),
        "S_exponent": str(s),
        "J_exponent": str(j_exponent),
        "T_exponent": str(t),
        "high_face": str(high_face),
        "mixed_face": str(mixed_face),
        "sharp_eta": str(sharp_eta(beta, t)),
        "margins": {name: str(value) for name, value in margins.items()},
    }


def main() -> None:
    checks = 0
    subcounts: dict[str, int] = {}

    count, prefix_cases = check_annular_prefix_identity()
    checks += count
    subcounts["annular_prefix_and_orbit_partition"] = count

    count, zero_cases, sample_zero = check_zero_kernels()
    checks += count
    subcounts["zero_kernel_and_annulus_partition"] = count

    count, formal_pairs = check_a_product_identity()
    checks += count
    subcounts["formal_a_product_identity"] = count

    count, crt_cases = check_crt_density()
    checks += count
    subcounts["crt_compatibility_and_density"] = count

    count, ledger_cases, grid_points = check_sharp_ledger()
    checks += count
    subcounts["sharp_ledger"] = count

    count, old_sample = check_old_sample()
    checks += count
    subcounts["old_sample"] = count

    count, high_beta_sample = check_high_beta_sample()
    checks += count
    subcounts["high_beta_sample"] = count

    source_path = Path(__file__)
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    payload = {
        "paper": "TPC-26",
        "certificate": "joint-before-separation annular recombination",
        "exact_check_count": checks,
        "subcheck_counts": subcounts,
        "annular_prefix_cases": prefix_cases,
        "zero_kernel_cases": zero_cases,
        "formal_a_identity_pairs": formal_pairs,
        "crt_cases": crt_cases,
        "sharp_ledger_cases": ledger_cases,
        "sharp_ledger_grid_points": grid_points,
        "old_crossing_sample": old_sample,
        "high_beta_source_sample": high_beta_sample,
        "sample_both_new_zero_polynomial": serialize_poly(sample_zero),
        "source_sha256": source_hash,
        "claims": {
            "finite_annular_prefix_identity": True,
            "finite_annulus_partition": True,
            "finite_both_new_zero_gcd_identity": True,
            "finite_crt_density_identity": True,
            "finite_sharp_ledger_grid": True,
            "asymptotic_mobius_evidence": False,
            "full_residual_closure": False,
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
