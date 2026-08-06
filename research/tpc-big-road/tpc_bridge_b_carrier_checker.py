#!/usr/bin/env python3
"""Exact read-only checker for the TPC Bridge-B sieve-carrier geometry.

The checker works only with finite primorial quotients and rational arithmetic.
It verifies the scaled-isometry and orthogonal-forcing identities used by the
symbolic proof in ``bridge_b_physical_intertwiner.md``.  It does not construct a
Logistic/Henon intertwiner and it does not supply arithmetic or TPC credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from typing import Iterable


REGISTRY = {
    "BRIDGE_B_ARITHMETIC_ADVANCE": "NO",
    "BRIDGE_B_BRATTELI_S_ADIC_AGING_CLOCK": "OPEN_RESERVE_RANK_GROWTH_FALSIFIER",
    "BRIDGE_B_CENTERED_ENERGY_RECURSION": "PROVED_EXACT_FINITE",
    "BRIDGE_B_CENTERED_SUBSPACE_INVARIANCE": "PROVED_EXACT_FINITE",
    "BRIDGE_B_EXACT_PAIR_REPLICATION_DELETION": "PROVED_EXACT_FINITE",
    "BRIDGE_B_FORCING_MEAN_ZERO": "PROVED_EXACT_FINITE",
    "BRIDGE_B_FORCING_ORTHOGONAL_TO_CENTERED_IMAGE": "PROVED_EXACT_FINITE",
    "BRIDGE_B_FULL_SPACE_COERCIVE_EXP_MIX_EXACT_INTERTWINER": "STOP_SCOPED_EXACT_SCALED_ISOMETRY_RATE_MISMATCH",
    "BRIDGE_B_FULL_SPACE_COERCIVE_EXP_MIX_NEGLIGIBLE_DEFECT": "STOP_SCOPED_EXACT_DUHAMEL_RATE_MISMATCH",
    "BRIDGE_B_HAAR_L2_GRAM": "PROVED_EXACT_FINITE",
    "BRIDGE_B_HENON_NATURAL_EXTENSION": "OPTIONAL_OPEN_EXACT_FACTOR_REQUIRED",
    "BRIDGE_B_METRIC_DBC_TO_NAMED_SEED": "STOP_SCOPED_FALSE_COUNTERMODEL",
    "BRIDGE_B_NORMALIZED_CENTERED_HAAR_CONTRACTION": "STOP_SCOPED_FALSE_EXACT_ENERGY_GROWTH",
    "BRIDGE_B_NORMALIZED_SCALED_ISOMETRY": "PROVED_EXACT_FINITE",
    "BRIDGE_B_PHYSICAL_OBSERVABLE_QUOTIENT_INTERTWINER": "SELECTED_OPEN_NEW_THEOREM",
    "BRIDGE_B_POINTED_DIRECT_GATE": "OPEN_ENDPOINT_EQUIVALENT_TARGET",
    "FIXED_ATOM_CREDIT": "0",
    "L2": "NONE",
    "STRICT_1_OVER_400": "UNPAID",
    "TPC_207_TRIGGER": "false",
}

EXPECTED_REGISTRY_SHA256 = "cc63154e3a1bb21513ed7b86fe30236133d110d48eef191bc3bfab7841bc9fb1"


def canonical_registry_bytes(registry: dict[str, str]) -> bytes:
    return "".join(f"{key}\t{registry[key]}\n" for key in sorted(registry)).encode("utf-8")


def registry_sha256(registry: dict[str, str]) -> str:
    return hashlib.sha256(canonical_registry_bytes(registry)).hexdigest()


def normalized_mean(values: Iterable[Fraction]) -> Fraction:
    data = list(values)
    if not data:
        raise AssertionError("empty finite quotient")
    return sum(data, Fraction()) / len(data)


def normalized_inner(left: list[Fraction], right: list[Fraction]) -> Fraction:
    if len(left) != len(right) or not left:
        raise AssertionError("incompatible finite quotient vectors")
    return sum((a * b for a, b in zip(left, right)), Fraction()) / len(left)


def normalized_norm_sq(values: list[Fraction]) -> Fraction:
    return normalized_inner(values, values)


def pair_mask(modulus: int) -> list[Fraction]:
    return [
        Fraction(int(math.gcd(r * (r + 2), modulus) == 1), 1)
        for r in range(modulus)
    ]


def replication_deletion(
    parent: list[Fraction], new_prime: int, *, delete_shift: bool = True
) -> list[Fraction]:
    modulus = len(parent)
    if new_prime <= 2 or any(new_prime % q == 0 for q in range(2, math.isqrt(new_prime) + 1)):
        raise AssertionError("new modulus factor must be an odd prime")
    if math.gcd(modulus, new_prime) != 1:
        raise AssertionError("new prime already divides the parent modulus")
    child = [Fraction() for _ in range(modulus * new_prime)]
    for residue, value in enumerate(parent):
        for copy_index in range(new_prime):
            lifted = residue + copy_index * modulus
            survives = lifted % new_prime != 0
            if delete_shift:
                survives = survives and (lifted + 2) % new_prime != 0
            if survives:
                child[lifted] = value
    return child


def centered_fixture(modulus: int, degree: int) -> list[Fraction]:
    raw = [Fraction(r**degree, 1) for r in range(modulus)]
    average = normalized_mean(raw)
    return [value - average for value in raw]


def exact_fixture(parent_modulus: int, new_prime: int) -> dict[str, str | int]:
    alpha = Fraction(new_prime - 2, new_prime)
    one_parent = [Fraction(1, 1)] * parent_modulus
    one_child = [Fraction(1, 1)] * (parent_modulus * new_prime)
    f = centered_fixture(parent_modulus, 1)
    g = centered_fixture(parent_modulus, 2)
    rf = replication_deletion(f, new_prime)
    rg = replication_deletion(g, new_prime)

    if normalized_inner(rf, rg) != alpha * normalized_inner(f, g):
        raise AssertionError("R_p^* R_p = alpha_p I failed")
    if normalized_mean(rf) != alpha * normalized_mean(f):
        raise AssertionError("mean scaling failed")
    if normalized_mean(rf) != 0:
        raise AssertionError("centered subspace was not preserved")
    if normalized_norm_sq(rf) / alpha != normalized_norm_sq(f):
        raise AssertionError("alpha^(-1/2) R_p was not an isometry")

    r_one = replication_deletion(one_parent, new_prime)
    forcing = [value - alpha for value in r_one]
    if normalized_mean(forcing) != 0:
        raise AssertionError("deletion forcing was not centered")
    if normalized_norm_sq(forcing) != alpha * (1 - alpha):
        raise AssertionError("deletion forcing energy failed")
    if normalized_inner(rf, forcing) != 0:
        raise AssertionError("forcing was not orthogonal to centered image")

    parent_pair = pair_mask(parent_modulus)
    child_pair = pair_mask(parent_modulus * new_prime)
    if replication_deletion(parent_pair, new_prime) != child_pair:
        raise AssertionError("pair replication-deletion identity failed")
    a_parent = normalized_mean(parent_pair)
    a_child = normalized_mean(child_pair)
    if a_child != alpha * a_parent:
        raise AssertionError("pair mass recursion failed")
    w_parent = [value - a_parent for value in parent_pair]
    w_child = [value - a_child for value in child_pair]
    rw_parent = replication_deletion(w_parent, new_prime)
    rhs = [value + a_parent * force for value, force in zip(rw_parent, forcing)]
    if w_child != rhs:
        raise AssertionError("forced-triangular centered recursion failed")
    expected_energy = (
        alpha * normalized_norm_sq(w_parent)
        + a_parent * a_parent * alpha * (1 - alpha)
    )
    if normalized_norm_sq(w_child) != expected_energy:
        raise AssertionError("orthogonal centered-energy recursion failed")
    if normalized_norm_sq(w_child) != a_child * (1 - a_child):
        raise AssertionError("indicator variance identity failed")

    false_alpha = Fraction(new_prime - 1, new_prime)
    one_deletion = replication_deletion(f, new_prime, delete_shift=False)
    if normalized_norm_sq(one_deletion) == alpha * normalized_norm_sq(f):
        raise AssertionError("one-deletion Gram mutation escaped")
    wrong_forcing = [value - false_alpha for value in r_one]
    if normalized_mean(wrong_forcing) == 0:
        raise AssertionError("wrong forcing-centering mutation escaped")
    normalized_linear_energy_ratio = normalized_norm_sq(rf) / (
        alpha * alpha * normalized_norm_sq(f)
    )
    if normalized_linear_energy_ratio != 1 / alpha or normalized_linear_energy_ratio <= 1:
        raise AssertionError("false normalized-contraction mutation escaped")

    return {
        "parent_modulus": parent_modulus,
        "new_prime": new_prime,
        "alpha": f"{alpha.numerator}/{alpha.denominator}",
        "forcing_norm_sq": (
            f"{(alpha * (1 - alpha)).numerator}/{(alpha * (1 - alpha)).denominator}"
        ),
        "normalized_linear_energy_ratio": (
            f"{normalized_linear_energy_ratio.numerator}/"
            f"{normalized_linear_energy_ratio.denominator}"
        ),
    }


def product_fixture() -> dict[str, str | int]:
    parent_modulus = 2
    vector = centered_fixture(parent_modulus, 1)
    initial_energy = normalized_norm_sq(vector)
    alpha_product = Fraction(1, 1)
    stages = 0
    for new_prime in (3, 5, 7, 11):
        alpha = Fraction(new_prime - 2, new_prime)
        vector = replication_deletion(vector, new_prime)
        parent_modulus *= new_prime
        alpha_product *= alpha
        stages += 1
        if normalized_norm_sq(vector) != alpha_product * initial_energy:
            raise AssertionError("multi-stage scaled-isometry product failed")
    return {
        "stages": stages,
        "terminal_modulus": parent_modulus,
        "raw_energy_ratio": f"{alpha_product.numerator}/{alpha_product.denominator}",
        "scaled_energy_ratio": "1/1",
    }


def run_check() -> dict[str, object]:
    digest = registry_sha256(REGISTRY)
    if EXPECTED_REGISTRY_SHA256 == "TO_BE_FILLED":
        raise AssertionError(f"registry hash not frozen: {digest}")
    if digest != EXPECTED_REGISTRY_SHA256:
        raise AssertionError("canonical V16 registry hash mismatch")

    fixtures = [
        exact_fixture(2, 3),
        exact_fixture(6, 5),
        exact_fixture(30, 7),
        exact_fixture(210, 11),
    ]
    product = product_fixture()
    return {
        "status": "PASS",
        "claim_level": "EXACT_FINITE_OPERATOR_GEOMETRY_NO_ARITHMETIC_ADVANCE",
        "fixtures": fixtures,
        "product_fixture": product,
        "identities": [
            "R_p^*R_p=(1-2/p)I",
            "mean(R_p f)=(1-2/p)mean(f)",
            "(1-2/p)^(-1/2)R_p is an isometry",
            "forcing is centered and orthogonal to R_p(V_k^0)",
            "W_(k+1)=R_pW_k+a_k forcing",
        ],
        "mutation_tests": {
            "one_deletion_instead_of_pair_deletion": "DETECTED",
            "wrong_forcing_center": "DETECTED",
            "false_normalized_contraction": "DETECTED",
        },
        "registry_rows": len(REGISTRY),
        "registry_sha256": digest,
        "arithmetic_advance": False,
        "tpc_207_trigger": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run exact read-only checks")
    parser.add_argument(
        "--registry-hash", action="store_true", help="print the canonical registry hash"
    )
    args = parser.parse_args()
    if args.registry_hash:
        print(registry_sha256(REGISTRY))
        return 0
    if not args.check:
        parser.error("use --check")
    print(json.dumps(run_check(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
