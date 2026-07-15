"""Exact finite certificate for the TPC-18 algebraic reductions.

This program deliberately uses only finite integer and rational arithmetic.  It
checks identities and elementary counting bounds that organize the Mobius-tail
obstruction.  It does *not* sample prime correlations, estimate a limiting
constant, test a prime asymptotic, or provide evidence for the fixed-shift
Hardy--Littlewood or twin-prime conjectures.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Sequence


def require(condition: bool, message: str) -> None:
    """Raise independently of Python's optional assertion optimization."""

    if not condition:
        raise RuntimeError(message)


def prime_factorization(n: int) -> Dict[int, int]:
    """Return the exact prime factorization of a positive integer."""

    if n < 1:
        raise ValueError("n must be positive")
    factors: Dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            n //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def divisors(n: int) -> List[int]:
    """List the positive divisors of n."""

    answer = [1]
    for prime, exponent in prime_factorization(n).items():
        answer = [
            divisor * prime**power
            for divisor in answer
            for power in range(exponent + 1)
        ]
    return sorted(answer)


def mobius(n: int) -> int:
    factors = prime_factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def is_prime(n: int) -> bool:
    return n >= 2 and prime_factorization(n) == {n: 1}


def euler_phi(n: int) -> int:
    answer = n
    for prime in prime_factorization(n):
        answer -= answer // prime
    return answer


def radical(n: int) -> int:
    return math.prod(prime_factorization(n))


def tail_interval(d_0: int, v: int) -> List[int]:
    return list(range(d_0 + 1, v + 1))


def beta_tail(k: int, interval: Sequence[int]) -> int:
    return sum(mobius(d) for d in interval if k % d == 0)


def gamma_lcm(q: int, interval: Sequence[int]) -> int:
    """The direct lcm assembly coefficient Gamma_I(q)."""

    return sum(
        mobius(d) * mobius(e)
        for d in interval
        for e in interval
        if math.lcm(d, e) == q
    )


def gamma_inversion(q: int, interval: Sequence[int]) -> int:
    """Mobius inversion of beta_I(k)^2 = sum_{q|k} Gamma_I(q)."""

    return sum(
        mobius(q // divisor) * beta_tail(divisor, interval) ** 2
        for divisor in divisors(q)
    )


def gamma_gab(q: int, d_0: int, v: int) -> int:
    """Squarefree, pairwise-coprime g-a-b parameterization of Gamma."""

    answer = 0
    for g in divisors(q):
        quotient = q // g
        for a in divisors(quotient):
            b = quotient // a
            if g * a * b != q:
                continue
            if any(mobius(value) == 0 for value in (g, a, b)):
                continue
            if not (
                math.gcd(g, a) == math.gcd(g, b) == math.gcd(a, b) == 1
            ):
                continue
            if d_0 < g * a <= v and d_0 < g * b <= v:
                answer += mobius(a) * mobius(b)
    return answer


def gram_direct(interval: Sequence[int]) -> Fraction:
    return sum(
        (
            Fraction(mobius(d) * mobius(e), math.lcm(d, e))
            for d in interval
            for e in interval
        ),
        start=Fraction(0),
    )


def gram_diagonalized(interval: Sequence[int], v: int) -> Fraction:
    answer = Fraction(0)
    for r in range(1, v + 1):
        coordinate = sum(
            (Fraction(mobius(d), d) for d in interval if d % r == 0),
            start=Fraction(0),
        )
        answer += euler_phi(r) * coordinate * coordinate
    return answer


def fraction_record(value: Fraction) -> dict:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": str(value),
    }


def omega_endpoint(e: int, h_radical: int, d_0: int, v: int) -> int:
    return sum(
        mobius(f)
        for f in divisors(h_radical)
        if d_0 < e * f <= v
    )


def in_endpoint_bands(e: int, h_radical: int, d_0: int, v: int) -> bool:
    lower_band = h_radical * e > d_0 and e <= d_0
    upper_band = h_radical * e > v and e <= v
    return lower_band or upper_band


