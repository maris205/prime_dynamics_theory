#!/usr/bin/env python3
"""Independent exact replay of the TPC-224 certificate.

This file intentionally does not import the producer.  It reconstructs the
prime shells, literal rows, channel sums, and sharp inequality independently,
then compares the resulting rational fields with the stored certificate.
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import gcd
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results" / "certificate.json"
PACKET_SLOPES = (0, 1, -1, 2)
PACKET_COUNT = 4


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor += 1
    return True


def shell(Q: int) -> tuple[int, ...]:
    return tuple(q for q in range(Q + 1, 2 * Q + 1) if prime(q))


def parameters(Q: int, clock: str) -> tuple[int, int, int]:
    if clock == "source_surrogate":
        return Q**3, 4 * Q**2, 4 * Q
    if clock == "collision_stress":
        return Q**3, 5 * Q, 5
    raise CheckFailure(f"unknown clock {clock}")


def active(Q: int, clock: str) -> tuple[int, ...]:
    values = shell(Q)
    if clock == "source_surrogate":
        return values
    return tuple(q for q in values if q % 5 == 1)


def row_vectors(Q: int, clock: str, profile: str):
    _, H, h = parameters(Q, clock)
    values = active(Q, clock)
    output = {}
    for q in values:
        require(gcd(q, h) == 1, "non-unit prime")
        inverse = pow(q, -1, h)
        cutoff = h * q // H
        require(cutoff >= 1, "empty cutoff")
        for packet in range(PACKET_COUNT):
            vector = {}
            for m in range(-cutoff, cutoff + 1):
                if m == 0 or gcd(m, h) != 1:
                    continue
                if profile == "constant":
                    value = Fraction(1)
                elif profile == "affine":
                    value = Fraction(1) + Fraction(PACKET_SLOPES[packet] * H * m, 10 * h * q)
                else:
                    raise CheckFailure("unknown profile")
                coordinate = (h, (m * inverse) % h)
                vector[coordinate] = vector.get(coordinate, Fraction(0)) + value / h
            require(bool(vector), "empty row")
            output[(q, packet)] = vector
    return output, values, h, H


def add(vectors):
    result = {}
    for vector in vectors:
        for coordinate, value in vector.items():
            result[coordinate] = result.get(coordinate, Fraction(0)) + value
            if result[coordinate] == 0:
                del result[coordinate]
    return result


def norm(vector):
    return sum((value * value for value in vector.values()), Fraction(0))


def replay_record(record: dict[str, object]) -> dict[str, object]:
    Q = int(record["Q"])
    clock = record["clock"]
    profile = record["profile"]
    vectors, primes, h, H = row_vectors(Q, clock, profile)
    by_packet = [add(vectors[(q, packet)] for q in primes) for packet in range(PACKET_COUNT)]
    by_prime = [add(vectors[(q, packet)] for packet in range(PACKET_COUNT)) for q in primes]
    full = add(vectors.values())
    E_diag = sum((norm(vector) for vector in vectors.values()), Fraction(0))
    E_AP = sum((norm(vector) for vector in by_packet), Fraction(0))
    E_pol = sum((norm(vector) for vector in by_prime), Fraction(0))
    E_all = norm(full)
    count = len(primes)
    sharp = Fraction(count * PACKET_COUNT, count + PACKET_COUNT)
    return {
        "Q": Q,
        "x": Q**3,
        "H": H,
        "h": h,
        "clock": clock,
        "profile": profile,
        "prime_count": count,
        "prime_values": list(primes),
        "packet_count": PACKET_COUNT,
        "cutoffs": sorted({h * q // H for q in primes}),
        "coordinate_count": len({c for vector in vectors.values() for c in vector}),
        "shared_normalization": "C_h=1/h",
        "E_diag": str(E_diag),
        "E_AP": str(E_AP),
        "E_pol": str(E_pol),
        "E_all": str(E_all),
        "sharp_constant": str(sharp),
        "unit_ratio": str(E_all / (E_AP + E_pol)),
        "sharp_ratio": str(E_all / (sharp * (E_AP + E_pol))),
        "sharp_bound_residual": str(sharp * (E_AP + E_pol) - E_all),
        "unit_interface_holds": E_all <= E_AP + E_pol,
        "sharp_interface_holds": E_all <= sharp * (E_AP + E_pol),
        "support_is_shared": True,
    }


def check_record(observed: dict[str, object], expected: dict[str, object]) -> None:
    require(type(observed) is dict, "record is not an object")
    require(observed == expected, f"record mismatch at Q={expected['Q']}, clock={expected['clock']}")


def main() -> int:
    try:
        data = json.loads(CERTIFICATE.read_text())
        require(data["schema"] == "tpc224-literal-two-channel-compatibility-audit-v1", "schema")
        require(data["status"] == "PASS", "status")
        require(data["claim_level"] == "PROVED_STRUCTURAL_L1", "claim level")
        require(data["author"] == "Liang Wang", "author")
        require(data["affiliation"] == "Huazhong University of Science and Technology", "affiliation")
        theorem = data["theorem"]
        require(theorem["common_vector_interface"] == "PROVED_EXACT", "theorem interface")
        require(theorem["sharp_additive_constant"] == "PJ/(P+J)", "sharp constant")
        require(theorem["unit_constant_interface"] == "REFUTED_SCOPED", "unit firewall")
        firewall = data["firewall"]
        require(firewall["arithmetic_advance"] == "NO", "arithmetic firewall")
        require(firewall["fixed_atom_credit"] == 0, "atom firewall")
        require(firewall["l2"] == "NONE", "L2 firewall")
        require(firewall["full_gate_b"] == "OPEN", "Gate B firewall")
        require(firewall["strict_1_over_400"] == "UNPAID", "strict firewall")
        source = data["source_clock"]
        stress = data["collision_stress_clock"]
        require(source["clock"] == "source_surrogate", "source clock")
        require(stress["clock"] == "collision_stress", "stress clock")
        require(source["classification"].startswith("MODELING_CHOICE"), "source classification")
        require(stress["classification"].startswith("MODELING_CHOICE"), "stress classification")
        source_expected = [replay_record(record) for record in source["records"]]
        stress_expected = [replay_record(record) for record in stress["records"]]
        require(source["records"] == source_expected, "source records")
        require(stress["records"] == stress_expected, "stress records")
        require(all(record["sharp_ratio"] != "0" for record in source_expected), "source ratio")
        require(all(record["sharp_ratio"] == "1" for record in stress_expected), "stress sharpness")
        require(all(record["unit_interface_holds"] is False for record in stress_expected), "stress unit bound")
        require(all(record["sharp_bound_residual"] == "0" for record in stress_expected), "stress residual")
        aligned = data["aligned_fixture"]
        require(aligned[1]["unit_interface_refuted"] is True, "aligned adversary")
        require(aligned[1]["sharp_equality"] is True, "aligned sharpness")
        require(all(type(value) is bool and value for value in data["checks"].values()), "check flags")
    except (CheckFailure, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"TPC224_INDEPENDENT_CHECK=FAIL: {error}")
        return 1
    print("TPC224_INDEPENDENT_CHECK=PASS")
    print(f"source_scales={len(source_expected)}")
    print(f"stress_scales={len(stress_expected)}")
    print("sharp_constant=PJ/(P+J)")
    print("arithmetic_advance=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
