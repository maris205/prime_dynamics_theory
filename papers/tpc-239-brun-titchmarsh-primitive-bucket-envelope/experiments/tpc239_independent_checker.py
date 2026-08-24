#!/usr/bin/env python3
"""Independent TPC-239 checker; it imports no producer implementation."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "tpc239_certificate.json"


class IndependentFailure(RuntimeError):
    """Independent fail-closed validation error."""


def ensure(condition: bool, message: str) -> None:
    if type(condition) is not bool:
        raise IndependentFailure("checker condition is not a strict bool")
    if not condition:
        raise IndependentFailure(message)


def exact_int(value: object, name: str) -> int:
    ensure(type(value) is int, f"{name} is not an exact int")
    return value


def check_json_types(value: Any, location: str = "document") -> None:
    value_type = type(value)
    if value_type in {str, int, bool}:
        return
    if value_type is float:
        ensure(math.isfinite(value), f"nonfinite float at {location}")
        return
    if value_type is list:
        for index, item in enumerate(value):
            check_json_types(item, f"{location}[{index}]")
        return
    if value_type is dict:
        for key, item in value.items():
            ensure(type(key) is str, f"nonstr key at {location}")
            check_json_types(item, f"{location}.{key}")
        return
    raise IndependentFailure(f"unsupported JSON type at {location}")


def normalized_json(value: Any) -> bytes:
    check_json_types(value)
    return json.dumps(
        value, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("ascii")


def independent_prime_sieve(limit: int) -> list[int]:
    exact_int(limit, "sieve limit")
    ensure(limit >= 2, "sieve limit too small")
    flags = [True] * (limit + 1)
    flags[0] = False
    flags[1] = False
    for prime in range(2, isqrt(limit) + 1):
        if flags[prime]:
            for multiple in range(prime * prime, limit + 1, prime):
                flags[multiple] = False
    return [value for value, flag in enumerate(flags) if flag]


def independent_is_prime(value: int) -> bool:
    exact_int(value, "prime candidate")
    return value >= 2 and value in independent_prime_sieve(max(2, value))


def independent_phi(value: int) -> int:
    exact_int(value, "totient input")
    ensure(value >= 1, "totient input must be positive")
    result = value
    remaining = value
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            result -= result // prime
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result -= result // remaining
    return result


def real_string(value: float) -> str:
    ensure(type(value) is float and math.isfinite(value), "invalid real")
    return format(value, ".12f")


def admit_spec(Q: object, H: object, h: object) -> tuple[int, int, int]:
    q_value = exact_int(Q, "Q")
    h_scale = exact_int(H, "H")
    modulus = exact_int(h, "h")
    ensure(q_value >= 2, "Q too small")
    ensure(modulus >= 2, "h=1 is separate")
    ensure(4 * q_value < h_scale, "4Q < H fails")
    ensure(modulus < q_value, "h < Q fails")
    return q_value, h_scale, modulus


def independent_fixture() -> dict[str, Any]:
    Q, H, h = admit_spec(101, 8830, 82)
    primes = [prime for prime in independent_prime_sieve(2 * Q) if Q < prime]
    phi = independent_phi(h)
    maximum = (2 * h * Q) // H
    multipliers = [
        value
        for value in range(-maximum, maximum + 1)
        if value != 0 and gcd(value, h) == 1
    ]
    logarithm = math.log(Fraction(2 * Q, h).numerator / Fraction(2 * Q, h).denominator)
    class_rhs = 4.0 * Q / (phi * logarithm)
    factor_rhs = 16.0 * Q * Q / H * (h / phi) / logarithm

    physical_rows: list[dict[str, Any]] = []
    multiplier_table: dict[int, list[int]] = {}
    for prime in primes:
        cutoff = (h * prime) // H
        row_multipliers = [
            value for value in range(-cutoff, cutoff + 1) if value != 0
        ]
        inverse = pow(prime, -1, h)
        residues = [(value * inverse) % h for value in row_multipliers]
        ensure(len(residues) == len(set(residues)), "independent row injectivity")
        multiplier_table[prime] = row_multipliers
        physical_rows.append(
            {
                "cutoff": cutoff,
                "multipliers": row_multipliers,
                "primitive_residues": sorted(
                    residue for residue in residues if gcd(residue, h) == 1
                ),
                "q": prime,
                "residues": residues,
            }
        )

    buckets: list[dict[str, Any]] = []
    for residue in range(h):
        if gcd(residue, h) != 1:
            continue
        inverse = pow(residue, -1, h)
        actual_pairs: list[dict[str, int]] = []
        for prime in primes:
            target = (residue * prime) % h
            matches = [
                multiplier
                for multiplier in multiplier_table[prime]
                if multiplier % h == target
            ]
            ensure(len(matches) <= 1, "independent hidden duplicate")
            if matches:
                actual_pairs.append({"m": matches[0], "q": prime})

        ap_rows: list[dict[str, Any]] = []
        q_multiplicity = {prime: 0 for prime in primes}
        for multiplier in multipliers:
            ensure(gcd(multiplier, h) == 1, "independent nonunit multiplier")
            prime_class = (inverse * multiplier) % h
            ensure(gcd(prime_class, h) == 1, "independent nonreduced AP")
            row_primes = [prime for prime in primes if prime % h == prime_class]
            ensure(len(row_primes) <= class_rhs + 1.0e-12, "independent BT row")
            for prime in row_primes:
                q_multiplicity[prime] += 1
            ap_rows.append(
                {
                    "b": prime_class,
                    "count": len(row_primes),
                    "m": multiplier,
                    "primes": row_primes,
                }
            )
        census = sum(row["count"] for row in ap_rows)
        actual = len(actual_pairs)
        ensure(actual <= census, "independent actual/AP order")
        ensure(census <= factor_rhs + 1.0e-12, "independent factor-16 bound")
        dropped = sum(
            1
            for row in ap_rows
            for prime in row["primes"]
            if abs(row["m"]) > (h * prime) // H
        )
        buckets.append(
            {
                "a": residue,
                "a_inverse": inverse,
                "actual_R": actual,
                "actual_pairs": actual_pairs,
                "ap_census": census,
                "ap_rows": ap_rows,
                "dropped_cutoff_pairs": dropped,
                "max_q_pair_multiplicity_in_ap_sum": max(q_multiplicity.values()),
            }
        )

    ensure(len(buckets) == phi, "independent primitive bucket count")
    ensure(Fraction(2 * maximum, 1) <= Fraction(4 * h * Q, H), "m-count bound")
    return {
        "H": H,
        "M_h": maximum,
        "Q": Q,
        "ap_class_bt_rhs_approx": real_string(class_rhs),
        "buckets": buckets,
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "factor_16_rhs_approx": real_string(factor_rhs),
        "four_Q_less_than_H": True,
        "h": h,
        "h_less_than_Q": True,
        "max_actual_R": max(row["actual_R"] for row in buckets),
        "max_ap_census": max(row["ap_census"] for row in buckets),
        "multiplier_count": len(multipliers),
        "multipliers": multipliers,
        "name": "V59_SHAPED_SQUAREFREE_TRIPLE_COLLISION",
        "phi_h": phi,
        "physical_rows": physical_rows,
        "shell_prime_count": len(primes),
        "shell_primes": primes,
    }


def read_fraction(record: dict[str, Any], name: str) -> Fraction:
    numerator = exact_int(record.get("numerator"), f"{name} numerator")
    denominator = exact_int(record.get("denominator"), f"{name} denominator")
    ensure(denominator > 0, f"{name} denominator is not positive")
    value = Fraction(numerator, denominator)
    ensure(record.get("value") == str(value), f"{name} string encoding")
    ensure(type(record.get("identity")) is str, f"{name} identity type")
    return value


def reject(name: str, operation: Callable[[], None]) -> str:
    try:
        operation()
    except IndependentFailure:
        return name
    raise IndependentFailure(f"independent mutation accepted: {name}")


def independent_mutations() -> list[str]:
    def shell_entry(value: object) -> None:
        prime = exact_int(value, "shell entry")
        ensure(101 < prime <= 202, "shell range")
        ensure(independent_is_prime(prime), "shell primality")

    def cutoff(prime: object, encoded: object) -> None:
        q_value = exact_int(prime, "cutoff q")
        encoded_value = exact_int(encoded, "cutoff value")
        shell_entry(q_value)
        ensure(encoded_value == (82 * q_value) // 8830, "cutoff mutation")

    def factor(value: object) -> None:
        constant = exact_int(value, "factor")
        ensure(constant == 16, "factor mutation")

    def bucket(value: object) -> None:
        residue = exact_int(value, "bucket")
        ensure(0 <= residue < 82 and gcd(residue, 82) == 1, "primitive bucket")

    def multiplier(value: object) -> None:
        item = exact_int(value, "multiplier")
        ensure(item != 0 and gcd(item, 82) == 1, "unit multiplier")

    def order(actual: object, census: object) -> None:
        first = exact_int(actual, "actual")
        second = exact_int(census, "census")
        ensure(0 <= first <= second, "actual/AP order")

    cases: list[tuple[str, Callable[[], None]]] = [
        ("bool_Q_rejected_by_strict_type", lambda: admit_spec(True, 8830, 82)),
        ("composite_shell_entry", lambda: shell_entry(121)),
        ("cutoff_decrement", lambda: cutoff(109, 0)),
        ("factor_15", lambda: factor(15)),
        ("four_Q_equals_H", lambda: admit_spec(11, 44, 7)),
        ("h_equals_Q", lambda: admit_spec(11, 100, 11)),
        ("h_one_sent_to_main_branch", lambda: admit_spec(11, 100, 1)),
        ("nonprimitive_bucket", lambda: bucket(2)),
        ("nonunit_multiplier", lambda: multiplier(2)),
        ("reversed_actual_ap_order", lambda: order(2, 1)),
        ("shell_lower_endpoint", lambda: shell_entry(101)),
    ]
    return sorted(reject(name, operation) for name, operation in cases)


def verify() -> dict[str, Any]:
    ensure(CERTIFICATE.is_file(), "certificate is missing")
    raw = CERTIFICATE.read_bytes()
    ensure(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "JSON EOF format")
    document = json.loads(raw.decode("ascii"))
    check_json_types(document)
    supplied_digest = document.get("payload_sha256")
    ensure(type(supplied_digest) is str, "digest type")
    payload = dict(document)
    payload.pop("payload_sha256", None)
    computed_digest = hashlib.sha256(normalized_json(payload)).hexdigest()
    ensure(supplied_digest == computed_digest, "payload digest mismatch")

    expected_markers = {
        "TPC239_ARITHMETIC_ADVANCE": "NO",
        "TPC239_ARITHMETIC_INPUT": "BRUN_TITCHMARSH",
        "TPC239_BUCKET_ENVELOPE": "PROVED_FACTOR_16",
        "TPC239_PACKET_TRACE": "PROVED_X_1_OVER_48_LOG4_LOGLOG",
        "TPC239_PRIMITIVE_AP_COMPILER": "PROVED_REDUCED",
        "TPC239_ROUTE_ADVANCE": "YES_LOGARITHMIC_ONLY",
        "TPC239_ROUND2_CLUE": (
            "TEST_EXACT_TOP_BAND_C_H_BEFORE_SEEKING_FURTHER_UNIFORM_BUCKET_SAVINGS"
        ),
        "TPC239_STATUS": "PROVED_SOURCE_BACKED_PRIME_DENSITY_L1",
        "TPC239_UNNORMALIZED_EXPONENT": "PROVED_49_OVER_48_PLUS_O_1",
        "TPC239_V59_MAX_ROW": "PROVED_X_1_OVER_96_LOGLOG_OVER_LOG",
    }
    ensure(document.get("markers") == expected_markers, "status marker mismatch")

    firewall = document.get("scope_firewall")
    ensure(type(firewall) is dict, "firewall type")
    ensure(firewall["C_H_SIGNED_CANCELLATION"] == "NONE", "C_h overclaim")
    ensure(firewall["L2"] == "NONE", "L2 overclaim")
    ensure(firewall["FULL_GATE_B"] == "OPEN", "Gate-B overclaim")
    ensure(firewall["FIXED_ATOM_CREDIT"] == 0, "fixed-atom overclaim")
    ensure(firewall["SHARPNESS"] == "NOT_CLAIMED", "sharpness overclaim")
    ensure(firewall["TWIN_PRIME_RESULT"] == "NONE", "endpoint overclaim")
    ensure(
        firewall["NUMERICAL_CHECKS_ARE_THEOREM_EVIDENCE"] is False,
        "numerical evidence mutation",
    )

    rebuilt = independent_fixture()
    ensure(document.get("finite_fixture") == rebuilt, "fixture reconstruction mismatch")
    bucket_map = {row["a"]: row for row in rebuilt["buckets"]}
    ensure(rebuilt["max_actual_R"] == 3, "maximum collision mismatch")
    ensure(bucket_map[3]["actual_R"] == 3, "a=3 collision mismatch")
    ensure(bucket_map[79]["actual_R"] == 3, "a=79 collision mismatch")

    h_one = document.get("h_one_fixture")
    ensure(type(h_one) is dict, "h=1 fixture type")
    ensure(h_one["Q"] == 101 and h_one["H"] == 8830, "h=1 scales")
    ensure(h_one["M_1"] == 0 and h_one["row_empty"] is True, "h=1 row")
    ensure(all(value == 0 for value in h_one["cutoffs"]), "h=1 cutoff")

    expected_exponents = {
        "H": Fraction(21, 32),
        "Q": Fraction(1, 3),
        "Q_over_U": Fraction(1, 1200),
        "U": Fraction(133, 400),
        "direct_energy_power": Fraction(1, 96),
        "leading_unnormalized_power": Fraction(49, 48),
        "normalized_trace_power": Fraction(1, 48),
        "row_density_power": Fraction(1, 96),
        "secondary_trace_power": Fraction(1, 50),
        "window_correction_power": Fraction(-67, 200),
    }
    ledger = document.get("exact_exponent_ledger")
    ensure(type(ledger) is dict, "exponent ledger type")
    for name, expected in expected_exponents.items():
        ensure(read_fraction(ledger[name], name) == expected, f"{name} exponent")

    rejected = independent_mutations()
    mutation_document = document.get("mutation_firewalls")
    ensure(type(mutation_document) is dict, "mutation document type")
    ensure(rejected == mutation_document["rejected"], "mutation set mismatch")
    ensure(len(rejected) == mutation_document["rejected_count"], "mutation count")

    source = Path(__file__).read_text(encoding="utf-8")
    forbidden = "import " + "tpc239_bt_bucket_certificate"
    ensure(forbidden not in source, "checker imports producer")
    return {
        "TPC239_INDEPENDENT_CHECK": "PASS",
        "digest": supplied_digest,
        "max_actual_R": rebuilt["max_actual_R"],
        "mutations_rejected": len(rejected),
        "primitive_buckets": len(rebuilt["buckets"]),
        "producer_imports": 0,
        "shell_primes": rebuilt["shell_prime_count"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    print(
        json.dumps(
            verify(),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except IndependentFailure as error:
        raise SystemExit(f"TPC239_INDEPENDENT_CHECK=FAIL: {error}")
