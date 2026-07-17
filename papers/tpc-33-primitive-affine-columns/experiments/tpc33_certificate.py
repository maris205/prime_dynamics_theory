#!/usr/bin/env python3
"""Exact finite certificate for TPC-33.

This standard-library script checks the finite algebra used in

    Primitive Affine Columns at a Distinguished Zero Frequency:
    Fixed-Determinant Projective Plancherel,
    Structured-Mask Disintegration, and the Q^3 Energy Gate.

All checks are exception based and therefore run identically under ordinary
Python and ``python -O``.  Integers and ``Fraction`` arithmetic are used;
no floating-point root of unity or probabilistic test is used.

The certificate verifies the SL_2 affine normal form, gcd identities,
Mobius gcd layers, square discriminant, balanced and reduced origins, local
squarefree root counts, the exact row-gcd mask projector and coefficient
mass, projected affine-column determinants, the exact fixed-determinant
second moment, the product-slope lift, quadratic-character coherent-line
obstruction, finite Cauchy--Schwarz transfers, and the rational high-beta
ledger.  It does not certify any asymptotic Mobius cancellation, the Q^3
physical column-energy estimate, a prime-pair asymptotic, twin primes, or a
breach of sieve parity.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Sequence


def require(condition: bool, label: str, *details: object) -> None:
    """Raise in ordinary and optimized Python if a check fails."""
    if not condition:
        raise RuntimeError((label,) + details)


def factor(n: int) -> dict[int, int]:
    require(n >= 1, "factor-positive", n)
    out: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            out[divisor] = out.get(divisor, 0) + 1
            n //= divisor
        divisor += 1
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
    require(n >= 1, "mobius-positive", n)
    fac = factor(n)
    if any(exponent > 1 for exponent in fac.values()):
        return 0
    return -1 if len(fac) % 2 else 1


def omega(n: int) -> int:
    return len(factor(n))


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


def balanced_bezout(a: int, s: int) -> tuple[int, int]:
    require(a >= 1 and s >= 1 and math.gcd(a, s) == 1,
            "balanced-bezout-domain", a, s)
    if a == 1:
        return 0, -1
    candidates = [
        x for x in range(-a, a + 1)
        if 2 * x > -a and 2 * x <= a and (s * x - 1) % a == 0
    ]
    require(len(candidates) == 1,
            "balanced-bezout-unique", a, s, candidates)
    x = candidates[0]
    y = (s * x - 1) // a
    return x, y


def check_affine_normal_form() -> tuple[int, dict[str, object]]:
    checks = 0
    parameter_sets = 0
    affine_points = 0
    mobius_layer_points = 0
    for h in range(-7, 8):
        if h == 0:
            continue
        for a in range(1, 13):
            for s in range(1, 13):
                if math.gcd(a, s) != 1 or math.gcd(a * s, h) != 1:
                    continue
                x, y = balanced_bezout(a, s)
                require(s * x - a * y == 1,
                        "bezout-identity", h, a, s, x, y)
                checks += 1
                require(2 * abs(x) <= a,
                        "balanced-x-bound", h, a, s, x)
                checks += 1
                require(abs(y) <= Fraction(s, 2) + 1,
                        "balanced-y-bound", h, a, s, y)
                checks += 1

                quadratic_a = a * s
                quadratic_b = h * (s * x + a * y)
                quadratic_c = h * h * x * y
                discriminant = quadratic_b * quadratic_b - 4 * quadratic_a * quadratic_c
                require(discriminant == h * h,
                        "square-discriminant", h, a, s, x, y,
                        discriminant)
                checks += 1
                parameter_sets += 1

                for t in range(-18, 19):
                    u = h * x + a * t
                    d = h * y + s * t
                    require(s * u - a * d == h,
                            "fixed-determinant", h, a, s, t, d, u)
                    checks += 1
                    inverse_h = s * u - a * d
                    inverse_t = -y * u + x * d
                    require((inverse_h, inverse_t) == (h, t),
                            "unimodular-inverse", h, a, s, t,
                            inverse_h, inverse_t)
                    checks += 1
                    common = math.gcd(d, u)
                    expected = math.gcd(h, t)
                    require(common == expected,
                            "common-gcd", h, a, s, t, d, u,
                            common, expected)
                    checks += 1
                    require(math.gcd(d, h) == expected,
                            "D-h-gcd", h, a, s, t, d, expected)
                    checks += 1
                    require(math.gcd(u, h) == expected,
                            "U-h-gcd", h, a, s, t, u, expected)
                    checks += 1
                    require(math.gcd(d, s) == 1,
                            "D-s-coprime", h, a, s, t, d)
                    checks += 1
                    require(math.gcd(u, a) == 1,
                            "U-a-coprime", h, a, s, t, u)
                    checks += 1
                    require(d * u == quadratic_a * t * t
                            + quadratic_b * t + quadratic_c,
                            "quadratic-product", h, a, s, t, d, u)
                    checks += 1
                    affine_points += 1

                lower = 4 * (abs(h) + 1)
                for t in range(lower + 1, 2 * lower + 1):
                    u = h * x + a * t
                    d = h * y + s * t
                    require(d > 0 and u > 0,
                            "balanced-positive", h, a, s, t, d, u)
                    checks += 1
                    g = math.gcd(h, t)
                    require(d % g == 0 and u % g == 0,
                            "gcd-layer-divisibility", h, a, s, t, d, u, g)
                    checks += 1
                    d_reduced = d // g
                    u_reduced = u // g
                    right = (
                        mobius(g) ** 2
                        * int(math.gcd(g, d_reduced * u_reduced) == 1)
                        * mobius(d_reduced * u_reduced)
                    )
                    left = mobius(d) * mobius(u)
                    require(left == right,
                            "mobius-gcd-layer", h, a, s, t,
                            d, u, g, left, right)
                    checks += 1
                    if g == 1:
                        require(left == mobius(d * u),
                                "primitive-mobius-fusion", h, a, s, t,
                                d, u, left)
                        checks += 1
                    mobius_layer_points += 1

    return checks, {
        "parameter_sets": parameter_sets,
        "affine_points": affine_points,
        "positive_mobius_layer_points": mobius_layer_points,
        "identities": [
            "sU-aD=h",
            "(h,t)^T=[[s,-a],[-y,x]](U,D)^T",
            "gcd(D,U)=gcd(D,h)=gcd(U,h)=gcd(h,t)",
            "disc(D_t U_t)=h^2",
            "mu(D)mu(U)=mu(g)^2 1_{(g,D'U')=1}mu(D'U')",
        ],
    }


def reduced_origin(a: int, s: int, h: int) -> tuple[int, int]:
    candidates = [d for d in range(1, s + 1) if (a * d + h) % s == 0]
    require(len(candidates) == 1,
            "reduced-origin-unique", a, s, h, candidates)
    d0 = candidates[0]
    return d0, (a * d0 + h) // s


def check_reduced_and_projected_origins() -> tuple[int, dict[str, object]]:
    checks = 0
    reduced_cases = 0
    projected_cases = 0
    primes = [2, 3, 5, 7, 11, 13]
    for h in range(-6, 7):
        if h == 0:
            continue
        for a in range(1, 18):
            for s in range(1, 15):
                if math.gcd(a, s) != 1 or math.gcd(a * s, h) != 1:
                    continue
                d0, u0 = reduced_origin(a, s, h)
                require(1 <= d0 <= s,
                        "reduced-D0-range", a, s, h, d0)
                checks += 1
                require(abs(u0) <= a + abs(h),
                        "reduced-U0-bound", a, s, h, d0, u0)
                checks += 1
                for r in range(-8, 9):
                    d = d0 + s * r
                    u = u0 + a * r
                    require(s * u - a * d == h,
                            "reduced-origin-determinant", a, s, h, r, d, u)
                    checks += 1
                reduced_cases += 1

    for ell in primes:
        for j in range(1, 9):
            for v in range(1, 9):
                for s in range(1, 10):
                    for h in (-5, -2, 1, 3, 7):
                        a = ell * j * v
                        if math.gcd(a, s) != 1 or math.gcd(a * s, h) != 1:
                            continue
                        d0, u0 = reduced_origin(a, s, h)
                        for r in range(0, 9):
                            d = d0 + s * r
                            u = u0 + a * r
                            require(s * u - ell * j * v * d == h,
                                    "projected-column-determinant",
                                    ell, j, v, s, h, r, d, u)
                            checks += 1
                            require(math.gcd(s, ell * j * v) == 1,
                                    "projected-slope-coprime",
                                    ell, j, v, s)
                            checks += 1
                            projected_cases += 1

    return checks, {
        "reduced_origin_parameter_sets": reduced_cases,
        "projected_affine_points": projected_cases,
        "projected_identity": "s U_r - ell*j*v D_r = h",
    }


def check_local_squarefree_roots() -> tuple[int, dict[str, object]]:
    checks = 0
    cases = {"p_divides_h": 0, "p_divides_slope": 0, "generic": 0}
    primes = [2, 3, 5, 7, 11, 13]
    for a in range(1, 17):
        for s in range(1, 17):
            if math.gcd(a, s) != 1:
                continue
            x, y = balanced_bezout(a, s)
            for h in range(1, 16):
                if math.gcd(a * s, h) != 1:
                    continue
                for p in primes:
                    if h % p == 0:
                        allowed = 0
                        for t in range(p):
                            d = h * y + s * t
                            u = h * x + a * t
                            good = t % p != 0 and d % p != 0 and u % p != 0
                            allowed += int(good)
                        require(allowed == p - 1,
                                "local-p-divides-h", a, s, h, p, allowed)
                        checks += 1
                        cases["p_divides_h"] += 1
                    else:
                        modulus = p * p
                        allowed = 0
                        bad_d: list[int] = []
                        bad_u: list[int] = []
                        for t in range(modulus):
                            d = h * y + s * t
                            u = h * x + a * t
                            if d % modulus == 0:
                                bad_d.append(t)
                            if u % modulus == 0:
                                bad_u.append(t)
                            allowed += int(d % modulus != 0 and u % modulus != 0)
                        if (a * s) % p == 0:
                            require(allowed == modulus - 1,
                                    "local-p-divides-slope",
                                    a, s, h, p, allowed, bad_d, bad_u)
                            checks += 1
                            cases["p_divides_slope"] += 1
                        else:
                            require(allowed == modulus - 2,
                                    "local-generic", a, s, h, p,
                                    allowed, bad_d, bad_u)
                            checks += 1
                            require(set(bad_d).isdisjoint(bad_u),
                                    "local-roots-distinct",
                                    a, s, h, p, bad_d, bad_u)
                            checks += 1
                            cases["generic"] += 1
    return checks, {
        "local_case_counts": cases,
        "factors": {
            "p_divides_h": "1-1/p",
            "p_divides_as_not_h": "1-1/p^2",
            "p_divides_neither_a_s_h": "1-2/p^2",
        },
    }


def lambda_gcd(cutoff: int, v: int) -> int:
    return sum(
        mobius(v // g)
        for g in divisors(v)
        if g <= cutoff
    )


def check_mask_projector() -> tuple[int, dict[str, object]]:
    checks = 0
    projector_cases = 0
    mass_cases = 0
    maximum_ratio = Fraction(0)
    for d in range(1, 81):
        for e in range(1, 81):
            common = math.gcd(d, e)
            for cutoff in range(1, 21):
                projected = sum(lambda_gcd(cutoff, v) for v in divisors(common))
                require(projected == int(common <= cutoff),
                        "row-gcd-projector", d, e, cutoff,
                        common, projected)
                checks += 1
                projector_cases += 1

    for e in range(1, 301):
        if mobius(e) == 0:
            continue
        bound = 3 ** omega(e)
        for cutoff in range(1, 41):
            mass = sum(abs(lambda_gcd(cutoff, v)) for v in divisors(e))
            require(mass <= bound,
                    "row-gcd-projector-mass", e, cutoff, mass, bound)
            checks += 1
            mass_cases += 1
            maximum_ratio = max(maximum_ratio, Fraction(mass, bound))
    return checks, {
        "projector_cases": projector_cases,
        "squarefree_column_mass_cases": mass_cases,
        "maximum_mass_over_3_to_omega": str(maximum_ratio),
        "identity": "1_{gcd(d,e)<=G}=sum_{v|d,e}lambda_G(v)",
    }


def centered(values: Sequence[int | Fraction]) -> tuple[list[Fraction], Fraction]:
    mean = sum((Fraction(value) for value in values), Fraction(0)) / len(values)
    return [Fraction(value) - mean for value in values], mean


def affine_correlation(
    f: Sequence[int | Fraction],
    g: Sequence[int | Fraction],
    a: int,
    s: int,
    h: int,
) -> Fraction:
    q = len(f)
    inverse_s = pow(s % q, -1, q)
    return sum(
        (
            Fraction(f[d])
            * Fraction(g[(inverse_s * (a * d + h)) % q])
            for d in range(q)
        ),
        Fraction(0),
    )


def norm_squared(values: Sequence[Fraction]) -> Fraction:
    return sum((value * value for value in values), Fraction(0))


def check_projective_plancherel() -> tuple[int, dict[str, object]]:
    checks = 0
    function_cases = 0
    product_lift_cases = 0
    primes = [3, 5, 7, 11, 13]
    maximum_energy = 0
    for q in primes:
        for seed in range(1, 8):
            f = [((seed * x * x + 3 * x + 2) % 9) - 4 for x in range(q)]
            g = [((2 * seed * x + x * x + 5) % 11) - 5 for x in range(q)]
            f0, mean_f = centered(f)
            g0, mean_g = centered(g)
            for h in range(1, q):
                left = Fraction(0)
                for a in range(1, q):
                    for s in range(1, q):
                        deviation = (
                            affine_correlation(f, g, a, s, h)
                            - q * mean_f * mean_g
                        )
                        left += deviation * deviation
                dilation = Fraction(0)
                for b in range(1, q):
                    value = sum(
                        (f0[d] * g0[(b * d) % q] for d in range(q)),
                        Fraction(0),
                    )
                    dilation += value * value
                right = q * norm_squared(f0) * norm_squared(g0) - dilation
                require(left == right,
                        "projective-plancherel", q, seed, h, left, right)
                checks += 1
                require(left <= q * norm_squared(f0) * norm_squared(g0),
                        "projective-plancherel-upper", q, seed, h, left)
                checks += 1
                maximum_energy = max(maximum_energy, left.numerator)
                function_cases += 1

                ell_set = [value for value in (1, 2, 4) if value < q]
                lifted = Fraction(0)
                for ell in ell_set:
                    for j in range(1, q):
                        for s in range(1, q):
                            deviation = (
                                affine_correlation(f, g, ell * j, s, h)
                                - q * mean_f * mean_g
                            )
                            lifted += deviation * deviation
                require(lifted == len(ell_set) * left,
                        "product-slope-lift", q, seed, h,
                        ell_set, lifted, left)
                checks += 1
                product_lift_cases += 1
    return checks, {
        "function_determinant_cases": function_cases,
        "product_slope_lift_cases": product_lift_cases,
        "largest_recorded_energy_numerator": maximum_energy,
        "normalization": "unnormalized l2 norm and unnormalized finite sum",
        "identity": (
            "sum_{a,s!=0}|C-q fbar gbar|^2 = "
            "q||f0||^2||g0||^2-sum_{b!=0}|sum_D f0(D)g0(bD)|^2"
        ),
    }


def legendre(n: int, q: int) -> int:
    n %= q
    if n == 0:
        return 0
    value = pow(n, (q - 1) // 2, q)
    return 1 if value == 1 else -1


def cyclic_autocorrelation(values: Sequence[int], shift: int) -> int:
    q = len(values)
    return sum(values[x] * values[(x + shift) % q] for x in range(q))


def check_legendre_coherent_line() -> tuple[int, dict[str, object]]:
    checks = 0
    line_cases = 0
    autocorrelation_cases = 0
    for q in (3, 5, 7, 11, 13, 17, 19, 23):
        f = [legendre(d, q) for d in range(q)]
        require(sum(f) == 0, "legendre-mean-zero", q, f)
        checks += 1
        for shift in range(q):
            value = cyclic_autocorrelation(f, shift)
            expected = q - 1 if shift == 0 else -1
            require(value == expected,
                    "legendre-autocorrelation", q, shift, value, expected)
            checks += 1
            autocorrelation_cases += 1

        for a0 in range(1, q):
            for s0 in range(1, q):
                h = (2 * a0 + 3 * s0) % q
                if h == 0:
                    h = 1
                inverse_a = pow(a0, -1, q)
                g = [
                    legendre(inverse_a * (s0 * u - h), q)
                    for u in range(q)
                ]
                require(sum(g) == 0,
                        "coherent-g-mean-zero", q, a0, s0, h, g)
                checks += 1
                correlation = affine_correlation(f, g, a0, s0, h)
                require(correlation == q - 1,
                        "coherent-line", q, a0, s0, h, correlation)
                checks += 1
                for shift in range(q):
                    value = cyclic_autocorrelation(g, shift)
                    expected = q - 1 if shift == 0 else -1
                    require(value == expected,
                            "coherent-g-autocorrelation",
                            q, a0, s0, h, shift, value, expected)
                    checks += 1
                    autocorrelation_cases += 1
                line_cases += 1
    return checks, {
        "coherent_line_cases": line_cases,
        "autocorrelation_cases": autocorrelation_cases,
        "coherent_value": "q-1",
        "fourier_flatness_certificate": (
            "cyclic autocorrelation is q-1 at zero and -1 off zero; "
            "finite-character orthogonality therefore gives |fhat(r)|^2=q "
            "for every nonzero r"
        ),
    }


def check_column_cauchy_schwarz() -> tuple[int, dict[str, object]]:
    checks = 0
    vector_cases = 0
    for length in range(1, 8):
        for seed in range(1, 31):
            gamma_left = [((seed + 2 * i) % 9) - 4 for i in range(length)]
            gamma_right = [((3 * seed + i) % 11) - 5 for i in range(length)]
            b_left = [((5 * seed + 3 * i) % 13) - 6 for i in range(length)]
            b_right = [((7 * seed + 4 * i) % 15) - 7 for i in range(length)]
            scalar_left = sum(x * y for x, y in zip(gamma_right, b_left))
            scalar_right = sum(x * y for x, y in zip(gamma_left, b_right))
            gamma_right_energy = sum(x * x for x in gamma_right)
            gamma_left_energy = sum(x * x for x in gamma_left)
            e_left = sum(x * x for x in b_left)
            e_right = sum(x * x for x in b_right)
            require(scalar_left * scalar_left <= gamma_right_energy * e_left,
                    "left-column-CS", length, seed, scalar_left,
                    gamma_right_energy, e_left)
            checks += 1
            require(scalar_right * scalar_right <= gamma_left_energy * e_right,
                    "right-column-CS", length, seed, scalar_right,
                    gamma_left_energy, e_right)
            checks += 1
            require((abs(scalar_left) + abs(scalar_right)) ** 2
                    <= 2 * (gamma_right_energy + gamma_left_energy)
                    * (e_left + e_right),
                    "two-polarization-CS", length, seed,
                    scalar_left, scalar_right)
            checks += 1
            vector_cases += 1
    return checks, {
        "finite_vector_cases": vector_cases,
        "transfer": (
            "row l2 scale Q times column-energy scale Q^3 gives "
            "amplitude scale Q^2 after square roots"
        ),
    }


def check_high_beta_ledger() -> tuple[int, dict[str, object]]:
    checks = 0
    beta = Fraction(267, 400)
    orbit = 1 - beta
    source_prime = Fraction(99979, 210000)
    opened_d = Fraction(10049, 52500)
    cutoff = Fraction(193, 500)
    reflected = 1 - cutoff
    ell_j = source_prime + orbit
    single_fiber = opened_d / 2
    missing = orbit - single_fiber
    drift_ratio = orbit - source_prime

    identities = [
        (orbit, Fraction(133, 400), "orbit-exponent"),
        (source_prime + opened_d, beta, "L-times-D-equals-Q"),
        (ell_j, Fraction(42451, 52500), "ell-j-slope"),
        (ell_j + opened_d, Fraction(1), "projected-slope-endpoint"),
        (reflected, Fraction(307, 500), "reflected-complement-range"),
        (single_fiber, Fraction(10049, 105000), "single-fiber-sqrt"),
        (missing, Fraction(49727, 210000), "single-fiber-gap"),
        (drift_ratio, Fraction(-15077, 105000), "drift-ratio-exponent"),
        (3 * beta - 2, Fraction(1, 400), "TPC32-flatness-energy-gate"),
    ]
    for actual, expected, label in identities:
        require(actual == expected, label, actual, expected)
        checks += 1

    return checks, {
        "beta": str(beta),
        "J_exponent": str(orbit),
        "L_exponent": str(source_prime),
        "D_exponent": str(opened_d),
        "T_exponent": str(cutoff),
        "reflected_s_max_exponent": str(reflected),
        "ell_j_exponent": str(ell_j),
        "ell_j_v_max_exponent": "1",
        "single_fiber_square_root_saving": str(single_fiber),
        "missing_exponent_after_single_fiber_sqrt": str(missing),
        "J_over_L_exponent": str(drift_ratio),
    }


def check_scope_flags() -> tuple[int, dict[str, bool]]:
    claims = {
        "finite_SL2_affine_normal_form": True,
        "finite_gcd_identities": True,
        "finite_mobius_gcd_layers": True,
        "finite_square_discriminant": True,
        "finite_balanced_origin_checks": True,
        "finite_reduced_origin_checks": True,
        "finite_local_squarefree_root_counts": True,
        "finite_exact_row_gcd_mask_projector": True,
        "finite_projected_affine_column_determinant": True,
        "finite_exact_projective_second_moment": True,
        "finite_exact_product_slope_lift": True,
        "finite_legendre_coherent_line_obstruction": True,
        "finite_column_Cauchy_Schwarz": True,
        "finite_high_beta_fraction_ledger": True,
        "uses_floating_point_roots_of_unity": False,
        "certifies_asymptotic_squarefree_error_term": False,
        "proves_signed_affine_mobius_cancellation": False,
        "proves_physical_Q3_column_energy": False,
        "proves_zero_frequency_flatness_ratio": False,
        "proves_complete_residual_closure": False,
        "proves_positivity": False,
        "proves_hardy_littlewood_asymptotic": False,
        "proves_twin_primes": False,
        "breaks_sieve_parity": False,
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

    count, affine_summary = check_affine_normal_form()
    checks += count
    subcounts["affine_normal_form_and_mobius_layers"] = count

    count, origin_summary = check_reduced_and_projected_origins()
    checks += count
    subcounts["reduced_and_projected_origins"] = count

    count, squarefree_summary = check_local_squarefree_roots()
    checks += count
    subcounts["local_squarefree_root_counts"] = count

    count, mask_summary = check_mask_projector()
    checks += count
    subcounts["actual_mask_gcd_projector"] = count

    count, projective_summary = check_projective_plancherel()
    checks += count
    subcounts["projective_plancherel_and_product_lift"] = count

    count, coherent_summary = check_legendre_coherent_line()
    checks += count
    subcounts["legendre_coherent_line"] = count

    count, transfer_summary = check_column_cauchy_schwarz()
    checks += count
    subcounts["column_cauchy_schwarz"] = count

    count, ledger_summary = check_high_beta_ledger()
    checks += count
    subcounts["high_beta_fraction_ledger"] = count

    count, claims = check_scope_flags()
    checks += count
    subcounts["scope_flags"] = count

    source_path = Path(__file__)
    source_bytes = source_path.read_bytes()
    normalized_source = source_bytes.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")
    source_hash = hashlib.sha256(normalized_source).hexdigest()
    payload = {
        "paper": "TPC-33",
        "certificate": "primitive affine columns",
        "description": (
            "finite exact regression for fixed-determinant affine normal "
            "forms, structured-mask projectors, projective second moments, "
            "product-slope lifts, coherent-line obstructions, and exact "
            "exponent ledgers; not evidence for asymptotic Mobius or "
            "prime-pair claims"
        ),
        "exact_check_count": checks,
        "subcheck_counts": subcounts,
        "affine_summary": affine_summary,
        "origin_summary": origin_summary,
        "squarefree_local_summary": squarefree_summary,
        "mask_summary": mask_summary,
        "projective_summary": projective_summary,
        "coherent_line_summary": coherent_summary,
        "column_transfer_summary": transfer_summary,
        "high_beta_summary": ledger_summary,
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
