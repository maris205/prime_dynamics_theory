#!/usr/bin/env python3
"""Exact finite certificate for TPC-29.

The certificate uses only the Python standard library.  It checks
finite calibrated-prefix algebra, generalized CRT fibers, a finite
explicit-constant incidence inequality, long-fiber bookkeeping, and
rational exponent ledgers.  Logarithms are formal prime-log variables.
It is not numerical evidence for an asymptotic Mobius estimate, a
prime-pair main term, or twin primes.
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


def tau(n: int) -> int:
    out = 1
    for exponent in factor(abs(n)).values():
        out *= exponent + 1
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
    return {monomial: coefficient
            for monomial, coefficient in poly.items() if coefficient}


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


def delta_h(h_rad: int, ell: int, d_open: int) -> Fraction:
    require(is_prime(ell), "delta-prime", ell)
    require(mobius(d_open) != 0 and math.gcd(d_open, h_rad) == 1,
            "delta-opened-row", h_rad, d_open)
    return Fraction(h_rad, phi(h_rad)) * Fraction(
        d_open, phi(d_open) * (ell - 1))


def raw_prefix(r_cut: int, s_cut: int, m: int, h: int, j: int) -> Poly:
    target = m * j + h
    require(target > 0, "positive-target", r_cut, s_cut, m, h, j)
    out: Poly = {}
    for w in range(1, min(s_cut, target) + 1):
        if target % w == 0:
            out = add(out, b_poly(r_cut, w))
    return out


def ultra_increment(t_cut: int, u_cut: int,
                    m: int, h: int, j: int) -> Poly:
    target = m * j + h
    require(target > 0 and t_cut < u_cut,
            "ultra-domain", t_cut, u_cut, m, h, j)
    out: Poly = {}
    for w in range(t_cut + 1, min(u_cut, target) + 1):
        if target % w == 0:
            out = add(out, a_poly(w))
    return out


def check_calibrated_difference() -> tuple[int, list[dict[str, object]]]:
    cases = (
        {"R": 5, "T": 8, "U": 200, "h": 1,
         "left": (13, 1), "right": (17, 1), "j": (1, 2, 4, 7)},
        {"R": 6, "T": 10, "U": 400, "h": 2,
         "left": (17, 1), "right": (19, 3), "j": (1, 3, 5)},
        {"R": 10, "T": 14, "U": 1200, "h": 6,
         "left": (23, 1), "right": (29, 5), "j": (1, 5, 7)},
    )
    checks = 0
    summaries: list[dict[str, object]] = []
    for case in cases:
        r_cut = int(case["R"])
        t_cut = int(case["T"])
        u_cut = int(case["U"])
        h = int(case["h"])
        h_rad = radical(h)
        ell_m, d_m = case["left"]  # type: ignore[misc]
        ell_n, d_n = case["right"]  # type: ignore[misc]
        m, n = ell_m * d_m, ell_n * d_n
        drift_m = delta_h(h_rad, ell_m, d_m)
        drift_n = delta_h(h_rad, ell_n, d_n)
        require(r_cut <= t_cut < u_cut, "cutoff-order", case)
        local = 0
        sample: Poly = {}
        for j in case["j"]:  # type: ignore[assignment]
            require(math.gcd(j, h_rad) == 1,
                    "prefix-primitive-j", case, j)
            require(m * j + h <= u_cut and n * j + h <= u_cut,
                    "horizon-covers-targets", case, j)
            for w in range(t_cut + 1, u_cut + 1):
                require(b_poly(r_cut, w) == a_poly(w),
                        "b-equals-a-above-R", case, j, w)
                local += 1

            a_m_t = raw_prefix(r_cut, t_cut, m, h, j)
            a_n_t = raw_prefix(r_cut, t_cut, n, h, j)
            p_m_t = add(a_m_t, constant(-drift_m))
            p_n_t = add(a_n_t, constant(-drift_n))
            p_m_u = add(raw_prefix(r_cut, u_cut, m, h, j),
                        constant(-drift_m))
            p_n_u = add(raw_prefix(r_cut, u_cut, n, h, j),
                        constant(-drift_n))
            c_m = ultra_increment(t_cut, u_cut, m, h, j)
            c_n = ultra_increment(t_cut, u_cut, n, h, j)
            require(add(p_m_u, scale(p_m_t, -1)) == c_m,
                    "calibrated-cutoff-left", case, j)
            require(add(p_n_u, scale(p_n_t, -1)) == c_n,
                    "calibrated-cutoff-right", case, j)
            local += 2

            left = add(multiply(p_m_u, p_n_u),
                       scale(multiply(p_m_t, p_n_t), -1))
            right = add(
                multiply(a_m_t, c_n),
                multiply(c_m, a_n_t),
                multiply(c_m, c_n),
                scale(c_n, -drift_m),
                scale(c_m, -drift_n),
            )
            require(left == right, "five-term-joint-identity",
                    case, j, serialize_poly(left), serialize_poly(right))
            local += 1
            sample = left
        checks += local
        summaries.append({
            "R": r_cut, "T": t_cut, "U0": u_cut, "h": h,
            "rows": [m, n], "orbit_points": len(tuple(case["j"])),
            "checks": local,
            "sample_joint_polynomial": serialize_poly(sample),
        })
    return checks, summaries


def residue_for_row(m: int, h: int, modulus: int) -> int:
    require(modulus >= 1 and math.gcd(m, modulus) == 1,
            "residue-domain", m, h, modulus)
    if modulus == 1:
        return 0
    return (-h * pow(m, -1, modulus)) % modulus


def crt_class(h: int, m: int, n: int,
              r: int, s: int) -> tuple[bool, int | None, int]:
    require(math.gcd(m, r) == 1 and math.gcd(n, s) == 1,
            "crt-primitive-moduli", h, m, n, r, s)
    d = math.gcd(r, s)
    q = lcm(r, s)
    ar = residue_for_row(m, h, r)
    ass = residue_for_row(n, h, s)
    compatible = (ar - ass) % d == 0
    expected = (h * (m - n)) % d == 0
    require(compatible == expected, "crt-compatibility-equivalence",
            h, m, n, r, s, ar, ass, d)
    if not compatible:
        return False, None, q
    residues = [j for j in range(q)
                if (m * j + h) % r == 0 and (n * j + h) % s == 0]
    require(len(residues) == 1, "crt-unique-class",
            h, m, n, r, s, q, residues)
    return True, residues[0], q


def window_occupancy(j0: int, q: int, horizon: int) -> int:
    require(0 <= j0 < q and horizon >= 0,
            "occupancy-domain", j0, q, horizon)
    return sum(1 for j in range(1, horizon + 1) if j % q == j0)


def check_crt_fibers() -> tuple[int, dict[str, object]]:
    shifts = (1, 2, 6, 12)
    row_pairs = ((2, 3), (3, 5), (5, 7), (5, 11),
                 (7, 13), (11, 17))
    max_modulus = 18
    checks = 0
    compatible_count = 0
    incompatible_count = 0
    nontrivial_content = 0
    zero_class = 0
    nonsquarefree_shift = 0
    tested_pairs = 0
    for h in shifts:
        h_rad = radical(h)
        for m, n in row_pairs:
            if math.gcd(m * n, h_rad) != 1 or m == n:
                continue
            for r in range(1, max_modulus + 1):
                if math.gcd(r, m * h_rad) != 1:
                    continue
                for s in range(1, max_modulus + 1):
                    if math.gcd(s, n * h_rad) != 1:
                        continue
                    compatible, j0, q = crt_class(h, m, n, r, s)
                    direct = [j for j in range(q)
                              if (m * j + h) % r == 0
                              and (n * j + h) % s == 0]
                    require(len(direct) == (1 if compatible else 0),
                            "crt-direct-cardinality",
                            h, m, n, r, s, direct)
                    checks += 2
                    tested_pairs += 1
                    if compatible:
                        require(j0 is not None and direct == [j0],
                                "crt-class-match", h, m, n, r, s)
                        compatible_count += 1
                        if math.gcd(r, s) > 1:
                            nontrivial_content += 1
                        if j0 == 0:
                            zero_class += 1
                        if h != h_rad:
                            nonsquarefree_shift += 1
                        horizons = (1, 2, max(1, q - 1), q, q + 1,
                                    2 * q + 3)
                        for horizon in horizons:
                            direct_window = sum(
                                1 for j in range(1, horizon + 1)
                                if (m * j + h) % r == 0
                                and (n * j + h) % s == 0)
                            formula_window = window_occupancy(
                                int(j0), q, horizon)
                            require(direct_window == formula_window,
                                    "crt-window-occupancy", h, m, n,
                                    r, s, horizon, direct_window,
                                    formula_window)
                            checks += 1
                    else:
                        incompatible_count += 1
    require(compatible_count > 0 and incompatible_count > 0,
            "crt-both-compatibility-types",
            compatible_count, incompatible_count)
    require(nontrivial_content > 0 and zero_class > 0,
            "crt-content-and-zero-class", nontrivial_content, zero_class)
    require(nonsquarefree_shift > 0,
            "crt-nonsquarefree-shift", nonsquarefree_shift)
    checks += 3
    return checks, {
        "max_modulus": max_modulus,
        "tested_modulus_pairs": tested_pairs,
        "compatible_pairs": compatible_count,
        "incompatible_pairs": incompatible_count,
        "nontrivial_content_pairs": nontrivial_content,
        "zero_residue_classes": zero_class,
        "nonsquarefree_shift_compatible_pairs": nonsquarefree_shift,
    }


def direct_incidence(h: int, m: int, n: int,
                     a_scale: int, b_scale: int, g_scale: int,
                     horizon: int) -> int:
    h_rad = radical(h)
    total = 0
    for j in range(1, horizon + 1):
        for r in range(a_scale + 1, 2 * a_scale + 1):
            if math.gcd(r, m * h_rad) != 1:
                continue
            if (m * j + h) % r != 0:
                continue
            for s in range(b_scale + 1, 2 * b_scale + 1):
                if math.gcd(s, n * h_rad) != 1:
                    continue
                d = math.gcd(r, s)
                if not in_content_cell(d, g_scale):
                    continue
                if (n * j + h) % s == 0:
                    total += 1
    return total


def in_content_cell(content: int, g_scale: int) -> bool:
    """Use the paper's closed base cell and half-open later cells."""
    require(content >= 1 and g_scale >= 1,
            "content-cell-domain", content, g_scale)
    if g_scale == 1:
        return 1 <= content <= 2
    return g_scale < content <= 2 * g_scale


