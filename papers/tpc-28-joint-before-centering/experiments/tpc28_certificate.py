#!/usr/bin/env python3
"""Exact finite certificate for TPC-28.

The certificate uses only the Python standard library.  Scale
computations use Fraction, while logarithms in the finite divisor
identities are formal prime-log variables.  It checks exact algebra,
CRT densities, and rational conductor ledgers.  It is not numerical
evidence for an asymptotic Mobius estimate, Hardy--Littlewood, or twin
primes.
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
    fac = factor(n)
    if any(exponent > 1 for exponent in fac.values()):
        return 0
    return -1 if len(fac) % 2 else 1


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


def lcm(left: int, right: int) -> int:
    return left // math.gcd(left, right) * right


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
    require(is_prime(ell), "delta-prime", ell)
    require(mobius(d) != 0 and math.gcd(d, h_rad) == 1,
            "delta-opened-row", h_rad, d)
    return Fraction(h_rad, phi(h_rad)) * Fraction(
        d, phi(d) * (ell - 1))


def raw_prefix(r_cut: int, s_cut: int, m: int, h: int, j: int) -> Poly:
    target = m * j + h
    require(target != 0, "nonzero-target", r_cut, s_cut, m, h, j)
    out: Poly = {}
    for u in range(1, s_cut + 1):
        if target % u == 0:
            out = add(out, b_poly(r_cut, u))
    return out


def check_raw_drift_identity() -> tuple[int, list[dict[str, object]]]:
    cases = (
        {"R": 5, "S": 8, "h": 1, "left": (13, 1),
         "right": (17, 1), "j": range(1, 10)},
        {"R": 6, "S": 10, "h": 2, "left": (17, 1),
         "right": (19, 3), "j": (1, 3, 5, 7, 9)},
        {"R": 10, "S": 14, "h": 6, "left": (23, 1),
         "right": (29, 5), "j": (1, 5, 7, 11)},
    )
    checks = 0
    summaries: list[dict[str, object]] = []
    for case in cases:
        r_cut = int(case["R"])
        s_cut = int(case["S"])
        h = int(case["h"])
        h_rad = radical(h)
        ell_m, d_m = case["left"]  # type: ignore[misc]
        ell_n, d_n = case["right"]  # type: ignore[misc]
        m, n = ell_m * d_m, ell_n * d_n
        require(r_cut <= s_cut, "raw-cut-order", case)
        require(ell_m > 2 * r_cut and ell_n > 2 * r_cut,
                "raw-row-separation", case)
        drift_m = delta_h(h_rad, ell_m, d_m)
        drift_n = delta_h(h_rad, ell_n, d_n)
        local = 0
        for j in case["j"]:  # type: ignore[assignment]
            require(math.gcd(j, h_rad) == 1, "raw-primitive-j", case, j)
            a_m = raw_prefix(r_cut, s_cut, m, h, j)
            a_n = raw_prefix(r_cut, s_cut, n, h, j)
            p_m = add(a_m, constant(-drift_m))
            p_n = add(a_n, constant(-drift_n))
            left = multiply(p_m, p_n)
            right = add(
                multiply(a_m, a_n),
                scale(a_n, -drift_m),
                scale(a_m, -drift_n),
                constant(drift_m * drift_n),
            )
            require(left == right, "raw-drift-product", case, j,
                    serialize_poly(left), serialize_poly(right))
            local += 1
        checks += local
        summaries.append({
            "R": r_cut, "S": s_cut, "h": h, "rows": [m, n],
            "orbit_points": len(tuple(case["j"])), "checks": local,
        })
    return checks, summaries


def prefix_density(r_cut: int, s_cut: int, m: int, h_rad: int) -> Poly:
    out: Poly = {}
    for u in range(1, s_cut + 1):
        if math.gcd(u, m * h_rad) == 1:
            out = add(out, scale(b_poly(r_cut, u), Fraction(1, u)))
    return out


def raw_zero(r_cut: int, s_cut: int, m: int, n: int,
             h_rad: int) -> Poly:
    out: Poly = {}
    delta = m - n
    for u in range(1, s_cut + 1):
        if math.gcd(u, m * h_rad) != 1:
            continue
        for v in range(1, s_cut + 1):
            if math.gcd(v, n * h_rad) != 1:
                continue
            g = math.gcd(u, v)
            if delta % g == 0:
                out = add(out, scale(
                    multiply(b_poly(r_cut, u), b_poly(r_cut, v)),
                    Fraction(g, u * v)))
    return out


def connected_zero(r_cut: int, s_cut: int, m: int, n: int,
                   h_rad: int) -> Poly:
    """Compute the connected kernel directly, not by subtraction."""
    out: Poly = {}
    delta = m - n
    for u in range(1, s_cut + 1):
        if math.gcd(u, m * h_rad) != 1:
            continue
        for v in range(1, s_cut + 1):
            if math.gcd(v, n * h_rad) != 1:
                continue
            g = math.gcd(u, v)
            numerator = g * int(delta % g == 0) - 1
            out = add(out, scale(
                multiply(b_poly(r_cut, u), b_poly(r_cut, v)),
                Fraction(numerator, u * v)))
    return out


def complete_period_calibrated_zero(
        r_cut: int, s_cut: int, h: int,
        ell_m: int, d_m: int, ell_n: int, d_n: int) -> Poly:
    """Average the calibrated product over a complete primitive period."""
    h_rad = radical(h)
    period = h_rad
    for u in range(1, s_cut + 1):
        period = lcm(period, u)
    m, n = ell_m * d_m, ell_n * d_n
    drift_m = delta_h(h_rad, ell_m, d_m)
    drift_n = delta_h(h_rad, ell_n, d_n)
    total: Poly = {}
    primitive_points = 0
    for j in range(period):
        if math.gcd(j, h_rad) != 1:
            continue
        p_m = add(raw_prefix(r_cut, s_cut, m, h, j),
                  constant(-drift_m))
        p_n = add(raw_prefix(r_cut, s_cut, n, h, j),
                  constant(-drift_n))
        total = add(total, multiply(p_m, p_n))
        primitive_points += 1
    require(primitive_points > 0, "complete-period-nonempty", h, s_cut)
    return scale(total, Fraction(1, primitive_points))


def check_zero_recombination() -> tuple[int, list[dict[str, object]], Poly]:
    cases = (
        (5, 8, 1, 13, 1, 17, 1),
        (6, 9, 2, 17, 1, 19, 3),
        (9, 12, 12, 23, 1, 29, 5),
    )
    checks = 0
    summaries: list[dict[str, object]] = []
    sample: Poly = {}
    for r_cut, s_cut, h, ell_m, d_open_m, ell_n, d_open_n in cases:
        h_rad = radical(h)
        m, n = ell_m * d_open_m, ell_n * d_open_n
        drift_m = delta_h(h_rad, ell_m, d_open_m)
        drift_n = delta_h(h_rad, ell_n, d_open_n)
        require(m != n and math.gcd(m * n, h_rad) == 1,
                "zero-row-shape", h, m, n)
        d_m = prefix_density(r_cut, s_cut, m, h_rad)
        d_n = prefix_density(r_cut, s_cut, n, h_rad)
        raw = raw_zero(r_cut, s_cut, m, n, h_rad)
        connected = connected_zero(r_cut, s_cut, m, n, h_rad)
        e_m = add(d_m, constant(-drift_m))
        e_n = add(d_n, constant(-drift_n))
        calibrated = add(
            raw,
            scale(d_n, -drift_m),
            scale(d_m, -drift_n),
            constant(drift_m * drift_n),
        )
        expected = add(connected, multiply(e_m, e_n))
        require(raw == add(connected, multiply(d_m, d_n)),
                "raw-connected-zero", r_cut, s_cut, h, m, n)
        require(calibrated == expected, "calibrated-zero-recombination",
                r_cut, s_cut, h, m, n,
                serialize_poly(calibrated), serialize_poly(expected))
        period_average = complete_period_calibrated_zero(
            r_cut, s_cut, h,
            ell_m, d_open_m, ell_n, d_open_n)
        require(period_average == calibrated,
                "complete-period-calibrated-zero",
                r_cut, s_cut, h, m, n,
                serialize_poly(period_average), serialize_poly(calibrated))
        checks += 3
        sample = calibrated
        summaries.append({
            "R": r_cut, "S": s_cut, "h": h, "rows": [m, n],
            "opened_rows": [[ell_m, d_open_m], [ell_n, d_open_n]],
            "drifts": [str(drift_m), str(drift_n)],
            "monomial_count": len(calibrated), "checks": 3,
        })
    return checks, summaries, sample


def check_crt_case(h: int, m: int, n: int,
                   max_modulus: int) -> tuple[int, int]:
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
            residues = [
                j for j in range(q)
                if (m * j + h) % u == 0 and (n * j + h) % v == 0
            ]
            require(len(residues) == (1 if compatible else 0),
                    "crt-class-count", h, m, n, u, v, residues)
            checks += 1
            if compatible:
                require(math.gcd(residues[0], q) == 1,
                        "crt-unit-class", h, m, n, u, v, residues[0])
                checks += 1
            period = h_rad * q
            count = sum(
                1 for j in range(period)
                if math.gcd(j, h_rad) == 1
                and (m * j + h) % u == 0
                and (n * j + h) % v == 0
            )
            expected = phi(h_rad) if compatible else 0
            require(count == expected, "crt-primitive-period-count",
                    h, m, n, u, v, count, expected)
            checks += 1
            density = Fraction(count, period)
            expected_density = (Fraction(phi(h_rad), h_rad * q)
                                if compatible else Fraction(0))
            require(density == expected_density, "crt-density",
                    h, m, n, u, v, density, expected_density)
            checks += 1
            pairs += 1
    return checks, pairs


def check_crt_density() -> tuple[int, list[dict[str, int]]]:
    cases = (
        (1, 13, 17, 12),
        (2, 17, 57, 12),
        (6, 23, 145, 11),
        (12, 23, 145, 11),
        (30, 49, 121, 10),
    )
    checks = 0
    summaries: list[dict[str, int]] = []
    for h, m, n, max_modulus in cases:
        local, pairs = check_crt_case(h, m, n, max_modulus)
        checks += local
        summaries.append({
            "h": h, "h_radical": radical(h), "m": m, "n": n,
            "max_modulus": max_modulus, "modulus_pairs": pairs,
            "checks": local,
        })
    return checks, summaries


def k_exponent(beta: Fraction, conductor: Fraction) -> Fraction:
    return max(conductor, beta - conductor)


def cell_savings(beta: Fraction, y: Fraction, f1: Fraction,
                 f2: Fraction) -> tuple[Fraction, Fraction]:
    k1 = k_exponent(beta, f1)
    k2 = k_exponent(beta, f2)
    eta_a = (beta + 1 - y - k1 - k2) / 2
    eta_b = 1 - f1 - f2 - (k1 + k2) / 2
    return eta_a, eta_b


def sharp_m(beta: Fraction, s: Fraction) -> Fraction:
    require(Fraction(1, 2) <= beta < 1 and s >= 0,
            "sharp-domain", beta, s)
    if s <= (1 - beta) / 2:
        return 1 - beta - s
    if s <= beta / 2:
        return (3 - 3 * beta - 2 * s) / 4
    if s <= (3 * beta - 1) / 2:
        return (3 - beta - 6 * s) / 4
    return (beta + 1 - 4 * s) / 2


def fraction_grid(limit: Fraction, denominator: int) -> Iterable[Fraction]:
    for numerator in range(denominator + 1):
        yield limit * Fraction(numerator, denominator)


def check_minimax_grid(beta: Fraction, s: Fraction,
                       f_denominator: int = 24,
                       y_denominator: int = 12) -> tuple[int, int]:
    target = sharp_m(beta, s)
    checks = 0
    points = 0
    for f1 in fraction_grid(s, f_denominator):
        for f2 in fraction_grid(s, f_denominator):
            for y in fraction_grid(2 * s, y_denominator):
                eta_a, eta_b = cell_savings(beta, y, f1, f2)
                require(max(eta_a, eta_b) >= target,
                        "minimax-grid-lower-bound", beta, s, y, f1,
                        f2, eta_a, eta_b, target)
                checks += 1
                points += 1
    return checks, points


def check_minimax_ledger() -> tuple[int, list[dict[str, str]], int]:
    cases = (
        (Fraction(7, 10), Fraction(1, 20), "short-endpoint"),
        (Fraction(7, 10), Fraction(1, 4), "low-low"),
        (Fraction(267, 400), Fraction(23, 60), "mixed"),
        (Fraction(11, 20), Fraction(1, 3), "high-high"),
    )
    checks = 0
    points = 0
    summaries: list[dict[str, str]] = []
    for beta, s, region in cases:
        local, grid_points = check_minimax_grid(beta, s)
        checks += local
        points += grid_points
        target = sharp_m(beta, s)

        if s <= (1 - beta) / 2:
            eta_a, eta_b = cell_savings(beta, 2 * s, s, s)
            require(max(eta_a, eta_b) == target,
                    "short-endpoint-witness", beta, s, eta_a, eta_b)
        elif s <= beta / 2:
            sigma = s + (1 - beta) / 2
            f1 = sigma / 2
            f2 = sigma / 2
            eta_a, eta_b = cell_savings(beta, 2 * s, f1, f2)
            require(eta_a == eta_b == target,
                    "low-low-witness", beta, s, f1, f2)
        elif s <= (3 * beta - 1) / 2:
            f1 = (1 - beta) / 2
            f2 = s
            eta_a, eta_b = cell_savings(beta, 2 * s, f1, f2)
            require(eta_a == eta_b == target,
                    "mixed-witness", beta, s, f1, f2)
        else:
            eta_a, eta_b = cell_savings(beta, 2 * s, s, s)
            require(max(eta_a, eta_b) == target,
                    "high-high-witness", beta, s, eta_a, eta_b)
        checks += 1
        summaries.append({
            "beta": str(beta), "s": str(s), "region": region,
            "M_beta_s": str(target), "grid_points": str(grid_points),
        })

    joins = (
        (Fraction(7, 10), (1 - Fraction(7, 10)) / 2),
        (Fraction(7, 10), Fraction(7, 20)),
        (Fraction(7, 10), (3 * Fraction(7, 10) - 1) / 2),
    )
    for beta, s in joins:
        left = sharp_m(beta, s)
        if s == (1 - beta) / 2:
            right = (3 - 3 * beta - 2 * s) / 4
        elif s == beta / 2:
            right = (3 - beta - 6 * s) / 4
        else:
            right = (beta + 1 - 4 * s) / 2
        require(left == right, "minimax-branch-continuity", beta, s,
                left, right)
        checks += 1
    return checks, summaries, points


def check_high_beta_sample() -> tuple[int, dict[str, object]]:
    sigma = Fraction(1, 10000)
    source_lambda = Fraction(10, 21) - sigma
    delta = Fraction(7, 60)
    beta = Fraction(267, 400)
    s = Fraction(23, 60)
    t = Fraction(193, 500)
    j_exponent = 1 - beta
    d_exponent = beta - source_lambda
    v_exponent = Fraction(1, 4) - delta / 2
    old_faces = (
        1 - Fraction(3, 2) * beta,
        (beta + 1 - 4 * s) / 2,
        (3 - beta - 6 * s) / 4,
    )
    base_m = sharp_m(beta, s)
    upper_m = sharp_m(beta, t)
    margins = {
        "beta_above_two_thirds": beta - Fraction(2, 3),
        "base_above_J": s - j_exponent,
        "T_above_S": t - s,
        "source_above_T": source_lambda - t,
        "D_below_V": v_exponent - d_exponent,
    }
    for name, margin in margins.items():
        require(margin > 0, "high-sample-positive-margin", name, margin)
    require(source_lambda == Fraction(99979, 210000),
            "high-source-lambda", source_lambda)
    require(d_exponent == Fraction(10049, 52500),
            "high-D-exponent", d_exponent)
    require(v_exponent == Fraction(23, 120),
            "high-V-exponent", v_exponent)
    require(margins["D_below_V"] == Fraction(9, 35000),
            "high-D-margin", margins["D_below_V"])
    require(margins["base_above_J"] == Fraction(61, 1200),
            "high-Poisson-overrun", margins["base_above_J"])
    require(margins["T_above_S"] == Fraction(1, 375),
            "high-annular-width", margins["T_above_S"])
    require(margins["source_above_T"] == Fraction(18919, 210000),
            "high-L-above-T", margins["source_above_T"])
    require(old_faces == (Fraction(-1, 800), Fraction(161, 2400),
                           Fraction(13, 1600)),
            "high-old-faces", old_faces)
    require(s == Fraction(1, 2) - delta,
            "high-sieve-base-relation", s, delta)
    require(beta / 2 < s < (3 * beta - 1) / 2,
            "high-base-minimax-branch", beta, s)
    require(beta / 2 < t < (3 * beta - 1) / 2,
            "high-upper-minimax-branch", beta, t)
    require(base_m == Fraction(13, 1600), "high-base-M", base_m)
    require(upper_m == Fraction(33, 8000), "high-upper-M", upper_m)
    checks = len(margins) + 13
    return checks, {
        "sigma": str(sigma), "delta": str(delta),
        "source_lambda": str(source_lambda), "beta": str(beta),
        "D_exponent": str(d_exponent), "V_exponent": str(v_exponent),
        "J_exponent": str(j_exponent), "S_exponent": str(s),
        "T_exponent": str(t),
        "old_centered_faces": [str(value) for value in old_faces],
        "base_M": str(base_m), "upper_M": str(upper_m),
        "margins": {name: str(value) for name, value in margins.items()},
    }


def main() -> None:
    checks = 0
    subcounts: dict[str, int] = {}

    count, raw_cases = check_raw_drift_identity()
    checks += count
    subcounts["raw_drift_product_identity"] = count

    count, zero_cases, sample_zero = check_zero_recombination()
    checks += count
    subcounts["raw_centered_calibrated_zero"] = count

    count, crt_cases = check_crt_density()
    checks += count
    subcounts["full_base_crt_density"] = count

    count, minimax_cases, grid_points = check_minimax_ledger()
    checks += count
    subcounts["full_base_minimax"] = count

    count, high_sample = check_high_beta_sample()
    checks += count
    subcounts["high_beta_sample"] = count

    source_path = Path(__file__)
    source_bytes = source_path.read_bytes()
    normalized_source = source_bytes.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")
    source_hash = hashlib.sha256(normalized_source).hexdigest()
    payload = {
        "paper": "TPC-28",
        "certificate": "joint-before-centering full-base closure",
        "exact_check_count": checks,
        "subcheck_counts": subcounts,
        "raw_drift_cases": raw_cases,
        "zero_recombination_cases": zero_cases,
        "crt_cases": crt_cases,
        "minimax_cases": minimax_cases,
        "minimax_grid_points": grid_points,
        "high_beta_source_sample": high_sample,
        "sample_calibrated_zero_polynomial": serialize_poly(sample_zero),
        "source_sha256": source_hash,
        "claims": {
            "finite_raw_drift_identity": True,
            "finite_zero_recombination": True,
            "finite_crt_density": True,
            "finite_minimax_grid": True,
            "asymptotic_mobius_evidence": False,
            "ultra_long_complement_closed": False,
            "full_residual_closed": False,
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
    output_path.write_bytes(
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
