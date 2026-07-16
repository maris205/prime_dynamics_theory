#!/usr/bin/env python3
"""Exact structural certificate for TPC-25.

The script uses only the Python standard library and ``Fraction``.
Logarithms are formal variables: a polynomial is a dictionary whose
monomial is a tuple of primes.  The checks concern finite identities,
matrix ranges, and rational exponent bookkeeping.  They are not
numerical evidence for a Mobius-shell asymptotic or for twin primes.
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
    for p, exponent in factor(n).items():
        out = [d * p**j for d in out for j in range(exponent + 1)]
    return sorted(out)


def mobius(n: int) -> int:
    fs = factor(n)
    if any(exponent > 1 for exponent in fs.values()):
        return 0
    return -1 if len(fs) % 2 else 1


def phi(n: int) -> int:
    out = n
    for p in factor(n):
        out = out // p * (p - 1)
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


def clean(poly: defaultdict[tuple[int, ...], Fraction] | Poly) -> Poly:
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def add(*polys: Poly) -> Poly:
    out: defaultdict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] += coefficient
    return clean(out)


def scale(poly: Poly, scalar: int | Fraction) -> Poly:
    q = Fraction(scalar)
    return clean({monomial: q * coefficient
                  for monomial, coefficient in poly.items()})


def multiply(left: Poly, right: Poly) -> Poly:
    out: defaultdict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(sorted(monomial_left + monomial_right))
            out[monomial] += coefficient_left * coefficient_right
    return clean(out)


def constant(value: int | Fraction) -> Poly:
    q = Fraction(value)
    return {} if q == 0 else {(): q}


def formal_log(n: int) -> Poly:
    return {(p,): Fraction(exponent) for p, exponent in factor(n).items()}


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


def zero_direct(r_cut: int, s_cut: int, t_cut: int,
                m: int, n: int, h_rad: int) -> Poly:
    out: Poly = {}
    delta = m - n
    for u in range(1, s_cut + 1):
        if math.gcd(u, m * h_rad) != 1:
            continue
        for v in range(s_cut + 1, t_cut + 1):
            if math.gcd(v, n * h_rad) != 1:
                continue
            g = math.gcd(u, v)
            if delta % g:
                continue
            term = multiply(b_poly(r_cut, u), a_poly(v))
            out = add(out, scale(term, Fraction(g, u * v)))
    return out


def omega(r_cut: int, s_cut: int, t_cut: int,
          g: int, h_rad: int) -> Poly:
    if mobius(g) == 0 or math.gcd(g, h_rad) != 1:
        return {}
    out: Poly = {}
    for c in range(1, s_cut // g + 1):
        if math.gcd(g * c, h_rad) != 1:
            continue
        for d in range(s_cut // g + 1, t_cut // g + 1):
            if not (s_cut < g * d <= t_cut):
                continue
            if math.gcd(d, g * c * h_rad) != 1:
                continue
            term = multiply(b_poly(r_cut, g * c), a_poly(g * d))
            out = add(out, scale(term, Fraction(1, g * c * d)))
    return out


def zero_skeleton(r_cut: int, s_cut: int, t_cut: int,
                  m: int, n: int, h_rad: int) -> Poly:
    if m == n:
        return {}
    out: Poly = {}
    for g in range(1, s_cut + 1):
        if (m - n) % g == 0:
            out = add(out, omega(r_cut, s_cut, t_cut, g, h_rad))
    return out


def matrix_rank(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    a = [[Fraction(value) for value in row] for row in matrix]
    rows = len(a)
    cols = len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if a[row][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pivot_value = a[rank][col]
        a[rank] = [value / pivot_value for value in a[rank]]
        for row in range(rows):
            if row == rank or not a[row][col]:
                continue
            multiplier = a[row][col]
            a[row] = [a[row][j] - multiplier * a[rank][j]
                      for j in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def congruence_matrix(rows: list[int], g: int) -> list[list[int]]:
    return [[int((m - n) % g == 0) for n in rows] for m in rows]


def poly_matvec(matrix: list[list[Poly]], vector: list[int]) -> list[Poly]:
    out: list[Poly] = []
    for row in matrix:
        value: Poly = {}
        for entry, coefficient in zip(row, vector):
            value = add(value, scale(entry, coefficient))
        out.append(value)
    return out


def check_kernel_case(r_cut: int, s_cut: int, t_cut: int,
                      h_rad: int, rows: list[int]) -> int:
    checks = 0
    if not all(is_prime(row) and row > t_cut
               and math.gcd(row, h_rad) == 1 for row in rows):
        raise AssertionError(("invalid prime-row test case", h_rad, rows))
    for m in rows:
        for n in rows:
            if m == n:
                continue
            direct = zero_direct(r_cut, s_cut, t_cut, m, n, h_rad)
            skeleton = zero_skeleton(r_cut, s_cut, t_cut, m, n, h_rad)
            if direct != skeleton:
                raise AssertionError(("kernel skeleton", r_cut, s_cut,
                                      t_cut, h_rad, m, n, direct, skeleton))
            checks += 1

    for g in range(1, s_cut + 1):
        a_g = congruence_matrix(rows, g)
        rank = matrix_rank(a_g)
        occupied = len({row % g for row in rows})
        if rank != occupied or rank > min(g, len(rows)):
            raise AssertionError(("congruence rank", g, rank, occupied))
        checks += 1
    return checks


def check_constant_mode() -> tuple[int, Poly]:
    rows = [5, 7, 11, 13, 17]
    expected: Poly = {(2, 3): Fraction(1, 6), (3,): Fraction(-1, 3)}
    matrix: list[list[Poly]] = []
    checks = 0
    for m in rows:
        matrix_row: list[Poly] = []
        for n in rows:
            value = {} if m == n else zero_direct(2, 2, 3, m, n, 1)
            if m != n and value != expected:
                raise AssertionError(("constant kernel", m, n, value, expected))
            matrix_row.append(value)
            checks += 1
        matrix.append(matrix_row)

    ones = [1] * len(rows)
    contrast = [1, -1] + [0] * (len(rows) - 2)
    row_mode = poly_matvec(matrix, ones)
    contrast_mode = poly_matvec(matrix, contrast)
    for value in row_mode:
        if value != scale(expected, len(rows) - 1):
            raise AssertionError(("principal eigenvector", value))
        checks += 1
    for value, coefficient in zip(contrast_mode, contrast):
        if value != scale(expected, -coefficient):
            raise AssertionError(("contrast eigenvector", value, coefficient))
        checks += 1
    return checks, expected


def check_soft_interface_saturation() -> int:
    # Finite rational model: N=Q=5, rho=1/16, x=y=1/sqrt(rho)=4.
    n = 5
    q = 5
    rho = Fraction(1, 16)
    x = [Fraction(4)] * n
    bilinear = sum((x[i] * rho * x[j]
                    for i in range(n) for j in range(n) if i != j),
                   Fraction(0))
    expected = Fraction(q * q * (n - 1), n)
    if bilinear != expected:
        raise AssertionError(("soft saturation", bilinear, expected))
    energy = sum((value * value for value in x), Fraction(0))
    if energy != Fraction(q, rho):
        raise AssertionError(("soft energy", energy, Fraction(q, rho)))
    return 2


def check_exponent_sample() -> int:
    delta = Fraction(3, 20)
    beta = Fraction(31, 50)
    xi = Fraction(1, 25)
    entries = (
        1 - Fraction(3, 2) * beta,
        (beta + 4 * delta - 1) / 2 - xi,
        (6 * delta - beta - 5 * xi) / 4,
    )
    if entries != (Fraction(7, 100), Fraction(7, 100), Fraction(1, 50)):
        raise AssertionError(("exponent sample", entries))
    if not (Fraction(1, 2) + delta - beta < xi):
        raise AssertionError("sample does not cross T=J")
    return 2


def serialize_poly(poly: Poly) -> dict[str, str]:
    return {
        "1" if not monomial else "*".join(f"log({p})" for p in monomial):
        str(coefficient)
        for monomial, coefficient in sorted(poly.items())
    }


def main() -> None:
    checks = 0
    constant_checks, exact_constant = check_constant_mode()
    checks += constant_checks
    cases = (
        (5, 5, 9, 1, [11, 13, 17, 19, 23]),
        (7, 7, 14, 2, [17, 19, 23, 29, 31]),
        (8, 8, 15, 6, [17, 19, 23, 29, 31]),
    )
    case_counts = []
    for r_cut, s_cut, t_cut, h_rad, rows in cases:
        count = check_kernel_case(r_cut, s_cut, t_cut, h_rad, rows)
        checks += count
        case_counts.append(count)
    checks += check_soft_interface_saturation()
    checks += check_exponent_sample()

    source_path = Path(__file__)
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    payload = {
        "paper": "TPC-25",
        "certificate": "zero-before-separation and principal-row-mode",
        "exact_check_count": checks,
        "kernel_case_check_counts": case_counts,
        "constant_kernel": serialize_poly(exact_constant),
        "constant_matrix_size": 5,
        "abstract_saturation": {
            "N": 5,
            "Q": 5,
            "rho": "1/16",
            "bilinear": "20",
        },
        "source_sha256": source_hash,
        "claims": {
            "finite_kernel_identity": True,
            "congruence_skeleton": True,
            "principal_mode_present": True,
            "asymptotic_mobius_evidence": False,
            "full_residual_closure": False,
            "hardy_littlewood": False,
            "twin_primes": False,
            "general_parity_breakthrough": False,
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_digest"] = hashlib.sha256(canonical.encode()).hexdigest()
    output_path = source_path.with_suffix(".json")
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
