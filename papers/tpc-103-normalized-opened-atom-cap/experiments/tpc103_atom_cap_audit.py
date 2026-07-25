#!/usr/bin/env python3
"""Deterministic finite regression for the TPC-103 factor audit.

This checks exact projector and source/child identities plus the
six-ledger schema.  It is not evidence for asymptotic cancellation.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass


def mobius(n: int) -> int:
    value = n
    sign = 1
    p = 2
    while p * p <= value:
        if value % p == 0:
            value //= p
            sign = -sign
            if value % p == 0:
                return 0
            while value % p == 0:
                value //= p
        p += 1
    if value > 1:
        sign = -sign
    return sign


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def projector_lambda(v: int, cutoff: int) -> int:
    return sum(mobius(v // g) for g in divisors(v) if g <= cutoff)


@dataclass(frozen=True)
class Child:
    polarization: str
    ell: int
    moving_d: int
    opposite_d: int
    j: int
    u: int
    sigma: int
    v: int
    residue: int
    t: int


def make_child(
    polarization: str,
    ell: int,
    moving_d: int,
    opposite_d: int,
    j: int,
    u: int,
    sigma: int,
    v: int,
) -> Child:
    residues = [
        r for r in range(sigma) if (ell * j * v * r + 1) % sigma == 0
    ]
    if len(residues) != 1:
        raise AssertionError("canonical residue is not unique")
    residue = residues[0]
    if moving_d % v:
        raise AssertionError("v does not divide moving row")
    quotient = moving_d // v
    if (quotient - residue) % sigma:
        raise AssertionError("source is not on the child progression")
    t = (quotient - residue) // sigma
    recovered_d = v * (residue + sigma * t)
    recovered_u = (ell * j * v * residue + 1) // sigma + ell * j * v * t
    if (recovered_d, recovered_u) != (moving_d, u):
        raise AssertionError("child-to-source round trip failed")
    return Child(
        polarization,
        ell,
        moving_d,
        opposite_d,
        j,
        u,
        sigma,
        v,
        residue,
        t,
    )


def main() -> None:
    projector_checks = 0
    for d in range(1, 49):
        for e in range(1, 49):
            common = math.gcd(d, e)
            for cutoff in range(1, 13):
                lhs = sum(projector_lambda(v, cutoff) for v in divisors(common))
                rhs = int(common <= cutoff)
                if lhs != rhs:
                    raise AssertionError((d, e, cutoff, lhs, rhs))
                projector_checks += 1

    roundtrip_checks = 0
    for polarization in ("L", "R"):
        for ell in (2, 3, 5, 7):
            for moving_d in range(1, 36):
                for opposite_d in range(1, 16):
                    for j in range(1, 8):
                        target = ell * moving_d * j + 1
                        for u in divisors(target):
                            sigma = target // u
                            if sigma == 1 or math.gcd(ell * j, sigma) != 1:
                                continue
                            for v in divisors(math.gcd(moving_d, opposite_d)):
                                if math.gcd(ell * j * v, sigma) != 1:
                                    continue
                                make_child(
                                    polarization,
                                    ell,
                                    moving_d,
                                    opposite_d,
                                    j,
                                    u,
                                    sigma,
                                    v,
                                )
                                roundtrip_checks += 1

    ledgers = {
        "physical_rows": ["gamma_left", "gamma_right"],
        "opened_logarithmic_leg": ["mu_u", "log_u"],
        "matched_prefix": ["half_prefix"],
        "row_gcd_projector": ["lambda_G_v", "projector_mask"],
        "exact_content": [
            "mu_kappa",
            "mu_B",
            "squarefree_D",
            "squarefree_V",
            "content_masks",
        ],
        "local_smooth": [
            "fixed_period",
            "residue",
            "smooth",
            "interval",
            "actual_support",
            "active_divisibility",
            "global_normalization_once",
        ],
    }
    upstream_factor_universe = {
        "gamma_left",
        "gamma_right",
        "mu_u",
        "log_u",
        "half_prefix",
        "lambda_G_v",
        "projector_mask",
        "mu_kappa",
        "mu_B",
        "squarefree_D",
        "squarefree_V",
        "content_masks",
        "fixed_period",
        "residue",
        "smooth",
        "interval",
        "actual_support",
        "active_divisibility",
        "global_normalization_once",
    }
    flattened = [factor for values in ledgers.values() for factor in values]
    if len(flattened) != len(set(flattened)):
        raise AssertionError("factor assigned to more than one ledger")
    if set(flattened) != upstream_factor_universe:
        raise AssertionError("ledger union differs from upstream factor universe")

    result = {
        "schema": "tpc-103-opened-atom-cap-audit-v1",
        "status": "PASS",
        "checks": {
            "projector_identities": projector_checks,
            "source_child_roundtrips": roundtrip_checks,
            "factor_categories": len(flattened),
            "factor_ledgers": len(ledgers),
        },
        "claim_boundary": {
            "finite_regression_only": True,
            "literal_atom_cap_proved_in_paper": True,
            "principal_mass_bound": False,
            "cross_map_bound": False,
            "new_L2_fixed_shift_estimate": False,
            "parity_breakthrough": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