def crt_incidence(h: int, m: int, n: int,
                  a_scale: int, b_scale: int, g_scale: int,
                  horizon: int) -> tuple[int, int, int]:
    h_rad = radical(h)
    total = 0
    compatible_pairs = 0
    incompatible_pairs = 0
    for r in range(a_scale + 1, 2 * a_scale + 1):
        if math.gcd(r, m * h_rad) != 1:
            continue
        for s in range(b_scale + 1, 2 * b_scale + 1):
            if math.gcd(s, n * h_rad) != 1:
                continue
            d = math.gcd(r, s)
            if not in_content_cell(d, g_scale):
                continue
            compatible, j0, q = crt_class(h, m, n, r, s)
            if compatible:
                compatible_pairs += 1
                require(j0 is not None, "incidence-class-present")
                total += window_occupancy(int(j0), q, horizon)
            else:
                incompatible_pairs += 1
    return total, compatible_pairs, incompatible_pairs


def check_incidence_inequality() -> tuple[int, dict[str, object]]:
    cases = ((1, 13, 17), (2, 17, 57),
             (6, 23, 145), (12, 23, 145))
    horizons = (1, 2, 5, 11, 23, 47)
    checks = 0
    cells = 0
    compatible_pairs = 0
    incompatible_pairs = 0
    nonzero_cells = 0
    max_ratio = Fraction(0)
    max_ratio_cell: dict[str, int | str] = {}
    for h, m, n in cases:
        require(m != n and math.gcd(m * n, radical(h)) == 1,
                "incidence-row-shape", h, m, n)
        h_det = abs(h * (m - n))
        for a_scale in range(2, 9):
            for b_scale in range(2, 9):
                for g_scale in range(1, min(a_scale, b_scale) + 1):
                    for horizon in horizons:
                        direct = direct_incidence(
                            h, m, n, a_scale, b_scale,
                            g_scale, horizon)
                        via_crt, comp, incomp = crt_incidence(
                            h, m, n, a_scale, b_scale,
                            g_scale, horizon)
                        require(direct == via_crt,
                                "incidence-direct-crt", h, m, n,
                                a_scale, b_scale, g_scale, horizon,
                                direct, via_crt)
                        checks += 1
                        cells += 1
                        compatible_pairs += comp
                        incompatible_pairs += incomp
                        if direct:
                            nonzero_cells += 1

                        d_max = max(
                            tau(m * j + h) * tau(n * j + h)
                            for j in range(1, horizon + 1))
                        c_arith = max(d_max, 9 * tau(h_det))
                        geometry = min(
                            Fraction(horizon),
                            Fraction(a_scale * b_scale,
                                     g_scale * g_scale)
                            + Fraction(horizon, g_scale),
                        )
                        bound = c_arith * geometry
                        require(Fraction(direct) <= bound,
                                "incidence-explicit-bound",
                                h, m, n, a_scale, b_scale,
                                g_scale, horizon, direct, bound,
                                c_arith)
                        checks += 1
                        ratio = (Fraction(direct, 1) / bound
                                 if bound else Fraction(0))
                        if ratio > max_ratio:
                            max_ratio = ratio
                            max_ratio_cell = {
                                "h": h, "m": m, "n": n,
                                "A": a_scale, "B": b_scale,
                                "G": g_scale, "J": horizon,
                                "count": direct,
                                "C_arith": c_arith,
                                "ratio": str(ratio),
                            }
    require(compatible_pairs > 0 and incompatible_pairs > 0,
            "incidence-compatibility-coverage",
            compatible_pairs, incompatible_pairs)
    require(nonzero_cells > 0 and max_ratio > 0,
            "incidence-nonzero-coverage", nonzero_cells, max_ratio)
    checks += 2
    return checks, {
        "cells": cells,
        "compatible_pair_occurrences": compatible_pairs,
        "incompatible_pair_occurrences": incompatible_pairs,
        "nonzero_cells": nonzero_cells,
        "maximum_normalized_ratio": str(max_ratio),
        "maximum_ratio_cell": max_ratio_cell,
        "finite_bound": (
            "N <= C_arith * min(J, A*B/G^2 + J/G), "
            "C_arith=max(max_j tau(N_m)tau(N_n),9tau(|h(m-n)|))"
        ),
    }


