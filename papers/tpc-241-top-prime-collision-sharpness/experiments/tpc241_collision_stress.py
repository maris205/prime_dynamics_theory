#!/usr/bin/env python3
"""Independent finite collision stresses for TPC-241."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import isqrt


class StressFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise StressFailure(message)


def is_prime(value: int) -> bool:
    require(type(value) is int, "prime type")
    if value < 2:
        return False
    for divisor in range(2, isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def primes_between(lower: int, upper: int) -> list[int]:
    return [value for value in range(lower + 1, upper + 1) if is_prime(value)]


def weight(profile: str, m: int, p: int, q: int, H: int) -> Fraction:
    t_num = H * abs(m)
    t_den = p * q
    require(t_num <= t_den, "support")
    base = Fraction(t_den * t_den - t_num * t_num, t_den * t_den)
    if profile == "QUADRATIC_BUMP":
        return base * base
    if profile == "QUARTIC_BUMP":
        return base**4
    raise StressFailure("unknown profile")


def stress_row(profile: str, p: int, q_values: list[int], H: int) -> dict[str, object]:
    aggregate: dict[int, Fraction] = {}
    direct = Fraction()
    mass = Fraction()
    fixed_q_rows = 0
    for q in q_values:
        cutoff = p * q // H
        require(cutoff > 0 and 2 * cutoff < p, "primitive interval")
        inverse = pow(q, -1, p)
        seen: set[int] = set()
        for m in range(-cutoff, cutoff + 1):
            if m == 0:
                continue
            residue = m * inverse % p
            require(residue != 0 and residue not in seen, "fixed-q injectivity")
            seen.add(residue)
            value = weight(profile, m, p, q, H)
            aggregate[residue] = aggregate.get(residue, Fraction()) + value
            direct += value * value
            mass += value
        fixed_q_rows += 1
    collapsed = sum((value * value for value in aggregate.values()), Fraction())
    cauchy = mass * mass / (p - 1)
    require(collapsed >= cauchy, "post-collapse Cauchy")
    require(collapsed > direct, "no collision excess")
    return {
        "cauchy_ratio_at_least_one": collapsed / cauchy >= 1,
        "collision_excess_positive": collapsed - direct > 0,
        "fixed_q_rows": fixed_q_rows,
        "occupied_residues": len(aggregate),
        "p": p,
        "profile": profile,
    }


def run_scale(Q: int, H: int, U: int) -> dict[str, object]:
    require(4 * Q < H and U < Q, "scale inequalities")
    q_values = primes_between(Q, 2 * Q)
    p_values = primes_between(U // 2, U)
    require(bool(q_values) and bool(p_values), "empty prime shell")
    rows: list[dict[str, object]] = []
    for profile in ("QUADRATIC_BUMP", "QUARTIC_BUMP"):
        for p in p_values:
            if p * q_values[0] // H > 0:
                rows.append(stress_row(profile, p, q_values, H))
    require(bool(rows), "no active stress rows")
    return {
        "H": H,
        "Q": Q,
        "U": U,
        "active_rows": len(rows),
        "all_cauchy": all(row["cauchy_ratio_at_least_one"] is True for row in rows),
        "all_collision_positive": all(row["collision_excess_positive"] is True for row in rows),
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "profiles": 2,
        "q_count": len(q_values),
    }


def run() -> None:
    scales = [(29, 149, 23), (43, 223, 41), (61, 307, 59), (101, 509, 97)]
    records = [run_scale(*scale) for scale in scales]
    require(all(record["all_cauchy"] is True for record in records), "Cauchy stress")
    require(all(record["all_collision_positive"] is True for record in records),
            "collision stress")
    payload = {
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "records": records,
        "scales": len(records),
        "status": "PASS",
    }
    print("TPC241_COLLISION_STRESS=PASS")
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC241_COLLISION_STRESS=FAIL: use --check")
    try:
        run()
    except (StressFailure, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC241_COLLISION_STRESS=FAIL: " + str(error))


if __name__ == "__main__":
    main()
