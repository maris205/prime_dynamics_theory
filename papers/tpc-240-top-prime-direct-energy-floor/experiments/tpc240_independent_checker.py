#!/usr/bin/env python3
"""Independent reconstruction and mutation audit for the TPC-240 certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any, Callable


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results" / "tpc240_certificate.json"
EXPECTED_STATUS = (
    "PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR"
)
EXPECTED_OBJECT = "Q_SPLIT_UNSIGNED_TOP_PRIME_DIRECT_RESIDUE_ROW_ENERGY"
EXPECTED_PROFILE = (
    "FIXED_REAL_CINF_NONNEGATIVE_LE_ONE_SUPPORT_MINUS1_PLUS1_INTEGRAL_ONE"
)
EXPECTED_CLUE = (
    "TEST_THE_TOP_PRIME_Q_COLLAPSED_COLLISION_EXCESS_OVER_THE_EXACT_DIRECT_"
    "FLOOR_BEFORE_CLAIMING_X_1_OVER_48_SHARPNESS"
)


class IndependentFailure(RuntimeError):
    """Fail-closed independent-check error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool:
        raise IndependentFailure("independent condition is not a strict bool")
    if not condition:
        raise IndependentFailure(message)


def exact_integer(value: object, label: str) -> int:
    require(type(value) is int, f"{label} is not an exact integer")
    return value


def nonempty_text(value: object, label: str) -> str:
    require(type(value) is str and len(value) > 0, f"{label} text type")
    return value


