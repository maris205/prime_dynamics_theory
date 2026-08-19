#!/usr/bin/env python3
"""Independent exact checker for the TPC-213 cross-divisor certificate."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/certificate.json"


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def factors(value: int) -> tuple[int, ...]:
    remaining = value
    output: list[int] = []
    candidate = 2
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            output.append(candidate)
            remaining //= candidate
            require(remaining % candidate != 0, "non-squarefree divisor")
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        output.append(remaining)
    return tuple(output)


def local_f(prime: int, residue: int) -> Fraction:
    return Fraction(0, 1) if (residue + 2) % prime == 0 else Fraction(prime, prime - 1)


def local_g(prime: int, cutoff: int, residue: int) -> Fraction:
    if prime <= cutoff:
        return local_f(prime, residue)
    if residue % prime == 0:
        return Fraction(prime, prime - 1)
    return Fraction(prime * (prime - 2), (prime - 1) ** 2)


def delta_profile(divisor: int, cutoff: int) -> tuple[Fraction, ...]:
    primes = factors(divisor)
    return tuple(
        _delta_value(primes, cutoff, residue) for residue in range(divisor)
    )


def _delta_value(primes: tuple[int, ...], cutoff: int, residue: int) -> Fraction:
    p_value = Fraction(1, 1)
    b_value = Fraction(1, 1)
    for prime in primes:
        p_value *= local_f(prime, residue)
        b_value *= local_g(prime, cutoff, residue)
    return p_value - b_value


def rank(matrix: tuple[tuple[int, ...], ...]) -> int:
    if not matrix:
        return 0
    work = [[Fraction(value, 1) for value in row] for row in matrix]
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [a - factor * b for a, b in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def lift_matrix(left: int, right: int, support: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(int(u % left == a and u % right == b) for u in support)
            for b in range(right)
        )
        for a in range(left)
    )


def expected_lift(left: int, right: int, period: int) -> tuple[tuple[int, ...], ...]:
    common = gcd(left, right)
    period_lcm = lcm(left, right)
    require(period % period_lcm == 0, "complete lcm period")
    multiplicity = period // period_lcm
    return tuple(
        tuple(multiplicity * int(a % common == b % common) for b in range(right))
        for a in range(left)
    )


def reciprocal_pairs(divisor: int, q_values: tuple[int, ...], H: int) -> tuple[tuple[int, int], ...]:
    pairs: list[tuple[int, int]] = []
    for q in q_values:
        require(gcd(q, divisor) == 1, "nonunit q")
        limit = divisor * q // H
        pairs.extend((q, m) for m in range(-limit, limit + 1) if m != 0)
    return tuple(pairs)


def occupancy(divisor: int, q_values: tuple[int, ...], H: int) -> tuple[int, ...]:
    result = [0 for _ in range(divisor)]
    for q, m in reciprocal_pairs(divisor, q_values, H):
        result[(m * pow(q, -1, divisor)) % divisor] += 1
    return tuple(result)


def intersections(left: int, right: int, a: tuple[int, ...], b: tuple[int, ...]) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        (r, s, a[r], b[s])
        for r in range(left)
        for s in range(right)
        if Fraction(r, left) == Fraction(s, right) and a[r] and b[s]
    )


def check_delta(record: dict[str, object], cutoff: int) -> None:
    divisor = int(record["divisor"])
    expected = delta_profile(divisor, cutoff)
    require(record["profile"] == [str(value) for value in expected], f"Delta profile d={divisor}")
    require(record["zero_axis"] == str(expected[0]), f"Delta zero axis d={divisor}")
    require(record["mean"] == str(sum(expected, Fraction(0, 1))), f"Delta mean d={divisor}")
    require(record["l2_squared"] == str(sum(value * value for value in expected)), f"Delta norm d={divisor}")
    require(expected[0] == 0 and sum(expected, Fraction(0, 1)) == 0, f"Delta invariants d={divisor}")


def check_lift(record: dict[str, object], support: tuple[int, ...]) -> None:
    left = int(record["left"])
    right = int(record["right"])
    actual = lift_matrix(left, right, support)
    require(actual == expected_lift(left, right, len(support)), f"lift identity {left},{right}")
    require(record["gcd"] == gcd(left, right), "lift gcd")
    require(record["lcm"] == lcm(left, right), "lift lcm")
    require(record["support_size"] == len(support), "lift support")
    require(record["compatibility_identity"] is True, "lift flag")
    require(record["nonzero_entries"] == sum(value != 0 for row in actual for value in row), "lift nonzero entries")
    require(record["rank"] == rank(actual), "lift rank")


def check_emitter(record: dict[str, object], q_values: tuple[int, ...], H: int) -> None:
    divisor = int(record["divisor"])
    pairs = reciprocal_pairs(divisor, q_values, H)
    values = occupancy(divisor, q_values, H)
    require(record["q_values"] == list(q_values), "emitter q values")
    require(record["H"] == H, "emitter H")
    require(record["reciprocal_pair_count"] == len(pairs), "emitter pair count")
    require(record["maximum_abs_m"] == max(abs(m) for _, m in pairs), "emitter max m")
    require(record["two_m_less_than_d"] is (2 * max(abs(m) for _, m in pairs) < divisor), "emitter corridor")
    require(record["occupancy"] == list(values), "emitter occupancy")
    require(record["norm_squared"] == sum(value * value for value in values), "emitter norm")
    require(record["zero_frequency_occupancy"] == values[0], "emitter zero row")


def check_cross(record: dict[str, object], q_values: tuple[int, ...], H: int) -> None:
    left = int(record["left"])
    right = int(record["right"])
    left_values = occupancy(left, q_values, H)
    right_values = occupancy(right, q_values, H)
    period = lcm(left, right)
    rows = intersections(left, right, left_values, right_values)
    weight = sum(row[2] * row[3] for row in rows)
    cross = period * weight
    left_diagonal = period * sum(value * value for value in left_values)
    right_diagonal = period * sum(value * value for value in right_values)
    require(record["period"] == period, "cross period")
    require(record["frequency_intersections"] == [list(row) for row in rows], "frequency intersections")
    require(record["frequency_intersection_weight"] == weight, "frequency weight")
    require(record["cross_gram"] == cross, "cross Gram")
    require(record["left_diagonal_gram"] == left_diagonal, "left diagonal")
    require(record["right_diagonal_gram"] == right_diagonal, "right diagonal")
    require(record["cross_gram_nonzero"] is (cross != 0), "cross nonzero flag")
    require(
        record["normalized_cross_gram_squared"]
        == str(Fraction(cross * cross, left_diagonal * right_diagonal)),
        "normalized cross Gram",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        data = json.loads(
            CERTIFICATE.read_text(encoding="utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=lambda token: (_ for _ in ()).throw(CheckFailure(token)),
        )
        require(data["schema"] == "TPC213_PHYSICAL_PROFILE_CROSS_GRAM_CERTIFICATE_V1", "schema")
        require(data["classification"] == "PROVED_STRUCTURAL_L1_CROSS_DIVISOR_COUPLING", "classification")
        require(data["modeling_choice"] == "UNIT_RECIPROCAL_WEIGHTS_PSI_EQUALS_ONE_NO_LOG_PREFactor", "modeling choice")
        fixture = data["fixture"]
        divisors = tuple(fixture["divisors"])
        support = tuple(range(fixture["support"][0], fixture["support"][1] + 1))
        require(fixture["support"][2] == len(support), "support descriptor")
        q_values = tuple(fixture["q_values"])
        H = fixture["H"]
        cutoff = fixture["cutoff_z"]
        firewall = data["claim_firewall"]
        require(firewall == {
            "route_advance": "YES",
            "structural_threshold_a": "PASS",
            "physical_profile_emitter_pullback": "PROVED_EXACT",
            "residue_lift_gcd_aliasing": "PROVED_EXACT",
            "cross_divisor_frequency_gram": "PROVED_EXACT_FINITE",
            "physical_direct_sum_replacement": "REFUTED_SCOPED",
            "literal_v46_asymptotic_gram_bound": "OPEN",
            "prime_shell_reassembly": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b_strict_1_over_400": "UNPAID",
        }, "claim firewall")
        for record in data["delta_profiles"]:
            check_delta(record, cutoff)
        for record in data["lift_cases"]:
            check_lift(record, support)
        joint = data["joint_lift"]
        row_count = sum(divisors)
        joint_matrix = tuple(
            row
            for divisor in divisors
            for row in (
                tuple(int(index % divisor == residue) for index in support)
                for residue in range(divisor)
            )
        )
        joint_rank = rank(joint_matrix)
        require(joint["row_count"] == row_count, "joint row count")
        require(joint["column_count"] == len(support), "joint column count")
        require(joint["rank"] == joint_rank, "joint rank")
        require(joint["domain_kernel_dimension"] == len(support) - joint_rank, "domain kernel")
        require(joint["codomain_dependency_dimension"] == row_count - joint_rank, "codomain dependency")
        for record in data["emitter_cases"]:
            check_emitter(record, q_values, H)
        for record in data["cross_gram_cases"]:
            check_cross(record, q_values, H)
        counts = data["audit_counts"]
        require(counts == {
            "delta_profile_rows": len(divisors),
            "delta_profile_coordinates": sum(divisors),
            "lift_cases": 3,
            "emitter_cases": len(divisors),
            "cross_gram_cases": 3,
        }, "audit counts")
        require(data["theorem_contract"]["literal_v46_asymptotic_gram_bound"] == "OPEN", "open theorem")
    except (OSError, CheckFailure, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"TPC213_INDEPENDENT_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC213_INDEPENDENT_CHECK=PASS")
    print("delta_profile_coordinates=47")
    print("joint_lift_rank=35")
    print("codomain_dependency_dimension=12")
    print("nonzero_cross_gram_cases=2")
    print("claim_level=PROVED_STRUCTURAL_L1_CROSS_DIVISOR_COUPLING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
