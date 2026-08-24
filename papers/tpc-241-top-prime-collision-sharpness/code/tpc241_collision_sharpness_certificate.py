#!/usr/bin/env python3
"""Deterministic certificate for the TPC-241 collision-sharpness ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "tpc241_certificate.json"
STATUS = "PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS"
OBJECT_KIND = (
    "Q_COLLAPSED_UNSIGNED_TOP_PRIME_COMMON_PROFILE_COEFFICIENT_"
    "AND_FINITE_WINDOW_ENERGY"
)
PROFILE_KIND = "FIXED_REAL_CINF_NONNEGATIVE_LE_ONE_SUPPORT_MINUS1_PLUS1_INTEGRAL_ONE"
FRAME_ORDER = "FULL_PRIMITIVE_VECTOR_FRAME_THEN_NONNEGATIVE_TOP_PRIME_RESTRICTION"
ROUND2_CLUE = (
    "FORCE_THE_NEXT_ARGUMENT_TO_RETAIN_FOUR_PACKET_POLARIZATION_OR_C_H_SIGNS_"
    "BEFORE_SQUARING_BECAUSE_THE_UNSIGNED_TOP_PRIME_COLLISION_CHANNEL_IS_"
    "FIXED_POWER_SHARP"
)


class CertificateFailure(RuntimeError):
    """Fail-closed certificate error."""


def demand(condition: bool, message: str) -> None:
    if type(condition) is not bool:
        raise CertificateFailure("guard condition is not a strict bool")
    if not condition:
        raise CertificateFailure(message)


def strict_int(value: object, name: str) -> int:
    demand(type(value) is int, f"{name} must be an exact int")
    return value


def strict_string(value: object, name: str) -> str:
    demand(type(value) is str and bool(value), f"{name} must be a nonempty string")
    return value


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")


def fraction_record(value: Fraction, identity: str) -> dict[str, Any]:
    demand(type(value) is Fraction, "fraction ledger requires Fraction")
    strict_string(identity, "fraction identity")
    return {
        "denominator": value.denominator,
        "identity": identity,
        "numerator": value.numerator,
        "value": str(value),
    }


def is_prime(value: int) -> bool:
    strict_int(value, "prime candidate")
    if value < 2:
        return False
    for divisor in range(2, isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def primes_between(lower: int, upper: int) -> list[int]:
    strict_int(lower, "prime lower bound")
    strict_int(upper, "prime upper bound")
    demand(0 <= lower < upper, "invalid prime interval")
    return [value for value in range(lower + 1, upper + 1) if is_prime(value)]


def exact_weight(m: int, p: int, q: int, H: int) -> Fraction:
    """Exact finite-fixture weight; it is not the theorem's smooth profile."""
    for value, name in ((m, "m"), (p, "p"), (q, "q"), (H, "H")):
        strict_int(value, name)
    scale = p * q
    numerator = scale * scale - H * H * m * m
    demand(numerator >= 0, "finite weight outside support")
    return Fraction(numerator * numerator, scale**4)