def normalized(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")


def encode_fraction(number: Fraction, reason: str) -> dict[str, Any]:
    require(type(number) is Fraction, "independent ledger fraction type")
    nonempty_text(reason, "fraction reason")
    return {
        "denominator": number.denominator,
        "identity": reason,
        "numerator": number.numerator,
        "value": str(number),
    }


def prime_test(number: int) -> bool:
    exact_integer(number, "prime candidate")
    if number < 2:
        return False
    candidate = 2
    while candidate <= isqrt(number):
        if number % candidate == 0:
            return False
        candidate += 1
    return True


def rational_fixture_weight(m: int, p: int, q: int, H: int) -> Fraction:
    exact_integer(m, "m")
    exact_integer(p, "p")
    exact_integer(q, "q")
    exact_integer(H, "H")
    top = p * p * q * q - H * H * m * m
    require(top >= 0, "negative independent fixture weight")
    return Fraction(top * top, p**4 * q**4)


def reconstruct_row(p: int, q: int, H: int) -> dict[str, Any]:
    require(prime_test(p) and prime_test(q), "independent row primality")
    require(p < q and 2 * q < H, "independent row source inequalities")
    cutoff = p * q // H
    require(2 * cutoff < p, "independent row injectivity range")
    inverse = pow(q, -1, p)
    entries: list[dict[str, Any]] = []
    buckets: dict[int, Fraction] = {}
    atom_norm = Fraction(0, 1)
    for m in range(-cutoff, cutoff + 1):
        if not m:
            continue
        residue = m * inverse % p
        require(residue != 0, "independent zero residue")
        require(residue not in buckets, "independent residue collision")
        weight = rational_fixture_weight(m, p, q, H)
        buckets[residue] = weight
        atom_norm += weight**2
        entries.append(
            {
                "m": m,
                "residue": residue,
                "weight": encode_fraction(weight, "(1-(Hm/(pq))^2)^2"),
            }
        )
    residue_norm = sum((weight**2 for weight in buckets.values()), Fraction(0, 1))
    require(atom_norm == residue_norm, "independent row energy identity")
    return {
        "H": H,
        "atom_count": len(entries),
        "classification": "FINITE_ALGEBRAIC_FIXTURE_NOT_THEOREM_PROFILE",
        "cutoff": cutoff,
        "direct_energy": encode_fraction(atom_norm, "sum_m weight(m)^2"),
        "entries": entries,
        "injective": True,
        "p": p,
        "primitive_support": True,
        "q": q,
        "row_energy": encode_fraction(residue_norm, "sum_a B(a)^2"),
    }


def reconstruct_fixture() -> dict[str, Any]:
    Q, H, U = 101, 509, 97
    p_values = (53, 73, 97)
    q_values = (103, 151, 199)
    require(4 * Q < H and U < Q, "independent fixture scales")
    require(all(prime_test(p) and U // 2 < p <= U for p in p_values), "p domain")
    require(all(prime_test(q) and Q < q <= 2 * Q for q in q_values), "q domain")
    rows = [reconstruct_row(p, q, H) for p, q in zip(p_values, q_values)]
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


def inspect_status(value: object) -> None:
    require(nonempty_text(value, "status") == EXPECTED_STATUS, "status promotion")


def inspect_fraction(value: object, expected: Fraction, label: str) -> None:
    require(type(value) is Fraction, f"{label} Fraction type")
    require(value == expected, f"{label} exact value")


def inspect_lock(value: object) -> None:
    require(type(value) is dict, "object lock mapping")
    require(value.get("coefficient") == "C_p=-log(p)/p", "coefficient sign")
    require(value.get("main_object") == EXPECTED_OBJECT, "q-split object")
    require(value.get("p_domain") == "PRIMES_U_OVER_2_LT_P_LE_U", "p domain")
    require(value.get("q_domain") == "PRIMES_Q_LT_Q_LE_2Q", "q domain")
    require(value.get("profile_class") == EXPECTED_PROFILE, "profile class")
    require(
        value.get("plateau_profile") == "REJECTED_NOT_LITERAL_V59_CLASS",
        "plateau exclusion",
    )


def expect_rejection(label: str, operation: Callable[[], None]) -> str:
    try:
        operation()
    except IndependentFailure:
        return label
    raise IndependentFailure(f"independent mutation accepted: {label}")


def independent_mutations() -> list[str]:
    base = {
        "coefficient": "C_p=-log(p)/p",
        "main_object": EXPECTED_OBJECT,
        "p_domain": "PRIMES_U_OVER_2_LT_P_LE_U",
        "plateau_profile": "REJECTED_NOT_LITERAL_V59_CLASS",
        "profile_class": EXPECTED_PROFILE,
        "q_domain": "PRIMES_Q_LT_Q_LE_2Q",
    }

    def mutate(field: str, value: object) -> dict[str, Any]:
        altered = dict(base)
        altered[field] = value
        return altered

    tests: list[tuple[str, Callable[[], None]]] = [
        ("bool_int_confusion", lambda: exact_integer(False, "mutated integer")),
        ("coefficient_sign_flip", lambda: inspect_lock(mutate("coefficient", "C_p=+log(p)/p"))),
        ("p_domain_expansion", lambda: inspect_lock(mutate("p_domain", "ALL_ACTIVE_DENOMINATORS"))),
        ("plateau_substitution", lambda: inspect_lock(mutate("plateau_profile", "IDENTICALLY_ONE_ON_MINUS1_PLUS1"))),
        ("profile_sign_change", lambda: inspect_lock(mutate("profile_class", "FIXED_REAL_CINF_SIGNED"))),
        ("q_collapsed_substitution", lambda: inspect_lock(mutate("main_object", "Q_COLLAPSED_COMPLETE_PERIOD_ENERGY"))),
        ("status_promotion", lambda: inspect_status("PROVED_ARITHMETIC_L2_FULL_GATE_B")),
        ("wrong_constant_1197_over_800", lambda: inspect_fraction(Fraction(1196, 800), Fraction(1197, 800), "leading rational")),
        ("wrong_exponent_1_over_96", lambda: inspect_fraction(Fraction(1, 95), Fraction(1, 96), "direct exponent")),
    ]
    return sorted(expect_rejection(label, operation) for label, operation in tests)


def reconstruct_payload() -> dict[str, Any]:
    lock = {
        "coefficient": "C_p=-log(p)/p",
        "main_object": EXPECTED_OBJECT,
        "normalization": "NO_COMPLETE_PERIOD_OR_FINITE_WINDOW_FACTOR_IN_MAIN_THEOREM",
        "p_domain": "PRIMES_U_OVER_2_LT_P_LE_U",
        "plateau_profile": "REJECTED_NOT_LITERAL_V59_CLASS",
        "profile_class": EXPECTED_PROFILE,
        "q_domain": "PRIMES_Q_LT_Q_LE_2Q",
    }
    inspect_lock(lock)
    mutations = independent_mutations()
    return {
        "certificate_version": 1,
        "date": "2026-08-24",
        "exact_fraction_ledger": {
            "H_exponent": encode_fraction(Fraction(21, 32), "H=x^(21/32)"),
            "Q_exponent": encode_fraction(Fraction(1, 3), "Q=x^(1/3)"),
            "U_exponent": encode_fraction(Fraction(133, 400), "U=x^(133/400)"),
            "direct_energy_exponent": encode_fraction(Fraction(1, 96), "2/3-21/32"),
            "leading_rational": encode_fraction(Fraction(1197, 800), "(3/2)*(399/400)"),
            "log_ratio": encode_fraction(Fraction(399, 400), "log(U)/log(Q)"),
            "profile_kappa_lower": encode_fraction(Fraction(1, 2), "Cauchy on [-1,1]"),
            "profile_kappa_upper": encode_fraction(Fraction(1, 1), "psi^2<=psi"),
            "relative_error_exponent": encode_fraction(Fraction(-23, 2400), "H/(UQ)"),
            "row_depth_exponent": encode_fraction(Fraction(23, 2400), "UQ/H"),
        },
        "finite_fixture": reconstruct_fixture(),
        "markers": {
            "TPC240_ARITHMETIC_ADVANCE": "NO",
            "TPC240_DIRECT_ENERGY": "PROVED_X_1_OVER_96_WITH_EXACT_CONSTANT",
            "TPC240_FULL_GATE_B": "OPEN",
            "TPC240_L2": "NONE",
            "TPC240_ROUTE_LEVEL": "PROVED_STRUCTURAL_L1_OBSTRUCTION",
            "TPC240_ROUND2_CLUE": EXPECTED_CLUE,
            "TPC240_STATUS": EXPECTED_STATUS,
            "TPC240_STRICT_1_OVER_400": "UNPAID_GLOBAL",
        },
        "mutation_firewalls": {
            "rejected": mutations,
            "rejected_count": len(mutations),
        },
        "object_lock": lock,
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


def scan_types(value: Any, location: str = "root") -> None:
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is list:
        for index, item in enumerate(value):
            scan_types(item, f"{location}[{index}]")
        return
    if type(value) is dict:
        for key, item in value.items():
            require(type(key) is str, f"non-string key at {location}")
            scan_types(item, f"{location}.{key}")
        return
    raise IndependentFailure(f"unsupported JSON type at {location}")


def verify() -> dict[str, Any]:
    require(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_bytes()
    require(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "certificate EOF")
    document = json.loads(raw.decode("ascii"))
    scan_types(document)
    payload = reconstruct_payload()
    expected = dict(payload)
    expected["payload_sha256"] = hashlib.sha256(normalized(payload)).hexdigest()
    require(document == expected, "independent reconstruction mismatch")
    require(raw == normalized(expected) + b"\n", "noncanonical certificate bytes")
    supplied = nonempty_text(document.get("payload_sha256"), "payload digest")
    stripped = dict(document)
    stripped.pop("payload_sha256")
    require(hashlib.sha256(normalized(stripped)).hexdigest() == supplied, "hash mismatch")
    inspect_status(document["markers"]["TPC240_STATUS"])
    inspect_lock(document["object_lock"])
    source = Path(__file__).read_text(encoding="utf-8")
    forbidden = "import " + "tpc240_top_prime_energy_certificate"
    require(forbidden not in source, "independent checker imports producer")
    return {
        "TPC240_INDEPENDENT_CHECK": "PASS",
        "finite_rows": document["finite_fixture"]["top_prime_rows"],
        "mutations_rejected": len(independent_mutations()),
        "payload_sha256": supplied,
        "producer_imports": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    print(normalized(verify()).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except IndependentFailure as error:
        raise SystemExit(f"TPC240_INDEPENDENT_CHECK=FAIL: {error}")
