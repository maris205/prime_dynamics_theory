#!/usr/bin/env python3
"""Deterministic finite certificate for the TPC-17 algebraic ledgers."""

from __future__ import annotations

import argparse
import cmath
import json
import math
from fractions import Fraction
from pathlib import Path


def solve_two_by_two(a, b, c, d, e, f):
    """Solve ax+by=e, cx+dy=f exactly over the rationals."""
    det = a * d - b * c
    return Fraction(e * d - b * f, det), Fraction(a * f - e * c, det)


def mobius(n: int) -> int:
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


def divisors(n: int):
    return [d for d in range(1, n + 1) if n % d == 0]


def finite_fourier_certificate():
    coeffs = {
        (2, 1): 2.0,
        (2, 2): -1.0,
        (3, 1): 3.0,
        (4, 3): 1.5,
    }
    n_l, n_k = 19, 17
    energy = sum(abs(value) ** 2 for value in coeffs.values())
    sampled = 0.0
    for a in range(n_l):
        for b in range(n_k):
            value = sum(
                coefficient
                * cmath.exp(2j * math.pi * (a * ell / n_l + b * k / n_k))
                for (ell, k), coefficient in coeffs.items()
            )
            sampled += abs(value) ** 2
    sampled /= n_l * n_k

    row_sums = {}
    for (ell, k), value in coeffs.items():
        row_sums[k] = row_sums.get(k, 0.0) + value
    ttstar_left = sum(abs(value) ** 2 for value in row_sums.values())
    off = 0.0
    for (ell_1, k_1), value_1 in coeffs.items():
        for (ell_2, k_2), value_2 in coeffs.items():
            if k_1 == k_2 and ell_1 != ell_2:
                off += value_1 * value_2

    return {
        "coefficient_energy": energy,
        "nyquist_average": sampled,
        "nyquist_absolute_error": abs(sampled - energy),
        "ttstar_left": ttstar_left,
        "ttstar_diagonal_plus_off": energy + off,
        "ttstar_absolute_error": abs(ttstar_left - energy - off),
    }


def build_certificate():
    maynard_lambda, maynard_nu = solve_two_by_two(2, 1, 19, 20, 1, 10)
    li_lambda, li_nu = solve_two_by_two(2, 1, 7, 12, 1, 4)

    sigma = Fraction(1, 2000)
    delta = Fraction(1, 20)

    prefix_tail_ok = True
    v, d0 = 20, 7
    for k in range(1, 301):
        beta_v = sum(mobius(d) for d in divisors(k) if d <= v)
        beta_prefix = sum(mobius(d) for d in divisors(k) if d <= d0)
        beta_tail = sum(mobius(d) for d in divisors(k) if d0 < d <= v)
        prefix_tail_ok &= beta_v == beta_prefix + beta_tail

    fourier = finite_fourier_certificate()

    exact = {
        "maynard_vertex": [str(maynard_lambda), str(maynard_nu)],
        "maynard_total_modulus": str(maynard_lambda + maynard_nu),
        "maynard_second_face_value": str(7 * maynard_lambda + 12 * maynard_nu),
        "li_vertex": [str(li_lambda), str(li_nu)],
        "li_total_modulus": str(li_lambda + li_nu),
        "li_deleted_third_face_value": str(19 * li_lambda + 20 * li_nu),
        "vertex_total_gap": str((li_lambda + li_nu) - (maynard_lambda + maynard_nu)),
        "published_monomials_at_sigma": [
            str(1 - 3 * sigma),
            str(Fraction(82, 21) - 19 * sigma),
            str(10 - 39 * sigma),
        ],
        "li_monomials_at_sigma": [
            str(1 - Fraction(3, 2) * sigma),
            str(4 - sigma),
        ],
        "published_delta_lower": str(Fraction(1, 42) + 3 * sigma),
        "li_delta_lower": str(Fraction(1, 34) + 2 * sigma),
        "chosen_delta": str(delta),
    }

    checks = {
        "maynard_vertex_exact": (maynard_lambda, maynard_nu)
        == (Fraction(10, 21), Fraction(1, 21)),
        "maynard_second_face_strict": 7 * maynard_lambda + 12 * maynard_nu < 4,
        "li_vertex_exact": (li_lambda, li_nu)
        == (Fraction(8, 17), Fraction(1, 17)),
        "li_vertex_outside_maynard_third": 19 * li_lambda + 20 * li_nu > 10,
        "li_total_exceeds_published_total": li_lambda + li_nu
        > maynard_lambda + maynard_nu,
        "prefix_tail_identity_k_le_300": prefix_tail_ok,
        "published_sample_delta_admissible": Fraction(1, 42) + 3 * sigma
        < delta < Fraction(1, 4),
        "li_sample_delta_admissible": Fraction(1, 34) + 2 * sigma
        < delta < Fraction(1, 4),
        "nyquist_parseval": fourier["nyquist_absolute_error"] < 1e-10,
        "ttstar_identity": fourier["ttstar_absolute_error"] < 1e-12,
    }

    return {
        "paper": "TPC-17",
        "description": "Exact exponent, prefix-tail, Nyquist, and TT* checks",
        "parameters": {"sigma": str(sigma), "delta": str(delta)},
        "exact_arithmetic": exact,
        "finite_fourier": fourier,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    rendered = json.dumps(certificate, indent=2, sort_keys=True)
    print(rendered)
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    raise SystemExit(0 if certificate["all_checks_passed"] else 1)


if __name__ == "__main__":
    main()
