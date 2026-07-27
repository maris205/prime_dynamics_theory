#!/usr/bin/env python3
"""Deterministic checks for the TPC-129 quantifier firewall."""

from __future__ import annotations

import argparse
import difflib
from fractions import Fraction
import json
import math
from pathlib import Path
import sys


def translated_tauberian(coordinates: list[Fraction], anchor: int) -> tuple[
    Fraction, Fraction
]:
    partial: list[Fraction] = []
    total = Fraction(0)
    for index, value in enumerate(coordinates, start=1):
        total += value / (anchor + index)
        partial.append(total)
    ordinary = sum(coordinates, Fraction(0))
    reconstructed = (anchor + len(coordinates)) * partial[-1] - sum(
        partial[:-1], Fraction(0)
    )
    return ordinary, reconstructed


def callable_masses(
    rho: list[int], weights: list[int]
) -> tuple[int, int, int]:
    """Return unweighted mass, literal weighted mass, and signed sum."""
    if len(rho) != len(weights):
        raise ValueError("rho and weights must have equal length")
    unweighted = sum(abs(value) for value in rho)
    weighted = sum(
        abs(value) * abs(weight)
        for value, weight in zip(rho, weights)
    )
    signed = sum(
        value * weight for value, weight in zip(rho, weights)
    )
    return unweighted, weighted, signed


def audit() -> dict:
    # Exact translated Tauberian identity.
    real_values = [
        Fraction((k % 5) - 2) for k in range(1, 31)
    ]
    imaginary_values = [
        Fraction(k % 3, 4) for k in range(1, 31)
    ]
    anchor = 17
    ordinary_real, reconstructed_real = translated_tauberian(
        real_values, anchor
    )
    ordinary_imag, reconstructed_imag = translated_tauberian(
        imaginary_values, anchor
    )
    tauberian_ok = (
        ordinary_real == reconstructed_real
        and ordinary_imag == reconstructed_imag
    )

    # Fixed residue substitution preserves nonzero determinant.
    a, s, d, u = 3, 5, 1, 1
    modulus, residue = 49, 11
    new_slope_d = s * modulus
    new_slope_v = a * modulus
    new_origin_d = d + s * residue
    new_origin_v = u + a * residue
    scaled_determinant_ok = (
        new_slope_d * new_origin_v
        - new_slope_v * new_origin_d
        == 2 * modulus
    )

    # Finite reciprocal/ordinary separation.
    x = 2_000_000
    omega = 400
    lower = x // omega
    middle = int(x / math.sqrt(omega))
    reciprocal = 0.0
    ordinary_window = 0
    for n in range(lower + 1, x + 1):
        sign = -1 if n <= middle else 1
        reciprocal += sign / n
        ordinary_window += sign
    reciprocal_small = abs(reciprocal) < 5.0 * omega / x
    ordinary_large = ordinary_window > 0.85 * x

    # A model slow diagonal: E_j(x)=j/x and J(x)=floor(sqrt(x)).
    diagonal_checks: list[Fraction] = []
    for x_model in (100, 10_000, 1_000_000):
        j_max = math.isqrt(x_model)
        diagonal_checks.append(
            max(
                Fraction(j, x_model)
                for j in range(1, j_max + 1)
            )
        )
    slow_diagonal_ok = (
        diagonal_checks[0] > diagonal_checks[1] > diagonal_checks[2]
        and diagonal_checks[2] <= Fraction(1, 1000)
    )

    # Final cancellation does not imply prefix cancellation.
    signs = [1] * 50 + [-1] * 50
    prefix = 0
    max_prefix = 0
    for sign in signs:
        prefix += sign
        max_prefix = max(max_prefix, abs(prefix))
    prefix_firewall_ok = prefix == 0 and max_prefix == 50

    # The callable theorem must state which absolute mass normalizes
    # the estimate.  A literal physical weight can change that mass.
    rho = [2, -1, 0, 3]
    weights = [1, 2, 5, -1]
    unweighted_mass, weighted_mass, signed_sum = callable_masses(
        rho, weights
    )
    callable_mass_definitions_ok = (
        unweighted_mass == 6
        and weighted_mass == 7
        and abs(signed_sum) <= weighted_mass
    )

    # A nonzero coefficient fiber can acquire zero literal mass when
    # its physical weight vanishes.  It is then a trivial zero case,
    # not a normalized positive-mass estimate.
    zero_rho = [1, -1, 2]
    zero_weights = [0, 0, 0]
    (
        zero_unweighted_mass,
        zero_weighted_mass,
        zero_signed_sum,
    ) = callable_masses(zero_rho, zero_weights)
    zero_mass_metadata_ok = (
        zero_unweighted_mass > 0
        and zero_weighted_mass == 0
        and zero_signed_sum == 0
    )

    result = {
        "translated_tauberian_identity": tauberian_ok,
        "residue_determinant_scaling": scaled_determinant_ok,
        "reciprocal_window_small": reciprocal_small,
        "ordinary_window_large": ordinary_large,
        "slow_diagonal_model": slow_diagonal_ok,
        "final_sum_not_all_prefixes": prefix_firewall_ok,
        "callable_mass_definitions": callable_mass_definitions_ok,
        "zero_mass_is_trivial_and_not_normalized": zero_mass_metadata_ok,
        "sample": {
            "reciprocal_sum": reciprocal,
            "ordinary_sum": ordinary_window,
            "diagonal_errors_exact": [
                str(value) for value in diagonal_checks
            ],
            "callable_mass": {
                "unweighted_definition": "sum_abs_rho",
                "weighted_definition": "sum_abs_rho_times_abs_weight",
                "unweighted_value": unweighted_mass,
                "weighted_value": weighted_mass,
                "signed_sum": signed_sum,
                "normalization": "declare which mass the theorem uses",
            },
            "zero_weighted_mass_case": {
                "unweighted_value": zero_unweighted_mass,
                "weighted_value": zero_weighted_mass,
                "signed_sum": zero_signed_sum,
                "status": "trivial_zero_excluded_from_normalized_maximum",
            },
        },
        "level": {
            "finite_firewalls": "L0",
            "fixed_form_logarithmic_corollary": "auxiliary L1",
            "actual_growing_prefix_power": "not proved",
        },
    }
    result["all_checks_passed"] = all(
        result[key]
        for key in (
            "translated_tauberian_identity",
            "residue_determinant_scaling",
            "reciprocal_window_small",
            "ordinary_window_large",
            "slow_diagonal_model",
            "final_sum_not_all_prefixes",
            "callable_mass_definitions",
            "zero_mass_is_trivial_and_not_normalized",
        )
    )
    return result


def serialized(output: dict) -> str:
    return json.dumps(output, indent=2, sort_keys=True) + "\n"


def check_or_write(path: Path, rendered: str, check: bool) -> bool:
    if not check:
        path.write_text(rendered, encoding="utf-8")
        return True
    if not path.exists():
        print(f"{path}: missing audit artifact", file=sys.stderr)
        return False
    current = path.read_text(encoding="utf-8")
    if current == rendered:
        return True
    print(f"{path}: stale audit artifact", file=sys.stderr)
    sys.stderr.writelines(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            rendered.splitlines(keepends=True),
            fromfile=str(path),
            tofile="generated",
        )
    )
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with the committed JSON without rewriting it",
    )
    args = parser.parse_args()
    output = audit()
    path = Path(__file__).with_suffix(".json")
    rendered = serialized(output)
    artifact_ok = check_or_write(path, rendered, args.check)
    print(rendered, end="")
    if not output["all_checks_passed"] or not artifact_ok:
        raise SystemExit(1)
