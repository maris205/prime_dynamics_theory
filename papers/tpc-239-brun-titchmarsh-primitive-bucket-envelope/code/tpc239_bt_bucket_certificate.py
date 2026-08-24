#!/usr/bin/env python3
"""Deterministic certificate producer for the TPC-239 bucket theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_PATH = PROJECT_ROOT / "results" / "tpc239_certificate.json"

MARKERS = {
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

SCOPE_FIREWALL = {
    "ARITHMETIC_ADVANCE_IN_L2_GATE_B_SENSE": "NO",
    "C_H_SIGNED_CANCELLATION": "NONE",
    "FIXED_ATOM_CREDIT": 0,
    "FULL_GATE_B": "OPEN",
    "L2": "NONE",
    "NUMERICAL_CHECKS_ARE_THEOREM_EVIDENCE": False,
    "SHARPNESS": "NOT_CLAIMED",
    "SIGNED_FOUR_PACKET_PROJECTION": "NOT_PROVED",
    "STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TWIN_PRIME_RESULT": "NONE",
    "WEIGHTED_OR_SIGNED_WITHIN_BUCKET_CANCELLATION": "OPEN",
}


class CertificateFailure(RuntimeError):
    """Fail-closed validation error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool:
        raise CertificateFailure("validation condition is not a strict bool")
    if not condition:
        raise CertificateFailure(message)


def require_int(value: object, name: str) -> int:
    require(type(value) is int, f"{name} must be an exact int")
    return value


def require_str(value: object, name: str) -> str:
    require(type(value) is str and bool(value), f"{name} must be a nonempty str")
    return value


@dataclass(frozen=True)
class FixtureSpec:
    name: str
    Q: int
    H: int
    h: int

    def __post_init__(self) -> None:
        require_str(self.name, "name")
        require_int(self.Q, "Q")
        require_int(self.H, "H")
        require_int(self.h, "h")
        require(self.Q >= 2, "Q must be at least two")
        require(self.H > 0, "H must be positive")
        require(self.h >= 2, "h=1 belongs to the separate empty-row branch")
        require(4 * self.Q < self.H, "the fixture requires strict 4Q < H")
        require(self.h < self.Q, "the fixture requires h < Q")


def is_prime(value: int) -> bool:
    require_int(value, "prime candidate")
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def shell_primes(spec: FixtureSpec) -> list[int]:
    return [
        value
        for value in range(spec.Q + 1, 2 * spec.Q + 1)
        if is_prime(value)
    ]


def euler_phi(value: int) -> int:
    require_int(value, "totient input")
    require(value >= 1, "totient input must be positive")
    return sum(1 for residue in range(1, value + 1) if gcd(residue, value) == 1)


def validate_bucket(spec: FixtureSpec, residue: int) -> None:
    require_int(residue, "bucket residue")
    require(0 <= residue < spec.h, "bucket residue must be canonical")
    require(gcd(residue, spec.h) == 1, "bucket residue must be primitive")


def global_unit_multipliers(spec: FixtureSpec) -> tuple[int, list[int]]:
    maximum = (2 * spec.h * spec.Q) // spec.H
    multipliers = [
        value
        for value in range(-maximum, maximum + 1)
        if value != 0 and gcd(value, spec.h) == 1
    ]
    return maximum, multipliers


def validate_unit_multiplier(modulus: int, multiplier: int) -> None:
    require_int(modulus, "modulus")
    require_int(multiplier, "multiplier")
    require(modulus >= 2, "modulus must be at least two")
    require(multiplier != 0, "multiplier must be nonzero")
    require(gcd(multiplier, modulus) == 1, "multiplier is not a unit")


def validate_shell_prime(spec: FixtureSpec, prime: int) -> None:
    require_int(prime, "shell prime")
    require(spec.Q < prime <= 2 * spec.Q, "prime is outside the shell")
    require(is_prime(prime), "shell entry is not prime")


def physical_row(spec: FixtureSpec, prime: int) -> dict[str, Any]:
    validate_shell_prime(spec, prime)
    require(gcd(prime, spec.h) == 1, "shell prime is not invertible modulo h")
    cutoff = (spec.h * prime) // spec.H
    inverse = pow(prime, -1, spec.h)
    multipliers = [value for value in range(-cutoff, cutoff + 1) if value]
    residues = [(value * inverse) % spec.h for value in multipliers]
    require(len(residues) == len(set(residues)), "internal row injectivity failed")
    primitive = sorted(residue for residue in residues if gcd(residue, spec.h) == 1)
    return {
        "cutoff": cutoff,
        "multipliers": multipliers,
        "primitive_residues": primitive,
        "q": prime,
        "residues": residues,
    }


