#!/usr/bin/env python3
"""Produce and check the exact TPC-242 phase-Fourier certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "tpc242_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER"
CLAIM_CEILING = "PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER"
BASELINE_HEAD = "845256279ca1126c592e210801ce3dbb3d743eab"
HANDOFF_SHA256 = "48c2a5cf18928e3058c3fef4d50052fae9cd90b3dc910e4c66bff1dfbeec35c6"
PREWRITE_STATUS_SHA256 = "4791573e6877bd20e60a8a3338c1522847744e865d34daff52b4fdf3f9209699"
FINITE_CLASS = "NUMERICAL_FINITE_ILLUSTRATION_ONLY"
MUTATIONS = [
    "bool_int_confusion",
    "common_offset_projection",
    "duplicate_json_key",
    "f2_zero",
    "inner_product_orientation",
    "nonfinite_json_constant",
    "phase_sign_i_j_vs_minus_i_j",
    "physical_attachment",
    "status_promotion",
]

Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, ...]


class CertificateFailure(RuntimeError):
    """Fail-closed certificate error."""


def demand(condition: bool, message: str) -> None:
    if type(condition) is not bool:
        raise CertificateFailure("guard condition is not a strict bool")
    if not condition:
        raise CertificateFailure(message)


def strict_int(value: object, label: str) -> int:
    demand(type(value) is int, label + " must be an exact int")
    return value


def strict_string(value: object, label: str) -> str:
    demand(type(value) is str and bool(value), label + " must be a nonempty string")
    return value


def q(value: int | Fraction) -> Fraction:
    demand(type(value) in (int, Fraction), "rational input type")
    return Fraction(value)


def z(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return (q(real), q(imag))


def z_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def z_mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def z_conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def z_scale(value: Gaussian, scalar: Fraction) -> Gaussian:
    demand(type(scalar) is Fraction, "Gaussian scale type")
    return (scalar * value[0], scalar * value[1])


def z_abs_sq(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def i_power(exponent: int) -> Gaussian:
    strict_int(exponent, "phase exponent")
    return (z(1), z(0, 1), z(-1), z(0, -1))[exponent % 4]


def vector_add(left: Vector, right: Vector) -> Vector:
    demand(len(left) == len(right), "vector dimension mismatch")
    return tuple(z_add(a, b) for a, b in zip(left, right))


def vector_scale(scalar: Gaussian, value: Vector) -> Vector:
    return tuple(z_mul(scalar, coordinate) for coordinate in value)


def inner(first: Vector, second: Vector) -> Gaussian:
    """Conjugate-linear in first, linear in second."""
    demand(len(first) == len(second), "inner-product dimension mismatch")
    total = z()
    for left, right in zip(first, second):
        total = z_add(total, z_mul(z_conj(left), right))
    return total


def norm_sq(value: Vector) -> Fraction:
    result = inner(value, value)
    demand(result[1] == 0 and result[0] >= 0, "invalid squared norm")
    return result[0]


def phase_energies(x_value: Vector, y_value: Vector) -> list[Fraction]:
    return [
        norm_sq(vector_add(x_value, vector_scale(i_power(j), y_value)))
        for j in range(4)
    ]


def phase_spectrum(energies: list[Fraction]) -> list[Gaussian]:
    demand(type(energies) is list and len(energies) == 4, "energy vector length")
    output: list[Gaussian] = []
    for k in range(4):
        total = z()
        for j, energy in enumerate(energies):
            demand(type(energy) is Fraction, "energy type")
            total = z_add(total, z_mul(i_power(k * j), z(energy)))
        output.append(z_scale(total, Fraction(1, 4)))
    return output


def fraction_record(value: Fraction) -> dict[str, int]:
    demand(type(value) is Fraction, "fraction record type")
    return {"denominator": value.denominator, "numerator": value.numerator}


def gaussian_record(value: Gaussian) -> dict[str, dict[str, int]]:
    return {"im": fraction_record(value[1]), "re": fraction_record(value[0])}


def vector_record(value: Vector) -> list[dict[str, dict[str, int]]]:
    return [gaussian_record(coordinate) for coordinate in value]


def pair_fixtures() -> list[tuple[str, Vector, Vector]]:
    return [
        (
            "ORIENTATION_NONREAL",
            (z(1, 2), z(Fraction(1, 2), -1)),
            (z(Fraction(3, 2), -1), z(-2, Fraction(1, 3))),
        ),
        ("CENTER_ORTHOGONAL", (z(1), z()), (z(), z(1))),
        ("BOUNDARY_POSITIVE_I", (z(1), z()), (z(0, -1), z())),
    ]


def fixture_record(identifier: str, x_value: Vector, y_value: Vector) -> dict[str, Any]:
    energies = phase_energies(x_value, y_value)
    spectrum = phase_spectrum(energies)
    nx = norm_sq(x_value)
    ny = norm_sq(y_value)
    selected = inner(y_value, x_value)
    gram = nx * ny - z_abs_sq(selected)
    imbalance = (nx - ny) ** 2
    lhs = (nx + ny) ** 2 - 4 * z_abs_sq(selected)
    rhs = imbalance + 4 * gram
    demand(spectrum == [z(nx + ny), selected, z(), inner(x_value, y_value)],
           "phase spectrum computation")
    demand(lhs == rhs and gram >= 0, "defect computation")
    return {
        "E": [fraction_record(value) for value in energies],
        "F": [gaussian_record(value) for value in spectrum],
        "X": vector_record(x_value),
        "Y": vector_record(y_value),
        "classification": FINITE_CLASS,
        "defect": {
            "gram_determinant": fraction_record(gram),
            "imbalance_square": fraction_record(imbalance),
            "lhs": fraction_record(lhs),
            "rhs": fraction_record(rhs),
        },
        "id": strict_string(identifier, "fixture id"),
        "selected_coefficient": gaussian_record(selected),
        "total_energy": fraction_record(nx + ny),
    }


def disk_pairs() -> list[tuple[str, Vector, Vector]]:
    return [
        ("ZERO_S", (z(), z()), (z(), z())),
        ("CENTER_S2", (z(1), z()), (z(), z(1))),
        (
            "INTERIOR_COMPLEX_S2",
            (z(1), z()),
            (z(Fraction(1, 3), Fraction(-2, 3)), z(Fraction(2, 3))),
        ),
        ("BOUNDARY_I_S2", (z(1), z()), (z(0, -1), z())),
    ]


def disk_record(identifier: str, x_value: Vector, y_value: Vector) -> dict[str, Any]:
    total = norm_sq(x_value) + norm_sq(y_value)
    selected = inner(y_value, x_value)
    magnitude = z_abs_sq(selected)
    radius_sq = (total / 2) ** 2
    demand(magnitude <= radius_sq, "disk witness outside feasible disk")
    return {
        "X": vector_record(x_value),
        "Y": vector_record(y_value),
        "classification": FINITE_CLASS,
        "id": strict_string(identifier, "disk id"),
        "inside_closed_disk": True,
        "radius_squared": fraction_record(radius_sq),
        "selected_coefficient": gaussian_record(selected),
        "selected_magnitude_squared": fraction_record(magnitude),
        "total_energy": fraction_record(total),
    }


def source_anchors() -> dict[str, dict[str, str]]:
    return {
        "TPC222": {
            "locator": "papers/tpc-222-four-packet-cross-term-obstruction/PROOF_PACKAGE.md:8-24",
            "sha256": "1963e7fd0011f0e3bc83ebc0c6bb68885180c3a9f5da06597f228fe00be27811",
        },
        "TPC228": {
            "locator": "papers/tpc-228-source-native-polarized-collision-compiler/PROOF_PACKAGE.md:3-65",
            "sha256": "1b6f91f100b89222dc08a070623e6162539b8e88b17b807b2d4ccfb6338da61d",
        },
        "TPC241": {
            "locator": "papers/tpc-241-top-prime-collision-sharpness/PROOF_PACKAGE.md:19-40,141-146",
            "sha256": "f5ba7b04a432cac12d576a34e69c887e9f925b2b6906cc41a5a588ef32d19d8c",
        },
        "V59": {
            "locator": "research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:143-205",
            "sha256": "74e42689e17efad75e9718a9d6ac3d8f3ec9c16239204a4915b0b7bdc17ae218",
        },
    }


def build_payload() -> dict[str, Any]:
    offset = Fraction(7, 5)
    offset_delta = phase_spectrum([offset, offset, offset, offset])
    demand(offset_delta == [z(offset), z(), z(), z()], "common-offset projection")
    return {
        "certificate_version": 1,
        "common_offset_fixture": {
            "additive_scalar": fraction_record(offset),
            "classification": FINITE_CLASS,
            "delta_spectrum": [gaussian_record(value) for value in offset_delta],
        },
        "date": "2026-08-25",
        "exact_fixtures": [fixture_record(*record) for record in pair_fixtures()],
        "feasible_disk_witnesses": [disk_record(*record) for record in disk_pairs()],
        "mutation_firewalls": {
            "rejected": MUTATIONS,
            "rejected_count": len(MUTATIONS),
        },
        "object_lock": {
            "ambient_space": "COMPLEX_HILBERT_SPACE",
            "energy_phase": "E_j=||X+i^jY||^2",
            "fourier_phase": "F_k=(1/4)sum_j i^(k*j)E_j",
            "inner_product": "CONJUGATE_LINEAR_FIRST_LINEAR_SECOND",
            "selected_mode": "F_1=<Y,X>",
            "source_type": "ABSTRACT_HILBERT_PHASE_ENERGIES_ONLY",
            "v59_scalar_orientation": "x*conjugate(y)=<y,x>",
        },
        "scope_firewall": {
            "ARITHMETIC_L2": "NONE",
            "FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE": False,
            "FIXED_ATOM_CREDIT": 0,
            "FULL_GATE_B": "OPEN",
            "PHYSICAL_TOP_PRIME_MODE_ANNIHILATION": "NOT_CLAIMED",
            "SIGNED_C_H_THEOREM": "NONE",
            "STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC241_DIRECT_QUANTITATIVE_IMPLICATION_FOR_F1": "ZERO",
            "TPC241_TO_V59_IDENTIFICATION": "OPEN",
            "TWIN_PRIME_RESULT": "NONE",
        },
        "source_lock": {
            "anchors": source_anchors(),
            "direct_tpc241_to_v59_attachment": "STOP_SCOPED",
            "proof_audit": "GO_AT_PROVED_STRUCTURAL_L1_ONLY",
        },
        "status_ledger": {
            "arithmetic_advance": "NO",
            "claim_ceiling": CLAIM_CEILING,
            "route_advance": "YES_OBSTRUCTION",
            "status": STATUS,
        },
        "task_lock": {
            "baseline_head": BASELINE_HEAD,
            "handoff_sha256": HANDOFF_SHA256,
            "paper_number": 242,
            "prewrite_status_sha256": PREWRITE_STATUS_SHA256,
            "task_id": "TPC242-WRITE-20260825-A",
        },
        "theorem": {
            "classification": "PROVED_STRUCTURAL_L1_ONLY",
            "complete_spectrum": {
                "F_0": "||X||^2+||Y||^2",
                "F_1": "<Y,X>",
                "F_2": "0",
                "F_3": "<X,Y>",
            },
            "defect_identity": "S^2-4|F_1|^2=(||X||^2-||Y||^2)^2+4(||X||^2||Y||^2-|<Y,X>|^2)",
            "fixed_energy_feasible_set": "{z in C: |z|<=S/2},INCLUDING_S=0",
            "phase_blind_additive_scalar": "DELTA_F_0=A_AND_DELTA_F_1=DELTA_F_2=DELTA_F_3=0",
        },
    }


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True).encode("ascii")


def build_document() -> dict[str, Any]:
    payload = build_payload()
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


def reject_constant(value: str) -> None:
    raise CertificateFailure("nonfinite JSON constant: " + value)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise CertificateFailure("duplicate JSON key: " + key)
        result[key] = value
    return result


def strict_json_loads(text: str) -> object:
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def validate_document(document: object, raw_bytes: bytes | None = None) -> dict[str, Any]:
    demand(type(document) is dict, "top-level JSON type")
    expected_payload = build_payload()
    digest = document.get("payload_sha256")
    demand(type(digest) is str and len(digest) == 64, "payload digest type")
    payload = dict(document)
    del payload["payload_sha256"]
    demand(same_typed(payload, expected_payload), "certificate payload mismatch")
    demand(hashlib.sha256(canonical_json(payload)).hexdigest() == digest,
           "payload digest mismatch")
    if raw_bytes is not None:
        demand(raw_bytes == canonical_json(document) + b"\n", "noncanonical JSON bytes")
    return document


def rebound(document: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(document)
    result.pop("payload_sha256", None)
    digest = hashlib.sha256(canonical_json(result)).hexdigest()
    result["payload_sha256"] = digest
    return result


def rejected(name: str, operation: Callable[[], None]) -> str:
    try:
        operation()
    except CertificateFailure:
        return name
    raise CertificateFailure("mutation accepted: " + name)


def run_mutation_firewalls(base: dict[str, Any]) -> list[str]:
    def semantic(path: tuple[str, ...], value: object) -> None:
        mutated = deepcopy(base)
        cursor: dict[str, Any] = mutated
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        validate_document(rebound(mutated))

    cases: dict[str, Callable[[], None]] = {
        "bool_int_confusion": lambda: semantic(("certificate_version",), True),
        "common_offset_projection": lambda: semantic(
            ("theorem", "phase_blind_additive_scalar"), "DELTA_F_1=A"
        ),
        "duplicate_json_key": lambda: strict_json_loads('{"a":1,"a":2}'),
        "f2_zero": lambda: semantic(("theorem", "complete_spectrum", "F_2"), "NONZERO"),
        "inner_product_orientation": lambda: semantic(
            ("object_lock", "inner_product"), "LINEAR_FIRST_CONJUGATE_LINEAR_SECOND"
        ),
        "nonfinite_json_constant": lambda: strict_json_loads('{"a":NaN}'),
        "phase_sign_i_j_vs_minus_i_j": lambda: semantic(
            ("object_lock", "energy_phase"), "E_j=||X+(-i)^jY||^2"
        ),
        "physical_attachment": lambda: semantic(
            ("scope_firewall", "TPC241_TO_V59_IDENTIFICATION"), "PROVED"
        ),
        "status_promotion": lambda: semantic(("scope_firewall", "ARITHMETIC_L2"), "PROVED"),
    }
    demand(sorted(cases) == MUTATIONS, "mutation registry drift")
    return sorted(rejected(name, cases[name]) for name in cases)


def check_certificate() -> dict[str, Any]:
    demand(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_bytes()
    document = strict_json_loads(raw.decode("ascii"))
    checked = validate_document(document, raw)
    demand(run_mutation_firewalls(checked) == MUTATIONS, "mutation firewall failure")
    return checked


def write_certificate() -> dict[str, Any]:
    document = build_document()
    validate_document(document)
    demand(run_mutation_firewalls(document) == MUTATIONS, "mutation firewall failure")
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_bytes(canonical_json(document) + b"\n")
    return document


def summary(mode: str) -> None:
    print("TPC242_PHASE_FOURIER_CERTIFICATE=PASS")
    print("mode=" + mode)
    print("status=" + STATUS)
    print("exact_pair_fixtures=" + str(len(pair_fixtures())))
    print("disk_witnesses=" + str(len(disk_pairs())))
    print("mutation_firewalls=" + str(len(MUTATIONS)))
    print("tpc241_direct_F1_credit=ZERO")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write_certificate()
            summary("write")
        else:
            check_certificate()
            summary("check")
    except (CertificateFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC242_PHASE_FOURIER_CERTIFICATE=FAIL: " + str(error))


if __name__ == "__main__":
    main()