def check_long_fiber_bookkeeping() -> tuple[int, dict[str, int]]:
    cases = ((1, 13, 17), (2, 17, 57), (6, 23, 145))
    horizons = (5, 11, 23, 41)
    y_values = (3, 5, 8, 12)
    checks = 0
    cells = 0
    nonzero = 0
    for h, m, n in cases:
        h_rad = radical(h)
        for horizon in horizons:
            for y_cut in y_values:
                if y_cut > horizon:
                    continue
                for d_cut in range(0, y_cut):
                    direct = 0
                    via_crt = 0
                    for r in range(1, y_cut + 1):
                        if math.gcd(r, m * h_rad) != 1:
                            continue
                        for s in range(1, y_cut + 1):
                            if math.gcd(s, n * h_rad) != 1:
                                continue
                            d = math.gcd(r, s)
                            q = lcm(r, s)
                            if q > y_cut or d <= d_cut:
                                continue
                            a_part, b_part = r // d, s // d
                            require(math.gcd(a_part, b_part) == 1,
                                    "long-coprime-parts", r, s, d)
                            require(q == d * a_part * b_part,
                                    "long-lcm-factorization", r, s,
                                    d, q, a_part, b_part)
                            checks += 2
                            direct += sum(
                                1 for j in range(1, horizon + 1)
                                if (m * j + h) % r == 0
                                and (n * j + h) % s == 0)
                            compatible, j0, q_crt = crt_class(
                                h, m, n, r, s)
                            require(q_crt == q,
                                    "long-crt-modulus", q_crt, q)
                            checks += 1
                            if compatible:
                                require(j0 is not None,
                                        "long-class-present")
                                via_crt += window_occupancy(
                                    int(j0), q, horizon)
                    require(direct == via_crt,
                            "long-direct-crt", h, m, n, horizon,
                            y_cut, d_cut, direct, via_crt)
                    checks += 1
                    cells += 1
                    nonzero += int(direct > 0)
    require(nonzero > 0, "long-nonzero-coverage", nonzero)
    checks += 1
    return checks, {"cells": cells, "nonzero_cells": nonzero}