def nonprimitive_collapsed_beta(
    k: int, h_radical: int, d_0: int, v: int
) -> int:
    return sum(
        mobius(e) * omega_endpoint(e, h_radical, d_0, v)
        for e in divisors(k)
        if math.gcd(e, h_radical) == 1
    )


def crt_compatibility_expected(
    q: int, u: int, v: int, ell_1: int, ell_2: int, h: int
) -> bool:
    if math.gcd(ell_1, u) != 1 or math.gcd(ell_2, v) != 1:
        raise ValueError(
            "CRT criterion requires gcd(ell_1,u)=gcd(ell_2,v)=1"
        )
    return (
        h % math.gcd(q, u) == 0
        and h % math.gcd(q, v) == 0
        and (h * (ell_1 - ell_2)) % math.gcd(u, v) == 0
    )


def crt_solution_count(
    q: int, u: int, v: int, ell_1: int, ell_2: int, h: int
) -> int:
    """Count solutions in one complete period of the three congruences."""

    period = math.lcm(q, u, v)
    return sum(
        1
        for k in range(period)
        if k % q == 0
        and (ell_1 * k + h) % u == 0
        and (ell_2 * k + h) % v == 0
    )


def synthetic_entry(ell: int, d: int, j: int, h: int) -> int:
    """A deterministic integer array used only for the finite TT* identity."""

    return (ell * d * j + h) % 17 - 8


def finite_ttstar_certificate() -> dict:
    ell_values = [37, 41, 43]
    ell_weights = {37: 2, 41: 3, 43: 5}
    d_values = [7, 10, 11, 13, 14, 15, 17]
    j_values = list(range(1, 8))
    h = 6

    labels = [(ell, d) for ell in ell_values for d in d_values]
    entries = {
        (ell, d, j): ell_weights[ell]
        * mobius(d)
        * synthetic_entry(ell, d, j, h)
        for ell, d in labels
        for j in j_values
    }
    column_sums = {
        j: sum(entries[(ell, d, j)] for ell, d in labels) for j in j_values
    }
    energy = sum(value * value for value in column_sums.values())
    full_gram = sum(
        entries[(ell_1, d_1, j)] * entries[(ell_2, d_2, j)]
        for ell_1, d_1 in labels
        for ell_2, d_2 in labels
        for j in j_values
    )
    diagonal = sum(value * value for value in entries.values())
    off_diagonal = sum(
        entries[(ell_1, d_1, j)] * entries[(ell_2, d_2, j)]
        for ell_1, d_1 in labels
        for ell_2, d_2 in labels
        if (ell_1, d_1) != (ell_2, d_2)
        for j in j_values
    )
    total = sum(column_sums.values())
    cauchy_slack = len(j_values) * energy - total * total
    pair_difference_sum = sum(
        (column_sums[j_1] - column_sums[j_2]) ** 2
        for index, j_1 in enumerate(j_values)
        for j_2 in j_values[index + 1 :]
    )

    ttstar_holds = energy == full_gram == diagonal + off_diagonal
    finite_cauchy_holds = cauchy_slack == pair_difference_sum >= 0
    require(ttstar_holds, "finite TT* expansion failed")
    require(finite_cauchy_holds, "finite Cauchy identity failed")
    return {
        "array_kind": "synthetic deterministic integers; not prime data",
        "ell_values": ell_values,
        "d_values": d_values,
        "j_values": j_values,
        "column_sums": [column_sums[j] for j in j_values],
        "energy": energy,
        "full_gram": full_gram,
        "diagonal": diagonal,
        "off_diagonal": off_diagonal,
        "ttstar_identity_holds": ttstar_holds,
        "total_sum": total,
        "cauchy_slack": cauchy_slack,
        "pair_difference_sum": pair_difference_sum,
        "finite_cauchy_identity_holds": finite_cauchy_holds,
    }


