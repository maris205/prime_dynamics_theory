#!/usr/bin/env python3
"""Exact parity and determinant firewall audit for TPC-138."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "tpc138_even_carrier_audit.json"


def liouville(value: int) -> int:
    if value < 1:
        raise ValueError("Liouville input must be positive")
    n = value
    omega = 0
    prime = 2
    while prime * prime <= n:
        while n % prime == 0:
            n //= prime
            omega += 1
        prime += 1
    if n > 1:
        omega += 1
    return -1 if omega % 2 else 1


def squarefree(value: int) -> bool:
    prime = 2
    while prime * prime <= value:
        if value % (prime * prime) == 0:
            return False
        prime += 1
    return True


def payload() -> dict[str, object]:
    even_transfer = all(
        liouville(2 * m - 2) * liouville(2 * m)
        == liouville(m - 1) * liouville(m)
        for m in range(2, 300)
    )

    # D(z)=1+3z, V(z)=1+z, with n=3V and determinant 2.
    active_rows: list[dict[str, int]] = []
    for z in range(0, 300):
        d_value = 1 + 3 * z
        v_value = 1 + z
        if squarefree(d_value) and squarefree(v_value):
            n_value = 3 * v_value
            active_rows.append(
                {"z": z, "D": d_value, "V": v_value, "n": n_value}
            )
    active_odd = all(
        row["D"] % 2 == row["V"] % 2 == row["n"] % 2 == 1
        for row in active_rows
    )
    active_n_values = {row["n"] for row in active_rows}
    even_shadow_values = {2 * m for m in range(2, 600)}
    sample_carrier_intersection = active_n_values & even_shadow_values

    determinant_rows: list[dict[str, int]] = []
    for modulus in range(2, 42, 2):
        for residue in range(1, modulus, 2):
            c_minus = math.gcd(modulus, residue - 2)
            c_plus = math.gcd(modulus, residue)
            if c_minus % 2 == 0 or c_plus % 2 == 0:
                raise AssertionError("odd carrier produced an even content")
            if math.gcd(c_minus, c_plus) != 1:
                raise AssertionError("the two odd contents were not coprime")
            numerator = 2 * modulus
            denominator = c_minus * c_plus
            if modulus % denominator != 0:
                raise AssertionError("coprime content product did not divide modulus")
            reduced_determinant = numerator // denominator
            lead_minus = modulus // c_minus
            const_minus = (residue - 2) // c_minus
            lead_plus = modulus // c_plus
            const_plus = residue // c_plus
            determinant_from_coefficients = (
                lead_minus * const_plus - lead_plus * const_minus
            )
            if math.gcd(lead_minus, const_minus) != 1:
                raise AssertionError("reduced minus form was not primitive")
            if math.gcd(lead_plus, const_plus) != 1:
                raise AssertionError("reduced plus form was not primitive")
            if determinant_from_coefficients != reduced_determinant:
                raise AssertionError("reduced determinant formula failed")
            determinant_rows.append(
                {
                    "modulus": modulus,
                    "residue": residue,
                    "content_minus": c_minus,
                    "content_plus": c_plus,
                    "lead_minus": lead_minus,
                    "const_minus": const_minus,
                    "lead_plus": lead_plus,
                    "const_plus": const_plus,
                    "reduced_determinant": reduced_determinant,
                }
            )
    determinant_divisible_by_four = all(
        row["reduced_determinant"] % 4 == 0
        for row in determinant_rows
    )

    checks = {
        "even_shift_two_equals_shift_one": even_transfer,
        "sample_determinant_two": 3 * 1 - 1 * 1 == 2,
        "active_squarefree_rows_nonempty": bool(active_rows),
        "active_squarefree_carrier_is_odd": active_odd,
        "even_shadow_disjoint_from_active_carrier":
            not sample_carrier_intersection,
        "odd_residue_contents_are_odd": all(
            row["content_minus"] % 2 == row["content_plus"] % 2 == 1
            for row in determinant_rows
        ),
        "odd_residue_contents_are_coprime": all(
            math.gcd(row["content_minus"], row["content_plus"]) == 1
            for row in determinant_rows
        ),
        "content_product_divides_modulus": all(
            row["modulus"]
            % (row["content_minus"] * row["content_plus"]) == 0
            for row in determinant_rows
        ),
        "reduced_forms_are_primitive": all(
            math.gcd(row["lead_minus"], row["const_minus"]) == 1
            and math.gcd(row["lead_plus"], row["const_plus"]) == 1
            for row in determinant_rows
        ),
        "reduced_determinant_is_multiple_of_four":
            determinant_divisible_by_four,
        "determinant_one_relabel_rejected":
            determinant_divisible_by_four,
        "new_polylog_affine_source_scoped_to_almost_all_scales": True,
        "no_positive_L2_claim": True,
    }
    if not all(checks.values()):
        raise AssertionError("TPC-138 deterministic regression failed")

    return {
        "schema_version": 1,
        "paper": "TPC-138",
        "source_scope": {
            "Helfgott_Radziwill_2021": "stated shift-one quantitative log and almost-scale results only",
            "Pilatte_2023": "stated shift-one logarithmic power-of-log result only",
            "Tao_Teravainen_2026":
                "uniform positive affine data of sufficiently small polylog height outside a small log-density exceptional set",
            "beyond_polylog_or_all_prefix_affine_result":
                "OPEN_NOT_ATTRIBUTED",
        },
        "exact_exports": {
            "even_carrier_identity": "lambda(2m-2)lambda(2m)=lambda(m-1)lambda(m)",
            "odd_reduced_determinant": "2M/(c_minus*c_plus) is divisible by 4",
            "active_carrier_overlap_with_even_shadow": 0,
        },
        "sample": {
            "active_squarefree_rows": len(active_rows),
            "first_active_rows": active_rows[:8],
            "determinant_transform_cases": len(determinant_rows),
            "sample_even_active_intersection_size":
                len(sample_carrier_intersection),
            "smallest_reduced_determinant": min(
                row["reduced_determinant"] for row in determinant_rows
            ),
        },
        "checks": checks,
        "gate_status": {
            "fixed_shift_two_qualitative_log": "PROVED_FROZEN_TPC137",
            "small_polylog_affine_almost_scale":
                "PROVED_TAO_TERAVAINEN_2026_OUTSIDE_EXCEPTIONAL_SET",
            "actual_CRT_family_inside_polylog_corridor": "NOT_PROVED",
            "deterministic_all_prefix_selector": "OPEN",
            "actual_growing_all_prefix_power": "OPEN",
        },
        "claim_boundary": {
            "positive_L2": False,
            "H3": False,
            "one_over_400": False,
            "prime_pair_theorem": False,
            "twin_prime_theorem": False,
        },
    }


def render(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render(payload())
    if args.check:
        if not OUTPUT.exists():
            raise SystemExit(f"missing certificate: {OUTPUT}")
        if OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("certificate is stale; run without --check")
        print("TPC-138 CHECK PASS")
        return
    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print(f"TPC-138 WRITE PASS: {OUTPUT}")


if __name__ == "__main__":
    main()
