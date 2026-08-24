#!/usr/bin/env python3
"""Independent exact-rational checker for the TPC-241 certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "tpc241_certificate.json"
STATUS = "PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS"
OBJECT_KIND = (
    "Q_COLLAPSED_UNSIGNED_TOP_PRIME_COMMON_PROFILE_COEFFICIENT_"
    "AND_FINITE_WINDOW_ENERGY"
)
PROFILE_KIND = "FIXED_REAL_CINF_NONNEGATIVE_LE_ONE_SUPPORT_MINUS1_PLUS1_INTEGRAL_ONE"
FRAME_ORDER = "FULL_PRIMITIVE_VECTOR_FRAME_THEN_NONNEGATIVE_TOP_PRIME_RESTRICTION"


class IndependentFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise IndependentFailure(message)


def reject_constant(value: str) -> None:
    raise IndependentFailure("nonfinite JSON constant: " + value)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise IndependentFailure("duplicate JSON key: " + key)
        result[key] = value
    return result


def load_document() -> dict[str, Any]:
    require(CERTIFICATE.is_file(), "certificate missing")
    value = json.loads(
        CERTIFICATE.read_text(encoding="ascii"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, "top-level JSON type")
    return value


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")


def exact_fraction(record: object, expected: Fraction, label: str) -> None:
    require(type(record) is dict, label + " record type")
    require(set(record) == {"denominator", "identity", "numerator", "value"},
            label + " record keys")
    require(type(record["numerator"]) is int, label + " numerator type")
    require(type(record["denominator"]) is int and record["denominator"] > 0,
            label + " denominator")
    require(type(record["identity"]) is str and bool(record["identity"]),
            label + " identity")
    value = Fraction(record["numerator"], record["denominator"])
    require(value == expected and record["value"] == str(expected), label + " value")


def is_prime(value: int) -> bool:
    require(type(value) is int, "prime type")
    if value < 2:
        return False
    for divisor in range(2, isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def exact_weight(m: int, p: int, q: int, H: int) -> Fraction:
    scale = p * q
    numerator = scale * scale - H * H * m * m
    require(numerator >= 0, "weight support")
    return Fraction(numerator * numerator, scale**4)


def fraction_value(record: object, label: str) -> Fraction:
    require(type(record) is dict, label + " type")
    numerator = record.get("numerator")
    denominator = record.get("denominator")
    require(type(numerator) is int and type(denominator) is int and denominator > 0,
            label + " fraction fields")
    value = Fraction(numerator, denominator)
    require(record.get("value") == str(value), label + " string value")
    return value


def recompute_row(p: int, q_values: list[int], H: int) -> dict[str, object]:
    residue_weights: dict[int, Fraction] = {}
    direct = Fraction()
    mass = Fraction()
    atoms = 0
    for q in q_values:
        require(is_prime(q) and p < q, "shell prime")
        cutoff = p * q // H
        require(cutoff > 0 and 2 * cutoff < p, "primitive interval")
        inverse = pow(q, -1, p)
        seen: set[int] = set()
        for m in range(-cutoff, cutoff + 1):
            if m == 0:
                continue
            residue = m * inverse % p
            require(residue != 0 and residue not in seen, "fixed-q primitive injectivity")
            seen.add(residue)
            weight = exact_weight(m, p, q, H)
            residue_weights[residue] = residue_weights.get(residue, Fraction()) + weight
            direct += weight * weight
            mass += weight
            atoms += 1
    collapsed = sum((weight * weight for weight in residue_weights.values()), Fraction())
    floor = mass * mass / (p - 1)
    require(collapsed >= floor, "Cauchy")
    require(collapsed > direct, "positive collision excess")
    return {
        "atom_count": atoms,
        "cauchy_floor": floor,
        "collapsed_energy": collapsed,
        "collision_excess": collapsed - direct,
        "direct_energy": direct,
        "occupied_primitive_residues": len(residue_weights),
        "row_mass": mass,
    }


def check_fixture(fixture: object) -> int:
    require(type(fixture) is dict, "fixture type")
    require(set(fixture) == {
        "H", "Q", "U", "classification", "four_Q_less_than_H", "q_count",
        "q_values", "rows", "top_prime_rows", "U_less_than_Q"
    }, "fixture keys")
    Q, H, U = fixture["Q"], fixture["H"], fixture["U"]
    require((Q, H, U) == (101, 509, 97), "fixture scales")
    require(fixture["classification"] == "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
            "fixture classification")
    require(fixture["four_Q_less_than_H"] is True and fixture["U_less_than_Q"] is True,
            "fixture scale booleans")
    q_values = fixture["q_values"]
    require(type(q_values) is list and all(type(q) is int for q in q_values),
            "q list type")
    expected_q = [q for q in range(Q + 1, 2 * Q + 1) if is_prime(q)]
    require(q_values == expected_q and fixture["q_count"] == len(q_values),
            "q-shell census")
    rows = fixture["rows"]
    require(type(rows) is list and len(rows) == fixture["top_prime_rows"] == 3,
            "row count")
    for row in rows:
        require(type(row) is dict, "row type")
        require(set(row) == {
            "atom_count", "cauchy_floor", "cauchy_pass", "classification",
            "collapsed_energy", "collision_excess", "collision_excess_positive",
            "direct_energy", "occupied_primitive_residues", "p", "primitive_support",
            "q_count", "row_mass"
        }, "row keys")
        p = row["p"]
        require(type(p) is int and is_prime(p) and U // 2 < p <= U, "top p")
        expected = recompute_row(p, q_values, H)
        for field in ("atom_count", "occupied_primitive_residues"):
            require(row[field] == expected[field] and type(row[field]) is int,
                    "row integer " + field)
        for field in (
            "cauchy_floor", "collapsed_energy", "collision_excess",
            "direct_energy", "row_mass"
        ):
            require(fraction_value(row[field], field) == expected[field],
                    "row fraction " + field)
        require(row["cauchy_pass"] is True and row["collision_excess_positive"] is True,
                "row booleans")
        require(row["primitive_support"] is True and row["q_count"] == len(q_values),
                "row support/count")
        require(row["classification"] == "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
                "row classification")
    return len(rows)


def run() -> None:
    document = load_document()
    require(type(document.get("certificate_version")) is int
            and document["certificate_version"] == 1, "certificate version")
    digest = document.get("payload_sha256")
    require(type(digest) is str and len(digest) == 64, "payload digest type")
    payload = dict(document)
    del payload["payload_sha256"]
    require(hashlib.sha256(canonical_json(payload)).hexdigest() == digest,
            "payload digest mismatch")
    require(CERTIFICATE.read_bytes() == canonical_json(document) + b"\n",
            "noncanonical certificate bytes")

    ledger = document["exact_fraction_ledger"]
    require(type(ledger) is dict, "ledger type")
    constant = Fraction(9, 4) * Fraction(399, 400) * 3
    collision = 4 * Fraction(1, 3) - 2 * Fraction(21, 32)
    direct = 2 * Fraction(1, 3) - Fraction(21, 32)
    depth = Fraction(133, 400) + Fraction(1, 3) - Fraction(21, 32)
    defect = 4 * Fraction(133, 400) - 2
    exact_fraction(ledger["H_exponent"], Fraction(21, 32), "H")
    exact_fraction(ledger["Q_exponent"], Fraction(1, 3), "Q")
    exact_fraction(ledger["U_exponent"], Fraction(133, 400), "U")
    exact_fraction(ledger["coefficient_constant"], constant, "coefficient constant")
    exact_fraction(ledger["collision_exponent"], collision, "collision exponent")
    exact_fraction(ledger["direct_exponent"], direct, "direct exponent")
    exact_fraction(ledger["finite_window_constant"], constant / 2, "window constant")
    exact_fraction(ledger["frame_defect_exponent"], defect, "frame defect")
    exact_fraction(ledger["log_ratio"], Fraction(399, 400), "log ratio")
    exact_fraction(ledger["row_depth_exponent"], depth, "row depth")
    exact_fraction(ledger["row_error_exponent"], -depth, "row error")

    lock = document["object_lock"]
    require(type(lock) is dict and lock["main_object"] == OBJECT_KIND, "object lock")
    require(lock["profile_class"] == PROFILE_KIND, "profile lock")
    require(lock["coefficient"] == "C_p=-log(p)/p", "coefficient lock")
    require(lock["frame_order"] == FRAME_ORDER, "frame-order lock")
    require(lock["p_domain"] == "PRIMES_U_OVER_2_LT_P_LE_U", "p lock")
    require(lock["q_domain"] == "PRIMES_Q_LT_Q_LE_2Q", "q lock")

    theorem = document["theorem"]
    require(theorem["classification"] == "PROVED", "theorem class")
    require("10773*log(2)/1600" in theorem["coefficient_liminf"], "coefficient theorem")
    require("10773*log(2)/3200" in theorem["finite_window_liminf"], "window theorem")
    require("DELTA_POSITIVE" in theorem["fixed_power_refutation"], "delta quantifier")
    require("PROFILEWISE" in theorem["quantifier"], "profilewise quantifier")

    markers = document["markers"]
    require(markers["TPC241_STATUS"] == STATUS, "status")
    require(markers["TPC241_ARITHMETIC_ADVANCE"] == "NO", "arithmetic firewall")
    require(type(markers["TPC241_FIXED_ATOM_CREDIT"]) is int
            and markers["TPC241_FIXED_ATOM_CREDIT"] == 0, "fixed atom")
    require(markers["TPC241_L2"] == "NONE", "L2 firewall")
    require(markers["TPC241_FULL_GATE_B"] == "OPEN", "Gate-B firewall")
    require(markers["TPC241_STRICT_1_OVER_400"] == "UNPAID_GLOBAL", "strict firewall")

    firewall = document["scope_firewall"]
    require(firewall["PHYSICAL_WINDOW_CROSS_TERM_DELETION"] == "FORBIDDEN",
            "frame-order firewall")
    require(firewall["SIGNED_C_H_CANCELLATION"] == "NONE", "signed firewall")
    require(firewall["SIGNED_FOUR_PACKET_PROJECTION"] == "OPEN", "packet firewall")
    require(firewall["FINITE_FIXTURE_IS_THEOREM_EVIDENCE"] is False,
            "fixture evidence firewall")
    mutations = document["mutation_firewalls"]
    require(type(mutations["rejected_count"]) is int
            and mutations["rejected_count"] == len(mutations["rejected"]) == 11,
            "mutation count")

    rows = check_fixture(document["finite_fixture"])
    print("TPC241_INDEPENDENT_CHECK=PASS")
    print("constant=" + str(constant))
    print("collision_exponent=" + str(collision))
    print("finite_window_constant=" + str(constant / 2))
    print("recomputed_collision_rows=" + str(rows))
    print("signed_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC241_INDEPENDENT_CHECK=FAIL: use --check")
    try:
        run()
    except (IndependentFailure, KeyError, TypeError, ValueError, OSError) as error:
        raise SystemExit("TPC241_INDEPENDENT_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
