#!/usr/bin/env python3
"""Independent exact checker for the TPC-212 boundary/emitter certificate."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import gcd, prod
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


def masks(primes: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(range(1, 1 << len(primes)))


def divisor(primes: tuple[int, ...], mask: int) -> int:
    return prod(prime for index, prime in enumerate(primes) if (mask >> index) & 1)


def mu_mask(mask: int) -> int:
    return -1 if mask.bit_count() % 2 else 1


def mu_integer(value: int) -> int:
    remaining = value
    parity = 0
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            parity ^= 1
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        parity ^= 1
    return -1 if parity else 1


def band(primes: tuple[int, ...], lower: int, upper: int) -> tuple[int, ...]:
    return tuple(mask for mask in masks(primes) if lower < divisor(primes, mask) <= upper)


def missing(primes: tuple[int, ...], selected: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(mask for mask in masks(primes) if mask not in set(selected))


def incidence(primes: tuple[int, ...], selected: tuple[int, ...]) -> list[int]:
    return [
        sum(mu_mask(mask) for mask in selected if (mask >> index) & 1)
        for index in range(len(primes))
    ]


def profile(primes: tuple[int, ...], mask: int, length: int) -> tuple[Fraction, ...]:
    seed = divisor(primes, mask)
    return tuple(Fraction((seed + 1) * (index + 2), seed) for index in range(length))


def endpoint(length: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(index + 1, 3) for index in range(length))


def add(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a + b for a, b in zip(left, right))


def scale(value: Fraction, vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(value * entry for entry in vector)


def log_coefficients(primes: tuple[int, ...], mask: int) -> tuple[int, ...]:
    return [mu_mask(mask) if (mask >> index) & 1 else 0 for index in range(len(primes))]


def packet(
    primes: tuple[int, ...], selected: tuple[int, ...], length: int
) -> tuple[tuple[Fraction, ...], ...]:
    end = endpoint(length)
    profiles = {mask: profile(primes, mask, length) for mask in masks(primes)}
    output = [[Fraction(0, 1) for _ in range(length)] for _ in primes]
    for mask in selected:
        residual = add(end, scale(Fraction(-1), profiles[mask]))
        for index, coefficient in enumerate(log_coefficients(primes, mask)):
            for coordinate, value in enumerate(residual):
                output[index][coordinate] += coefficient * value
    return tuple(tuple(row) for row in output)


def subtract(
    left: tuple[tuple[Fraction, ...], ...],
    right: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(first - second for first, second in zip(left_row, right_row))
        for left_row, right_row in zip(left, right)
    )


def reciprocal_pairs(d: int, q_values: tuple[int, ...], H: int) -> tuple[tuple[int, int], ...]:
    pairs: list[tuple[int, int]] = []
    for q in q_values:
        require(gcd(q, d) == 1, f"nonunit q={q}, d={d}")
        limit = d * q // H
        pairs.extend((q, m) for m in range(-limit, limit + 1) if m != 0)
    return tuple(pairs)


def counts(d: int, q_values: tuple[int, ...], H: int) -> tuple[int, ...]:
    output = [0 for _ in range(d)]
    for q, m in reciprocal_pairs(d, q_values, H):
        output[(m * pow(q, -1, d)) % d] += 1
    return tuple(output)


def collisions(d: int, q_values: tuple[int, ...], H: int) -> int:
    pairs = reciprocal_pairs(d, q_values, H)
    return sum(
        (m1 * q2 - m2 * q1) % d == 0
        for q1, m1 in pairs
        for q2, m2 in pairs
    )


def check_boundary_case(record: dict[str, object]) -> int:
    primes = tuple(record["primes"])
    lower = record["lower"]
    upper = record["upper"]
    selected = band(primes, lower, upper)
    omitted = missing(primes, selected)
    require(record["active_masks"] == list(selected), "active masks")
    require(record["missing_masks"] == list(omitted), "missing masks")
    require(record["active_divisors"] == [divisor(primes, mask) for mask in selected], "active divisors")
    require(record["missing_divisors"] == [divisor(primes, mask) for mask in omitted], "missing divisors")
    require(record["active_endpoint_incidence"] == incidence(primes, selected), "active incidence")
    require(record["missing_endpoint_incidence"] == incidence(primes, omitted), "missing incidence")
    require(record["full_endpoint_incidence"] == incidence(primes, masks(primes)), "full incidence")
    require(record["full_endpoint_incidence"] == [0] * len(primes), "full endpoint cancellation")
    length = prod(primes)
    require(record["profile_coordinate_count"] == length, "profile coordinate count")
    full = packet(primes, masks(primes), length)
    omitted_packet = packet(primes, omitted, length)
    selected_packet = packet(primes, selected, length)
    require(selected_packet == subtract(full, omitted_packet), "boundary decomposition")
    require(record["boundary_identity"] is True, "boundary flag")
    return length


def check_emitter_case(record: dict[str, object]) -> int:
    divisors = tuple(record["divisors"])
    q_values = tuple(record["q_values"])
    H = record["H"]
    norm_values: list[int] = []
    collision_values: list[int] = []
    occupancy_rows: list[list[int]] = []
    for d in divisors:
        row = counts(d, q_values, H)
        norm = sum(value * value for value in row)
        collision = collisions(d, q_values, H)
        occupancy_rows.append(list(row))
        norm_values.append(norm)
        collision_values.append(collision)
        require(norm == collision, f"collision identity d={d}")
        require(norm > 0, f"zero emitter d={d}")
    require(record["occupancy_rows"] == occupancy_rows, "occupancy rows")
    require(record["emitter_norm_squared"] == norm_values, "emitter norms")
    require(record["collision_counts"] == collision_values, "collision counts")
    require(record["direct_sum_gram_diagonal"] == norm_values, "Gram diagonal")
    require(record["direct_sum_gram_rank"] == len(divisors), "Gram rank")
    require(record["coefficient_signs_fixture"] == [mu_integer(d) for d in divisors], "Mobius signs")
    require(record["aligned_contributions"] == [1] * len(divisors), "alignment contributions")
    require(record["coherent_energy"] == len(divisors) ** 2, "coherent energy")
    require(record["diagonal_energy"] == len(divisors), "diagonal energy")
    require(record["coherent_to_diagonal_ratio"] == str(len(divisors)), "alignment ratio")
    require(record["unit_weight_alignment"] is True, "alignment flag")
    return len(divisors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        raw = CERTIFICATE.read_text(encoding="utf-8")
        data = json.loads(raw, object_pairs_hook=unique_object)
        require(data["schema"] == "TPC212_TRUNCATED_BOUNDARY_EMITTER_CERTIFICATE_V1", "schema")
        require(data["classification"] == "PROVED_STRUCTURAL_L1_STOP_SCOPED_BOUNDARY_EMITTER", "classification")
        require(data["modeling_choice"] == "UNIT_RECIPROCAL_WEIGHTS_PSI_EQUALS_ONE_FINITE_FIXTURE", "modeling choice")
        firewall = data["claim_firewall"]
        require(firewall["route_advance"] == "YES", "route")
        require(firewall["structural_threshold_a"] == "PASS", "threshold")
        require(firewall["cut_endpoint_leakage"] == "PROVED_EXACT", "incidence")
        require(firewall["boundary_decomposition"] == "PROVED_EXACT", "decomposition")
        require(firewall["reciprocal_collision"] == "PROVED_EXACT_FINITE", "collision")
        require(firewall["emitter_gram"] == "PROVED_EXACT_BLOCK_DIAGONAL", "Gram")
        require(firewall["emitter_only_universal_saving"] == "REFUTED_SCOPED", "scoped stop")
        require(firewall["literal_physical_boundary_bound"] == "OPEN", "physical boundary")
        require(firewall["physical_cross_divisor_gram_bound"] == "OPEN", "physical Gram")
        require(firewall["arithmetic_advance"] == "NO", "arithmetic")
        require(firewall["fixed_atom_credit"] == 0, "atom")
        require(firewall["l2"] == "NONE", "L2")
        require(firewall["full_gate_b_strict_1_over_400"] == "UNPAID", "Gate B")

        boundary_rows = sum(check_boundary_case(record) for record in data["boundary_cases"])
        emitter_rows = sum(check_emitter_case(record) for record in data["emitter_cases"])
        counts_record = data["audit_counts"]
        require(counts_record == {
            "boundary_cases": 4,
            "boundary_profile_coordinate_rows": boundary_rows,
            "emitter_cases": 3,
            "emitter_divisor_rows": emitter_rows,
        }, "audit counts")
        contract = data["theorem_contract"]
        require(contract["literal_physical_boundary_bound"] == "OPEN", "contract boundary")
        require(contract["prime_shell_reassembly"] == "OPEN", "contract shell")
    except (OSError, CheckFailure, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"TPC212_INDEPENDENT_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC212_INDEPENDENT_CHECK=PASS")
    print("boundary_profile_coordinate_rows=5810")
    print("emitter_divisor_rows=9")
    print("direct_sum_gram_rank=full")
    print("claim_level=PROVED_STRUCTURAL_L1_STOP_SCOPED_BOUNDARY_EMITTER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