def validate_encoded_cutoff(spec: FixtureSpec, prime: int, encoded: int) -> None:
    validate_shell_prime(spec, prime)
    require_int(encoded, "encoded cutoff")
    require(encoded == (spec.h * prime) // spec.H, "q-dependent cutoff mutation")


def validate_factor_constant(value: int) -> None:
    require_int(value, "factor constant")
    require(value == 16, "factor-16 theorem constant was mutated")


def validate_order(actual: int, census: int) -> None:
    require_int(actual, "actual row count")
    require_int(census, "AP census")
    require(0 <= actual <= census, "actual row count exceeds AP census")


def decimal(value: float) -> str:
    require(type(value) is float and math.isfinite(value), "nonfinite real value")
    return format(value, ".12f")


def rational_record(value: Fraction, identity: str) -> dict[str, Any]:
    require(type(value) is Fraction, "exponent must be a Fraction")
    require_str(identity, "exponent identity")
    return {
        "denominator": value.denominator,
        "identity": identity,
        "numerator": value.numerator,
        "value": str(value),
    }


def bucket_record(
    spec: FixtureSpec,
    residue: int,
    primes: list[int],
    physical_rows: list[dict[str, Any]],
    multipliers: list[int],
    class_rhs: float,
    factor_rhs: float,
) -> dict[str, Any]:
    validate_bucket(spec, residue)
    inverse = pow(residue, -1, spec.h)
    actual_pairs: list[dict[str, int]] = []
    for row in physical_rows:
        matches = [
            multiplier
            for multiplier in row["multipliers"]
            if (multiplier * pow(row["q"], -1, spec.h)) % spec.h == residue
        ]
        require(len(matches) <= 1, "hidden duplicate inside one q-row")
        if matches:
            actual_pairs.append({"m": matches[0], "q": row["q"]})

    ap_rows: list[dict[str, Any]] = []
    pair_multiplicity = {prime: 0 for prime in primes}
    for multiplier in multipliers:
        validate_unit_multiplier(spec.h, multiplier)
        prime_class = (inverse * multiplier) % spec.h
        require(gcd(prime_class, spec.h) == 1, "compiled AP class is not reduced")
        row_primes = [prime for prime in primes if prime % spec.h == prime_class]
        require(
            len(row_primes) <= class_rhs + 1.0e-12,
            "finite AP row exceeds the stated real Brun--Titchmarsh bound",
        )
        for prime in row_primes:
            pair_multiplicity[prime] += 1
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
    validate_order(actual, census)
    require(census <= len(multipliers) * class_rhs + 1.0e-12, "AP row sum failed")
    require(census <= factor_rhs + 1.0e-12, "factor-16 real upper bound failed")
    dropped = sum(
        1
        for row in ap_rows
        for prime in row["primes"]
        if abs(row["m"]) > (spec.h * prime) // spec.H
    )
    return {
        "a": residue,
        "a_inverse": inverse,
        "actual_R": actual,
        "actual_pairs": actual_pairs,
        "ap_census": census,
        "ap_rows": ap_rows,
        "dropped_cutoff_pairs": dropped,
        "max_q_pair_multiplicity_in_ap_sum": max(pair_multiplicity.values()),
    }


def physical_fixture(spec: FixtureSpec) -> dict[str, Any]:
    primes = shell_primes(spec)
    require(bool(primes), "finite fixture has no shell primes")
    maximum, multipliers = global_unit_multipliers(spec)
    phi = euler_phi(spec.h)
    logarithm = math.log(2.0 * spec.Q / spec.h)
    require(logarithm > 0.0, "Brun--Titchmarsh logarithm is not positive")
    class_rhs = 4.0 * spec.Q / (phi * logarithm)
    factor_rhs = (
        16.0
        * spec.Q
        * spec.Q
        / spec.H
        * (spec.h / phi)
        / logarithm
    )
    rows = [physical_row(spec, prime) for prime in primes]
    buckets = [
        bucket_record(
            spec,
            residue,
            primes,
            rows,
            multipliers,
            class_rhs,
            factor_rhs,
        )
        for residue in range(spec.h)
        if gcd(residue, spec.h) == 1
    ]
    require(len(buckets) == phi, "primitive bucket count differs from phi(h)")
    require(len(multipliers) <= 2 * maximum, "unit multiplier count bound failed")
    require(
        Fraction(2 * maximum, 1) <= Fraction(4 * spec.h * spec.Q, spec.H),
        "2M_h <= 4hQ/H failed",
    )
    maximum_actual = max(row["actual_R"] for row in buckets)
    maximum_census = max(row["ap_census"] for row in buckets)
    return {
        "H": spec.H,
        "M_h": maximum,
        "Q": spec.Q,
        "ap_class_bt_rhs_approx": decimal(class_rhs),
        "buckets": buckets,
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "factor_16_rhs_approx": decimal(factor_rhs),
        "four_Q_less_than_H": True,
        "h": spec.h,
        "h_less_than_Q": True,
        "max_actual_R": maximum_actual,
        "max_ap_census": maximum_census,
        "multiplier_count": len(multipliers),
        "multipliers": multipliers,
        "name": spec.name,
        "phi_h": phi,
        "physical_rows": rows,
        "shell_prime_count": len(primes),
        "shell_primes": primes,
    }


def h_one_fixture(Q: int, H: int) -> dict[str, Any]:
    require_int(Q, "h=1 Q")
    require_int(H, "h=1 H")
    require(Q >= 2 and 2 * Q < H, "h=1 branch requires 2Q < H")
    primes = [value for value in range(Q + 1, 2 * Q + 1) if is_prime(value)]
    cutoffs = [(prime // H) for prime in primes]
    require(all(cutoff == 0 for cutoff in cutoffs), "h=1 row is not empty")
    return {
        "H": H,
        "M_1": (2 * Q) // H,
        "Q": Q,
        "classification": "EXACT_FINITE_EMPTY_ROW_CHECK",
        "cutoffs": cutoffs,
        "h": 1,
        "reason": "Every q <= 2Q < H, so floor(q/H)=0.",
        "row_empty": True,
        "shell_primes": primes,
    }


def exponent_ledger() -> dict[str, Any]:
    h_scale = Fraction(21, 32)
    q_scale = Fraction(1, 3)
    u_scale = Fraction(133, 400)
    q_over_u = q_scale - u_scale
    row_power = 2 * q_scale - h_scale
    direct_power = 2 * q_scale - h_scale
    trace_power = row_power + direct_power
    secondary_power = u_scale + q_scale - h_scale + direct_power
    window_power = 2 * u_scale - 1
    unnormalized = 1 + trace_power
    require(q_over_u == Fraction(1, 1200), "Q/U exponent mutation")
    require(row_power == Fraction(1, 96), "row exponent mutation")
    require(trace_power == Fraction(1, 48), "trace exponent mutation")
    require(secondary_power == Fraction(1, 50), "secondary exponent mutation")
    require(window_power == Fraction(-67, 200), "window exponent mutation")
    require(unnormalized == Fraction(49, 48), "unnormalized exponent mutation")
    return {
        "H": rational_record(h_scale, "H=x^(21/32)"),
        "Q": rational_record(q_scale, "Q=x^(1/3)"),
        "Q_over_U": rational_record(q_over_u, "1/3-133/400=1/1200"),
        "U": rational_record(u_scale, "U=x^(133/400)"),
        "direct_energy_power": rational_record(
            direct_power, "2/3-21/32=1/96"
        ),
        "leading_unnormalized_power": rational_record(
            unnormalized, "1+1/48=49/48"
        ),
        "normalized_trace_power": rational_record(
            trace_power, "1/96+1/96=1/48"
        ),
        "row_density_power": rational_record(
            row_power, "2/3-21/32=1/96"
        ),
        "secondary_trace_power": rational_record(
            secondary_power, "23/2400+1/96=1/50"
        ),
        "window_correction_power": rational_record(
            window_power, "2*(133/400)-1=-67/200"
        ),
    }


def expect_rejection(name: str, operation: Callable[[], None]) -> str:
    require_str(name, "mutation name")
    try:
        operation()
    except CertificateFailure:
        return name
    raise CertificateFailure(f"mutation was accepted: {name}")


def mutation_checks(spec: FixtureSpec) -> dict[str, Any]:
    cases: list[tuple[str, Callable[[], None]]] = [
        (
            "bool_Q_rejected_by_strict_type",
            lambda: FixtureSpec("bad_bool", True, spec.H, spec.h),
        ),
        (
            "composite_shell_entry",
            lambda: validate_shell_prime(spec, 121),
        ),
        (
            "cutoff_decrement",
            lambda: validate_encoded_cutoff(spec, 109, 0),
        ),
        (
            "factor_15",
            lambda: validate_factor_constant(15),
        ),
        (
            "four_Q_equals_H",
            lambda: FixtureSpec("bad_boundary", 11, 44, 7),
        ),
        (
            "h_equals_Q",
            lambda: FixtureSpec("bad_modulus", 11, 100, 11),
        ),
        (
            "h_one_sent_to_main_branch",
            lambda: FixtureSpec("bad_h_one", 11, 100, 1),
        ),
        (
            "nonprimitive_bucket",
            lambda: validate_bucket(spec, 2),
        ),
        (
            "nonunit_multiplier",
            lambda: validate_unit_multiplier(spec.h, 2),
        ),
        (
            "reversed_actual_ap_order",
            lambda: validate_order(2, 1),
        ),
        (
            "shell_lower_endpoint",
            lambda: validate_shell_prime(spec, spec.Q),
        ),
    ]
    rejected = sorted(expect_rejection(name, operation) for name, operation in cases)
    return {
        "classification": "MUTATION_FIREWALL",
        "rejected": rejected,
        "rejected_count": len(rejected),
    }


def validate_json_tree(value: Any, location: str = "payload") -> None:
    exact_type = type(value)
    if exact_type in {str, int, bool}:
        return
    if exact_type is float:
        require(math.isfinite(value), f"nonfinite float at {location}")
        return
    if exact_type is list:
        for index, item in enumerate(value):
            validate_json_tree(item, f"{location}[{index}]")
        return
    if exact_type is dict:
        for key, item in value.items():
            require(type(key) is str, f"nonstr key at {location}")
            validate_json_tree(item, f"{location}.{key}")
        return
    raise CertificateFailure(f"non-JSON strict type at {location}: {exact_type.__name__}")


def canonical_bytes(value: Any) -> bytes:
    validate_json_tree(value)
    return json.dumps(
        value, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("ascii")


def payload_digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def build_payload() -> dict[str, Any]:
    spec = FixtureSpec("V59_SHAPED_SQUAREFREE_TRIPLE_COLLISION", 101, 8830, 82)
    fixture = physical_fixture(spec)
    bucket_map = {row["a"]: row for row in fixture["buckets"]}
    require(fixture["max_actual_R"] == 3, "fixture maximum collision changed")
    require(bucket_map[3]["actual_R"] == 3, "a=3 triple collision changed")
    require(bucket_map[79]["actual_R"] == 3, "a=79 triple collision changed")
    payload = {
        "artifact": "TPC-239 Brun--Titchmarsh primitive-bucket certificate",
        "citation_boundary": {
            "classification": "LOCAL_SOURCE_VERIFICATION",
            "statement": (
                "TPC-61 lines 118--167 invoke the interval Brun--Titchmarsh"
                " theorem and cite MontgomeryVaughan2007; the repository contains"
                " the bibliography metadata but no page-level scan of the book."
            ),
        },
        "date": "2026-08-24",
        "exact_exponent_ledger": exponent_ledger(),
        "exact_theorem_ledger": {
            "ap_compiler": (
                "R_h(a) <= sum_{m in M_h^x} [pi(2Q;h,a^-1m)-pi(Q;h,a^-1m)]"
            ),
            "bt_class_bound": (
                "pi(2Q;h,b) <= 4Q/(phi(h)*log(2Q/h)) for reduced b"
            ),
            "factor_16": (
                "R_h(a) <= 16*(Q^2/H)*(h/phi(h))/log(2Q/h)"
            ),
            "h_one": "R_1(0)=0 because 2Q<H",
            "internal_row_injectivity": "4Q<H implies |m-m'|<h within one q-row",
            "packet_trace": (
                "N^-1 sum_{n in I_x} sum_j |K_j(n)|^2"
                " << J*M^2*x^(1/48)*(log x)^4*loglog x"
            ),
            "v59_row": (
                "max_{h<=U,(a,h)=1} R_h(a)"
                " << x^(1/96)*loglog(x)/log(x)"
            ),
        },
        "finite_fixture": fixture,
        "h_one_fixture": h_one_fixture(spec.Q, spec.H),
        "logarithmic_ledger": {
            "direct_energy": "(log x)^5",
            "improvement_over_TPC237": "log x/loglog x",
            "new_packet_trace": "(log x)^4 loglog x",
            "prime_density_row": "loglog x/log x",
        },
        "markers": MARKERS,
        "mutation_firewalls": mutation_checks(spec),
        "research_extraction": {
            "OPEN_THEOREM": (
                "weighted or signed within-bucket cancellation beyond"
                " coefficient-blind prime counting"
            ),
            "REUSABLE_STRUCTURE": "primitive residue -> reduced prime AP compiler",
            "ROUND2_CLUE": "test exact top-band C_h before seeking further uniform bucket savings",
            "STRONGEST_OBSTRUCTION": (
                "prime density saves only logarithm and leaves fixed-power 1/48"
            ),
            "STRONGEST_POSITIVE_RESULT": (
                "finite-window common-source packet trace with"
                " x^(1/48)(log x)^4 loglog x"
            ),
        },
        "schema_version": 1,
        "scope_firewall": SCOPE_FIREWALL,
        "source_locks": {
            "baseline_HEAD": "9603bffddb97f10dad81b2afbcbb1b0a2ddaff8a",
            "handoff_sha256": (
                "dee2986cbb0cb1cf698fa8a5edc557f9991fb8a03494617d19cfb80688ac4ef0"
            ),
            "tpc236_derivation_sha256": (
                "143c3620725350ad2658c022e0d32b5d0baefbebd2f3d41feaf8c7b2839152ec"
            ),
            "tpc236_proof_sha256": (
                "71f1b7a7f8d75dafed54ec5d59f4586483ddfaaa6001e5c2d21d0d22a9123c57"
            ),
            "tpc237_derivation_sha256": (
                "6a506ada581e424900c5587c157e851324b525a2426189d91af0b8796bd8f961"
            ),
            "tpc237_proof_sha256": (
                "9464a698148f57c7b0ed57ad1f45760585d68b6b8d56969de2347833b6aee425"
            ),
            "tpc61_bibliography_sha256": (
                "8c4352a5bf0154e7ebb30099e3e5d99b3d2c5fcdedfb7ed713a1ef2a6326e9a3"
            ),
            "tpc61_ladder_sha256": (
                "ea33868e7360e21d02da6d3dc587c29f8438945c57bb681eec85bf15fdaa8332"
            ),
        },
    }
    validate_json_tree(payload)
    return payload


def build_certificate() -> dict[str, Any]:
    payload = build_payload()
    return {**payload, "payload_sha256": payload_digest(payload)}


def pretty_bytes(value: Any) -> bytes:
    validate_json_tree(value)
    return (
        json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode("ascii")


def write_certificate() -> dict[str, Any]:
    certificate = build_certificate()
    CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE_PATH.write_bytes(pretty_bytes(certificate))
    return certificate


def check_certificate() -> dict[str, Any]:
    require(CERTIFICATE_PATH.is_file(), "certificate is missing")
    actual = CERTIFICATE_PATH.read_bytes()
    expected = build_certificate()
    require(actual == pretty_bytes(expected), "certificate bytes are not deterministic")
    loaded = json.loads(actual.decode("ascii"))
    supplied = loaded.get("payload_sha256")
    payload = dict(loaded)
    payload.pop("payload_sha256", None)
    require(supplied == payload_digest(payload), "payload digest mismatch")
    return loaded


def summary(certificate: dict[str, Any], action: str) -> dict[str, Any]:
    fixture = certificate["finite_fixture"]
    return {
        "TPC239_CERTIFICATE": "PASS",
        "action": action,
        "digest": certificate["payload_sha256"],
        "max_actual_R": fixture["max_actual_R"],
        "max_ap_census": fixture["max_ap_census"],
        "mutations_rejected": certificate["mutation_firewalls"]["rejected_count"],
        "primitive_buckets": len(fixture["buckets"]),
        "shell_primes": fixture["shell_prime_count"],
        "status": certificate["markers"]["TPC239_STATUS"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    certificate = write_certificate() if arguments.write else check_certificate()
    action = "write" if arguments.write else "check"
    print(
        json.dumps(
            summary(certificate, action),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificateFailure as error:
        raise SystemExit(f"TPC239_CERTIFICATE=FAIL: {error}")