def degenerate_channel_counts() -> dict:
    """Enumerate the three elementary exceptional geometric channels."""

    ell_values = [37, 41, 43, 47]
    d_values = list(range(7, 15))
    determinant_window = 3
    gcd_threshold = 3
    labels = [(ell, d) for ell in ell_values for d in d_values]

    source_primes_verified = all(is_prime(ell) for ell in ell_values)
    source_size_separation = min(ell_values) > max(d_values)
    require(source_primes_verified, "source list contains a composite")
    require(source_size_separation, "source/d size separation failed")

    same_source = 0
    near_determinant = 0
    large_gcd = 0
    generic = 0
    gcd_reduction_failures = 0
    equal_slope_failures = 0
    for ell_1, d_1 in labels:
        for ell_2, d_2 in labels:
            if (ell_1, d_1) == (ell_2, d_2):
                continue
            q_1 = ell_1 * d_1
            q_2 = ell_2 * d_2
            if ell_1 == ell_2:
                same_source += 1
                continue
            if math.gcd(q_1, q_2) != math.gcd(d_1, d_2):
                gcd_reduction_failures += 1
            if q_1 == q_2:
                equal_slope_failures += 1
            if 0 < abs(q_1 - q_2) <= determinant_window:
                near_determinant += 1
            elif math.gcd(d_1, d_2) > gcd_threshold:
                large_gcd += 1
            else:
                generic += 1

    same_source_formula = len(ell_values) * len(d_values) * (len(d_values) - 1)
    near_interval_bound = sum(
        math.floor(2 * determinant_window / d_2) + 1
        for _ell_1 in ell_values
        for _d_1 in d_values
        for d_2 in d_values
    )
    divisor_union_bound_for_d_pairs = sum(
        (
            sum(1 for d in d_values if d % g == 0)
        )
        ** 2
        for g in range(gcd_threshold + 1, max(d_values) + 1)
    )
    large_gcd_bound = (
        len(ell_values)
        * (len(ell_values) - 1)
        * divisor_union_bound_for_d_pairs
    )
    total_off_diagonal = len(labels) * (len(labels) - 1)
    partition_total = same_source + near_determinant + large_gcd + generic

    same_source_check = same_source == same_source_formula
    near_bound_check = near_determinant <= near_interval_bound
    large_gcd_bound_check = large_gcd <= large_gcd_bound
    geometric_reduction_check = (
        gcd_reduction_failures == equal_slope_failures == 0
    )
    partition_check = partition_total == total_off_diagonal
    all_counting_checks = all(
        (
            same_source_check,
            near_bound_check,
            large_gcd_bound_check,
            geometric_reduction_check,
            partition_check,
        )
    )
    require(all_counting_checks, "degenerate-channel count check failed")
    return {
        "ell_values": ell_values,
        "d_values": d_values,
        "determinant_window": determinant_window,
        "gcd_threshold": gcd_threshold,
        "source_primes_verified": source_primes_verified,
        "min_source_exceeds_max_d": source_size_separation,
        "ordered_off_diagonal_pairs": total_off_diagonal,
        "same_source": {
            "exact_count": same_source,
            "formula_count": same_source_formula,
        },
        "near_determinant": {
            "exact_count": near_determinant,
            "integer_interval_bound": near_interval_bound,
        },
        "large_gcd_away_from_near": {
            "exact_count": large_gcd,
            "divisor_union_bound": large_gcd_bound,
        },
        "generic_remainder_count": generic,
        "partition_total": partition_total,
        "gcd_q_equals_gcd_d_failure_count": gcd_reduction_failures,
        "distinct_source_equal_slope_failure_count": equal_slope_failures,
        "all_counting_checks_hold": all_counting_checks,
    }


