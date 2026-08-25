#!/usr/bin/env python3
"""Produce and check the exact TPC-245 covariance-disk certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc245_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS"
FINITE_CLASS = "NUMERICAL_FINITE_ILLUSTRATION_ONLY"
BASELINE_HEAD = "edc6f6ee80249a6c29f96acdc2a47e088f533474"
HANDOFF_SHA256 = "cdeb66efabdbe32814c8f1a69d04dbba0b06d7b010b4835519d1c7fcc76a33df"
SOURCE_HASHES = {
    "TPC219_DERIVATION": "b1c3795762f780625edab11fbe8543799eb121a33deb203b269fd6c338b6daca",
    "TPC219_PROOF": "c4954445bfb83bd4bbdb7674b3401c2327a6e4cd69d6d6ed9264f29a8f7e6f60",
    "TPC243_PROOF": "e7b17bd6babb1a00f690697ab4163053cfe33ddb61419bd73f8bf77d86e44faf",
    "TPC244_BRIDGE": "28d14c10c1e59a5d87c10508e974d776a641edb0075be4d569e256a0e6015439",
    "TPC244_PROOF": "f24de94c94db9dadf15727fb72cfd1b8c1ae596585ed99a0615ff13534109b49",
}

Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, ...]


class CertificateFailure(RuntimeError):
    """Fail-closed certificate error."""


def demand(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CertificateFailure(message)


def z(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    demand(type(real) in (int, Fraction) and type(imag) in (int, Fraction),
           "Gaussian rational input type")
    return (Fraction(real), Fraction(imag))


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def sub(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] - right[0], left[1] - right[1])


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def scale(value: Gaussian, scalar: int | Fraction) -> Gaussian:
    factor = Fraction(scalar)
    return (factor * value[0], factor * value[1])


def abs_sq(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def inner(first: Vector, second: Vector) -> Gaussian:
    """Inner product conjugate-linear in the first slot."""
    demand(len(first) == len(second), "vector dimension mismatch")
    total = z()
    for left, right in zip(first, second):
        total = add(total, mul(conj(left), right))
    return total


def norm_sq(value: Vector) -> Fraction:
    answer = inner(value, value)
    demand(answer[1] == 0 and answer[0] >= 0, "invalid squared norm")
    return answer[0]


def fraction_record(value: Fraction) -> dict[str, int]:
    demand(type(value) is Fraction, "fraction record type")
    return {"denominator": value.denominator, "numerator": value.numerator}


def gaussian_record(value: Gaussian) -> dict[str, dict[str, int]]:
    return {"im": fraction_record(value[1]), "re": fraction_record(value[0])}


def vector_record(value: Vector) -> list[dict[str, dict[str, int]]]:
    return [gaussian_record(entry) for entry in value]


def analyze_vectors(b_vector: Vector, w_vector: Vector) -> dict[str, Any]:
    demand(len(b_vector) == len(w_vector) and len(b_vector) >= 1,
           "fixture vector dimension")
    b = b_vector[0]
    w = w_vector[0]
    b_perp = b_vector[1:]
    w_perp = w_vector[1:]
    eb = norm_sq(b_perp)
    ew = norm_sq(w_perp)
    center = mul(conj(w), b)
    transverse = inner(w_perp, b_perp)
    covariance = inner(w_vector, b_vector)
    demand(covariance == add(center, transverse), "covariance decomposition")
    demand(abs_sq(transverse) <= eb * ew, "Cauchy disk")
    return {
        "B": vector_record(b_vector),
        "W": vector_record(w_vector),
        "E_B": fraction_record(eb),
        "E_W": fraction_record(ew),
        "center": gaussian_record(center),
        "transverse_covariance": gaussian_record(transverse),
        "covariance": gaussian_record(covariance),
        "cauchy_residual": fraction_record(eb * ew - abs_sq(transverse)),
    }


def disk_fixture() -> dict[str, Any]:
    b = z(1, 2)
    w = z(2, -1)
    samples = (
        ("center", (b, z(), z(2)), (w, z(3), z())),
        ("boundary", (b, z(0, 2), z()), (w, z(3), z())),
        (
            "interior",
            (b, z(Fraction(6, 5)), z(Fraction(8, 5))),
            (w, z(3), z()),
        ),
    )
    records = []
    for label, b_vector, w_vector in samples:
        record = analyze_vectors(b_vector, w_vector)
        demand(record["E_B"] == fraction_record(Fraction(4)), "disk E_B")
        demand(record["E_W"] == fraction_record(Fraction(9)), "disk E_W")
        record["label"] = label
        records.append(record)
    demand(records[0]["center"] == gaussian_record(z(0, 5)), "disk center")
    demand(records[0]["transverse_covariance"] == gaussian_record(z()),
           "disk center sample")
    demand(records[1]["transverse_covariance"] == gaussian_record(z(0, 6)),
           "disk boundary sample")
    demand(records[2]["transverse_covariance"] ==
           gaussian_record(z(Fraction(18, 5))), "disk interior sample")
    return {
        "classification": FINITE_CLASS,
        "dimension_transverse": 2,
        "fixed_E_B": fraction_record(Fraction(4)),
        "fixed_E_W": fraction_record(Fraction(9)),
        "radius_squared": fraction_record(Fraction(36)),
        "sample_count": len(records),
        "samples": records,
    }


def circle_fixture() -> dict[str, Any]:
    phases = (z(1), z(0, 1), z(-1), z(0, -1))
    records = []
    for phase in phases:
        record = analyze_vectors((z(), scale(phase, 2)), (z(), z(3)))
        transverse = inner((z(3),), (scale(phase, 2),))
        demand(abs_sq(transverse) == 36, "dimension-one circle radius")
        records.append(record)
    demand(len({json.dumps(item["covariance"], sort_keys=True) for item in records}) == 4,
           "circle phase diversity")
    return {
        "classification": FINITE_CLASS,
        "dimension_transverse": 1,
        "interior_zero_feasible": False,
        "phase_count": len(records),
        "radius_squared": fraction_record(Fraction(36)),
        "samples": records,
    }


def singleton_and_zero_dimension_fixture() -> dict[str, Any]:
    b = z(1, 2)
    w = z(2, -1)
    one_dimensional = analyze_vectors((b, z()), (w, z(3)))
    zero_dimensional = analyze_vectors((b,), (w,))
    demand(one_dimensional["covariance"] == one_dimensional["center"],
           "zero-radius singleton")
    demand(zero_dimensional["covariance"] == zero_dimensional["center"],
           "zero-dimensional singleton")
    return {
        "classification": FINITE_CLASS,
        "dimension_one_radius_zero": one_dimensional,
        "dimension_zero_energy_zero": zero_dimensional,
        "dimension_zero_positive_energy_realizable": False,
    }


def phase_tangent_fixture() -> dict[str, Any]:
    q_tangent = z(Fraction(-9, 5), Fraction(12, 5))
    b_vector = (z(5), scale(q_tangent, Fraction(1, 3)))
    w_vector = (z(1), z(3))
    record = analyze_vectors(b_vector, w_vector)
    covariance = inner(w_vector, b_vector)
    demand(record["center"] == gaussian_record(z(5)), "phase center")
    demand(abs_sq(q_tangent) == 9, "phase radius squared")
    demand(covariance == z(Fraction(16, 5), Fraction(12, 5)), "tangent point")
    demand(abs_sq(covariance) == 16, "tangent modulus")
    demand(Fraction(abs(covariance[1]), 1) / 4 == Fraction(3, 5),
           "sharp sine ratio")
    return {
        "classification": FINITE_CLASS,
        "center_modulus": fraction_record(Fraction(5)),
        "radius": fraction_record(Fraction(3)),
        "tangent_covariance": gaussian_record(covariance),
        "tangent_modulus": fraction_record(Fraction(4)),
        "sharp_sine_ratio": fraction_record(Fraction(3, 5)),
        "vector_record": record,
    }


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def strict_json_loads(raw: str) -> dict[str, Any]:
    def pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        output: dict[str, object] = {}
        for key, value in pairs:
            demand(type(key) is str and key not in output, "duplicate JSON key")
            output[key] = value
        return output

    def reject_constant(value: str) -> object:
        raise CertificateFailure("nonfinite JSON constant: " + value)

    def reject_float(value: str) -> object:
        raise CertificateFailure("floating JSON number: " + value)

    parsed = json.loads(raw, object_pairs_hook=pairs_hook,
                        parse_constant=reject_constant, parse_float=reject_float)
    demand(type(parsed) is dict, "top-level certificate type")
    return parsed


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


def build_document() -> dict[str, Any]:
    payload = {
        "baseline": {
            "head": BASELINE_HEAD,
            "handoff_sha256": HANDOFF_SHA256,
            "source_hashes": SOURCE_HASHES,
        },
        "classification": FINITE_CLASS,
        "fixtures": {
            "dimension_at_least_two_disk": disk_fixture(),
            "dimension_one_circle": circle_fixture(),
            "low_dimension_singletons": singleton_and_zero_dimension_fixture(),
            "sharp_phase_tangent": phase_tangent_fixture(),
        },
        "scope_firewall": {
            "ARITHMETIC_ADVANCE": "NO",
            "ARITHMETIC_L2": "NONE",
            "CANONICAL_BLOCK_DIRECTION": "OPEN",
            "FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE": False,
            "FIXED_ATOM_CREDIT": 0,
            "FULL_GATE_B": "OPEN",
            "LITERAL_V59_TWO_LANE_ATTACHMENT": "OPEN",
            "STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC219_RELATION": "PROJECTION_LINEAGE_ONLY_NOT_LITERAL_OBJECT_IDENTITY",
            "TWIN_PRIME_RESULT": "NONE",
        },
        "status": STATUS,
        "theorem": {
            "decomposition": "<W,B>=conjugate(w)b+<W_perp,B_perp>",
            "dimension_at_least_two": "CLOSED_DISK_CENTER_C_RADIUS_SQRT_EB_EW",
            "dimension_one": "BOUNDARY_CIRCLE_IF_R_POSITIVE_ELSE_SINGLETON",
            "dimension_zero": "SINGLETON_IF_ZERO_ENERGIES_ELSE_UNREALIZABLE",
            "minimum_modulus_disk": "max(|c|-r,0)",
            "orientation": "CONJUGATE_LINEAR_FIRST_SLOT_CENTER_CONJUGATE_W_TIMES_B",
            "phase_sector": "SHARP_HALF_ANGLE_ARCSIN_R_OVER_ABS_C_WHEN_R_LT_ABS_C",
            "zero_feasibility_disk": "IFF_ABS_C_LE_R",
        },
    }
    return {
        "certificate_version": 1,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical_json(payload)).hexdigest(),
        "schema": "tpc245-longitudinal-transverse-covariance-disks-v1",
    }


def write_certificate() -> None:
    CERTIFICATE.write_bytes(canonical_json(build_document()) + b"\n")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    demand(raw.endswith(b"\n") and raw.count(b"\n") == 1,
           "certificate newline discipline")
    stored = strict_json_loads(raw.decode("ascii"))
    expected = build_document()
    demand(same_typed(stored, expected), "certificate payload mismatch")
    demand(raw == canonical_json(stored) + b"\n", "noncanonical certificate bytes")
    demand(type(stored["certificate_version"]) is int, "version exact int type")
    demand(stored["payload_sha256"] ==
           hashlib.sha256(canonical_json(stored["payload"])).hexdigest(),
           "payload hash")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write_certificate()
            print("TPC245_COMMON_COVARIANCE_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
            document = build_document()
            print("TPC245_COMMON_COVARIANCE_CERTIFICATE=PASS")
            print("mode=check")
            print("status=" + STATUS)
            print("disk_samples=" + str(document["payload"]["fixtures"]
                                           ["dimension_at_least_two_disk"]["sample_count"]))
            print("circle_phases=" + str(document["payload"]["fixtures"]
                                           ["dimension_one_circle"]["phase_count"]))
            print("canonical_block_direction=OPEN")
            print("arithmetic_advance=NO")
    except (CertificateFailure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, json.JSONDecodeError) as error:
        raise SystemExit("TPC245_COMMON_COVARIANCE_CERTIFICATE=FAIL: " + str(error))


if __name__ == "__main__":
    main()