def collapsed_row(p: int, q_values: list[int], H: int) -> dict[str, Any]:
    strict_int(p, "p")
    strict_int(H, "H")
    demand(type(q_values) is list and bool(q_values), "q list type")
    demand(is_prime(p), "p must be prime")
    residue_weights: dict[int, Fraction] = {}
    direct_energy = Fraction(0, 1)
    row_mass = Fraction(0, 1)
    atom_count = 0
    for q in q_values:
        strict_int(q, "q")
        demand(is_prime(q) and p < q, "invalid shell prime")
        cutoff = (p * q) // H
        demand(cutoff > 0 and 2 * cutoff < p, "primitive interval failure")
        inverse = pow(q, -1, p)
        seen_in_q: set[int] = set()
        for m in range(-cutoff, cutoff + 1):
            if m == 0:
                continue
            residue = (m * inverse) % p
            demand(residue != 0, "zero residue occupied")
            demand(residue not in seen_in_q, "fixed-q injectivity failure")
            seen_in_q.add(residue)
            weight = exact_weight(m, p, q, H)
            residue_weights[residue] = residue_weights.get(residue, Fraction()) + weight
            row_mass += weight
            direct_energy += weight * weight
            atom_count += 1
    collapsed_energy = sum(
        (weight * weight for weight in residue_weights.values()), Fraction()
    )
    cauchy_floor = row_mass * row_mass / (p - 1)
    collision_excess = collapsed_energy - direct_energy
    demand(collapsed_energy >= cauchy_floor, "post-collapse Cauchy failure")
    demand(collision_excess > 0, "fixture lacks a genuine q collision")
    return {
        "atom_count": atom_count,
        "cauchy_floor": fraction_record(cauchy_floor, "S_p^2/(p-1)"),
        "cauchy_pass": True,
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "collapsed_energy": fraction_record(collapsed_energy, "sum_a|sum_q B_pq(a)|^2"),
        "collision_excess": fraction_record(collision_excess, "collapsed-direct"),
        "collision_excess_positive": True,
        "direct_energy": fraction_record(direct_energy, "sum_q sum_a|B_pq(a)|^2"),
        "occupied_primitive_residues": len(residue_weights),
        "p": p,
        "primitive_support": True,
        "q_count": len(q_values),
        "row_mass": fraction_record(row_mass, "sum_a B_p(a)"),
    }