def build_certificate() -> dict:
    d_0 = 6
    v = 18
    interval = tail_interval(d_0, v)
    q_limit = v * v

    gamma_direct_values = {
        q: gamma_lcm(q, interval) for q in range(1, q_limit + 1)
    }
    gamma_inversion_values = {
        q: gamma_inversion(q, interval) for q in range(1, q_limit + 1)
    }
    gamma_gab_values = {
        q: gamma_gab(q, d_0, v) for q in range(1, q_limit + 1)
    }
    gamma_failure_count = sum(
        not (
            gamma_direct_values[q]
            == gamma_inversion_values[q]
            == gamma_gab_values[q]
        )
        for q in range(1, q_limit + 1)
    )
    beta_identity_range = range(1, 4 * q_limit + 1)
    beta_lcm_failure_count = sum(
        beta_tail(k, interval) ** 2
        != sum(
            gamma_direct_values[q]
            for q in divisors(k)
            if q <= q_limit
        )
        for k in beta_identity_range
    )
    nonzero_gamma = {
        str(q): value for q, value in gamma_direct_values.items() if value != 0
    }
    nonsquarefree_gamma_failures = sum(
        gamma_direct_values[q] != 0
        for q in range(1, q_limit + 1)
        if mobius(q) == 0
    )

    gram_left = gram_direct(interval)
    gram_right = gram_diagonalized(interval, v)
    terminal_indices = [r for r in range(1, v + 1) if 2 * r > v]
    terminal_singleton_failures = [
        r
        for r in terminal_indices
        if [d for d in interval if d % r == 0] != [r]
    ]
    terminal_floor = sum(
        (
            Fraction(mobius(r) ** 2 * euler_phi(r), r * r)
            for r in terminal_indices
        ),
        start=Fraction(0),
    )

    box_limit = 840
    finite_box_direct = sum(
        beta_tail(k, interval) ** 2 for k in range(1, box_limit + 1)
    )
    finite_box_lcm = sum(
        gamma_direct_values[q] * (box_limit // q)
        for q in range(1, q_limit + 1)
    )
    finite_box_main = box_limit * gram_left
    finite_box_boundary = Fraction(finite_box_direct) - finite_box_main
    nonzero_interval_size = sum(mobius(d) != 0 for d in interval)
    elementary_boundary_bound = nonzero_interval_size**2
    gamma_l1_boundary_bound = sum(abs(value) for value in gamma_direct_values.values())

    h = 6
    h_radicals = [2, 3, 6]
    endpoint_sectors = {}
    endpoint_test_count = 0
    endpoint_identity_failures = 0
    endpoint_support_failure_count = 0
    for h_radical in h_radicals:
        sector_ks = [
            k
            for k in range(1, 361)
            if radical(math.gcd(k, h)) == h_radical
        ]
        sector_identity_failures = sum(
            beta_tail(k, interval)
            != nonprimitive_collapsed_beta(k, h_radical, d_0, v)
            for k in sector_ks
        )
        sector_support_failures = [
            e
            for e in range(1, 2 * v + 1)
            if omega_endpoint(e, h_radical, d_0, v) != 0
            and not in_endpoint_bands(e, h_radical, d_0, v)
        ]
        nonzero_omega = {
            str(e): omega_endpoint(e, h_radical, d_0, v)
            for e in range(1, 2 * v + 1)
            if omega_endpoint(e, h_radical, d_0, v) != 0
        }
        endpoint_test_count += len(sector_ks)
        endpoint_identity_failures += sector_identity_failures
        endpoint_support_failure_count += len(sector_support_failures)
        endpoint_sectors[str(h_radical)] = {
            "tested_k_count": len(sector_ks),
            "identity_failure_count": sector_identity_failures,
            "support_failure_count": len(sector_support_failures),
            "nonzero_omega": nonzero_omega,
        }

    ell_1, ell_2 = 11, 13
    crt_modulus_limit = 10
    crt_source_coprimality = (
        is_prime(ell_1)
        and is_prime(ell_2)
        and all(math.gcd(ell_1, u) == 1 for u in range(1, crt_modulus_limit + 1))
        and all(math.gcd(ell_2, model_v) == 1 for model_v in range(1, crt_modulus_limit + 1))
    )
    require(crt_source_coprimality, "CRT source-coprimality hypothesis failed")
    crt_test_count = 0
    crt_failure_count = 0
    crt_compatible_count = 0
    crt_incompatible_count = 0
    for q in range(1, crt_modulus_limit + 1):
        for u in range(1, crt_modulus_limit + 1):
            for model_v in range(1, crt_modulus_limit + 1):
                crt_test_count += 1
                expected = crt_compatibility_expected(
                    q, u, model_v, ell_1, ell_2, h
                )
                solution_count = crt_solution_count(
                    q, u, model_v, ell_1, ell_2, h
                )
                crt_compatible_count += int(expected)
                crt_incompatible_count += int(not expected)
                if solution_count != int(expected):
                    crt_failure_count += 1

    gamma_identity_holds = gamma_failure_count == 0
    beta_lcm_identity_holds = beta_lcm_failure_count == 0
    nonsquarefree_support_holds = nonsquarefree_gamma_failures == 0
    gram_identity_holds = gram_left == gram_right
    endpoint_floor_holds = (
        2 * d_0 < v
        and not terminal_singleton_failures
        and gram_left >= terminal_floor > 0
    )
    finite_box_identity_holds = (
        finite_box_direct == finite_box_lcm
        and finite_box_boundary == Fraction(finite_box_lcm) - finite_box_main
        and abs(finite_box_boundary) <= gamma_l1_boundary_bound
        and abs(finite_box_boundary) <= elementary_boundary_bound
    )
    endpoint_collapse_holds = (
        endpoint_identity_failures == 0 and endpoint_support_failure_count == 0
    )
    crt_compatibility_holds = crt_failure_count == 0

    require(gamma_identity_holds, "Gamma direct/inversion/gab identity failed")
    require(beta_lcm_identity_holds, "beta-squared lcm transform failed")
    require(nonsquarefree_support_holds, "Gamma squarefree support failed")
    require(gram_identity_holds, "Fraction Gram identity failed")
    require(endpoint_floor_holds, "terminal-octave floor failed")
    require(finite_box_identity_holds, "finite-box identity failed")
    require(endpoint_collapse_holds, "nonprimitive endpoint collapse failed")
    require(crt_compatibility_holds, "generalized CRT criterion failed")

    finite_ttstar = finite_ttstar_certificate()
    channel_counts = degenerate_channel_counts()
    all_checks_passed = all(
        (
            gamma_identity_holds,
            beta_lcm_identity_holds,
            nonsquarefree_support_holds,
            gram_identity_holds,
            endpoint_floor_holds,
            finite_box_identity_holds,
            endpoint_collapse_holds,
            crt_compatibility_holds,
            finite_ttstar["ttstar_identity_holds"],
            finite_ttstar["finite_cauchy_identity_holds"],
            channel_counts["all_counting_checks_hold"],
        )
    )
    require(all_checks_passed, "one or more certificate checks failed")

    certificate = {
        "certificate": "TPC-18 exact finite Mobius-tail determinant certificate",
        "scope": (
            "exact finite integer/rational identities and elementary counts only"
        ),
        "prime_asymptotic_evidence": False,
        "excluded_claims": [
            "no estimate of a residual-prime correlation",
            "no asymptotic distribution theorem for primes",
            "no fixed-shift Hardy--Littlewood asymptotic",
            "no evidence for the twin-prime conjecture",
            "no Kloosterman or spectral cancellation estimate",
        ],
        "parameters": {
            "D0": d_0,
            "V": v,
            "tail_interval": interval,
            "q_limit": q_limit,
        },
        "beta_squared_lcm_transform": {
            "k_range": [1, beta_identity_range.stop - 1],
            "failure_count": beta_lcm_failure_count,
            "identity_holds": beta_lcm_identity_holds,
        },
        "gamma_inversion_and_gab": {
            "q_range": [1, q_limit],
            "failure_count": gamma_failure_count,
            "nonsquarefree_support_failure_count": nonsquarefree_gamma_failures,
            "nonzero_gamma": nonzero_gamma,
            "gab_hypotheses": (
                "g, a, b are squarefree and pairwise coprime"
            ),
            "direct_equals_inversion_equals_gab": gamma_identity_holds,
        },
        "gram_fraction_identity": {
            "direct_lcm_sum": fraction_record(gram_left),
            "selberg_square_sum": fraction_record(gram_right),
            "identity_holds": gram_identity_holds,
        },
        "finite_box_sum": {
            "K": box_limit,
            "direct_integer_sum": finite_box_direct,
            "gamma_floor_sum": finite_box_lcm,
            "K_times_gram": fraction_record(finite_box_main),
            "exact_boundary_term": fraction_record(finite_box_boundary),
            "gamma_l1_absolute_boundary_bound": gamma_l1_boundary_bound,
            "elementary_absolute_boundary_bound": elementary_boundary_bound,
            "identity_holds": finite_box_identity_holds,
        },
        "endpoint_floor": {
            "terminal_indices": terminal_indices,
            "terminal_singleton_failure_count": len(
                terminal_singleton_failures
            ),
            "terminal_floor": fraction_record(terminal_floor),
            "gram": fraction_record(gram_left),
            "finite_inequality_holds": endpoint_floor_holds,
            "interpretation": (
                "a finite nonnegative-coordinate lower bound, not an asymptotic"
            ),
        },
        "nonprimitive_endpoint_collapse": {
            "h": h,
            "H_radicals": h_radicals,
            "tested_k_count": endpoint_test_count,
            "tested_k_range": [1, 360],
            "identity_failure_count": endpoint_identity_failures,
            "support_failure_count": endpoint_support_failure_count,
            "sectors": endpoint_sectors,
            "support_description": "(D0/H,D0] union (V/H,V]",
            "identity_and_support_hold": endpoint_collapse_holds,
        },
        "generalized_crt_compatibility": {
            "ell_1": ell_1,
            "ell_2": ell_2,
            "h": h,
            "q_u_v_range": [1, crt_modulus_limit],
            "source_coprimality_hypothesis_verified": crt_source_coprimality,
            "test_count": crt_test_count,
            "compatible_count": crt_compatible_count,
            "incompatible_count": crt_incompatible_count,
            "failure_count": crt_failure_count,
            "conditions": [
                "gcd(ell_1,u)=gcd(ell_2,v)=1",
                "gcd(q,u) divides h",
                "gcd(q,v) divides h",
                "gcd(u,v) divides h*(ell_1-ell_2)",
            ],
            "compatibility_and_unique_class_hold": crt_compatibility_holds,
        },
        "finite_ttstar": finite_ttstar,
        "degenerate_channel_counts": channel_counts,
        "all_checks_passed": all_checks_passed,
    }
    return certificate


def validate(certificate: dict) -> None:
    checks = (
        certificate["prime_asymptotic_evidence"] is False,
        certificate["beta_squared_lcm_transform"]["failure_count"] == 0,
        certificate["gamma_inversion_and_gab"]["failure_count"] == 0,
        certificate["gram_fraction_identity"]["identity_holds"],
        certificate["finite_box_sum"]["identity_holds"],
        certificate["endpoint_floor"]["finite_inequality_holds"],
        certificate["nonprimitive_endpoint_collapse"][
            "identity_and_support_hold"
        ],
        certificate["generalized_crt_compatibility"]["failure_count"] == 0,
        certificate["finite_ttstar"]["ttstar_identity_holds"],
        certificate["finite_ttstar"]["finite_cauchy_identity_holds"],
        certificate["degenerate_channel_counts"]["all_counting_checks_hold"],
        certificate["all_checks_passed"],
    )
    require(all(checks), "certificate validation failed")


def main() -> None:
    certificate = build_certificate()
    validate(certificate)
    output_path = Path(__file__).with_suffix(".json")
    output_path.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"TPC-18 exact finite certificate passed: {output_path}")
    print("No prime asymptotic evidence is claimed or tested.")


if __name__ == "__main__":
    main()
