#!/usr/bin/env python3
"""Independent exact checker for TPC-242; it does not import the producer."""

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
HOSTILE_SCHEMA_MUTATIONS = [
    "route_advance_rebinding",
    "source_lock_rebinding",
    "strict_1_over_400_promotion",
    "twin_prime_result_promotion",
]

Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, ...]


class IndependentFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise IndependentFailure(message)


def g(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    require(type(real) in (int, Fraction) and type(imag) in (int, Fraction), "Gaussian type")
    return (Fraction(real), Fraction(imag))


def plus(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def times(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def conjugate(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def phase(exponent: int) -> Gaussian:
    require(type(exponent) is int, "phase exponent type")
    return (g(1), g(0, 1), g(-1), g(0, -1))[exponent % 4]


def add_vectors(left: Vector, right: Vector) -> Vector:
    require(len(left) == len(right), "dimension")
    return tuple(plus(a, b) for a, b in zip(left, right))


def scale_vector(scalar: Gaussian, value: Vector) -> Vector:
    return tuple(times(scalar, coordinate) for coordinate in value)


def product(first: Vector, second: Vector) -> Gaussian:
    require(len(first) == len(second), "inner dimension")
    total = g()
    for left, right in zip(first, second):
        total = plus(total, times(conjugate(left), right))
    return total


def squared_norm(value: Vector) -> Fraction:
    result = product(value, value)
    require(result[1] == 0 and result[0] >= 0, "norm")
    return result[0]


def compute_energies(x_value: Vector, y_value: Vector) -> list[Fraction]:
    return [squared_norm(add_vectors(x_value, scale_vector(phase(j), y_value))) for j in range(4)]


def compute_spectrum(energies: list[Fraction]) -> list[Gaussian]:
    require(type(energies) is list and len(energies) == 4, "energy count")
    result: list[Gaussian] = []
    for k in range(4):
        total = g()
        for j in range(4):
            total = plus(total, times(phase(k * j), g(energies[j])))
        result.append((total[0] / 4, total[1] / 4))
    return result


def decode_fraction(record: object, label: str) -> Fraction:
    require(type(record) is dict and set(record) == {"denominator", "numerator"}, label + " keys")
    numerator = record["numerator"]
    denominator = record["denominator"]
    require(type(numerator) is int and type(denominator) is int and denominator > 0, label + " types")
    value = Fraction(numerator, denominator)
    require(value.numerator == numerator and value.denominator == denominator, label + " nonminimal")
    return value


def decode_gaussian(record: object, label: str) -> Gaussian:
    require(type(record) is dict and set(record) == {"im", "re"}, label + " keys")
    return (decode_fraction(record["re"], label + ".re"),
            decode_fraction(record["im"], label + ".im"))


def decode_vector(record: object, label: str) -> Vector:
    require(type(record) is list and len(record) == 2, label + " dimension")
    return tuple(decode_gaussian(value, label) for value in record)


def strict_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise IndependentFailure("duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise IndependentFailure("nonfinite JSON constant: " + value)


def strict_loads(text: str) -> object:
    return json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_constant)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True).encode("ascii")


def expected_pairs() -> list[tuple[str, Vector, Vector]]:
    return [
        ("ORIENTATION_NONREAL", (g(1, 2), g(Fraction(1, 2), -1)),
         (g(Fraction(3, 2), -1), g(-2, Fraction(1, 3)))),
        ("CENTER_ORTHOGONAL", (g(1), g()), (g(), g(1))),
        ("BOUNDARY_POSITIVE_I", (g(1), g()), (g(0, -1), g())),
    ]


def expected_disks() -> list[tuple[str, Vector, Vector]]:
    return [
        ("ZERO_S", (g(), g()), (g(), g())),
        ("CENTER_S2", (g(1), g()), (g(), g(1))),
        ("INTERIOR_COMPLEX_S2", (g(1), g()),
         (g(Fraction(1, 3), Fraction(-2, 3)), g(Fraction(2, 3)))),
        ("BOUNDARY_I_S2", (g(1), g()), (g(0, -1), g())),
    ]


def check_metadata(document: dict[str, Any]) -> None:
    expected_top = {
        "certificate_version", "common_offset_fixture", "date", "exact_fixtures",
        "feasible_disk_witnesses", "mutation_firewalls", "object_lock", "payload_sha256",
        "scope_firewall", "source_lock", "status_ledger", "task_lock", "theorem"
    }
    require(set(document) == expected_top, "top-level keys")
    require(type(document["certificate_version"]) is int and document["certificate_version"] == 1,
            "certificate version")
    require(document["date"] == "2026-08-25", "date")
    lock = document["object_lock"]
    require(type(lock) is dict and lock == {
        "ambient_space": "COMPLEX_HILBERT_SPACE",
        "energy_phase": "E_j=||X+i^jY||^2",
        "fourier_phase": "F_k=(1/4)sum_j i^(k*j)E_j",
        "inner_product": "CONJUGATE_LINEAR_FIRST_LINEAR_SECOND",
        "selected_mode": "F_1=<Y,X>",
        "source_type": "ABSTRACT_HILBERT_PHASE_ENERGIES_ONLY",
        "v59_scalar_orientation": "x*conjugate(y)=<y,x>",
    }, "object/orientation lock")
    theorem = document["theorem"]
    require(type(theorem) is dict and theorem == {
        "classification": "PROVED_STRUCTURAL_L1_ONLY",
        "complete_spectrum": {
            "F_0": "||X||^2+||Y||^2",
            "F_1": "<Y,X>",
            "F_2": "0",
            "F_3": "<X,Y>",
        },
        "defect_identity":
            "S^2-4|F_1|^2=(||X||^2-||Y||^2)^2+4(||X||^2||Y||^2-|<Y,X>|^2)",
        "fixed_energy_feasible_set": "{z in C: |z|<=S/2},INCLUDING_S=0",
        "phase_blind_additive_scalar":
            "DELTA_F_0=A_AND_DELTA_F_1=DELTA_F_2=DELTA_F_3=0",
    }, "complete theorem schema")
    firewall = document["scope_firewall"]
    require(type(firewall) is dict and firewall == {
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
    }, "complete scope-firewall schema")
    source_lock = document["source_lock"]
    require(type(source_lock) is dict and source_lock == {
        "anchors": {
            "TPC222": {
                "locator":
                    "papers/tpc-222-four-packet-cross-term-obstruction/PROOF_PACKAGE.md:8-24",
                "sha256":
                    "1963e7fd0011f0e3bc83ebc0c6bb68885180c3a9f5da06597f228fe00be27811",
            },
            "TPC228": {
                "locator":
                    "papers/tpc-228-source-native-polarized-collision-compiler/PROOF_PACKAGE.md:3-65",
                "sha256":
                    "1b6f91f100b89222dc08a070623e6162539b8e88b17b807b2d4ccfb6338da61d",
            },
            "TPC241": {
                "locator":
                    "papers/tpc-241-top-prime-collision-sharpness/PROOF_PACKAGE.md:19-40,141-146",
                "sha256":
                    "f5ba7b04a432cac12d576a34e69c887e9f925b2b6906cc41a5a588ef32d19d8c",
            },
            "V59": {
                "locator":
                    "research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:143-205",
                "sha256":
                    "74e42689e17efad75e9718a9d6ac3d8f3ec9c16239204a4915b0b7bdc17ae218",
            },
        },
        "direct_tpc241_to_v59_attachment": "STOP_SCOPED",
        "proof_audit": "GO_AT_PROVED_STRUCTURAL_L1_ONLY",
    }, "complete source-lock schema")
    ledger = document["status_ledger"]
    require(type(ledger) is dict and ledger == {
        "arithmetic_advance": "NO",
        "claim_ceiling": STATUS,
        "route_advance": "YES_OBSTRUCTION",
        "status": STATUS,
    }, "complete status-ledger schema")
    task = document["task_lock"]
    require(type(task) is dict and task == {
        "baseline_head": "845256279ca1126c592e210801ce3dbb3d743eab",
        "handoff_sha256": "48c2a5cf18928e3058c3fef4d50052fae9cd90b3dc910e4c66bff1dfbeec35c6",
        "paper_number": 242,
        "prewrite_status_sha256": "4791573e6877bd20e60a8a3338c1522847744e865d34daff52b4fdf3f9209699",
        "task_id": "TPC242-WRITE-20260825-A",
    }, "task lock")
    require(type(task["paper_number"]) is int, "paper number bool/int")
    mutations = document["mutation_firewalls"]
    require(type(mutations) is dict and mutations == {
        "rejected": MUTATIONS,
        "rejected_count": len(MUTATIONS),
    }, "complete mutation manifest")
    require(type(mutations["rejected_count"]) is int, "mutation count type")


def check_exact_fixtures(document: dict[str, Any]) -> int:
    fixtures = document["exact_fixtures"]
    require(type(fixtures) is list and len(fixtures) == len(expected_pairs()), "fixture count")
    for record, (identifier, expected_x, expected_y) in zip(fixtures, expected_pairs()):
        require(type(record) is dict and record["id"] == identifier, "fixture id")
        require(record["classification"] == FINITE_CLASS, "fixture class")
        x_value = decode_vector(record["X"], identifier + ".X")
        y_value = decode_vector(record["Y"], identifier + ".Y")
        require(x_value == expected_x and y_value == expected_y, "fixture rebinding")
        energies = compute_energies(x_value, y_value)
        spectrum = compute_spectrum(energies)
        require([decode_fraction(item, "E") for item in record["E"]] == energies, "energy record")
        require([decode_gaussian(item, "F") for item in record["F"]] == spectrum, "spectrum record")
        nx, ny = squared_norm(x_value), squared_norm(y_value)
        selected = product(y_value, x_value)
        require(spectrum == [g(nx + ny), selected, g(), product(x_value, y_value)], "spectrum identity")
        defect = record["defect"]
        require(type(defect) is dict and set(defect) ==
                {"gram_determinant", "imbalance_square", "lhs", "rhs"}, "defect keys")
        gram = nx * ny - (selected[0] ** 2 + selected[1] ** 2)
        imbalance = (nx - ny) ** 2
        lhs = (nx + ny) ** 2 - 4 * (selected[0] ** 2 + selected[1] ** 2)
        rhs = imbalance + 4 * gram
        require(lhs == rhs and gram >= 0, "defect recomputation")
        require(decode_fraction(defect["lhs"], "lhs") == lhs and
                decode_fraction(defect["rhs"], "rhs") == rhs and
                decode_fraction(defect["gram_determinant"], "gram") == gram and
                decode_fraction(defect["imbalance_square"], "imbalance") == imbalance,
                "defect records")
        require(decode_gaussian(record["selected_coefficient"], "selected") == selected,
                "selected record")
        require(decode_fraction(record["total_energy"], "total") == nx + ny, "total record")
    return len(fixtures)


def check_disk_and_offset(document: dict[str, Any]) -> int:
    witnesses = document["feasible_disk_witnesses"]
    require(type(witnesses) is list and len(witnesses) == len(expected_disks()), "disk count")
    for record, (identifier, expected_x, expected_y) in zip(witnesses, expected_disks()):
        require(type(record) is dict and record["id"] == identifier, "disk id")
        require(record["classification"] == FINITE_CLASS and record["inside_closed_disk"] is True,
                "disk class")
        x_value = decode_vector(record["X"], "disk X")
        y_value = decode_vector(record["Y"], "disk Y")
        require((x_value, y_value) == (expected_x, expected_y), "disk rebinding")
        total = squared_norm(x_value) + squared_norm(y_value)
        selected = product(y_value, x_value)
        magnitude = selected[0] ** 2 + selected[1] ** 2
        radius = (total / 2) ** 2
        require(magnitude <= radius, "disk inequality")
        require(decode_fraction(record["total_energy"], "disk total") == total, "disk total")
        require(decode_gaussian(record["selected_coefficient"], "disk selected") == selected,
                "disk selected")
        require(decode_fraction(record["selected_magnitude_squared"], "disk magnitude") == magnitude,
                "disk magnitude")
        require(decode_fraction(record["radius_squared"], "disk radius") == radius, "disk radius")
    offset = document["common_offset_fixture"]
    require(type(offset) is dict and offset["classification"] == FINITE_CLASS, "offset class")
    additive = decode_fraction(offset["additive_scalar"], "offset")
    require(additive == Fraction(7, 5), "offset value")
    delta = [decode_gaussian(item, "offset delta") for item in offset["delta_spectrum"]]
    require(delta == compute_spectrum([additive] * 4) == [g(additive), g(), g(), g()],
            "offset projection")
    return len(witnesses)


def validate_document(document: object, raw: bytes | None = None) -> dict[str, Any]:
    require(type(document) is dict, "top-level type")
    digest = document.get("payload_sha256")
    require(type(digest) is str and len(digest) == 64, "digest type")
    payload = dict(document)
    del payload["payload_sha256"]
    require(hashlib.sha256(canonical(payload)).hexdigest() == digest, "digest mismatch")
    if raw is not None:
        require(raw == canonical(document) + b"\n", "noncanonical certificate")
    check_metadata(document)
    check_exact_fixtures(document)
    check_disk_and_offset(document)
    return document


def rebind(document: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(document)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = hashlib.sha256(canonical(result)).hexdigest()
    return result


def expect_rejection(name: str, operation: Callable[[], None]) -> str:
    try:
        operation()
    except IndependentFailure:
        return name
    raise IndependentFailure("mutation accepted: " + name)


def mutation_checks(base: dict[str, Any]) -> list[str]:
    def semantic(path: tuple[str, ...], value: object) -> None:
        changed = deepcopy(base)
        cursor: dict[str, Any] = changed
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        validate_document(rebind(changed))

    cases: dict[str, Callable[[], None]] = {
        "bool_int_confusion": lambda: semantic(("task_lock", "paper_number"), True),
        "common_offset_projection": lambda: semantic(
            ("theorem", "phase_blind_additive_scalar"), "DELTA_F_1=A"
        ),
        "duplicate_json_key": lambda: strict_loads('{"x":1,"x":2}'),
        "f2_zero": lambda: semantic(("theorem", "complete_spectrum", "F_2"), "1"),
        "inner_product_orientation": lambda: semantic(
            ("object_lock", "inner_product"), "LINEAR_FIRST_CONJUGATE_LINEAR_SECOND"
        ),
        "nonfinite_json_constant": lambda: strict_loads('{"x":Infinity}'),
        "phase_sign_i_j_vs_minus_i_j": lambda: semantic(
            ("object_lock", "fourier_phase"), "F_k=(1/4)sum_j (-i)^(k*j)E_j"
        ),
        "physical_attachment": lambda: semantic(
            ("scope_firewall", "PHYSICAL_TOP_PRIME_MODE_ANNIHILATION"), "PROVED"
        ),
        "status_promotion": lambda: semantic(("status_ledger", "arithmetic_advance"), "YES"),
    }
    require(sorted(cases) == MUTATIONS, "mutation registry")
    return sorted(expect_rejection(name, cases[name]) for name in cases)


def hostile_schema_checks(base: dict[str, Any]) -> list[str]:
    def semantic(path: tuple[str, ...], value: object) -> None:
        changed = deepcopy(base)
        cursor: dict[str, Any] = changed
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        validate_document(rebind(changed))

    cases: dict[str, Callable[[], None]] = {
        "route_advance_rebinding": lambda: semantic(
            ("status_ledger", "route_advance"), "YES_ARITHMETIC_BREAKTHROUGH"
        ),
        "source_lock_rebinding": lambda: semantic(
            ("source_lock",), {"anchors": "FABRICATED", "proof_audit": "GO"}
        ),
        "strict_1_over_400_promotion": lambda: semantic(
            ("scope_firewall", "STRICT_1_OVER_400"), "PROVED"
        ),
        "twin_prime_result_promotion": lambda: semantic(
            ("scope_firewall", "TWIN_PRIME_RESULT"), "PROVED"
        ),
    }
    require(sorted(cases) == HOSTILE_SCHEMA_MUTATIONS, "hostile schema registry")
    return sorted(expect_rejection(name, cases[name]) for name in cases)


def run() -> None:
    require(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_bytes()
    document = strict_loads(raw.decode("ascii"))
    checked = validate_document(document, raw)
    rejected = mutation_checks(checked)
    require(rejected == MUTATIONS, "mutation suite")
    hostile_rejected = hostile_schema_checks(checked)
    require(hostile_rejected == HOSTILE_SCHEMA_MUTATIONS, "hostile schema suite")
    print("TPC242_INDEPENDENT_CHECK=PASS")
    print("exact_pair_fixtures=" + str(len(expected_pairs())))
    print("disk_witnesses=" + str(len(expected_disks())))
    print("mutation_firewalls=" + str(len(rejected)))
    print("hostile_schema_firewalls=" + str(len(hostile_rejected)))
    print("status=" + STATUS)
    print("physical_top_prime_attachment=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC242_INDEPENDENT_CHECK=FAIL: use --check")
    try:
        run()
    except (IndependentFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC242_INDEPENDENT_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
