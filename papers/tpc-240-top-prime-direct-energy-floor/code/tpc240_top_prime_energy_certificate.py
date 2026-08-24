#!/usr/bin/env python3
"""Deterministic certificate for the TPC-240 direct-energy theorem ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "tpc240_certificate.json"
STATUS = "PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR"
OBJECT_KIND = "Q_SPLIT_UNSIGNED_TOP_PRIME_DIRECT_RESIDUE_ROW_ENERGY"
PROFILE_KIND = "FIXED_REAL_CINF_NONNEGATIVE_LE_ONE_SUPPORT_MINUS1_PLUS1_INTEGRAL_ONE"
ROUND2_CLUE = (
    "TEST_THE_TOP_PRIME_Q_COLLAPSED_COLLISION_EXCESS_OVER_THE_EXACT_DIRECT_"
    "FLOOR_BEFORE_CLAIMING_X_1_OVER_48_SHARPNESS"
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


def exact_weight(m: int, p: int, q: int, H: int) -> Fraction:
    """A rational finite-fixture weight, not the theorem's smooth profile."""
    for value, name in ((m, "m"), (p, "p"), (q, "q"), (H, "H")):
        strict_int(value, name)
    numerator = p * p * q * q - H * H * m * m
    demand(numerator >= 0, "fixture weight outside support")
    return Fraction(numerator * numerator, p**4 * q**4)


def fixture_row(p: int, q: int, H: int) -> dict[str, Any]:
    for value, name in ((p, "p"), (q, "q"), (H, "H")):
        strict_int(value, name)
    demand(is_prime(p) and is_prime(q), "fixture row requires primes")
    demand(p < q, "fixture p<q fails")
    demand(2 * q < H, "fixture 2q<H fails")
    cutoff = (p * q) // H
    demand(2 * cutoff < p, "fixture signed interval is not injective")
    inverse = pow(q, -1, p)
    entries: list[dict[str, Any]] = []
    residue_weights: dict[int, Fraction] = {}
    direct_energy = Fraction(0, 1)
    for m in range(-cutoff, cutoff + 1):
        if m == 0:
            continue
        residue = (m * inverse) % p
        demand(residue != 0, "fixture occupied zero residue")
        demand(residue not in residue_weights, "fixture residue collision")
        weight = exact_weight(m, p, q, H)
        residue_weights[residue] = weight
        direct_energy += weight * weight
        entries.append(
            {
                "m": m,
                "residue": residue,
                "weight": fraction_record(weight, "(1-(Hm/(pq))^2)^2"),
            }
        )
    row_energy = sum((weight * weight for weight in residue_weights.values()), Fraction())
    demand(row_energy == direct_energy, "fixture row/direct identity")
    return {
        "H": H,
        "atom_count": len(entries),
        "classification": "FINITE_ALGEBRAIC_FIXTURE_NOT_THEOREM_PROFILE",
        "cutoff": cutoff,
        "direct_energy": fraction_record(direct_energy, "sum_m weight(m)^2"),
        "entries": entries,
        "injective": True,
        "p": p,
        "primitive_support": True,
        "q": q,
        "row_energy": fraction_record(row_energy, "sum_a B(a)^2"),
    }


