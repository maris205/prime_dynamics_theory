#!/usr/bin/env python3
"""Independent exact checker for TPC-243; never imports the producer."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any, Callable


PROJECT = Path(__file__).resolve().parents[1]
REPOSITORY = Path(__file__).resolve().parents[3]
CERTIFICATE = PROJECT / "results" / "tpc243_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER"
FINITE_CLASS = "NUMERICAL_FINITE_ILLUSTRATION_ONLY"

SEMANTIC_MUTATIONS = [
    "bilinear_orientation_reversal",
    "bool_int_confusion",
    "duplicate_json_key",
    "finite_classification_promotion",
    "harmonic_row_bound_tamper",
    "nonfinite_json_constant",
    "source_digest_tamper",
    "v59_coefficient_tamper",
]

HOSTILE_REBOUND_MUTATIONS = [
    "arithmetic_advance_rebinding",
    "extra_scope_key_rebinding",
    "selected_mode_rebinding",
    "source_lock_rebinding",
    "strict_1_over_400_promotion",
    "twin_prime_result_promotion",
]

ComplexQ = tuple[Fraction, Fraction]
QVector = tuple[ComplexQ, ...]
QMatrix = tuple[tuple[ComplexQ, ...], ...]


class IndependentFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise IndependentFailure(message)


def c(real: int | Fraction = 0, imag: int | Fraction = 0) -> ComplexQ:
    require(type(real) in (int, Fraction), "real component type")
    require(type(imag) in (int, Fraction), "imaginary component type")
    return (Fraction(real), Fraction(imag))


def plus(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return (left[0] + right[0], left[1] + right[1])


def minus(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return (left[0] - right[0], left[1] - right[1])


def times(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: ComplexQ) -> ComplexQ:
    return (value[0], -value[1])


def scale(value: ComplexQ, factor: Fraction) -> ComplexQ:
    require(type(factor) is Fraction, "scale type")
    return (factor * value[0], factor * value[1])


def modulus_squared(value: ComplexQ) -> Fraction:
    return value[0] ** 2 + value[1] ** 2


def exact_root(value: Fraction) -> Fraction:
    require(type(value) is Fraction and value >= 0, "root input")
    top = isqrt(value.numerator)
    bottom = isqrt(value.denominator)
    require(top * top == value.numerator and bottom * bottom == value.denominator,
            "root not rational square")
    return Fraction(top, bottom)


def root4(exponent: int) -> ComplexQ:
    require(type(exponent) is int, "phase exponent type")
    return (c(1), c(0, 1), c(-1), c(0, -1))[exponent % 4]


def scalar_product(first: QVector, second: QVector) -> ComplexQ:
    require(len(first) == len(second), "scalar-product dimension")
    total = c()
    for left, right in zip(first, second):
        total = plus(total, times(conjugate(left), right))
    return total


def square_norm(value: QVector) -> Fraction:
    result = scalar_product(value, value)
    require(result[1] == 0 and result[0] >= 0, "norm validity")
    return result[0]


def harmonic_sum(index: int) -> Fraction:
    require(type(index) is int and index >= 0, "harmonic index")
    total = Fraction(0)
    for denominator in range(1, index + 1):
        total += Fraction(1, denominator)
    return total


def hard_gram(labels: tuple[int, ...], start: int, count: int) -> QMatrix:
    require(type(start) is int and type(count) is int and count >= 1, "interval")
    output: list[tuple[ComplexQ, ...]] = []
    for left_label in labels:
        row: list[ComplexQ] = []
        for right_label in labels:
            value = c()
            for integer in range(start, start + count):
                value = plus(value, root4(integer * (right_label - left_label)))
            row.append(value)
        output.append(tuple(row))
    return tuple(output)


def evaluate(coefficients: QVector, labels: tuple[int, ...], start: int,
             count: int) -> QVector:
    require(len(coefficients) == len(labels), "evaluation dimension")
    output: list[ComplexQ] = []
    for integer in range(start, start + count):
        value = c()
        for coefficient, label in zip(coefficients, labels):
            value = plus(value, times(coefficient, root4(integer * label)))
        output.append(value)
    return tuple(output)


def row_masses(matrix: QMatrix) -> list[Fraction]:
    output: list[Fraction] = []
    for row_index, row in enumerate(matrix):
        mass = Fraction(0)
        for column_index, entry in enumerate(row):
            if row_index != column_index:
                mass += exact_root(modulus_squared(entry))
        output.append(mass)
    return output


def encode_fraction(value: Fraction) -> dict[str, int]:
    require(type(value) is Fraction, "encode fraction")
    return {"denominator": value.denominator, "numerator": value.numerator}


def encode_complex(value: ComplexQ) -> dict[str, dict[str, int]]:
    return {"im": encode_fraction(value[1]), "re": encode_fraction(value[0])}


def encode_vector(value: QVector) -> list[dict[str, dict[str, int]]]:
    return [encode_complex(item) for item in value]


def encode_matrix(value: QMatrix) -> list[list[dict[str, dict[str, int]]]]:
    return [[encode_complex(item) for item in row] for row in value]


def decode_fraction(record: object, label: str) -> Fraction:
    require(type(record) is dict and set(record) == {"denominator", "numerator"},
            label + " fraction keys")
    numerator = record["numerator"]
    denominator = record["denominator"]
    require(type(numerator) is int and type(denominator) is int and denominator > 0,
            label + " fraction types")
    value = Fraction(numerator, denominator)
    require(value.numerator == numerator and value.denominator == denominator,
            label + " fraction not reduced")
    return value


def decode_complex(record: object, label: str) -> ComplexQ:
    require(type(record) is dict and set(record) == {"im", "re"}, label + " complex keys")
    return (decode_fraction(record["re"], label + ".re"),
            decode_fraction(record["im"], label + ".im"))


def decode_vector(record: object, label: str, dimension: int) -> QVector:
    require(type(record) is list and len(record) == dimension, label + " vector dimension")
    return tuple(decode_complex(item, label) for item in record)


def normalized_hash(path: Path) -> str:
    raw = path.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def locked_sources() -> dict[str, dict[str, str]]:
    return {
        "TPC217": {
            "locator":
                "papers/tpc-217-finite-window-rational-large-sieve/PROOF_PACKAGE.md:21-42,138-168",
            "path": "papers/tpc-217-finite-window-rational-large-sieve/PROOF_PACKAGE.md",
            "sha256": "591928fe33c658345f7b558266dcd021b7dbd5bea2dcd1f7fcd898a0b1d3b927",
        },
        "TPC238": {
            "locator":
                "papers/tpc-238-finite-window-lower-frame-obstruction/PROOF_PACKAGE.md:3-29,141-234",
            "path": "papers/tpc-238-finite-window-lower-frame-obstruction/PROOF_PACKAGE.md",
            "sha256": "9cc39a7209c0f343a71415d345e4bb892d436d7e6d2f961db45ee7163f3acba6",
        },
        "TPC242": {
            "locator":
                "papers/tpc-242-phase-fourier-collision-separation/PROOF_PACKAGE.md:3-60,163-194",
            "path": "papers/tpc-242-phase-fourier-collision-separation/PROOF_PACKAGE.md",
            "sha256": "b195b1247b415499476c90c9e9e5cc7f20eff526b439790075152ceac7ce31ba",
        },
    }


def audit_sources() -> None:
    for identifier, source in locked_sources().items():
        source_path = REPOSITORY / source["path"]
        require(source_path.is_file(), identifier + " missing")
        require(normalized_hash(source_path) == source["sha256"], identifier + " hash")


def fixture_coefficients() -> tuple[QVector, QVector]:
    first = (c(1, 1), c(2, -1), c(-1, 2), c(Fraction(1, 2), Fraction(-1, 2)))
    second = (c(2, -1), c(-1, 3), c(1, Fraction(1, 2)), c(-2, -1))
    return first, second


def expected_fixture() -> dict[str, Any]:
    labels = (0, 1, 2, 3)
    start = -3
    count = 17
    delta = Fraction(1, 4)
    packing_index = 2
    harmonic_value = harmonic_sum(packing_index)
    radius = harmonic_value / delta
    epsilon = radius / count
    require((harmonic_value, radius, epsilon) ==
            (Fraction(3, 2), Fraction(6), Fraction(6, 17)), "packing constants")

    gram = hard_gram(labels, start, count)
    masses = row_masses(gram)
    require(all(gram[index][index] == c(count) for index in range(4)), "diagonal")
    require(max(masses) <= radius, "row masses")

    z_value, w_value = fixture_coefficients()
    tz = evaluate(z_value, labels, start, count)
    tw = evaluate(w_value, labels, start, count)
    nz = square_norm(z_value)
    nw = square_norm(w_value)
    energy = square_norm(tz)
    lower = max(Fraction(0), Fraction(count) * nz - radius * nz)
    upper = Fraction(count) * nz + radius * nz
    require(lower <= energy <= upper, "quadratic inequality")

    coefficient = scalar_product(z_value, w_value)
    window = scalar_product(tz, tw)
    error = minus(window, scale(coefficient, Fraction(count)))
    bilinear_bound = radius * radius * nz * nw
    require(modulus_squared(error) <= bilinear_bound, "bilinear inequality")

    reverse_coefficient = scalar_product(w_value, z_value)
    reverse_window = scalar_product(tw, tz)
    selected = scale(reverse_window, Fraction(1, count))
    selected_error = minus(selected, reverse_coefficient)
    selected_bound = epsilon * epsilon * nz * nw
    require(reverse_coefficient != coefficient, "orientation sensitivity")
    require(reverse_window == conjugate(window), "reverse window")
    require(modulus_squared(selected_error) <= selected_bound, "selected transfer")

    return {
        "bilinear": {
            "coefficient_inner_z_w": encode_complex(coefficient),
            "error": encode_complex(error),
            "error_squared": encode_fraction(modulus_squared(error)),
            "squared_bound": encode_fraction(bilinear_bound),
            "window_inner_Tz_Tw": encode_complex(window),
        },
        "classification": FINITE_CLASS,
        "coefficients": {"w": encode_vector(w_value), "z": encode_vector(z_value)},
        "frequencies_quarters": list(labels),
        "gram_matrix": encode_matrix(gram),
        "interval": {"M": start, "N": count},
        "packing": {
            "H_K": encode_fraction(harmonic_value),
            "K": packing_index,
            "R_delta": encode_fraction(radius),
            "actual_row_sums": [encode_fraction(value) for value in masses],
            "delta": encode_fraction(delta),
            "epsilon": encode_fraction(epsilon),
        },
        "quadratic": {
            "energy_Tz": encode_fraction(energy),
            "lower_bound": encode_fraction(lower),
            "norm_z_squared": encode_fraction(nz),
            "upper_bound": encode_fraction(upper),
        },
        "tpc242_orientation": {
            "orientation_distinguishes_targets": True,
            "selected_error": encode_complex(selected_error),
            "selected_error_squared": encode_fraction(modulus_squared(selected_error)),
            "selected_mode_N_inverse_inner_Tw_Tz": encode_complex(selected),
            "squared_bound": encode_fraction(selected_bound),
            "target_inner_w_z": encode_complex(reverse_coefficient),
            "wrong_target_inner_z_w": encode_complex(coefficient),
        },
    }


def expected_payload() -> dict[str, Any]:
    audit_sources()
    return {
        "certificate_version": 1,
        "comparison_lock": {
            "TPC217_upper_scale": "ALREADY_PROVED_NOT_NEW_HERE",
            "TPC238_lower_baseline": "1/2-O(U^4/N^2)_TRIANGULAR_MINORANT",
            "TPC243_direct_baseline": "1-O(U^2_LOG_U/N)_HARD_RECTANGULAR",
            "TPC243_new_interface": "TWO_SIDED_OPERATOR_AND_SIGNED_BILINEAR_TRANSFER",
        },
        "date": "2026-08-25",
        "exact_fixture": expected_fixture(),
        "mutation_firewalls": {
            "hostile_rebound": HOSTILE_REBOUND_MUTATIONS,
            "hostile_rebound_count": len(HOSTILE_REBOUND_MUTATIONS),
            "semantic": SEMANTIC_MUTATIONS,
            "semantic_count": len(SEMANTIC_MUTATIONS),
        },
        "object_lock": {
            "frequency_space": "FINITE_DELTA_SEPARATED_SUBSET_OF_R_MOD_Z",
            "gram_entry": "G_alpha_beta=sum_n_in_I e(n*(beta-alpha))",
            "inner_product": "CONJUGATE_LINEAR_FIRST_LINEAR_SECOND",
            "interval": "ANY_N_CONSECUTIVE_INTEGERS",
            "synthesis": "Tz(n)=sum_alpha z_alpha*e(n*alpha)",
        },
        "primitive_corollary": {
            "K_U": "floor(U^2/2)",
            "R_U": "U^2*H_floor(U^2/2)",
            "delta": "U^(-2)",
            "height_range": "U>=2",
        },
        "scope_firewall": {
            "ARITHMETIC_L2": "NONE",
            "COEFFICIENT_NORM_BOUND": "NONE",
            "FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE": False,
            "FIXED_ATOM_CREDIT": 0,
            "FULL_GATE_B": "OPEN",
            "LITERAL_TOP_PRIME_ATTACHMENT": "OPEN",
            "SIGNED_C_H_THEOREM": "NONE",
            "STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TWIN_PRIME_RESULT": "NONE",
        },
        "source_lock": {
            "anchors": locked_sources(),
            "normalized_line_endings": "CRLF_AND_CR_TO_LF_BEFORE_SHA256",
            "verification": "DIRECT_FILE_HASH_MATCH",
        },
        "status_ledger": {
            "arithmetic_advance": "NO",
            "claim_ceiling": STATUS,
            "route_a": "N/A",
            "route_b": "STRUCTURAL_L1_ONLY",
            "status": STATUS,
        },
        "task_lock": {
            "baseline_head": "7b95d43a3dc6526851b1567071f36d48548295bd",
            "handoff_sha256":
                "a43fb5d8d4d98aba88aa5a817144bfb08759a233fbda414c0cc434f17b1129d7",
            "paper_number": 243,
            "prewrite_status_sha256":
                "25ceaa072759ccb1a761ef705516c235e32b3a8e3fa997c7be4050af197bfd08",
            "task_id": "TPC243-WRITE-20260825-A",
        },
        "theorem": {
            "bilinear":
                "|N^(-1)<Tz,Tw>-<z,w>|<=epsilon*||z||_2*||w||_2",
            "epsilon": "R_delta/N",
            "frame_lower": "[1-epsilon]_+*||z||_2^2<=N^(-1)||Tz||_2^2",
            "frame_upper": "N^(-1)||Tz||_2^2<=(1+epsilon)*||z||_2^2",
            "harmonic_index": "K=floor(1/(2*delta))",
            "row_bound": "R_delta=delta^(-1)*H_K",
            "row_statement": "DIAGONAL_N_AND_ABSOLUTE_OFF_DIAGONAL_ROW_SUM_LE_R_DELTA",
        },
        "tpc242_transport": {
            "X": "N^(-1/2)*Tz",
            "Y": "N^(-1/2)*Tw",
            "error": "|F_1-<w,z>|<=epsilon*||w||_2*||z||_2",
            "selected_mode": "F_1=<Y,X>=N^(-1)<Tw,Tz>",
            "status": "SIGNED_BILINEAR_INTERFACE_NOT_PHYSICAL_ATTACHMENT",
            "target": "<w,z>",
        },
        "v59_ledger": {
            "H_K_log_x_coefficient": encode_fraction(Fraction(133, 200)),
            "N_leading_coefficient": encode_fraction(Fraction(1, 2)),
            "U_exponent": encode_fraction(Fraction(133, 400)),
            "U_squared_exponent": encode_fraction(Fraction(133, 200)),
            "epsilon_log_x_coefficient": encode_fraction(Fraction(133, 100)),
            "epsilon_power_exponent": encode_fraction(Fraction(-67, 200)),
            "epsilon_statement":
                "(133/100+o(1))*x^(-67/200)*log(x)=x^(-67/200+o(1))",
        },
    }


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"),
                      sort_keys=True).encode("ascii")


def typed_equal(candidate: object, expected: object) -> bool:
    if type(candidate) is not type(expected):
        return False
    if type(expected) is dict:
        return candidate.keys() == expected.keys() and all(
            typed_equal(candidate[key], expected[key]) for key in expected
        )
    if type(expected) is list:
        return len(candidate) == len(expected) and all(
            typed_equal(left, right) for left, right in zip(candidate, expected)
        )
    return candidate == expected


def unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise IndependentFailure("duplicate JSON key: " + key)
        output[key] = value
    return output


def reject_nonfinite(value: str) -> None:
    raise IndependentFailure("nonfinite JSON constant: " + value)


def strict_loads(text: str) -> object:
    return json.loads(text, object_pairs_hook=unique_pairs,
                      parse_constant=reject_nonfinite)


def audit_observed_fixture(document: dict[str, Any]) -> None:
    fixture = document["exact_fixture"]
    require(type(fixture) is dict, "fixture type")
    z_value = decode_vector(fixture["coefficients"]["z"], "z", 4)
    w_value = decode_vector(fixture["coefficients"]["w"], "w", 4)
    require((z_value, w_value) == fixture_coefficients(), "coefficient rebinding")
    require(decode_fraction(fixture["packing"]["delta"], "delta") == Fraction(1, 4),
            "delta record")
    require(decode_fraction(fixture["packing"]["H_K"], "H_K") == Fraction(3, 2),
            "harmonic record")
    require(decode_fraction(fixture["packing"]["R_delta"], "R_delta") == 6,
            "row-bound record")
    require(decode_fraction(fixture["packing"]["epsilon"], "epsilon") == Fraction(6, 17),
            "epsilon record")
    selected = decode_complex(
        fixture["tpc242_orientation"]["selected_mode_N_inverse_inner_Tw_Tz"], "selected"
    )
    target = decode_complex(fixture["tpc242_orientation"]["target_inner_w_z"], "target")
    wrong = decode_complex(
        fixture["tpc242_orientation"]["wrong_target_inner_z_w"], "wrong target"
    )
    require(target != wrong and fixture["tpc242_orientation"]
            ["orientation_distinguishes_targets"] is True, "orientation lock")
    error = minus(selected, target)
    require(encode_complex(error) == fixture["tpc242_orientation"]["selected_error"],
            "selected error record")


def validate(document: object, raw: bytes | None = None) -> dict[str, Any]:
    require(type(document) is dict, "top-level type")
    digest = document.get("payload_sha256")
    require(type(digest) is str and len(digest) == 64 and
            all(character in "0123456789abcdef" for character in digest), "digest format")
    payload = dict(document)
    del payload["payload_sha256"]
    expected = expected_payload()
    require(typed_equal(payload, expected), "complete nested schema mismatch")
    require(hashlib.sha256(canonical(payload)).hexdigest() == digest, "payload digest")
    if raw is not None:
        require(raw == canonical(document) + b"\n", "canonical bytes")
    audit_observed_fixture(document)
    return document


def renew_digest(document: dict[str, Any]) -> dict[str, Any]:
    changed = deepcopy(document)
    changed.pop("payload_sha256", None)
    changed["payload_sha256"] = hashlib.sha256(canonical(changed)).hexdigest()
    return changed


def alter(document: dict[str, Any], path: tuple[str, ...], value: object) -> None:
    cursor: dict[str, Any] = document
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def must_reject(name: str, operation: Callable[[], None]) -> str:
    try:
        operation()
    except IndependentFailure:
        return name
    raise IndependentFailure("mutation accepted: " + name)


def check_semantic_mutations(base: dict[str, Any]) -> list[str]:
    def semantic(path: tuple[str, ...], value: object) -> None:
        changed = deepcopy(base)
        alter(changed, path, value)
        validate(renew_digest(changed))

    cases: dict[str, Callable[[], None]] = {
        "bilinear_orientation_reversal": lambda: semantic(
            ("tpc242_transport", "target"), "<z,w>"
        ),
        "bool_int_confusion": lambda: semantic(("task_lock", "paper_number"), True),
        "duplicate_json_key": lambda: strict_loads('{"v":1,"v":2}'),
        "finite_classification_promotion": lambda: semantic(
            ("exact_fixture", "classification"), "PROVED"
        ),
        "harmonic_row_bound_tamper": lambda: semantic(
            ("theorem", "row_bound"), "R_delta=delta^(-1)"
        ),
        "nonfinite_json_constant": lambda: strict_loads('{"v":Infinity}'),
        "source_digest_tamper": lambda: semantic(
            ("source_lock", "anchors", "TPC217", "sha256"), "f" * 64
        ),
        "v59_coefficient_tamper": lambda: semantic(
            ("v59_ledger", "epsilon_log_x_coefficient"), encode_fraction(Fraction(67, 50))
        ),
    }
    require(sorted(cases) == SEMANTIC_MUTATIONS, "semantic registry")
    return sorted(must_reject(name, cases[name]) for name in cases)


def check_hostile_rebound(base: dict[str, Any]) -> list[str]:
    def semantic(path: tuple[str, ...], value: object) -> None:
        changed = deepcopy(base)
        alter(changed, path, value)
        validate(renew_digest(changed))

    def inject_extra_key() -> None:
        changed = deepcopy(base)
        changed["scope_firewall"]["UNREAD_PROMOTION"] = "PROVED"
        validate(renew_digest(changed))

    cases: dict[str, Callable[[], None]] = {
        "arithmetic_advance_rebinding": lambda: semantic(
            ("status_ledger", "arithmetic_advance"), "YES"
        ),
        "extra_scope_key_rebinding": inject_extra_key,
        "selected_mode_rebinding": lambda: semantic(
            ("tpc242_transport", "selected_mode"), "F_1=N^(-1)<Tz,Tw>"
        ),
        "source_lock_rebinding": lambda: semantic(
            ("source_lock",), {"anchors": "FABRICATED", "verification": "PASS"}
        ),
        "strict_1_over_400_promotion": lambda: semantic(
            ("scope_firewall", "STRICT_1_OVER_400"), "PROVED"
        ),
        "twin_prime_result_promotion": lambda: semantic(
            ("scope_firewall", "TWIN_PRIME_RESULT"), "PROVED"
        ),
    }
    require(sorted(cases) == HOSTILE_REBOUND_MUTATIONS, "hostile registry")
    return sorted(must_reject(name, cases[name]) for name in cases)


def run() -> None:
    require(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_bytes()
    document = strict_loads(raw.decode("ascii"))
    checked = validate(document, raw)
    semantic = check_semantic_mutations(checked)
    hostile = check_hostile_rebound(checked)
    require(semantic == SEMANTIC_MUTATIONS, "semantic suite")
    require(hostile == HOSTILE_REBOUND_MUTATIONS, "hostile suite")
    print("TPC243_INDEPENDENT_CHECK=PASS")
    print("source_locks=3")
    print("frequencies=4")
    print("interval_N=17")
    print("row_bound_R=6")
    print("semantic_firewalls=" + str(len(semantic)))
    print("hostile_rebound_firewalls=" + str(len(hostile)))
    print("status=" + STATUS)
    print("literal_top_prime_attachment=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC243_INDEPENDENT_CHECK=FAIL: use --check")
    try:
        run()
    except (IndependentFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC243_INDEPENDENT_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
