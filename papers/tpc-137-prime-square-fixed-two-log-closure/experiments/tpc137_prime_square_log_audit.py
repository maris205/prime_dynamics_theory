#!/usr/bin/env python3
"""Deterministic exact audit for the TPC-137 prime-square closure."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "tpc137_prime_square_log_audit.json"


def primes_up_to(limit: int) -> list[int]:
    out: list[int] = []
    for value in range(2, limit + 1):
        if all(value % prime for prime in out if prime * prime <= value):
            out.append(value)
    return out


def mobius(value: int) -> int:
    n = value
    sign = 1
    prime = 2
    while prime * prime <= n:
        if n % prime == 0:
            n //= prime
            sign = -sign
            if n % prime == 0:
                return 0
            while n % prime == 0:
                n //= prime
        prime += 1
    if n > 1:
        sign = -sign
    return sign


def divisors(value: int) -> list[int]:
    return [candidate for candidate in range(1, value + 1) if value % candidate == 0]


def squarefree_indicator(value: int) -> int:
    prime = 2
    while prime * prime <= value:
        if value % (prime * prime) == 0:
            return 0
        prime += 1
    return 1


def prime_square_mask(value: int, cutoff: int) -> int:
    result = 1
    for prime in primes_up_to(cutoff):
        result *= 1 - int(value % (prime * prime) == 0)
    return result


def expanded_prime_square_mask(value: int, cutoff: int) -> int:
    primorial = math.prod(primes_up_to(cutoff))
    return sum(
        mobius(k)
        for k in divisors(primorial)
        if value % (k * k) == 0
    )


def feasible_residues(
    *,
    k: int,
    ell: int,
    period: int,
    d: int,
    s: int,
    u: int,
    a: int,
) -> tuple[int, list[int]]:
    modulus = math.lcm(period, k * k, ell * ell)
    residues = [
        z
        for z in range(modulus)
        if (d + s * z) % (k * k) == 0
        and (u + a * z) % (ell * ell) == 0
    ]
    return modulus, residues


def reduced_affine_record(
    *,
    residue: int,
    modulus: int,
    d: int,
    s: int,
    u: int,
    a: int,
) -> dict[str, int]:
    lead_d = s * modulus
    const_d = d + s * residue
    lead_v = a * modulus
    const_v = u + a * residue
    content_d = math.gcd(lead_d, const_d)
    content_v = math.gcd(lead_v, const_v)
    reduced_lead_d = lead_d // content_d
    reduced_const_d = const_d // content_d
    reduced_lead_v = lead_v // content_v
    reduced_const_v = const_v // content_v
    reduced_determinant = (
        reduced_lead_d * reduced_const_v
        - reduced_lead_v * reduced_const_d
    )
    return {
        "residue": residue,
        "modulus": modulus,
        "content_D": content_d,
        "content_V": content_v,
        "reduced_D_lead": reduced_lead_d,
        "reduced_D_const": reduced_const_d,
        "reduced_V_lead": reduced_lead_v,
        "reduced_V_const": reduced_const_v,
        "reduced_determinant": reduced_determinant,
    }


def payload() -> dict[str, object]:
    # D(z)=1+3z, V(z)=1+z has 3*1-1*1=2.
    d, s, u, a = 1, 3, 1, 1
    cutoff = 5
    period = 4
    sample_limit = 360
    prime_list = primes_up_to(cutoff)
    primorial = math.prod(prime_list)
    squarefree_divisors = [k for k in divisors(primorial) if mobius(k) != 0]

    identity_ok = all(
        prime_square_mask(value, cutoff)
        == expanded_prime_square_mask(value, cutoff)
        for value in range(1, sample_limit + 1)
    )

    component_moduli: list[int] = []
    reduction_rows: list[dict[str, int]] = []
    feasible_components = 0
    for k in squarefree_divisors:
        for ell in squarefree_divisors:
            modulus, residues = feasible_residues(
                k=k,
                ell=ell,
                period=period,
                d=d,
                s=s,
                u=u,
                a=a,
            )
            if residues:
                feasible_components += 1
                component_moduli.append(modulus)
                reduction_rows.extend(
                    reduced_affine_record(
                        residue=residue,
                        modulus=modulus,
                        d=d,
                        s=s,
                        u=u,
                        a=a,
                    )
                    for residue in residues
                )
            expected_upper = period * math.lcm(k, ell) ** 2
            if modulus > expected_upper:
                raise AssertionError("combined modulus exceeded period*lcm(k,ell)^2")

    interval = range(0, 240)
    interval_length = len(interval)
    y_bound = max(d + s * z for z in interval)
    exact_product_tail = sum(
        abs(
            squarefree_indicator(d + s * z)
            * squarefree_indicator(u + a * z)
            - prime_square_mask(d + s * z, cutoff)
            * prime_square_mask(u + a * z, cutoff)
        )
        for z in interval
    )
    union_majorant = 0
    one_form_root_counts_valid = True
    for prime in primes_up_to(math.isqrt(y_bound) + 1):
        if prime <= cutoff:
            continue
        d_count = sum(
            int((d + s * z) % (prime * prime) == 0)
            for z in interval
        )
        v_count = sum(
            int((u + a * z) % (prime * prime) == 0)
            for z in interval
        )
        union_majorant += d_count + v_count
        one_form_root_counts_valid = one_form_root_counts_valid and (
            d_count <= interval_length // (prime * prime) + 1
            and v_count <= interval_length // (prime * prime) + 1
        )
    if exact_product_tail > union_majorant:
        raise AssertionError("prime-square union tail failed")

    reductions_primitive = all(
        math.gcd(row["reduced_D_lead"], row["reduced_D_const"]) == 1
        and math.gcd(row["reduced_V_lead"], row["reduced_V_const"]) == 1
        for row in reduction_rows
    )
    reduced_determinant_formula = all(
        row["reduced_determinant"]
        * row["content_D"]
        * row["content_V"]
        == row["modulus"] * (s * u - a * d)
        for row in reduction_rows
    )
    reduced_determinants_nonzero = all(
        row["reduced_determinant"] != 0
        for row in reduction_rows
    )

    checks = {
        "determinant_two": s * u - a * d == 2,
        "prime_square_identity_exact": identity_ok,
        "prime_square_mask_is_boolean": all(
            prime_square_mask(value, cutoff) in {0, 1}
            for value in range(1, sample_limit + 1)
        ),
        "full_squarefree_difference_supported_on_large_prime_squares":
            exact_product_tail <= union_majorant,
        "one_form_large_prime_square_count_checked":
            one_form_root_counts_valid,
        "combined_modulus_bound_checked": bool(component_moduli),
        "component_pair_bound_checked":
            len(squarefree_divisors) ** 2 == 4 ** len(prime_list),
        "residue_reductions_are_primitive": reductions_primitive,
        "reduced_determinant_formula_exact": reduced_determinant_formula,
        "reduced_determinants_are_nonzero": reduced_determinants_nonzero,
        "no_power_or_L2_claim": True,
    }
    if not all(checks.values()):
        raise AssertionError("TPC-137 deterministic regression failed")

    return {
        "schema_version": 1,
        "paper": "TPC-137",
        "scope": {
            "carrier": "fixed determinant-two affine pair",
            "h0": 2,
            "data_growth": "fixed before x tends to infinity",
            "periodic_coefficient": True,
            "physical_weight": False,
            "all_prefix_uniformity": False,
        },
        "sample": {
            "forms": {"D": [d, s], "V": [u, a], "determinant": 2},
            "prime_cutoff": cutoff,
            "primes": prime_list,
            "primorial": primorial,
            "period": period,
            "component_pairs": len(squarefree_divisors) ** 2,
            "feasible_components": feasible_components,
            "largest_feasible_combined_modulus": max(component_moduli),
            "universal_combined_modulus_upper": period * primorial ** 2,
            "exact_product_tail": exact_product_tail,
            "large_prime_square_union_majorant": union_majorant,
            "residue_reduction_cases": len(reduction_rows),
            "smallest_absolute_reduced_determinant": min(
                abs(row["reduced_determinant"])
                for row in reduction_rows
            ),
        },
        "theorem_record": {
            "external_input": "Tao2016 fixed-affine terminal logarithmic theorem",
            "cutoff_order": "fix P; let x->infinity; then let P->infinity",
            "conclusion": "full-mu fixed-periodic qualitative logarithmic cancellation",
            "rate_kind": "o(1)",
            "x_power_exponent": 0,
            "evidence_level": "FROZEN_L1",
        },
        "checks": checks,
        "claim_boundary": {
            "growing_affine_uniformity": False,
            "ordinary_all_prefix_bound": False,
            "positive_L2": False,
            "H3": False,
            "twin_prime_theorem": False,
        },
    }


def render(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the committed JSON without writing",
    )
    args = parser.parse_args()
    expected = render(payload())
    if args.check:
        if not OUTPUT.exists():
            raise SystemExit(f"missing certificate: {OUTPUT}")
        actual = OUTPUT.read_text(encoding="utf-8")
        if actual != expected:
            raise SystemExit("certificate is stale; run without --check")
        print("TPC-137 CHECK PASS")
        return
    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print(f"TPC-137 WRITE PASS: {OUTPUT}")


if __name__ == "__main__":
    main()