def positive_part(value: Fraction) -> Fraction:
    return max(Fraction(0), value)


def sparse_saving(beta: Fraction, a: Fraction,
                  b: Fraction, c: Fraction) -> Fraction:
    return positive_part(1 - beta - a - b + 2 * c)


def check_exponent_ledger() -> tuple[int, dict[str, object]]:
    checks = 0
    beta = Fraction(267, 400)
    a = Fraction(1, 4)
    b = Fraction(1, 4)
    c = Fraction(1, 10)
    j_exp = 1 - beta
    q_exp = a + b - c
    primitive_exp = a + b - 2 * c
    eta = sparse_saving(beta, a, b, c)
    require(j_exp == Fraction(133, 400),
            "high-J-exponent", j_exp)
    require(q_exp == Fraction(2, 5),
            "high-q-exponent", q_exp)
    require(primitive_exp == Fraction(3, 10),
            "high-primitive-exponent", primitive_exp)
    require(q_exp - j_exp == Fraction(27, 400) > 0,
            "high-sparse-margin", q_exp - j_exp)
    require(eta == Fraction(13, 400),
            "high-incidence-margin", eta)
    require(Fraction(1, 4) < Fraction(307, 500),
            "high-reflected-range")
    require(1 - Fraction(1, 4) > Fraction(193, 500),
            "high-ultra-quotient")
    require(min(Fraction(1, 10), beta) == Fraction(1, 10),
            "high-long-content-saving")
    checks += 8

    grid_points = 0
    beta_values = (Fraction(1, 2), Fraction(3, 5), beta,
                   Fraction(3, 4))
    values = tuple(Fraction(k, 20) for k in range(0, 13))
    for beta_value in beta_values:
        j_value = 1 - beta_value
        for a_value in values:
            for b_value in values:
                for c_value in values:
                    if c_value > min(a_value, b_value):
                        continue
                    expected = positive_part(
                        j_value - (a_value + b_value - 2 * c_value))
                    actual = sparse_saving(
                        beta_value, a_value, b_value, c_value)
                    require(actual == expected,
                            "sparse-grid-formula", beta_value,
                            a_value, b_value, c_value, actual, expected)
                    if a_value + b_value - c_value >= j_value:
                        require(actual == positive_part(
                            j_value - a_value - b_value + 2 * c_value),
                            "sparse-grid-sparse-region", beta_value,
                            a_value, b_value, c_value, actual)
                        checks += 1
                    checks += 1
                    grid_points += 1

    boundary_cases = (
        (Fraction(3, 5), Fraction(1, 5), Fraction(1, 5),
         Fraction(0), Fraction(0)),
        (Fraction(3, 5), Fraction(3, 10), Fraction(3, 10),
         Fraction(0), Fraction(0)),
        (Fraction(3, 5), Fraction(1, 5), Fraction(1, 5),
         Fraction(1, 10), Fraction(1, 5)),
    )
    for beta_value, a_value, b_value, c_value, expected in boundary_cases:
        actual = sparse_saving(beta_value, a_value, b_value, c_value)
        require(actual == expected, "sparse-boundary-case",
                beta_value, a_value, b_value, c_value, actual, expected)
        checks += 1
    return checks, {
        "beta": str(beta),
        "J_exponent": str(j_exp),
        "A_exponent": str(a),
        "B_exponent": str(b),
        "G_exponent": str(c),
        "lcm_exponent": str(q_exp),
        "primitive_lcm_exponent": str(primitive_exp),
        "sparse_margin": str(q_exp - j_exp),
        "incidence_margin": str(eta),
        "long_content_cutoff_exponent": "1/10",
        "long_content_saving": "1/10",
        "grid_points": grid_points,
    }


