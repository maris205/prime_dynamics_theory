#!/usr/bin/env python3
"""Exact finite certificate for TPC-30.

The certificate uses only the Python standard library.  It checks the
primitive target-gcd identity, exact target-content layers and their
window occupancy, the fixed-row large-content bound, the exact
four-factor target-gcd decomposition, a finite row-residue energy
inequality with explicit constants, and the rational high-beta
ledger.  It is a regression certificate for finite algebra and
bookkeeping; it is not numerical evidence for an asymptotic Mobius
estimate, a prime-pair main term, or twin primes.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


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
    require(n >= 1, "divisors-positive", n)
    out = [1]
    for p, exponent in factor(n).items():
        powers = [p**e for e in range(exponent + 1)]
        out = [d * power for d in out for power in powers]
    return sorted(out)


def mobius(n: int) -> int:
    fac = factor(n)
    if any(exponent > 1 for exponent in fac.values()):
        return 0
    return -1 if len(fac) % 2 else 1


def tau(n: int) -> int:
    require(n >= 1, "tau-positive", n)
    out = 1
    for exponent in factor(n).values():
        out *= exponent + 1
    return out


def ceil_div(numerator: int, denominator: int) -> int:
    require(numerator >= 0 and denominator >= 1,
            "ceil-div-domain", numerator, denominator)
    return (numerator + denominator - 1) // denominator


def target(row: int, h: int, j: int) -> int:
    value = row * j + h
    require(value > 0, "positive-affine-target", row, h, j, value)
    return value


def target_content(m: int, n: int, h: int, j: int) -> int:
    return math.gcd(target(m, h, j), target(n, h, j))


def check_target_gcd_identity() -> tuple[int, dict[str, object]]:
    checks = 0
    cases = 0
    nontrivial = 0
    maximum_content = 1
    for h in range(1, 13):
        for m in range(1, 29):
            if math.gcd(m, h) != 1:
                continue
            for n in range(1, 29):
                if n == m or math.gcd(n, h) != 1:
                    continue
                delta = abs(m - n)
                for j in range(1, 49):
                    if math.gcd(j, h) != 1:
                        continue
                    left = target_content(m, n, h, j)
                    right = math.gcd(target(m, h, j), delta)
                    require(left == right, "target-gcd-identity",
                            h, m, n, j, left, right)
                    require(delta % left == 0,
                            "target-content-divides-row-difference",
                            h, m, n, j, left, delta)
                    require(math.gcd(left, m * n) == 1,
                            "target-content-coprime-to-rows",
                            h, m, n, j, left)
                    checks += 3
                    cases += 1
                    if left > 1:
                        nontrivial += 1
                    maximum_content = max(maximum_content, left)

    # The primitive-orbit hypothesis is substantive, rather than a
    # decoration: dropping gcd(j,h)=1 can destroy the displayed identity.
    witness = {"h": 2, "m": 1, "n": 3, "j": 2}
    witness_left = target_content(**witness)
    witness_right = math.gcd(
        target(witness["m"], witness["h"], witness["j"]),
        abs(witness["m"] - witness["n"]),
    )
    require(math.gcd(witness["j"], witness["h"]) > 1,
            "nonprimitive-witness-domain", witness)
    require(witness_left != witness_right,
            "nonprimitive-witness-fails-identity",
            witness, witness_left, witness_right)
    checks += 2
    return checks, {
        "primitive_cases": cases,
        "nontrivial_target_contents": nontrivial,
        "maximum_target_content": maximum_content,
        "nonprimitive_boundary_witness": {
            **witness,
            "left_gcd": witness_left,
            "right_gcd": witness_right,
        },
    }


def primitive_congruence_count(
        m: int, h: int, modulus: int, horizon: int) -> int:
    require(modulus >= 1 and horizon >= 0,
            "congruence-count-domain", modulus, horizon)
    return sum(
        1 for j in range(1, horizon + 1)
        if math.gcd(j, h) == 1 and target(m, h, j) % modulus == 0
    )


def residue_occupancy(residue: int, modulus: int, horizon: int) -> int:
    require(modulus >= 1 and 0 <= residue < modulus and horizon >= 0,
            "residue-occupancy-domain", residue, modulus, horizon)
    return sum(1 for j in range(1, horizon + 1)
               if j % modulus == residue)


def check_exact_content_occupancy() -> tuple[int, dict[str, object]]:
    row_cases = (
        (1, 5, 11), (1, 11, 29), (1, 13, 37),
        (2, 5, 17), (2, 11, 29),
        (6, 5, 17), (6, 7, 31),
        (12, 5, 29), (12, 7, 31),
    )
    horizons = (1, 2, 7, 19, 43, 79, 128)
    checks = 0
    layers = 0
    nonzero_layers = 0
    strict_exact_subsets = 0
    max_exact_count = 0
    for h, m, n in row_cases:
        require(m != n and math.gcd(m * n, h) == 1,
                "exact-layer-row-domain", h, m, n)
        delta = abs(m - n)
        for horizon in horizons:
            primitive_points = [
                j for j in range(1, horizon + 1)
                if math.gcd(j, h) == 1
            ]
            partition_total = 0
            for c in divisors(delta):
                exact_points = [
                    j for j in primitive_points
                    if target_content(m, n, h, j) == c
                ]
                exact_count = len(exact_points)
                partition_total += exact_count

                # Indicator Möbius inversion:
                # 1_{gcd(N_m,Delta)=c} =
                # sum_{d|Delta/c} mu(d) 1_{cd|N_m}.
                inverted = sum(
                    mobius(d) * primitive_congruence_count(
                        m, h, c * d, horizon)
                    for d in divisors(delta // c)
                )
                require(exact_count == inverted,
                        "exact-content-mobius-inversion",
                        h, m, n, horizon, c, exact_count, inverted)

                congruence_count = primitive_congruence_count(
                    m, h, c, horizon)
                require(exact_count <= congruence_count,
                        "exact-layer-subset-of-c-congruence",
                        h, m, n, horizon, c,
                        exact_count, congruence_count)
                require(Fraction(exact_count, 1)
                        <= 1 + Fraction(horizon, c),
                        "exact-c-window-bound",
                        h, m, n, horizon, c, exact_count)
                checks += 3
                layers += 1
                if exact_count:
                    nonzero_layers += 1
                    require(math.gcd(m, c) == 1,
                            "occupied-layer-invertible-row",
                            h, m, n, horizon, c)
                    residue = (-h * pow(m, -1, c)) % c if c > 1 else 0
                    unfiltered_occupancy = residue_occupancy(
                        residue, c, horizon)
                    require(congruence_count <= unfiltered_occupancy,
                            "primitive-occupancy-below-residue-occupancy",
                            h, m, n, horizon, c, residue,
                            congruence_count, unfiltered_occupancy)
                    require(unfiltered_occupancy <= ceil_div(horizon, c),
                            "single-residue-ceiling",
                            h, m, n, horizon, c, residue,
                            unfiltered_occupancy)
                    require(all(j % c == residue for j in exact_points),
                            "exact-layer-single-residue",
                            h, m, n, horizon, c, residue, exact_points)
                    checks += 4
                if exact_count < congruence_count:
                    strict_exact_subsets += 1
                max_exact_count = max(max_exact_count, exact_count)
            require(partition_total == len(primitive_points),
                    "exact-content-partition",
                    h, m, n, horizon,
                    partition_total, len(primitive_points))
            checks += 1

    require(nonzero_layers > 0 and strict_exact_subsets > 0,
            "exact-layer-coverage", nonzero_layers, strict_exact_subsets)
    checks += 1
    return checks, {
        "row_cases": len(row_cases),
        "horizons_per_case": len(horizons),
        "exact_layers": layers,
        "nonzero_layers": nonzero_layers,
        "strict_subsets_of_divisibility_class": strict_exact_subsets,
        "maximum_exact_layer_count": max_exact_count,
        "verified_window_bound": "#exact_c <= 1 + J/c",
        "verified_exact_formula": (
            "#exact_c = sum_{d|Delta/c} mu(d) #primitive{cd|N_m(j)}"
        ),
    }


def check_fixed_row_large_content() -> tuple[int, dict[str, object]]:
    row_cases = (
        (1, 5, 11), (1, 11, 29), (1, 13, 37),
        (2, 5, 17), (2, 11, 29),
        (6, 5, 17), (6, 7, 31),
        (12, 5, 29), (12, 7, 31),
    )
    horizons = (1, 2, 7, 19, 43, 79, 128)
    thresholds = (
        Fraction(1), Fraction(2), Fraction(5, 2), Fraction(3),
        Fraction(5), Fraction(7), Fraction(11), Fraction(19),
        Fraction(37),
    )
    checks = 0
    cells = 0
    nonzero_cells = 0
    maximum_ratio = Fraction(0)
    maximum_case: dict[str, int | str] = {}
    for h, m, n in row_cases:
        require(m != n and math.gcd(m * n, h) == 1,
                "fixed-row-domain", h, m, n)
        delta = abs(m - n)
        delta_divisors = divisors(delta)
        for horizon in horizons:
            primitive_points = tuple(
                j for j in range(1, horizon + 1)
                if math.gcd(j, h) == 1
            )
            for threshold in thresholds:
                direct = sum(
                    1 for j in primitive_points
                    if target_content(m, n, h, j) > threshold
                )
                by_exact_layers = sum(
                    1 for c in delta_divisors if c > threshold
                    for j in primitive_points
                    if target_content(m, n, h, j) == c
                )
                require(direct == by_exact_layers,
                        "large-content-exact-layer-partition",
                        h, m, n, horizon, threshold,
                        direct, by_exact_layers)

                bound = tau(delta) * (
                    1 + Fraction(horizon, 1) / threshold)
                require(Fraction(direct, 1) <= bound,
                        "fixed-row-large-content-bound",
                        h, m, n, horizon, threshold,
                        direct, bound, tau(delta))
                checks += 2
                cells += 1
                if direct:
                    nonzero_cells += 1
                ratio = (Fraction(direct, 1) / bound
                         if bound else Fraction(0))
                if ratio > maximum_ratio:
                    maximum_ratio = ratio
                    maximum_case = {
                        "h": h, "m": m, "n": n,
                        "Delta": delta, "tau_Delta": tau(delta),
                        "J": horizon, "Z": str(threshold),
                        "count": direct, "bound": str(bound),
                    }

    require(nonzero_cells > 0 and maximum_ratio > 0,
            "fixed-row-large-content-coverage",
            nonzero_cells, maximum_ratio)
    checks += 1
    return checks, {
        "cells": cells,
        "nonzero_cells": nonzero_cells,
        "maximum_normalized_ratio": str(maximum_ratio),
        "maximum_ratio_case": maximum_case,
        "verified_bound": (
            "#primitive{j<=J:G_j>Z} <= tau(|m-n|)(1+J/Z)"
        ),
    }


def check_exact_four_factor_decomposition() -> tuple[int, dict[str, object]]:
    cases = (
        (1, 5, 11, 1), (1, 11, 29, 2),
        (1, 29, 41, 1), (2, 5, 17, 3),
        (6, 5, 17, 5), (6, 7, 31, 7),
        (12, 5, 29, 5),
    )
    checks = 0
    complete_factor_box_side = 16
    complete_factor_quadruples = 0
    complete_box_nontrivial_cross = 0
    for r, s, u, v in itertools.product(
            range(1, complete_factor_box_side + 1), repeat=4):
        reflected = math.gcd(r, s)
        quotient = math.gcd(u, v)
        r0, s0 = r // reflected, s // reflected
        u0, v0 = u // quotient, v // quotient
        left_cross = math.gcd(r0, v0)
        right_cross = math.gcd(s0, u0)
        exact_four_factor = (
            reflected * quotient * left_cross * right_cross
        )
        require(math.gcd(r0, s0) == math.gcd(u0, v0) == 1,
                "complete-box-primitive-pairs",
                r, s, u, v, r0, s0, u0, v0)
        require(math.gcd(left_cross, right_cross) == 1,
                "complete-box-cross-couplings-coprime",
                r, s, u, v, left_cross, right_cross)
        require(math.gcd(r * u, s * v) == exact_four_factor,
                "complete-box-four-factor-equality",
                r, s, u, v, exact_four_factor,
                math.gcd(r * u, s * v))
        checks += 3
        complete_factor_quadruples += 1
        if left_cross > 1 or right_cross > 1:
            complete_box_nontrivial_cross += 1

    factorizations = 0
    coprime_reflected_with_quotient_content = 0
    nontrivial_left_cross_couplings = 0
    nontrivial_right_cross_couplings = 0
    both_cross_couplings_nontrivial = 0
    maximum_cross_content = 1
    sample: dict[str, int] | None = None
    for h, m, n, j in cases:
        require(math.gcd(j, h) == 1 and math.gcd(m * n, h) == 1,
                "cross-content-primitive-domain", h, m, n, j)
        nm = target(m, h, j)
        nn = target(n, h, j)
        common = target_content(m, n, h, j)
        for r in divisors(nm):
            u = nm // r
            for s in divisors(nn):
                v = nn // s
                reflected = math.gcd(r, s)
                quotient = math.gcd(u, v)
                r0, s0 = r // reflected, s // reflected
                u0, v0 = u // quotient, v // quotient
                left_cross = math.gcd(r0, v0)
                right_cross = math.gcd(s0, u0)
                cross = reflected * quotient
                exact_four_factor = (
                    reflected * quotient * left_cross * right_cross
                )
                require(nm == r * u and nn == s * v,
                        "cross-factorization", h, m, n, j, r, s, u, v)
                require(common % cross == 0,
                        "cross-content-divides-target-content",
                        h, m, n, j, r, s, u, v,
                        reflected, quotient, cross, common)
                require(abs(m - n) % cross == 0,
                        "cross-content-divides-row-difference",
                        h, m, n, j, cross, abs(m - n))
                require(math.gcd(r0, s0) == 1
                        and math.gcd(u0, v0) == 1,
                        "primitive-four-factor-pairs",
                        r, s, u, v, reflected, quotient,
                        r0, s0, u0, v0)
                require(math.gcd(left_cross, right_cross) == 1,
                        "cross-couplings-coprime",
                        r0, s0, u0, v0, left_cross, right_cross)
                require(common == exact_four_factor,
                        "exact-four-factor-target-gcd",
                        h, m, n, j, r, s, u, v,
                        reflected, quotient, r0, s0, u0, v0,
                        left_cross, right_cross,
                        exact_four_factor, common)
                checks += 6
                factorizations += 1
                maximum_cross_content = max(
                    maximum_cross_content, exact_four_factor)
                if left_cross > 1:
                    nontrivial_left_cross_couplings += 1
                if right_cross > 1:
                    nontrivial_right_cross_couplings += 1
                if left_cross > 1 and right_cross > 1:
                    both_cross_couplings_nontrivial += 1
                if reflected == 1 and quotient > 1:
                    coprime_reflected_with_quotient_content += 1
                    if sample is None or quotient > sample["quotient_gcd"]:
                        sample = {
                            "h": h, "m": m, "n": n, "j": j,
                            "N_m": nm, "N_n": nn,
                            "r": r, "s": s, "U": u, "V": v,
                            "reflected_gcd": reflected,
                            "quotient_gcd": quotient,
                            "left_cross_gcd": left_cross,
                            "right_cross_gcd": right_cross,
                            "base_cross_content": cross,
                            "exact_four_factor_content": exact_four_factor,
                            "target_gcd": common,
                        }

    # A transparent witness for the genuinely new geometric sector.
    witness = {
        "h": 1, "m": 29, "n": 41, "j": 1,
        "r": 5, "s": 7, "U": 6, "V": 6,
    }
    require(witness["r"] * witness["U"]
            == target(witness["m"], witness["h"], witness["j"]),
            "explicit-cross-witness-left", witness)
    require(witness["s"] * witness["V"]
            == target(witness["n"], witness["h"], witness["j"]),
            "explicit-cross-witness-right", witness)
    require(math.gcd(witness["r"], witness["s"]) == 1
            and math.gcd(witness["U"], witness["V"]) == 6,
            "explicit-cross-witness-nonoverlap", witness)
    require(target_content(witness["m"], witness["n"],
                           witness["h"], witness["j"]) == 6,
            "explicit-cross-witness-target-content", witness)
    four_factor_witness = {
        "h": 1, "m": 5, "n": 11, "j": 1,
        "r": 3, "s": 4, "U": 2, "V": 3,
    }
    four_reflected = math.gcd(
        four_factor_witness["r"], four_factor_witness["s"])
    four_quotient = math.gcd(
        four_factor_witness["U"], four_factor_witness["V"])
    four_r0 = four_factor_witness["r"] // four_reflected
    four_s0 = four_factor_witness["s"] // four_reflected
    four_u0 = four_factor_witness["U"] // four_quotient
    four_v0 = four_factor_witness["V"] // four_quotient
    four_left = math.gcd(four_r0, four_v0)
    four_right = math.gcd(four_s0, four_u0)
    require(four_reflected == four_quotient == 1,
            "four-factor-witness-base-contents-coprime",
            four_factor_witness)
    require(four_left == 3 and four_right == 2,
            "four-factor-witness-cross-couplings",
            four_factor_witness, four_left, four_right)
    require(target_content(
        four_factor_witness["m"], four_factor_witness["n"],
        four_factor_witness["h"], four_factor_witness["j"])
        == four_reflected * four_quotient * four_left * four_right == 6,
        "four-factor-witness-exact-equality", four_factor_witness)
    require(coprime_reflected_with_quotient_content > 0 and sample is not None,
            "cross-content-coprime-reflected-coverage",
            coprime_reflected_with_quotient_content)
    require(nontrivial_left_cross_couplings > 0
            and nontrivial_right_cross_couplings > 0
            and both_cross_couplings_nontrivial > 0,
            "four-factor-cross-coupling-coverage",
            nontrivial_left_cross_couplings,
            nontrivial_right_cross_couplings,
            both_cross_couplings_nontrivial)
    checks += 9
    return checks, {
        "complete_factor_box_side": complete_factor_box_side,
        "complete_factor_quadruples": complete_factor_quadruples,
        "complete_box_nontrivial_cross_couplings": (
            complete_box_nontrivial_cross
        ),
        "factorizations": factorizations,
        "coprime_reflected_positive_quotient_content": (
            coprime_reflected_with_quotient_content
        ),
        "maximum_cross_content": maximum_cross_content,
        "nontrivial_left_cross_couplings": nontrivial_left_cross_couplings,
        "nontrivial_right_cross_couplings": nontrivial_right_cross_couplings,
        "both_cross_couplings_nontrivial": both_cross_couplings_nontrivial,
        "largest_sample": sample,
        "transparent_nonoverlap_witness": witness,
        "transparent_four_factor_witness": {
            **four_factor_witness,
            "reflected_gcd": four_reflected,
            "quotient_gcd": four_quotient,
            "left_cross_gcd": four_left,
            "right_cross_gcd": four_right,
            "target_gcd": 6,
        },
        "verified_exact_identity": (
            "G = g*e*gcd(r0,V0)*gcd(s0,U0)"
        ),
    }


def residue_counts(rows: tuple[int, ...], modulus: int) -> dict[int, int]:
    counts: defaultdict[int, int] = defaultdict(int)
    for row in rows:
        counts[row % modulus] += 1
    return dict(counts)


def row_residue_check(
        left_rows: tuple[int, ...], right_rows: tuple[int, ...],
        left_weights: tuple[int, ...], right_weights: tuple[int, ...],
        modulus: int) -> tuple[int, Fraction]:
    require(len(left_rows) == len(left_weights)
            and len(right_rows) == len(right_weights),
            "row-weight-length")
    require(left_rows and right_rows and modulus >= 1,
            "row-residue-domain", left_rows, right_rows, modulus)
    left_counts = residue_counts(left_rows, modulus)
    right_counts = residue_counts(right_rows, modulus)
    k_c = max(max(left_counts.values()), max(right_counts.values()))
    row_min = min(min(left_rows), min(right_rows))
    row_max = max(max(left_rows), max(right_rows))
    span = row_max - row_min
    require(k_c <= span // modulus + 1,
            "row-occupancy-floor-bound", k_c, span, modulus)
    require(k_c <= ceil_div(span, modulus) + 1,
            "row-occupancy-requested-bound", k_c, span, modulus)

    direct = sum(
        abs(left_weight * right_weight)
        for left_row, left_weight in zip(left_rows, left_weights)
        for right_row, right_weight in zip(right_rows, right_weights)
        if (left_row - right_row) % modulus == 0
    )
    left_l1: defaultdict[int, int] = defaultdict(int)
    right_l1: defaultdict[int, int] = defaultdict(int)
    for row, weight in zip(left_rows, left_weights):
        left_l1[row % modulus] += abs(weight)
    for row, weight in zip(right_rows, right_weights):
        right_l1[row % modulus] += abs(weight)
    by_residue = sum(left_l1[a] * right_l1[a]
                     for a in set(left_l1) | set(right_l1))
    require(direct == by_residue,
            "row-residue-exact-decomposition", direct, by_residue)

    left_norm_squared = sum(weight * weight for weight in left_weights)
    right_norm_squared = sum(weight * weight for weight in right_weights)
    require(direct * direct
            <= k_c * k_c * left_norm_squared * right_norm_squared,
            "row-residue-l2-inequality",
            direct, k_c, left_norm_squared, right_norm_squared)
    denominator = k_c * k_c * left_norm_squared * right_norm_squared
    ratio = (Fraction(direct * direct, denominator)
             if denominator else Fraction(0))
    return k_c, ratio


def check_row_residue_inequality() -> tuple[int, dict[str, object]]:
    checks = 0
    cases = 0
    max_ratio = Fraction(0)
    max_case: dict[str, object] = {}

    # Exhaust all ternary weights on two four-row families.
    small_left = (3, 5, 8, 11)
    small_right = (2, 5, 9, 11)
    ternary = tuple(itertools.product((-1, 0, 1), repeat=4))
    for modulus in (1, 2, 3, 5, 11):
        for left_weights in ternary:
            for right_weights in ternary:
                k_c, ratio = row_residue_check(
                    small_left, small_right,
                    left_weights, right_weights, modulus)
                checks += 4
                cases += 1
                if ratio > max_ratio:
                    max_ratio = ratio
                    max_case = {
                        "kind": "exhaustive-ternary",
                        "modulus": modulus,
                        "K_c": k_c,
                        "left_weights": list(left_weights),
                        "right_weights": list(right_weights),
                    }

    deterministic = (
        (
            tuple(range(11, 40, 2)), tuple(range(13, 44, 3)),
            tuple((7 * m + 3) % 13 - 6 for m in range(11, 40, 2)),
            tuple((5 * n + 1) % 11 - 5 for n in range(13, 44, 3)),
        ),
        (
            tuple(m for m in range(41, 79) if m % 3),
            tuple(n for n in range(37, 83) if n % 5),
            tuple((m * m + 2 * m + 1) % 17 - 8
                  for m in range(41, 79) if m % 3),
            tuple((3 * n * n + 1) % 19 - 9
                  for n in range(37, 83) if n % 5),
        ),
    )
    deterministic_moduli = (1, 2, 3, 5, 7, 11, 17, 31, 47, 89)
    deterministic_records: list[dict[str, int]] = []
    for left_rows, right_rows, left_weights, right_weights in deterministic:
        span = max(max(left_rows), max(right_rows)) - min(
            min(left_rows), min(right_rows))
        for modulus in deterministic_moduli:
            k_c, ratio = row_residue_check(
                left_rows, right_rows,
                left_weights, right_weights, modulus)
            checks += 4
            cases += 1
            deterministic_records.append({
                "span_W": span, "modulus_c": modulus, "K_c": k_c,
                "floor_bound": span // modulus + 1,
                "requested_bound": ceil_div(span, modulus) + 1,
            })
            if ratio > max_ratio:
                max_ratio = ratio
                max_case = {
                    "kind": "deterministic",
                    "span_W": span,
                    "modulus": modulus,
                    "K_c": k_c,
                }

    require(max_ratio == 1,
            "row-residue-sharpness-witness", max_ratio, max_case)
    checks += 1
    return checks, {
        "tested_weight_pairs": cases,
        "exhaustive_weight_alphabet": [-1, 0, 1],
        "maximum_squared_ratio": str(max_ratio),
        "sharp_case": max_case,
        "deterministic_constant_records": deterministic_records,
        "verified_inequality": (
            "R_c <= K_c ||gamma||_2 ||gamma'||_2, "
            "K_c <= floor(W/c)+1 <= ceil(W/c)+1"
        ),
    }


def positive_part(value: Fraction) -> Fraction:
    return max(value, Fraction(0))


def tpc29_sparse_saving(
        beta: Fraction, a: Fraction,
        b: Fraction, reflected_content: Fraction) -> Fraction:
    j_exp = 1 - beta
    return positive_part(
        j_exp - (a + b - 2 * reflected_content))


def target_content_saving(beta: Fraction, z_exp: Fraction) -> Fraction:
    return min(z_exp, 1 - beta)


def check_high_beta_ledger() -> tuple[int, dict[str, object]]:
    beta = Fraction(267, 400)
    j_exp = Fraction(133, 400)
    t_exp = Fraction(193, 500)
    reflected_upper = 1 - t_exp
    a = b = Fraction(1, 4)
    reflected_content = Fraction(0)
    quotient_exp = 1 - a
    quotient_gcd_exp = Fraction(2, 5)
    lcm_exp = a + b - reflected_content
    primitive_lcm_exp = a + b - 2 * reflected_content
    old_saving = tpc29_sparse_saving(
        beta, a, b, reflected_content)
    cross_exp = reflected_content + quotient_gcd_exp
    new_saving = target_content_saving(beta, cross_exp)
    checks = 0

    require(beta + j_exp == 1, "high-beta-orbit-duality")
    require(reflected_upper == Fraction(307, 500),
            "high-beta-reflected-upper")
    require(a < reflected_upper and b < reflected_upper,
            "high-beta-reflected-admissibility")
    require(quotient_exp == Fraction(3, 4) > t_exp,
            "high-beta-both-ultra")
    require(a + quotient_exp == 1 and b + quotient_exp == 1,
            "high-beta-target-factorization")
    require(lcm_exp == Fraction(1, 2) > j_exp,
            "high-beta-sparse-cell")
    require(lcm_exp - j_exp == Fraction(67, 400),
            "high-beta-sparse-margin")
    require(primitive_lcm_exp == Fraction(1, 2) > j_exp,
            "high-beta-outside-tpc29-rich-wedge")
    require(old_saving == 0,
            "high-beta-tpc29-zero-incidence-saving")
    require(quotient_gcd_exp <= quotient_exp,
            "high-beta-quotient-gcd-feasible")
    require(cross_exp == Fraction(2, 5) < beta,
            "high-beta-cross-content-row-range")
    require(beta - cross_exp == Fraction(107, 400),
            "high-beta-row-difference-room")
    require(new_saving == j_exp == Fraction(133, 400),
            "high-beta-new-saving")
    checks += 13

    # Check directly that the two terms in the sharpened theorem have
    # gaps 1-beta and z from the natural exponent 1+beta.
    natural_exp = 1 + beta
    theorem_term_exponents = (2 * beta, 1 + beta - cross_exp)
    gaps = tuple(natural_exp - exponent
                 for exponent in theorem_term_exponents)
    require(gaps == (j_exp, cross_exp),
            "high-beta-theorem-term-gaps", gaps)
    require(min(gaps) == new_saving,
            "high-beta-minimum-gap", gaps, new_saving)
    checks += 2

    grid_points = 0
    for beta_value in (
            Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
            beta, Fraction(3, 4)):
        for z_value in tuple(Fraction(k, 20) for k in range(1, 16)):
            natural = 1 + beta_value
            term_exponents = (
                2 * beta_value,
                1 + beta_value - z_value,
            )
            direct_gap = min(natural - exponent
                             for exponent in term_exponents)
            formula_gap = target_content_saving(beta_value, z_value)
            require(direct_gap == formula_gap,
                    "target-content-grid-ledger",
                    beta_value, z_value, direct_gap, formula_gap)
            checks += 1
            grid_points += 1

    return checks, {
        "beta": str(beta),
        "J_exponent": str(j_exp),
        "T_exponent": str(t_exp),
        "reflected_upper_exponent": str(reflected_upper),
        "r_exponent": str(a),
        "s_exponent": str(b),
        "reflected_gcd_exponent": str(reflected_content),
        "U_exponent": str(quotient_exp),
        "V_exponent": str(quotient_exp),
        "quotient_gcd_exponent": str(quotient_gcd_exp),
        "cross_content_exponent": str(cross_exp),
        "reflected_lcm_exponent": str(lcm_exp),
        "primitive_lcm_exponent": str(primitive_lcm_exp),
        "sparse_margin": str(lcm_exp - j_exp),
        "TPC29_incidence_saving": str(old_saving),
        "TPC30_target_content_saving": str(new_saving),
        "row_difference_room": str(beta - cross_exp),
        "theorem_term_gaps": [str(gap) for gap in gaps],
        "grid_points": grid_points,
    }


def main() -> None:
    checks = 0
    subcounts: dict[str, int] = {}

    count, identity_summary = check_target_gcd_identity()
    checks += count
    subcounts["target_gcd_identity"] = count

    count, occupancy_summary = check_exact_content_occupancy()
    checks += count
    subcounts["exact_content_occupancy"] = count

    count, fixed_row_summary = check_fixed_row_large_content()
    checks += count
    subcounts["fixed_row_large_content"] = count

    count, cross_summary = check_exact_four_factor_decomposition()
    checks += count
    subcounts["exact_four_factor_target_gcd"] = count

    count, row_summary = check_row_residue_inequality()
    checks += count
    subcounts["row_residue_l2_inequality"] = count

    count, exponent_summary = check_high_beta_ledger()
    checks += count
    subcounts["rational_high_beta_ledger"] = count

    claims = {
        "finite_target_gcd_identity": True,
        "finite_exact_content_occupancy": True,
        "finite_fixed_row_large_content_bound": True,
        "finite_cross_content_divisibility": True,
        "finite_exact_four_factor_target_gcd": True,
        "finite_row_residue_l2_inequality": True,
        "finite_rational_exponent_ledger": True,
        "sample_has_coprime_reflected_divisors": True,
        "sample_has_positive_quotient_content": True,
        "sample_TPC29_incidence_saving_is_zero": True,
        "sample_TPC30_target_content_saving_is_positive": True,
        "uses_mobius_sign_cancellation": False,
        "uses_chowla_or_elliott_input": False,
        "closes_small_target_gcd_core": False,
        "closes_complete_ultra_difference": False,
        "closes_complete_residual": False,
        "proves_positivity": False,
        "proves_hardy_littlewood_asymptotic": False,
        "proves_twin_primes": False,
        "breaks_sieve_parity": False,
    }
    expected_claims = {
        name: (name.startswith("finite_") or name.startswith("sample_"))
        for name in claims
    }
    require(claims == expected_claims,
            "scope-and-nonoverlap-flags", claims, expected_claims)
    checks += len(claims)
    subcounts["scope_and_nonoverlap_flags"] = len(claims)

    source_path = Path(__file__)
    source_bytes = source_path.read_bytes()
    normalized_source = source_bytes.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")
    source_hash = hashlib.sha256(normalized_source).hexdigest()
    payload = {
        "paper": "TPC-30",
        "certificate": "common-target content and row-orbit pruning",
        "description": (
            "finite exact regression for the primitive target-gcd identity, "
            "exact content layers, the fixed-row large-content bound, the "
            "exact four-factor gcd decomposition, explicit row-residue energy "
            "constants, rational exponents, and non-overlap flags; "
            "not a numerical proof of asymptotic Mobius cancellation"
        ),
        "exact_check_count": checks,
        "subcheck_counts": subcounts,
        "target_gcd_summary": identity_summary,
        "exact_content_occupancy_summary": occupancy_summary,
        "fixed_row_large_content_summary": fixed_row_summary,
        "cross_content_summary": cross_summary,
        "row_residue_summary": row_summary,
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