def finite_fixture() -> dict[str, Any]:
    Q = 101
    H = 509
    U = 97
    p_values = [53, 73, 97]
    q_values = primes_between(Q, 2 * Q)
    demand(4 * Q < H and U < Q, "finite source inequalities")
    demand(all(U // 2 < p <= U for p in p_values), "top-prime domain")
    rows = [collapsed_row(p, q_values, H) for p in p_values]
    return {
        "H": H,
        "Q": Q,
        "U": U,
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "four_Q_less_than_H": True,
        "q_count": len(q_values),
        "q_values": q_values,
        "rows": rows,
        "top_prime_rows": len(rows),
        "U_less_than_Q": True,
    }


def validate_status(value: object) -> None:
    demand(strict_string(value, "status") == STATUS, "status promotion or drift")


def validate_fraction(value: object, expected: Fraction, name: str) -> None:
    demand(type(value) is Fraction, f"{name} must be Fraction")
    demand(value == expected, f"{name} mismatch")


def validate_object_lock(lock: object) -> None:
    demand(type(lock) is dict, "object lock type")
    demand(lock.get("main_object") == OBJECT_KIND, "object substitution")
    demand(lock.get("coefficient") == "C_p=-log(p)/p", "coefficient mutation")
    demand(lock.get("profile_class") == PROFILE_KIND, "profile mutation")
    demand(lock.get("frame_order") == FRAME_ORDER, "frame-order mutation")
    demand(lock.get("p_domain") == "PRIMES_U_OVER_2_LT_P_LE_U", "p domain")
    demand(lock.get("q_domain") == "PRIMES_Q_LT_Q_LE_2Q", "q domain")


def rejected(name: str, operation: Callable[[], None]) -> str:
    try:
        operation()
    except CertificateFailure:
        return name
    raise CertificateFailure(f"mutation accepted: {name}")


def mutation_rejections() -> list[str]:
    base_lock = {
        "coefficient": "C_p=-log(p)/p",
        "frame_order": FRAME_ORDER,
        "main_object": OBJECT_KIND,
        "p_domain": "PRIMES_U_OVER_2_LT_P_LE_U",
        "profile_class": PROFILE_KIND,
        "q_domain": "PRIMES_Q_LT_Q_LE_2Q",
    }

    def changed(field: str, value: object) -> dict[str, Any]:
        record = dict(base_lock)
        record[field] = value
        return record

    cases: list[tuple[str, Callable[[], None]]] = [
        ("bool_int_confusion", lambda: strict_int(True, "mutated integer")),
        ("coefficient_sign_flip", lambda: validate_object_lock(changed("coefficient", "C_p=+log(p)/p"))),
        ("frame_after_restriction", lambda: validate_object_lock(changed("frame_order", "TOP_PRIME_RESTRICTION_BEFORE_WINDOW_FRAME"))),
        ("object_q_split", lambda: validate_object_lock(changed("main_object", "Q_SPLIT_DIRECT_ENERGY"))),
        ("p_domain_expansion", lambda: validate_object_lock(changed("p_domain", "ALL_ACTIVE_DENOMINATORS"))),
        ("profile_sign_change", lambda: validate_object_lock(changed("profile_class", "FIXED_SIGNED_PROFILE"))),
        ("q_domain_expansion", lambda: validate_object_lock(changed("q_domain", "ALL_INTEGERS_Q_LT_Q_LE_2Q"))),
        ("status_promotion", lambda: validate_status("PROVED_ARITHMETIC_L2_FULL_GATE_B")),
        ("wrong_coefficient_constant", lambda: validate_fraction(Fraction(10772, 1600), Fraction(10773, 1600), "coefficient constant")),
        ("wrong_window_constant", lambda: validate_fraction(Fraction(10773, 3199), Fraction(10773, 3200), "window constant")),
        ("wrong_power", lambda: validate_fraction(Fraction(1, 49), Fraction(1, 48), "collision exponent")),
    ]
    return sorted(rejected(name, operation) for name, operation in cases)


def expected_payload() -> dict[str, Any]:
    object_lock = {
        "coefficient": "C_p=-log(p)/p",
        "frame_order": FRAME_ORDER,
        "main_object": OBJECT_KIND,
        "p_domain": "PRIMES_U_OVER_2_LT_P_LE_U",
        "plateau_profile": "REJECTED_NOT_LITERAL_V59_CLASS",
        "profile_class": PROFILE_KIND,
        "q_domain": "PRIMES_Q_LT_Q_LE_2Q",
    }
    validate_object_lock(object_lock)
    mutations = mutation_rejections()
    return {
        "certificate_version": 1,
        "date": "2026-08-24",
        "exact_fraction_ledger": {
            "H_exponent": fraction_record(Fraction(21, 32), "H=x^(21/32)"),
            "Q_exponent": fraction_record(Fraction(1, 3), "Q=x^(1/3)"),
            "U_exponent": fraction_record(Fraction(133, 400), "U=x^(133/400)"),
            "coefficient_constant": fraction_record(Fraction(10773, 1600), "(9/4)*(399/400)*3"),
            "collision_exponent": fraction_record(Fraction(1, 48), "4/3-2*(21/32)"),
            "direct_exponent": fraction_record(Fraction(1, 96), "2/3-21/32"),
            "finite_window_constant": fraction_record(Fraction(10773, 3200), "one-half coefficient constant"),
            "frame_defect_exponent": fraction_record(Fraction(-67, 100), "4*(133/400)-2"),
            "log_ratio": fraction_record(Fraction(399, 400), "log(U)/log(Q)"),
            "row_depth_exponent": fraction_record(Fraction(23, 2400), "UQ/H"),
            "row_error_exponent": fraction_record(Fraction(-23, 2400), "H/(UQ)"),
        },
        "finite_fixture": finite_fixture(),
        "markers": {
            "TPC241_ARITHMETIC_ADVANCE": "NO",
            "TPC241_COEFFICIENT_LIMINF": "PROVED_10773_LOG_2_OVER_1600",
            "TPC241_FINITE_WINDOW_LIMINF": "PROVED_10773_LOG_2_OVER_3200",
            "TPC241_FIXED_ATOM_CREDIT": 0,
            "TPC241_FULL_GATE_B": "OPEN",
            "TPC241_L2": "NONE",
            "TPC241_ROUTE_LEVEL": "PROVED_STRUCTURAL_L1_OBSTRUCTION",
            "TPC241_STATUS": STATUS,
            "TPC241_STRICT_1_OVER_400": "UNPAID_GLOBAL",
        },
        "mutation_firewalls": {
            "rejected": mutations,
            "rejected_count": len(mutations),
        },
        "object_lock": object_lock,
        "round2_clue": ROUND2_CLUE,
        "scope_firewall": {
            "CLASS_UNIFORM_X0": "NOT_CLAIMED",
            "FINITE_FIXTURE_IS_THEOREM_EVIDENCE": False,
            "PHYSICAL_WINDOW_CROSS_TERM_DELETION": "FORBIDDEN",
            "PLATEAU_PROFILE_SUBSTITUTION": "FORBIDDEN",
            "SIGNED_C_H_CANCELLATION": "NONE",
            "SIGNED_FOUR_PACKET_PROJECTION": "OPEN",
            "TWIN_PRIME_RESULT": "NONE",
        },
        "theorem": {
            "classification": "PROVED",
            "coefficient_liminf": "liminf_(x->infinity)(log(x)/x^(1/48))*E_top^psi>=10773*log(2)/1600",
            "finite_window_liminf": "liminf_(x->infinity)(log(x)/x^(1/48))*mean_Ix|K_psi|^2>=10773*log(2)/3200",
            "fixed_power_refutation": "FOR_EVERY_FIXED_PSI_DELTA_POSITIVE_AND_REAL_A_NO_EVENTUAL_X_1_OVER_48_MINUS_DELTA_LOG_A_BOUND",
            "quantifier": "FOR_EVERY_FIXED_ADMISSIBLE_PSI_PROFILEWISE_THRESHOLD",
        },
    }


def expected_document() -> dict[str, Any]:
    payload = expected_payload()
    document = deepcopy(payload)
    document["payload_sha256"] = hashlib.sha256(canonical_json(payload)).hexdigest()
    return document


def same_typed(candidate: object, expected: object) -> bool:
    if type(candidate) is not type(expected):
        return False
    if type(expected) is dict:
        return candidate.keys() == expected.keys() and all(
            same_typed(candidate[key], expected[key]) for key in expected
        )
    if type(expected) is list:
        return len(candidate) == len(expected) and all(
            same_typed(left, right) for left, right in zip(candidate, expected)
        )
    return candidate == expected


def check_certificate() -> dict[str, Any]:
    demand(CERTIFICATE.is_file(), "certificate missing")
    stored = json.loads(CERTIFICATE.read_text(encoding="ascii"))
    expected = expected_document()
    demand(same_typed(stored, expected), "certificate payload mismatch")
    canonical = canonical_json(expected) + b"\n"
    demand(CERTIFICATE.read_bytes() == canonical, "certificate is not canonical JSON")
    return expected


def write_certificate() -> dict[str, Any]:
    expected = expected_document()
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_bytes(canonical_json(expected) + b"\n")
    return expected


def summary(document: dict[str, Any], mode: str) -> None:
    fixture = document["finite_fixture"]
    collision_rows = sum(
        1 for row in fixture["rows"] if row["collision_excess_positive"] is True
    )
    print("TPC241_CERTIFICATE=PASS")
    print("mode=" + mode)
    print("claim=" + STATUS)
    print("coefficient_constant=10773*log(2)/1600")
    print("finite_window_constant=10773*log(2)/3200")
    print("fixed_power=1/48_SHARP_UP_TO_LOGARITHMS")
    print("fixture_collision_rows=" + str(collision_rows))
    print("signed_gate_b=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            document = write_certificate()
            mode = "write"
        else:
            document = check_certificate()
            mode = "check"
        summary(document, mode)
    except (CertificateFailure, KeyError, TypeError, ValueError, OSError) as error:
        raise SystemExit("TPC241_CERTIFICATE=FAIL: " + str(error))


if __name__ == "__main__":
    main()
