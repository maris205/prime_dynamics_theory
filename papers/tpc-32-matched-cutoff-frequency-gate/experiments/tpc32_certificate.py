#!/usr/bin/env python3
"""Exact finite certificate for TPC-32.

This standard-library certificate checks the finite algebra used in

    Matched Prime--Mobius Cutoff Shells: Rank--Two Factorization,
    Determinant--Frequency Dispersion, and the Distinguished
    Zero--Frequency Gate.

The checks are exception based and therefore run identically under ordinary
Python and ``python -O``.  Exact integers, ``Fraction`` arithmetic, character
orthogonality, and finite cyclotomic-coordinate vectors are used throughout;
no floating-point approximation to a root of unity is used.

The certificate verifies matched cutoff-shell and polarization identities,
rank-at-most-two matrices, exact target-content inversion, the canonical
phase split even when the content and Fourier modulus are not coprime, the
truncated Mobius projector and its first dyadic band, prime--Mobius sign
fusion, no-wrap Parseval, the elementary L2/L1/Linf inequality, the rational
high-beta ledger, two sharp zero-frequency obstructions, and a primitive
finite prime-row witness.  These are finite algebra and bookkeeping checks.
They are not numerical evidence for asymptotic Mobius cancellation, a
prime-pair asymptotic, twin primes, or a breach of sieve parity.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


Rational = int | Fraction
Matrix = list[list[Fraction]]
Monomial = tuple[tuple[str, int], ...]
Polynomial = dict[Monomial, Fraction]


def require(condition: bool, label: str, *details: object) -> None:
    """Raise in both ordinary and optimized Python if a check fails."""
    if not condition:
        raise RuntimeError((label,) + details)


def factor(n: int) -> dict[int, int]:
    require(n >= 1, "factor-positive", n)
    out: dict[int, int] = {}
    prime = 2
    while prime * prime <= n:
        while n % prime == 0:
            out[prime] = out.get(prime, 0) + 1
            n //= prime
        prime += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def divisors(n: int) -> list[int]:
    require(n >= 1, "divisors-positive", n)
    out = [1]
    for prime, exponent in factor(n).items():
        powers = [prime**power for power in range(exponent + 1)]
        out = [left * right for left in out for right in powers]
    return sorted(out)


def mobius(n: int) -> int:
    fac = factor(n)
    if any(exponent > 1 for exponent in fac.values()):
        return 0
    return -1 if len(fac) % 2 else 1


def euler_phi(n: int) -> int:
    require(n >= 1, "phi-positive", n)
    result = n
    for prime in factor(n):
        result = result // prime * (prime - 1)
    return result


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def outer(left: Sequence[Rational], right: Sequence[Rational]) -> Matrix:
    return [
        [Fraction(x) * Fraction(y) for y in right]
        for x in left
    ]


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    require(len(left) == len(right), "matrix-add-row-count")
    require(
        all(len(a) == len(b) for a, b in zip(left, right)),
        "matrix-add-column-count",
    )
    return [
        [a + b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def matrix_sub(left: Matrix, right: Matrix) -> Matrix:
    return matrix_add(
        left,
        [[-entry for entry in row] for row in right],
    )


def matrix_scale(scalar: Rational, matrix: Matrix) -> Matrix:
    factor_value = Fraction(scalar)
    return [[factor_value * entry for entry in row] for row in matrix]


def matrix_rank(matrix: Matrix) -> int:
    """Exact Gaussian rank over the rationals."""
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    require(
        all(len(row) == column_count for row in work),
        "rectangular-matrix",
    )
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count)
             if work[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            multiplier = work[row][column]
            work[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def dot(left: Sequence[Rational], right: Sequence[Rational]) -> Fraction:
    require(len(left) == len(right), "dot-length")
    return sum(
        (Fraction(x) * Fraction(y) for x, y in zip(left, right)),
        Fraction(0),
    )


def vector_add(left: Sequence[int], right: Sequence[int]) -> list[int]:
    require(len(left) == len(right), "vector-add-length")
    return [x + y for x, y in zip(left, right)]


def vector_sub(left: Sequence[int], right: Sequence[int]) -> list[int]:
    require(len(left) == len(right), "vector-sub-length")
    return [x - y for x, y in zip(left, right)]


def check_matched_shell_rank_and_polarization() -> tuple[int, dict[str, object]]:
    checks = 0
    scalar_cases = 0
    for a_m, a_n, c_m, c_n in itertools.product(range(-3, 4), repeat=4):
        left = a_m * c_n + c_m * a_n + c_m * c_n
        right = (a_m + c_m) * (a_n + c_n) - a_m * a_n
        require(left == right, "matched-shell-scalar", a_m, a_n, c_m, c_n)
        checks += 1
        scalar_cases += 1

    rank_cases = 0
    attained_rank_two = 0
    symmetric_polarization_cases = 0
    maximum_rank = 0
    for rows in range(1, 7):
        for columns in range(1, 7):
            for seed in range(1, 15):
                t_left = [((seed + 2 * i) % 7) - 3 for i in range(rows)]
                c_left = [((3 * seed + i) % 5) - 2 for i in range(rows)]
                t_right = [((2 * seed + 3 * j) % 7) - 3
                           for j in range(columns)]
                c_right = [((5 * seed + 2 * j) % 5) - 2
                           for j in range(columns)]
                u_left = vector_add(t_left, c_left)
                u_right = vector_add(t_right, c_right)

                matched = matrix_sub(
                    outer(u_left, u_right),
                    outer(t_left, t_right),
                )
                expanded = matrix_add(
                    matrix_add(
                        outer(t_left, c_right),
                        outer(c_left, t_right),
                    ),
                    outer(c_left, c_right),
                )
                require(matched == expanded,
                        "matched-shell-matrix", rows, columns, seed)
                checks += 1

                polarized_twice = matrix_add(
                    outer(c_left, vector_add(u_right, t_right)),
                    outer(vector_add(u_left, t_left), c_right),
                )
                require(
                    matrix_scale(2, matched) == polarized_twice,
                    "bilinear-polarization",
                    rows,
                    columns,
                    seed,
                )
                checks += 1

                rank = matrix_rank(matched)
                require(rank <= 2, "rank-at-most-two", rows, columns, seed, rank)
                checks += 1
                maximum_rank = max(maximum_rank, rank)
                attained_rank_two += int(rank == 2)
                rank_cases += 1

        for seed in range(1, 18):
            t = [((seed + 3 * i) % 9) - 4 for i in range(rows)]
            c = [((2 * seed + i) % 7) - 3 for i in range(rows)]
            u = vector_add(t, c)
            energy_difference = dot(u, u) - dot(t, t)
            polarized = 2 * dot(t, c) + dot(c, c)
            require(
                energy_difference == polarized,
                "symmetric-energy-polarization",
                rows,
                seed,
                energy_difference,
                polarized,
            )
            checks += 1
            symmetric_polarization_cases += 1

    require(maximum_rank == 2, "rank-two-attained", maximum_rank)
    checks += 1
    require(attained_rank_two > 0, "rank-two-witness-count", attained_rank_two)
    checks += 1
    return checks, {
        "scalar_matched_shell_cases": scalar_cases,
        "matrix_rank_cases": rank_cases,
        "rank_two_cases": attained_rank_two,
        "maximum_exact_rank": maximum_rank,
        "symmetric_polarization_cases": symmetric_polarization_cases,
        "identities": [
            "A_m C_n + C_m A_n + C_m C_n = (A_m+C_m)(A_n+C_n)-A_m A_n",
            "2(U1 tensor U2-T1 tensor T2) = C1 tensor (U2+T2) + (U1+T1) tensor C2",
            "||T+C||_2^2-||T||_2^2 = 2<T,C>+||C||_2^2",
        ],
    }


def lambda_content(content_cutoff: int, modulus: int) -> int:
    require(content_cutoff >= 1 and modulus >= 1,
            "lambda-content-domain", content_cutoff, modulus)
    return sum(
        mobius(modulus // divisor)
        for divisor in divisors(modulus)
        if divisor <= content_cutoff
    )


def check_content_inversion_and_projector() -> tuple[int, dict[str, object]]:
    checks = 0
    exact_content_cases = 0
    cumulative_projector_cases = 0
    for left in range(1, 101):
        for right in range(1, 101):
            content = math.gcd(left, right)
            for exact in range(1, 26):
                if left % exact == 0 and right % exact == 0:
                    reduced_content = math.gcd(left // exact, right // exact)
                    inversion = sum(mobius(k) for k in divisors(reduced_content))
                else:
                    inversion = 0
                require(
                    inversion == int(content == exact),
                    "exact-gcd-content-inversion",
                    left,
                    right,
                    exact,
                    content,
                    inversion,
                )
                checks += 1
                exact_content_cases += 1

            for cutoff in range(1, 16):
                projector = sum(
                    lambda_content(cutoff, k)
                    for k in divisors(content)
                )
                require(
                    projector == int(content <= cutoff),
                    "cumulative-content-projector",
                    left,
                    right,
                    cutoff,
                    content,
                    projector,
                )
                checks += 1
                cumulative_projector_cases += 1

    band_cases = 0
    dyadic_projector_cases = 0
    beyond_band_support_cases = 0
    for cutoff in range(1, 61):
        require(lambda_content(cutoff, 1) == 1,
                "lambda-unit", cutoff)
        checks += 1
        band_cases += 1
        for modulus in range(2, cutoff + 1):
            require(
                lambda_content(cutoff, modulus) == 0,
                "lambda-lower-gap",
                cutoff,
                modulus,
                lambda_content(cutoff, modulus),
            )
            checks += 1
            band_cases += 1
        for modulus in range(cutoff + 1, 2 * cutoff + 1):
            require(
                lambda_content(cutoff, modulus) == -1,
                "lambda-first-dyadic-band",
                cutoff,
                modulus,
                lambda_content(cutoff, modulus),
            )
            checks += 1
            band_cases += 1

        for content in range(1, 4 * cutoff + 1):
            dyadic = 1 - sum(
                1 for modulus in range(cutoff + 1, 2 * cutoff + 1)
                if content % modulus == 0
            )
            if content <= 2 * cutoff:
                require(
                    dyadic == int(content <= cutoff),
                    "dyadic-projector-exact-range",
                    cutoff,
                    content,
                    dyadic,
                )
                dyadic_projector_cases += 1
            else:
                error = int(content <= cutoff) - dyadic
                require(
                    abs(error) <= 1 + len(divisors(content)),
                    "dyadic-projector-supported-error",
                    cutoff,
                    content,
                    error,
                )
                beyond_band_support_cases += 1
            checks += 1

    return checks, {
        "exact_content_inversion_cases": exact_content_cases,
        "cumulative_projector_cases": cumulative_projector_cases,
        "lambda_band_cases": band_cases,
        "dyadic_exact_range_cases": dyadic_projector_cases,
        "dyadic_beyond_band_bound_cases": beyond_band_support_cases,
        "identities": [
            "1_{gcd(x,y)=c} = 1_{c|x,y} sum_{k|gcd(x/c,y/c)} mu(k)",
            "lambda_C(k) = sum_{c|k,c<=C} mu(k/c)",
            "1_{gcd(x,y)<=C} = sum_{k|x,y} lambda_C(k)",
            "lambda_C(1)=1, lambda_C(k)=0 for 2<=k<=C, lambda_C(k)=-1 for C<k<=2C",
        ],
    }


def fractional_part(value: Fraction) -> Fraction:
    return Fraction(value.numerator % value.denominator, value.denominator)


def check_phase_exponent_split() -> tuple[int, dict[str, object]]:
    checks = 0
    cases = 0
    noncoprime_content_modulus_cases = 0
    example: dict[str, int] | None = None
    for content in range(1, 13):
        for modulus in range(2, 16):
            for frequency in range(modulus):
                for delta in range(-8, 9):
                    if delta == 0:
                        continue
                    right_row = 100
                    left_row = right_row + content * delta
                    if left_row <= 0:
                        continue
                    direct = Fraction(-frequency * delta, modulus)
                    separated = (
                        Fraction(-frequency * left_row, content * modulus)
                        + Fraction(frequency * right_row, content * modulus)
                    )
                    require(
                        fractional_part(direct) == fractional_part(separated),
                        "canonical-phase-split",
                        content,
                        modulus,
                        frequency,
                        delta,
                        left_row,
                        right_row,
                        direct,
                        separated,
                    )
                    checks += 1
                    cases += 1
                    if math.gcd(content, modulus) > 1:
                        noncoprime_content_modulus_cases += 1
                        if example is None:
                            example = {
                                "content": content,
                                "modulus": modulus,
                                "frequency": frequency,
                                "delta_sharp": delta,
                                "left_row": left_row,
                                "right_row": right_row,
                            }

    require(noncoprime_content_modulus_cases > 0,
            "noncoprime-phase-cases-exist")
    checks += 1
    require(example is not None, "noncoprime-phase-example-exists")
    checks += 1
    return checks, {
        "phase_split_cases": cases,
        "noncoprime_content_modulus_cases": noncoprime_content_modulus_cases,
        "noncoprime_example": example,
        "identity": (
            "e_q(-r(m-n)/c) = e_{cq}(-rm)e_{cq}(rn) whenever c|(m-n); "
            "no inverse of c modulo q is used"
        ),
    }


def check_prime_mobius_sign_fusion() -> tuple[int, dict[str, object]]:
    checks = 0
    abstract_cases = 0
    target_divisor_cases = 0
    for d in range(1, 61):
        if mobius(d) == 0:
            continue
        for w in range(1, 81):
            if mobius(w) == 0 or math.gcd(d, w) != 1:
                continue
            positive_weight = Fraction(w * w + 3 * d + 1, w + d)
            b_r = -mobius(w) * positive_weight
            require(
                mobius(d) * b_r == -mobius(d * w) * positive_weight,
                "prime-mobius-bR-sign-fusion",
                d,
                w,
                positive_weight,
            )
            checks += 1
            log_symbol_coefficient = -mobius(w)
            require(
                mobius(d) * log_symbol_coefficient == -mobius(d * w),
                "prime-mobius-ultra-sign-fusion",
                d,
                w,
            )
            checks += 1
            abstract_cases += 1

    primes = [prime for prime in range(3, 42) if is_prime(prime)]
    for h in (1, 2, 3, 5, 6):
        for d in range(1, 16):
            if mobius(d) == 0 or math.gcd(d, h) != 1:
                continue
            for ell in primes:
                if math.gcd(ell * d, h) != 1:
                    continue
                for orbit in range(1, 9):
                    if math.gcd(orbit, h) != 1:
                        continue
                    target = ell * d * orbit + h
                    for w in divisors(target):
                        if mobius(w) == 0:
                            continue
                        require(
                            math.gcd(d, w) == 1,
                            "target-divisor-coprime-opened-d",
                            h,
                            d,
                            ell,
                            orbit,
                            target,
                            w,
                        )
                        checks += 1
                        weight = Fraction(target + w, target)
                        require(
                            mobius(d) * (-mobius(w) * weight)
                            == -mobius(d * w) * weight,
                            "physical-target-sign-fusion",
                            h,
                            d,
                            ell,
                            orbit,
                            w,
                        )
                        checks += 1
                        target_divisor_cases += 1

    return checks, {
        "abstract_coprime_squarefree_pairs": abstract_cases,
        "primitive_target_divisor_cases": target_divisor_cases,
        "identities": [
            "mu(d)b_R(w) = -mu(dw)w_R(w)",
            "mu(d)a(w) = -mu(dw)log(w)",
        ],
    }


def character_orthogonality(modulus: int, exponent: int) -> int:
    """Exact sum of e_modulus(r*exponent) over all r."""
    require(modulus >= 1, "character-modulus", modulus)
    return modulus if exponent % modulus == 0 else 0


def prime_zeta_power(modulus: int, exponent: int) -> tuple[Fraction, ...]:
    """Coordinate vector of zeta^exponent in Q[zeta_p].

    For prime p, use the basis 1,zeta,...,zeta^(p-2) and eliminate
    zeta^(p-1) with 1+zeta+...+zeta^(p-1)=0.
    """
    require(is_prime(modulus), "cyclotomic-prime-modulus", modulus)
    reduced = exponent % modulus
    if reduced == modulus - 1:
        return tuple(Fraction(-1) for _ in range(modulus - 1))
    return tuple(
        Fraction(1 if index == reduced else 0)
        for index in range(modulus - 1)
    )


def cyclotomic_dft(
    signal: Sequence[Fraction],
    frequency: int,
) -> tuple[Fraction, ...]:
    modulus = len(signal)
    require(is_prime(modulus), "dft-prime-length", modulus)
    result = [Fraction(0) for _ in range(modulus - 1)]
    for position, amplitude in enumerate(signal):
        power = prime_zeta_power(modulus, -frequency * position)
        result = [
            old + amplitude * coordinate
            for old, coordinate in zip(result, power)
        ]
    return tuple(result)


def check_exact_parseval_and_flat_no_go() -> tuple[int, dict[str, object]]:
    checks = 0
    parseval_cases = 0
    no_wrap_pair_checks = 0
    for modulus in (5, 7, 11, 13, 17, 19):
        half_span = (modulus - 2) // 2
        support = list(range(-half_span, half_span + 1))
        require(max(support) - min(support) < modulus,
                "parseval-no-wrap-span", modulus, support)
        checks += 1
        for seed in range(1, 12):
            amplitudes = {
                n: ((seed * (n + half_span + 1) + n * n) % 9) - 4
                for n in support
            }
            spectral_energy = 0
            for left in support:
                for right in support:
                    orthogonality = character_orthogonality(
                        modulus, left - right)
                    require(
                        (orthogonality == modulus) == (left == right),
                        "no-wrap-character-collision",
                        modulus,
                        left,
                        right,
                    )
                    checks += 1
                    no_wrap_pair_checks += 1
                    spectral_energy += (
                        amplitudes[left]
                        * amplitudes[right]
                        * orthogonality
                    )
            physical_energy = modulus * sum(
                amplitude * amplitude for amplitude in amplitudes.values())
            require(
                spectral_energy == physical_energy,
                "exact-no-wrap-parseval",
                modulus,
                seed,
                spectral_energy,
                physical_energy,
            )
            checks += 1
            parseval_cases += 1

    flat_cases = 0
    flat_examples: list[dict[str, str | int]] = []
    for modulus in (3, 5, 7, 11):
        for total_mass in (1, 2, 5, 11):
            signal = [Fraction(total_mass, modulus) for _ in range(modulus)]
            transforms = [
                cyclotomic_dft(signal, frequency)
                for frequency in range(modulus)
            ]
            expected_zero = tuple(Fraction(0) for _ in range(modulus - 1))
            expected_principal = tuple(
                [Fraction(total_mass)]
                + [Fraction(0) for _ in range(modulus - 2)]
            )
            require(
                transforms[0] == expected_principal,
                "flat-dft-principal-coefficient",
                modulus,
                total_mass,
                transforms[0],
            )
            checks += 1
            for frequency in range(1, modulus):
                require(
                    transforms[frequency] == expected_zero,
                    "flat-dft-nonzero-frequency",
                    modulus,
                    total_mass,
                    frequency,
                    transforms[frequency],
                )
                checks += 1
            l1 = sum((abs(value) for value in signal), Fraction(0))
            linf = max(abs(value) for value in signal)
            l2_squared = sum((value * value for value in signal), Fraction(0))
            require(l1 == total_mass,
                    "flat-signal-l1", modulus, total_mass, l1)
            checks += 1
            require(linf == Fraction(total_mass, modulus),
                    "flat-signal-linf", modulus, total_mass, linf)
            checks += 1
            require(l2_squared == Fraction(total_mass * total_mass, modulus),
                    "flat-signal-l2", modulus, total_mass, l2_squared)
            checks += 1
            require(l2_squared == l1 * linf,
                    "flat-signal-norm-saturation", modulus, total_mass)
            checks += 1
            flat_cases += 1
            if total_mass == 5:
                flat_examples.append({
                    "modulus": modulus,
                    "total_mass": str(total_mass),
                    "zero_frequency": str(total_mass),
                    "all_nonzero_frequencies": "0",
                })

    return checks, {
        "parseval_cases": parseval_cases,
        "no_wrap_pair_checks": no_wrap_pair_checks,
        "flat_signal_cases": flat_cases,
        "flat_signal_examples": flat_examples,
        "exact_root_representation": (
            "Q-basis 1,zeta,...,zeta^(p-2) with "
            "zeta^(p-1)=-(1+...+zeta^(p-2))"
        ),
        "parseval_identity": (
            "sum_r |Ahat(r)|^2 = p sum_n |A(n)|^2, certified by exact "
            "finite-character orthogonality"
        ),
    }


def check_l2_l1_linf() -> tuple[int, dict[str, object]]:
    checks = 0
    cases = 0
    equality_cases = 0
    zero_cases = 0
    for length in range(1, 7):
        for values in itertools.product(range(-2, 3), repeat=length):
            l1 = sum(abs(value) for value in values)
            linf = max(abs(value) for value in values)
            l2_squared = sum(value * value for value in values)
            require(
                l2_squared <= l1 * linf,
                "l2-squared-l1-linf",
                values,
                l2_squared,
                l1,
                linf,
            )
            checks += 1
            cases += 1
            equality_cases += int(l2_squared == l1 * linf)
            zero_cases += int(l1 == 0)
    return checks, {
        "integer_signal_cases": cases,
        "equality_cases": equality_cases,
        "zero_signal_cases": zero_cases,
        "identity": "||A||_2^2 <= ||A||_1 ||A||_infinity",
    }


def check_high_beta_fraction_ledger() -> tuple[int, dict[str, object]]:
    checks = 0
    beta = Fraction(267, 400)
    orbit = 1 - beta
    flat_threshold = 3 * beta - 2
    endpoint_chi = Fraction(1, 400)
    frequency_saving = orbit
    exceptional_proportion_saving = beta - 2 * frequency_saving

    identities = [
        (orbit, Fraction(133, 400), "orbit-exponent"),
        (flat_threshold, Fraction(1, 400), "flatness-threshold"),
        (exceptional_proportion_saving, Fraction(1, 400),
         "exceptional-proportion-saving"),
        ((beta - endpoint_chi) / 2, orbit,
         "flatness-transfer-endpoint"),
        (beta - 2 * orbit, Fraction(1, 400),
         "Q-versus-J-squared-gap"),
    ]
    for actual, expected, label in identities:
        require(actual == expected, label, actual, expected)
        checks += 1

    below_samples = (
        Fraction(0),
        Fraction(1, 1000),
        Fraction(1, 800),
        Fraction(1, 500),
    )
    for chi in below_samples:
        require(chi < endpoint_chi,
                "flatness-below-threshold-domain", chi)
        checks += 1
        transfer = (beta - chi) / 2
        require(transfer > orbit,
                "flatness-below-threshold-transfer", chi, transfer, orbit)
        checks += 1

    above_samples = (
        Fraction(1, 300),
        Fraction(1, 200),
        Fraction(1, 100),
    )
    for chi in above_samples:
        require(chi > endpoint_chi,
                "flatness-above-threshold-domain", chi)
        checks += 1
        transfer = (beta - chi) / 2
        require(transfer < orbit,
                "flatness-above-threshold-transfer", chi, transfer, orbit)
        checks += 1

    kappa = orbit
    endpoint_saving = min(orbit, kappa, (beta - endpoint_chi) / 2)
    require(endpoint_saving == orbit,
            "endpoint-minimum-saving", endpoint_saving, orbit)
    checks += 1

    return checks, {
        "beta": str(beta),
        "orbit_exponent_1_minus_beta": str(orbit),
        "C_equals_J_exponent": str(kappa),
        "almost_all_frequency_saving": str(frequency_saving),
        "exceptional_proportion_power": str(exceptional_proportion_saving),
        "flatness_threshold_3beta_minus_2": str(flat_threshold),
        "endpoint_flatness_exponent": str(endpoint_chi),
        "endpoint_transferred_saving": str(endpoint_saving),
        "checked_below_threshold": [str(value) for value in below_samples],
        "checked_above_threshold": [str(value) for value in above_samples],
    }


def matrix_vector_product(matrix: Matrix, vector: Sequence[Rational]) -> list[Fraction]:
    return [dot(row, vector) for row in matrix]


def check_coherent_matrix_and_primitive_witness() -> tuple[int, dict[str, object]]:
    checks = 0
    coherent_cases = 0
    for size in range(2, 21):
        matrix = [
            [Fraction(0 if row == column else 1)
             for column in range(size)]
            for row in range(size)
        ]
        ones = [Fraction(1) for _ in range(size)]
        require(
            matrix_vector_product(matrix, ones)
            == [Fraction(size - 1) for _ in range(size)],
            "J-minus-I-principal-eigenvector",
            size,
        )
        checks += 1
        for index in range(size - 1):
            difference = [Fraction(0) for _ in range(size)]
            difference[index] = 1
            difference[-1] = -1
            require(
                matrix_vector_product(matrix, difference)
                == [-value for value in difference],
                "J-minus-I-transverse-eigenvector",
                size,
                index,
            )
            checks += 1

        square = [
            [
                sum(
                    (matrix[row][middle] * matrix[middle][column]
                     for middle in range(size)),
                    Fraction(0),
                )
                for column in range(size)
            ]
            for row in range(size)
        ]
        expected_square = [
            [Fraction(size - 1 if row == column else size - 2)
             for column in range(size)]
            for row in range(size)
        ]
        require(square == expected_square,
                "J-minus-I-square-identity", size)
        checks += 1
        frobenius_squared = sum(
            (entry * entry for row in matrix for entry in row),
            Fraction(0),
        )
        require(frobenius_squared == size * (size - 1),
                "J-minus-I-frobenius", size, frobenius_squared)
        checks += 1
        operator_squared = Fraction((size - 1) ** 2)
        stable_rank = frobenius_squared / operator_squared
        require(stable_rank == Fraction(size, size - 1),
                "J-minus-I-stable-rank", size, stable_rank)
        checks += 1
        require(matrix_rank(matrix) == size,
                "J-minus-I-full-rank", size, matrix_rank(matrix))
        checks += 1
        coherent_cases += 1

    rows = [59, 71, 101, 107, 137, 149, 179, 191, 197]
    shift = 2
    orbit = 1
    opened_d = 1
    content_cutoff = 30
    targets = [row * orbit + shift for row in rows]
    for row, target in zip(rows, targets):
        require(is_prime(row), "primitive-witness-row-prime", row)
        checks += 1
        require(50 <= row <= 200,
                "primitive-witness-dyadic-row", row)
        checks += 1
        require(is_prime(target), "primitive-witness-target-prime", row, target)
        checks += 1
        require(math.gcd(row * opened_d, shift) == 1,
                "primitive-witness-row-shift-coprime", row, shift)
        checks += 1
        require(math.gcd(orbit, shift) == 1,
                "primitive-witness-orbit-shift-coprime", orbit, shift)
        checks += 1
        require(target > 2 * content_cutoff,
                "primitive-witness-target-above-two-C", target)
        checks += 1

    witness_matrix: Matrix = []
    off_diagonal_pairs = 0
    for left_index, left_target in enumerate(targets):
        row_entries: list[Fraction] = []
        for right_index, right_target in enumerate(targets):
            content = math.gcd(left_target, right_target)
            expected = int(left_index != right_index)
            actual = int(content <= content_cutoff)
            require(actual == expected,
                    "primitive-witness-content-matrix",
                    left_index, right_index, content, actual, expected)
            checks += 1
            row_entries.append(Fraction(actual))
            if left_index != right_index:
                require(content == 1,
                        "primitive-witness-offdiagonal-coprime",
                        left_target, right_target, content)
                checks += 1
                require(
                    all(not (left_target % modulus == 0
                             and right_target % modulus == 0)
                        for modulus in range(content_cutoff + 1,
                                             2 * content_cutoff + 1)),
                    "primitive-witness-empty-dyadic-common-divisor-band",
                    left_target,
                    right_target,
                )
                checks += 1
                off_diagonal_pairs += 1
        witness_matrix.append(row_entries)

    expected_witness_matrix = [
        [Fraction(0 if row == column else 1)
         for column in range(len(rows))]
        for row in range(len(rows))
    ]
    require(witness_matrix == expected_witness_matrix,
            "primitive-witness-J-minus-I")
    checks += 1
    witness_stable_rank = Fraction(len(rows), len(rows) - 1)
    require(witness_stable_rank == Fraction(9, 8),
            "primitive-witness-stable-rank", witness_stable_rank)
    checks += 1

    return checks, {
        "coherent_matrix_sizes": coherent_cases,
        "spectrum_formula": "{M-1 (once), -1 (multiplicity M-1)}",
        "stable_rank_formula": "M/(M-1)",
        "primitive_witness": {
            "h": shift,
            "j": orbit,
            "d": opened_d,
            "L": 100,
            "R": 12,
            "T": 50,
            "U0": 200,
            "C": content_cutoff,
            "rows": rows,
            "targets": targets,
            "off_diagonal_pairs": off_diagonal_pairs,
            "content_matrix": "J-I_9",
            "spectrum": [8] + [-1] * 8,
            "stable_rank": str(witness_stable_rank),
        },
    }


def lambda_prime(R: int, u: int) -> Fraction:
    require(R >= 1 and u >= 1, "lambda-prime-domain", R, u)
    if u > R:
        return Fraction(0)
    return u * sum(
        (
            Fraction(mobius(u * b) * mobius(b), euler_phi(u * b))
            for b in range(1, R // u + 1)
        ),
        Fraction(0),
    )


def monomial_from_variables(*variables: str) -> Monomial:
    powers: dict[str, int] = {}
    for variable in variables:
        powers[variable] = powers.get(variable, 0) + 1
    return tuple(sorted(powers.items()))


def poly_constant(value: Rational) -> Polynomial:
    coefficient = Fraction(value)
    return {} if coefficient == 0 else {(): coefficient}


def poly_variable(name: str) -> Polynomial:
    return {((name, 1),): Fraction(1)}


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
        if out[monomial] == 0:
            del out[monomial]
    return out


def poly_scale(scalar: Rational, polynomial: Polynomial) -> Polynomial:
    scalar_fraction = Fraction(scalar)
    if scalar_fraction == 0:
        return {}
    return {
        monomial: scalar_fraction * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar_fraction * coefficient != 0
    }


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            powers: dict[str, int] = {}
            for variable, exponent in left_monomial + right_monomial:
                powers[variable] = powers.get(variable, 0) + exponent
            monomial = tuple(sorted(powers.items()))
            out[monomial] = (
                out.get(monomial, Fraction(0))
                + left_coefficient * right_coefficient
            )
            if out[monomial] == 0:
                del out[monomial]
    return out


def check_lambda_prime_and_formal_logs() -> tuple[int, dict[str, object]]:
    checks = 0
    lambda_value = lambda_prime(12, 1)
    require(lambda_value == Fraction(113, 30),
            "lambda-prime-12-at-1", lambda_value)
    checks += 1

    rows = [59, 71, 101, 107, 137, 149, 179, 191, 197]
    targets = [row + 2 for row in rows]
    pair_cases = 0
    sample_coefficients: dict[str, str] | None = None
    for left_target, right_target in itertools.combinations(targets, 2):
        left_log = poly_variable(f"log_{left_target}")
        right_log = poly_variable(f"log_{right_target}")
        prefix_left = poly_constant(-lambda_value)
        prefix_right = poly_constant(-lambda_value)
        full_left = poly_add(prefix_left, left_log)
        full_right = poly_add(prefix_right, right_log)

        direct_difference = poly_add(
            poly_mul(full_left, full_right),
            poly_scale(-1, poly_mul(prefix_left, prefix_right)),
        )
        three_channels = poly_add(
            poly_add(
                poly_mul(prefix_left, right_log),
                poly_mul(left_log, prefix_right),
            ),
            poly_mul(left_log, right_log),
        )
        require(
            direct_difference == three_channels,
            "formal-log-matched-shell",
            left_target,
            right_target,
            direct_difference,
            three_channels,
        )
        checks += 1
        expected = {
            monomial_from_variables(f"log_{left_target}",
                                    f"log_{right_target}"): Fraction(1),
            monomial_from_variables(f"log_{left_target}"): -lambda_value,
            monomial_from_variables(f"log_{right_target}"): -lambda_value,
        }
        require(
            direct_difference == expected,
            "formal-log-coefficients",
            left_target,
            right_target,
            direct_difference,
            expected,
        )
        checks += 1
        require(
            direct_difference.get(
                monomial_from_variables(f"log_{left_target}",
                                        f"log_{right_target}"),
                Fraction(0),
            ) == 1,
            "formal-log-nonzero-quadratic-coefficient",
            left_target,
            right_target,
        )
        checks += 1
        pair_cases += 1
        if sample_coefficients is None:
            sample_coefficients = {
                "pair": f"({left_target},{right_target})",
                "log_product": "1",
                f"log_{left_target}": str(-lambda_value),
                f"log_{right_target}": str(-lambda_value),
                "constant": "0",
            }

    require(sample_coefficients is not None,
            "formal-log-sample-exists")
    checks += 1
    return checks, {
        "lambda_prime_12_1": str(lambda_value),
        "formal_prime_log_pair_cases": pair_cases,
        "kernel_formula": (
            "log(p_i)log(p_j) - (113/30)(log(p_i)+log(p_j))"
        ),
        "sample_coefficients": sample_coefficients,
    }


def check_scope_flags() -> tuple[int, dict[str, bool]]:
    claims = {
        "finite_matched_shell_identity": True,
        "finite_rank_at_most_two": True,
        "finite_polarization_identity": True,
        "finite_exact_content_inversion": True,
        "finite_lambda_content_projector": True,
        "finite_dyadic_projector_band": True,
        "finite_phase_split_without_content_modulus_coprimality": True,
        "finite_prime_mobius_sign_fusion": True,
        "finite_exact_character_orthogonality_parseval": True,
        "finite_l2_l1_linf_inequality": True,
        "finite_high_beta_fraction_ledger": True,
        "finite_flat_signal_zero_frequency_no_go": True,
        "finite_coherent_J_minus_I_spectrum": True,
        "finite_primitive_prime_row_witness": True,
        "finite_lambda_prime_12_value": True,
        "finite_formal_prime_log_identity": True,
        "uses_floating_point_roots_of_unity": False,
        "proves_zero_frequency_flatness": False,
        "proves_signed_full_shell_cancellation": False,
        "proves_asymptotic_mobius_cancellation": False,
        "proves_a_new_distribution_level": False,
        "closes_complete_ultra_difference": False,
        "closes_complete_residual": False,
        "proves_positivity": False,
        "proves_hardy_littlewood_asymptotic": False,
        "proves_twin_primes": False,
        "breaks_sieve_parity": False,
        "primitive_finite_witness_is_twin_prime_asymptotic_evidence": False,
    }
    positive = {name for name in claims if name.startswith("finite_")}
    require(all(claims[name] for name in positive),
            "positive-scope-flags", sorted(positive))
    negative = set(claims) - positive
    require(all(not claims[name] for name in negative),
            "negative-scope-flags", sorted(negative))
    return len(claims), claims


def main() -> None:
    checks = 0
    subcounts: dict[str, int] = {}

    count, matched_summary = check_matched_shell_rank_and_polarization()
    checks += count
    subcounts["matched_shell_rank_and_polarization"] = count

    count, content_summary = check_content_inversion_and_projector()
    checks += count
    subcounts["content_inversion_and_lambda_projector"] = count

    count, phase_summary = check_phase_exponent_split()
    checks += count
    subcounts["canonical_phase_exponent_split"] = count

    count, fusion_summary = check_prime_mobius_sign_fusion()
    checks += count
    subcounts["prime_mobius_sign_fusion"] = count

    count, parseval_summary = check_exact_parseval_and_flat_no_go()
    checks += count
    subcounts["exact_parseval_and_flat_signal_no_go"] = count

    count, norm_summary = check_l2_l1_linf()
    checks += count
    subcounts["l2_l1_linf_inequality"] = count

    count, high_beta_summary = check_high_beta_fraction_ledger()
    checks += count
    subcounts["high_beta_fraction_ledger"] = count

    count, coherent_summary = check_coherent_matrix_and_primitive_witness()
    checks += count
    subcounts["coherent_matrix_and_primitive_witness"] = count

    count, formal_summary = check_lambda_prime_and_formal_logs()
    checks += count
    subcounts["lambda_prime_and_formal_log_polynomials"] = count

    count, claims = check_scope_flags()
    checks += count
    subcounts["scope_flags"] = count

    source_path = Path(__file__)
    source_bytes = source_path.read_bytes()
    normalized_source = source_bytes.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")
    source_hash = hashlib.sha256(normalized_source).hexdigest()
    payload = {
        "paper": "TPC-32",
        "certificate": "matched cutoff frequency gate",
        "description": (
            "finite exact regression for matched cutoff shells, rank-two "
            "factorization, content inversion, noncoprime canonical phase "
            "splitting, prime-Mobius sign fusion, exact Parseval, norm and "
            "high-beta ledgers, and sharp zero-frequency interface "
            "obstructions; not evidence for an asymptotic prime-pair claim"
        ),
        "exact_check_count": checks,
        "subcheck_counts": subcounts,
        "matched_shell_summary": matched_summary,
        "content_projector_summary": content_summary,
        "phase_split_summary": phase_summary,
        "prime_mobius_fusion_summary": fusion_summary,
        "parseval_and_flat_no_go_summary": parseval_summary,
        "norm_summary": norm_summary,
        "high_beta_summary": high_beta_summary,
        "coherent_witness_summary": coherent_summary,
        "formal_log_summary": formal_summary,
        "claims": claims,
        "source_sha256": source_hash,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_digest"] = hashlib.sha256(
        canonical.encode("utf-8")).hexdigest()
    output_path = source_path.with_suffix(".json")
    output_path.write_bytes(
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