def finite_fixture() -> dict[str, Any]:
    Q = 101
    H = 509
    U = 97
    p_values = [53, 73, 97]
    q_values = [103, 151, 199]
    demand(4 * Q < H and U < Q, "finite source inequalities")
    demand(all(is_prime(value) for value in p_values + q_values), "fixture primality")
    demand(all(U // 2 < p <= U for p in p_values), "fixture top p domain")
    demand(all(Q < q <= 2 * Q for q in q_values), "fixture q shell")
    rows = [fixture_row(p, q, H) for p, q in zip(p_values, q_values)]
    return {
        "H": H,
        "Q": Q,
        "U": U,
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "four_Q_less_than_H": True,
        "rows": rows,
        "top_prime_rows": len(rows),
        "U_less_than_Q": True,
    }


def validate_main_status(value: object) -> None:
    demand(strict_string(value, "status") == STATUS, "status promotion or drift")


def validate_rational(value: object, expected: Fraction, name: str) -> None:
    demand(type(value) is Fraction, f"{name} must be Fraction")
    demand(value == expected, f"{name} mismatch")


def validate_object_lock(lock: object) -> None:
    demand(type(lock) is dict, "object lock type")
    demand(lock.get("main_object") == OBJECT_KIND, "q-collapsed substitution")
    demand(lock.get("coefficient") == "C_p=-log(p)/p", "coefficient sign mutation")
    demand(lock.get("profile_class") == PROFILE_KIND, "profile class mutation")
    demand(lock.get("p_domain") == "PRIMES_U_OVER_2_LT_P_LE_U", "p domain mutation")
    demand(lock.get("q_domain") == "PRIMES_Q_LT_Q_LE_2Q", "q domain mutation")
    demand(lock.get("plateau_profile") == "REJECTED_NOT_LITERAL_V59_CLASS", "plateau substitution")


def rejected(name: str, operation: Callable[[], None]) -> str:
    try:
        operation()
    except CertificateFailure:
        return name
    raise CertificateFailure(f"mutation accepted: {name}")


def mutation_rejections() -> list[str]:
    base_lock = {
        "coefficient": "C_p=-log(p)/p",
        "main_object": OBJECT_KIND,
        "p_domain": "PRIMES_U_OVER_2_LT_P_LE_U",
        "plateau_profile": "REJECTED_NOT_LITERAL_V59_CLASS",
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
        ("p_domain_expansion", lambda: validate_object_lock(changed("p_domain", "ALL_ACTIVE_DENOMINATORS"))),
        ("plateau_substitution", lambda: validate_object_lock(changed("plateau_profile", "IDENTICALLY_ONE_ON_MINUS1_PLUS1"))),
        ("profile_sign_change", lambda: validate_object_lock(changed("profile_class", "FIXED_REAL_CINF_SIGNED"))),
        ("q_collapsed_substitution", lambda: validate_object_lock(changed("main_object", "Q_COLLAPSED_COMPLETE_PERIOD_ENERGY"))),
        ("status_promotion", lambda: validate_main_status("PROVED_ARITHMETIC_L2_FULL_GATE_B")),
        ("wrong_constant_1197_over_800", lambda: validate_rational(Fraction(1196, 800), Fraction(1197, 800), "leading rational")),
        ("wrong_exponent_1_over_96", lambda: validate_rational(Fraction(1, 95), Fraction(1, 96), "direct exponent")),
    ]
    return sorted(rejected(name, operation) for name, operation in cases)


def expected_payload() -> dict[str, Any]:
    object_lock = {
        "coefficient": "C_p=-log(p)/p",
        "main_object": OBJECT_KIND,
        "normalization": "NO_COMPLETE_PERIOD_OR_FINITE_WINDOW_FACTOR_IN_MAIN_THEOREM",
        "p_domain": "PRIMES_U_OVER_2_LT_P_LE_U",
        "plateau_profile": "REJECTED_NOT_LITERAL_V59_CLASS",
        "profile_class": PROFILE_KIND,
        "q_domain": "PRIMES_Q_LT_Q_LE_2Q",
    }
    validate_object_lock(object_lock)
    rejected_mutations = mutation_rejections()
    return {
        "certificate_version": 1,
        "date": "2026-08-24",
        "exact_fraction_ledger": {
            "H_exponent": fraction_record(Fraction(21, 32), "H=x^(21/32)"),
            "Q_exponent": fraction_record(Fraction(1, 3), "Q=x^(1/3)"),
            "U_exponent": fraction_record(Fraction(133, 400), "U=x^(133/400)"),
            "direct_energy_exponent": fraction_record(Fraction(1, 96), "2/3-21/32"),
            "leading_rational": fraction_record(Fraction(1197, 800), "(3/2)*(399/400)"),
            "log_ratio": fraction_record(Fraction(399, 400), "log(U)/log(Q)"),
            "profile_kappa_lower": fraction_record(Fraction(1, 2), "Cauchy on [-1,1]"),
            "profile_kappa_upper": fraction_record(Fraction(1, 1), "psi^2<=psi"),
            "relative_error_exponent": fraction_record(Fraction(-23, 2400), "H/(UQ)"),
            "row_depth_exponent": fraction_record(Fraction(23, 2400), "UQ/H"),
        },
        "finite_fixture": finite_fixture(),
        "markers": {
            "TPC240_ARITHMETIC_ADVANCE": "NO",
            "TPC240_DIRECT_ENERGY": "PROVED_X_1_OVER_96_WITH_EXACT_CONSTANT",
            "TPC240_FULL_GATE_B": "OPEN",
            "TPC240_L2": "NONE",
            "TPC240_ROUTE_LEVEL": "PROVED_STRUCTURAL_L1_OBSTRUCTION",
            "TPC240_ROUND2_CLUE": ROUND2_CLUE,
            "TPC240_STATUS": STATUS,
            "TPC240_STRICT_1_OVER_400": "UNPAID_GLOBAL",
        },
        "mutation_firewalls": {
            "rejected": rejected_mutations,
            "rejected_count": len(rejected_mutations),
        },
        "object_lock": object_lock,
        "paper": "TPC-240",
        "scope_firewall": {
            "CLASS_UNIFORM_X0": "NOT_CLAIMED",
            "FIXED_ATOM_CREDIT": 0,
            "NUMERICAL_CHECKS_ARE_THEOREM_EVIDENCE": False,
            "Q_COLLAPSED_X_1_OVER_48_SHARPNESS": "OPEN",
            "SIGNED_C_H_CANCELLATION": "NONE",
            "SIGNED_FOUR_PACKET_PROJECTION": "OPEN",
            "TWIN_PRIME_RESULT": "NONE",
        },
        "theorem": {
            "asymptotic": "D_top^psi=[1197*kappa_psi*log(2)/800+o_psi(1)]Q^2/H",
            "classification": "PROVED",
            "consequence": "D_top^psi_IS_NOT_o(Q^2/H)_AND_HAS_NO_FIXED_POWER_SAVING",
            "quantifier": "FOR_EVERY_FIXED_ADMISSIBLE_PSI_AND_EPS_EXISTS_X0_PSI_EPS_FOR_ALL_X_GE_X0",
        },
    }


def expected_document() -> dict[str, Any]:
    payload = expected_payload()
    output = dict(payload)
    output["payload_sha256"] = hashlib.sha256(canonical_json(payload)).hexdigest()
    return output


def check_json_types(value: Any, path: str = "root") -> None:
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is list:
        for index, item in enumerate(value):
            check_json_types(item, f"{path}[{index}]")
        return
    if type(value) is dict:
        for key, item in value.items():
            demand(type(key) is str, f"non-string JSON key at {path}")
            check_json_types(item, f"{path}.{key}")
        return
    raise CertificateFailure(f"unsupported JSON type at {path}: {type(value).__name__}")


def write_certificate() -> dict[str, Any]:
    document = expected_document()
    check_json_types(document)
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_bytes(canonical_json(document) + b"\n")
    return {
        "TPC240_CERTIFICATE_WRITE": "PASS",
        "bytes": CERTIFICATE.stat().st_size,
        "mutations_rejected": document["mutation_firewalls"]["rejected_count"],
        "payload_sha256": document["payload_sha256"],
    }


def check_certificate() -> dict[str, Any]:
    demand(CERTIFICATE.is_file(), "certificate is missing")
    raw = CERTIFICATE.read_bytes()
    demand(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "certificate EOF")
    document = json.loads(raw.decode("ascii"))
    check_json_types(document)
    expected = expected_document()
    demand(document == expected, "certificate content mismatch")
    demand(raw == canonical_json(expected) + b"\n", "certificate is not canonical")
    supplied = strict_string(document.get("payload_sha256"), "payload digest")
    payload = dict(document)
    payload.pop("payload_sha256")
    demand(hashlib.sha256(canonical_json(payload)).hexdigest() == supplied, "digest mismatch")
    validate_main_status(document["markers"]["TPC240_STATUS"])
    validate_object_lock(document["object_lock"])
    return {
        "TPC240_CERTIFICATE": "PASS",
        "finite_rows": document["finite_fixture"]["top_prime_rows"],
        "mutations_rejected": document["mutation_firewalls"]["rejected_count"],
        "payload_sha256": supplied,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    report = write_certificate() if arguments.write else check_certificate()
    print(canonical_json(report).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificateFailure as error:
        raise SystemExit(f"TPC240_CERTIFICATE=FAIL: {error}")