def main() -> None:
    checks = 0
    subcounts: dict[str, int] = {}

    count, prefix_cases = check_calibrated_difference()
    checks += count
    subcounts["calibrated_cutoff_and_five_term"] = count

    count, crt_summary = check_crt_fibers()
    checks += count
    subcounts["crt_fibers"] = count

    count, incidence_summary = check_incidence_inequality()
    checks += count
    subcounts["explicit_constant_incidence"] = count

    count, long_summary = check_long_fiber_bookkeeping()
    checks += count
    subcounts["long_fiber_bookkeeping"] = count

    count, exponent_summary = check_exponent_ledger()
    checks += count
    subcounts["rational_exponent_ledger"] = count

    source_path = Path(__file__)
    source_bytes = source_path.read_bytes()
    normalized_source = source_bytes.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")
    source_hash = hashlib.sha256(normalized_source).hexdigest()
    claims = {
        "finite_calibrated_cutoff_identity": True,
        "finite_crt_fiber_identity": True,
        "finite_explicit_constant_incidence_bound": True,
        "finite_long_fiber_bookkeeping": True,
        "finite_rational_exponent_ledger": True,
        "uses_chowla_or_elliott_input": False,
        "closes_primitive_sparse_core": False,
        "closes_dense_small_content_core": False,
        "closes_complete_ultra_difference": False,
        "closes_complete_residual": False,
        "proves_positivity": False,
        "proves_hardy_littlewood_asymptotic": False,
        "proves_twin_primes": False,
        "breaks_sieve_parity": False,
    }
    for name, value in claims.items():
        if name.startswith("finite_"):
            require(value is True, "positive-scope-flag", name, value)
        else:
            require(value is False, "negative-scope-flag", name, value)
        checks += 1
    subcounts["scope_flags"] = len(claims)

    payload = {
        "paper": "TPC-29",
        "certificate": "content-rich reflected-fiber incidence",
        "description": (
            "finite exact regression for CRT, calibrated-prefix algebra, "
            "long-fiber bookkeeping, rational exponents, and an "
            "explicit-constant incidence inequality; not a numerical "
            "proof of an asymptotic Mobius estimate"
        ),
        "exact_check_count": checks,
        "subcheck_counts": subcounts,
        "calibrated_prefix_cases": prefix_cases,
        "crt_summary": crt_summary,
        "incidence_summary": incidence_summary,
        "long_fiber_summary": long_summary,
        "high_beta_exponent_summary": exponent_summary,
        "claims": claims,
        "source_sha256": source_hash,
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
