#!/usr/bin/env python3
"""Exact rational regression for the TPC-104 disintegration."""

from __future__ import annotations

from fractions import Fraction
import json


PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)


def width(q: int, n: int) -> int:
    return min((q - 1) // 2, q // n)


def rho(q: int, n: int) -> Fraction:
    return Fraction(2 * width(q, n), q - 1)


def main() -> None:
    coefficient_checks = 0
    endpoint_checks = 0
    for q in PRIMES:
        for n in range(1, q + 1):
            value = rho(q, n)
            if value < Fraction(1, n):
                raise AssertionError(("lower", q, n, value))
            if value > Fraction(2 * q, (q - 1) * n):
                raise AssertionError(("upper", q, n, value))
            if n in (1, 2):
                if value != 1 or width(q, n) != (q - 1) // 2:
                    raise AssertionError(("endpoint", q, n, value))
                endpoint_checks += 1
            else:
                if width(q, n) != q // n:
                    raise AssertionError(("long-width", q, n))
            coefficient_checks += 1

    if width(3, 3) != 1 or rho(3, 3) != 1:
        raise AssertionError("q=3 full-width degeneracy")
    degenerate_full_width_checks = 1

    family_checks = 0
    for q in PRIMES:
        branches: list[tuple[int, list[int]]] = []
        for n in range(1, q + 1):
            weights = [1 + ((q + n + 3 * z) % 7) for z in range(n)]
            branches.append((n, weights))
        principal = sum(
            rho(q, n) * sum(weights) for n, weights in branches
        )
        endpoint = sum(
            sum(weights) for n, weights in branches if n <= 2
        )
        inverse_length = sum(
            Fraction(sum(weights), n)
            for n, weights in branches
            if n >= 3
        )
        exact = endpoint + sum(
            Fraction(2 * (q // n), q - 1) * sum(weights)
            for n, weights in branches
            if n >= 3
        )
        if principal != exact:
            raise AssertionError(("disintegration", q))
        if not (
            endpoint + inverse_length
            <= principal
            <= endpoint + Fraction(2 * q, q - 1) * inverse_length
        ):
            raise AssertionError(("equivalence", q))
        family_checks += 1

    countermodel_checks = 0
    for q in PRIMES:
        for branch_count in (1, 2, 5, 11):
            for n in range(3, q + 1):
                long_mass = branch_count
                principal = branch_count * n * rho(q, n)
                if not (
                    long_mass <= principal <= 3 * long_mass
                ):
                    raise AssertionError(("long-countermodel", q, n))
                countermodel_checks += 1
            endpoint = branch_count
            principal_endpoint = branch_count * rho(q, 1)
            if endpoint != principal_endpoint:
                raise AssertionError(("endpoint-countermodel", q))
            countermodel_checks += 1

    result = {
        "schema": "tpc-104-principal-mass-audit-v1",
        "status": "PASS",
        "checks": {
            "coefficient_inequalities": coefficient_checks,
            "endpoint_identities": endpoint_checks,
            "degenerate_full_width_identities": degenerate_full_width_checks,
            "weighted_family_disintegrations": family_checks,
            "sharp_countermodel_identities": countermodel_checks,
        },
        "claim_boundary": {
            "finite_exact_certificate": True,
            "literal_disintegration_proved_in_paper": True,
            "endpoint_mass_target_proved": False,
            "inverse_length_mass_target_proved": False,
            "positive_route_stopped": False,
            "new_L2_fixed_shift_estimate": False,
            "parity_breakthrough": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
