#!/usr/bin/env python3
"""Produce and check the exact TPC-243 hard-window certificate."""

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
BASELINE_HEAD = "7b95d43a3dc6526851b1567071f36d48548295bd"
HANDOFF_SHA256 = "a43fb5d8d4d98aba88aa5a817144bfb08759a233fbda414c0cc434f17b1129d7"
PREWRITE_STATUS_SHA256 = "25ceaa072759ccb1a761ef705516c235e32b3a8e3fa997c7be4050af197bfd08"

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

Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, ...]
Matrix = tuple[tuple[Gaussian, ...], ...]


class CertificateFailure(RuntimeError):
    """Fail-closed TPC-243 certificate error."""


def demand(condition: bool, message: str) -> None:
    if type(condition) is not bool:
        raise CertificateFailure("guard is not an exact bool")
    if not condition:
        raise CertificateFailure(message)


def strict_int(value: object, label: str) -> int:
    demand(type(value) is int, label + " must be an exact int")
    return value


def strict_string(value: object, label: str) -> str:
    demand(type(value) is str and bool(value), label + " must be a nonempty string")
    return value


def rational(value: int | Fraction) -> Fraction:
    demand(type(value) in (int, Fraction), "rational input type")
    return Fraction(value)


def g(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return (rational(real), rational(imag))


def g_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def g_sub(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] - right[0], left[1] - right[1])


def g_mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def g_conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def g_scale(value: Gaussian, scalar: Fraction) -> Gaussian:
    demand(type(scalar) is Fraction, "Gaussian scale type")
    return (value[0] * scalar, value[1] * scalar)


def g_abs_sq(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def exact_sqrt_fraction(value: Fraction) -> Fraction:
    demand(type(value) is Fraction and value >= 0, "square-root input")
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    demand(numerator * numerator == value.numerator, "nonsquare numerator")
    demand(denominator * denominator == value.denominator, "nonsquare denominator")
    return Fraction(numerator, denominator)


def fourth_root(exponent: int) -> Gaussian:
    strict_int(exponent, "fourth-root exponent")
    return (g(1), g(0, 1), g(-1), g(0, -1))[exponent % 4]


def inner(first: Vector, second: Vector) -> Gaussian:
    """Conjugate-linear in first and linear in second."""
    demand(len(first) == len(second), "inner-product dimension")
    total = g()
    for left, right in zip(first, second):
        total = g_add(total, g_mul(g_conj(left), right))
    return total


def norm_sq(value: Vector) -> Fraction:
    result = inner(value, value)
    demand(result[1] == 0 and result[0] >= 0, "invalid squared norm")
    return result[0]


def harmonic(number: int) -> Fraction:
    strict_int(number, "harmonic index")
    demand(number >= 0, "negative harmonic index")
    return sum((Fraction(1, j) for j in range(1, number + 1)), Fraction(0))


def gram_matrix(frequencies: tuple[int, ...], start: int, length: int) -> Matrix:
    strict_int(start, "interval start")
    strict_int(length, "interval length")
    demand(length >= 1, "interval length positive")
    rows: list[tuple[Gaussian, ...]] = []
    for alpha in frequencies:
        row: list[Gaussian] = []
        for beta in frequencies:
            total = g()
            for n in range(start, start + length):
                total = g_add(total, fourth_root(n * (beta - alpha)))
            row.append(total)
        rows.append(tuple(row))
    return tuple(rows)


def synthesize(coefficients: Vector, frequencies: tuple[int, ...], start: int,
               length: int) -> Vector:
    demand(len(coefficients) == len(frequencies), "synthesis dimension")
    values: list[Gaussian] = []
    for n in range(start, start + length):
        total = g()
        for coefficient, frequency in zip(coefficients, frequencies):
            total = g_add(total, g_mul(coefficient, fourth_root(n * frequency)))
        values.append(total)
    return tuple(values)


def matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    demand(len(matrix) == len(vector), "matrix-vector dimension")
    output: list[Gaussian] = []
    for row in matrix:
        demand(len(row) == len(vector), "matrix row dimension")
        total = g()
        for entry, value in zip(row, vector):
            total = g_add(total, g_mul(entry, value))
        output.append(total)
    return tuple(output)


def row_absolute_sums(matrix: Matrix) -> list[Fraction]:
    sums: list[Fraction] = []
    for row_index, row in enumerate(matrix):
        total = Fraction(0)
        for column_index, entry in enumerate(row):
            if column_index != row_index:
                total += exact_sqrt_fraction(g_abs_sq(entry))
        sums.append(total)
    return sums


def fraction_record(value: Fraction) -> dict[str, int]:
    demand(type(value) is Fraction, "fraction record type")
    return {"denominator": value.denominator, "numerator": value.numerator}


def gaussian_record(value: Gaussian) -> dict[str, dict[str, int]]:
    return {"im": fraction_record(value[1]), "re": fraction_record(value[0])}


def vector_record(value: Vector) -> list[dict[str, dict[str, int]]]:
    return [gaussian_record(item) for item in value]


def matrix_record(value: Matrix) -> list[list[dict[str, dict[str, int]]]]:
    return [[gaussian_record(item) for item in row] for row in value]


def normalized_lf_sha256(path: Path) -> str:
    raw = path.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def source_anchors() -> dict[str, dict[str, str]]:
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


def verify_source_files() -> None:
    for identifier, anchor in source_anchors().items():
        path = REPOSITORY / anchor["path"]
        demand(path.is_file(), identifier + " source missing")
        demand(normalized_lf_sha256(path) == anchor["sha256"],
               identifier + " source hash mismatch")


def coefficient_fixture() -> tuple[Vector, Vector]:
    z_value = (g(1, 1), g(2, -1), g(-1, 2), g(Fraction(1, 2), Fraction(-1, 2)))
    w_value = (g(2, -1), g(-1, 3), g(1, Fraction(1, 2)), g(-2, -1))
    return z_value, w_value


def exact_fixture() -> dict[str, Any]:
    frequencies = (0, 1, 2, 3)
    start = -3
    length = 17
    delta = Fraction(1, 4)
    packing_index = 2
    harmonic_value = harmonic(packing_index)
    row_bound = harmonic_value / delta
    epsilon = row_bound / length
    demand(harmonic_value == Fraction(3, 2), "harmonic fixture")
    demand(row_bound == 6 and epsilon == Fraction(6, 17), "packing ledger")

    gram = gram_matrix(frequencies, start, length)
    row_sums = row_absolute_sums(gram)
    demand(all(gram[j][j] == g(length) for j in range(4)), "Gram diagonal")
    demand(max(row_sums) <= row_bound, "Gram row bound")

    z_value, w_value = coefficient_fixture()
    tz = synthesize(z_value, frequencies, start, length)
    tw = synthesize(w_value, frequencies, start, length)
    demand(matrix_vector(gram, z_value) == tuple(
        inner(tuple(fourth_root(n * alpha) for n in range(start, start + length)), tz)
        for alpha in frequencies
    ), "Gram synthesis identity")

    norm_z = norm_sq(z_value)
    norm_w = norm_sq(w_value)
    energy_z = norm_sq(tz)
    lower_z = Fraction(length) * norm_z - row_bound * norm_z
    upper_z = Fraction(length) * norm_z + row_bound * norm_z
    demand(max(Fraction(0), lower_z) <= energy_z <= upper_z, "quadratic fixture")

    coefficient_bilinear = inner(z_value, w_value)
    window_bilinear = inner(tz, tw)
    bilinear_error = g_sub(window_bilinear, g_scale(coefficient_bilinear, Fraction(length)))
    demand(g_abs_sq(bilinear_error) <= row_bound * row_bound * norm_z * norm_w,
           "bilinear fixture")

    reverse_coefficient = inner(w_value, z_value)
    reverse_window = inner(tw, tz)
    selected_mode = g_scale(reverse_window, Fraction(1, length))
    selected_error = g_sub(selected_mode, reverse_coefficient)
    demand(reverse_coefficient != coefficient_bilinear, "orientation fixture must be nonreal")
    demand(reverse_window == g_conj(window_bilinear), "window orientation conjugacy")
    demand(g_abs_sq(selected_error) <= epsilon * epsilon * norm_z * norm_w,
           "TPC-242 transport fixture")

    return {
        "bilinear": {
            "coefficient_inner_z_w": gaussian_record(coefficient_bilinear),
            "error": gaussian_record(bilinear_error),
            "error_squared": fraction_record(g_abs_sq(bilinear_error)),
            "squared_bound": fraction_record(row_bound * row_bound * norm_z * norm_w),
            "window_inner_Tz_Tw": gaussian_record(window_bilinear),
        },
        "classification": FINITE_CLASS,
        "coefficients": {"w": vector_record(w_value), "z": vector_record(z_value)},
        "frequencies_quarters": list(frequencies),
        "gram_matrix": matrix_record(gram),
        "interval": {"M": start, "N": length},
        "packing": {
            "H_K": fraction_record(harmonic_value),
            "K": packing_index,
            "R_delta": fraction_record(row_bound),
            "actual_row_sums": [fraction_record(value) for value in row_sums],
            "delta": fraction_record(delta),
            "epsilon": fraction_record(epsilon),
        },
        "quadratic": {
            "energy_Tz": fraction_record(energy_z),
            "lower_bound": fraction_record(max(Fraction(0), lower_z)),
            "norm_z_squared": fraction_record(norm_z),
            "upper_bound": fraction_record(upper_z),
        },
        "tpc242_orientation": {
            "orientation_distinguishes_targets": True,
            "selected_error": gaussian_record(selected_error),
            "selected_error_squared": fraction_record(g_abs_sq(selected_error)),
            "selected_mode_N_inverse_inner_Tw_Tz": gaussian_record(selected_mode),
            "squared_bound": fraction_record(epsilon * epsilon * norm_z * norm_w),
            "target_inner_w_z": gaussian_record(reverse_coefficient),
            "wrong_target_inner_z_w": gaussian_record(coefficient_bilinear),
        },
    }


def build_payload() -> dict[str, Any]:
    verify_source_files()
    return {
        "certificate_version": 1,
        "comparison_lock": {
            "TPC217_upper_scale": "ALREADY_PROVED_NOT_NEW_HERE",
            "TPC238_lower_baseline": "1/2-O(U^4/N^2)_TRIANGULAR_MINORANT",
            "TPC243_direct_baseline": "1-O(U^2_LOG_U/N)_HARD_RECTANGULAR",
            "TPC243_new_interface": "TWO_SIDED_OPERATOR_AND_SIGNED_BILINEAR_TRANSFER",
        },
        "date": "2026-08-25",
        "exact_fixture": exact_fixture(),
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
            "anchors": source_anchors(),
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
            "baseline_head": BASELINE_HEAD,
            "handoff_sha256": HANDOFF_SHA256,
            "paper_number": 243,
            "prewrite_status_sha256": PREWRITE_STATUS_SHA256,
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
            "H_K_log_x_coefficient": fraction_record(Fraction(133, 200)),
            "N_leading_coefficient": fraction_record(Fraction(1, 2)),
            "U_exponent": fraction_record(Fraction(133, 400)),
            "U_squared_exponent": fraction_record(Fraction(133, 200)),
            "epsilon_log_x_coefficient": fraction_record(Fraction(133, 100)),
            "epsilon_power_exponent": fraction_record(Fraction(-67, 200)),
            "epsilon_statement":
                "(133/100+o(1))*x^(-67/200)*log(x)=x^(-67/200+o(1))",
        },
    }


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"),
                      sort_keys=True).encode("ascii")


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
    return json.loads(text, object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def validate_document(document: object, raw_bytes: bytes | None = None) -> dict[str, Any]:
    demand(type(document) is dict, "top-level JSON type")
    digest = document.get("payload_sha256")
    demand(type(digest) is str and len(digest) == 64, "payload digest type")
    payload = dict(document)
    del payload["payload_sha256"]
    expected = build_payload()
    demand(same_typed(payload, expected), "certificate payload mismatch")
    demand(hashlib.sha256(canonical_json(payload)).hexdigest() == digest,
           "payload digest mismatch")
    if raw_bytes is not None:
        demand(raw_bytes == canonical_json(document) + b"\n", "noncanonical JSON bytes")
    return document


def rebound(document: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(document)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def rejected(name: str, operation: Callable[[], None]) -> str:
    try:
        operation()
    except CertificateFailure:
        return name
    raise CertificateFailure("mutation accepted: " + name)


def set_path(document: dict[str, Any], path: tuple[str, ...], value: object) -> None:
    cursor: dict[str, Any] = document
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def semantic_firewalls(base: dict[str, Any]) -> list[str]:
    def semantic(path: tuple[str, ...], value: object) -> None:
        changed = deepcopy(base)
        set_path(changed, path, value)
        validate_document(rebound(changed))

    cases: dict[str, Callable[[], None]] = {
        "bilinear_orientation_reversal": lambda: semantic(
            ("tpc242_transport", "target"), "<z,w>"
        ),
        "bool_int_confusion": lambda: semantic(("task_lock", "paper_number"), True),
        "duplicate_json_key": lambda: strict_json_loads('{"a":1,"a":2}'),
        "finite_classification_promotion": lambda: semantic(
            ("exact_fixture", "classification"), "PROVED"
        ),
        "harmonic_row_bound_tamper": lambda: semantic(
            ("theorem", "row_bound"), "R_delta=delta^(-1)"
        ),
        "nonfinite_json_constant": lambda: strict_json_loads('{"a":NaN}'),
        "source_digest_tamper": lambda: semantic(
            ("source_lock", "anchors", "TPC217", "sha256"), "0" * 64
        ),
        "v59_coefficient_tamper": lambda: semantic(
            ("v59_ledger", "epsilon_log_x_coefficient"), fraction_record(Fraction(67, 50))
        ),
    }
    demand(sorted(cases) == SEMANTIC_MUTATIONS, "semantic mutation registry drift")
    return sorted(rejected(name, cases[name]) for name in cases)


def hostile_rebound_firewalls(base: dict[str, Any]) -> list[str]:
    def semantic(path: tuple[str, ...], value: object) -> None:
        changed = deepcopy(base)
        set_path(changed, path, value)
        validate_document(rebound(changed))

    def extra_scope_key() -> None:
        changed = deepcopy(base)
        changed["scope_firewall"]["UNREAD_PROMOTION"] = "PROVED"
        validate_document(rebound(changed))

    cases: dict[str, Callable[[], None]] = {
        "arithmetic_advance_rebinding": lambda: semantic(
            ("status_ledger", "arithmetic_advance"), "YES"
        ),
        "extra_scope_key_rebinding": extra_scope_key,
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
    demand(sorted(cases) == HOSTILE_REBOUND_MUTATIONS,
           "hostile mutation registry drift")
    return sorted(rejected(name, cases[name]) for name in cases)


def run_firewalls(document: dict[str, Any]) -> None:
    demand(semantic_firewalls(document) == SEMANTIC_MUTATIONS,
           "semantic firewall failure")
    demand(hostile_rebound_firewalls(document) == HOSTILE_REBOUND_MUTATIONS,
           "hostile rebound firewall failure")


def check_certificate() -> dict[str, Any]:
    demand(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_bytes()
    document = strict_json_loads(raw.decode("ascii"))
    checked = validate_document(document, raw)
    run_firewalls(checked)
    return checked


def write_certificate() -> dict[str, Any]:
    document = build_document()
    validate_document(document)
    run_firewalls(document)
    CERTIFICATE.write_bytes(canonical_json(document) + b"\n")
    return document


def summary(mode: str, document: dict[str, Any]) -> None:
    fixture = document["exact_fixture"]
    actual = [
        Fraction(item["numerator"], item["denominator"])
        for item in fixture["packing"]["actual_row_sums"]
    ]
    print("TPC243_HARD_WINDOW_CERTIFICATE=PASS")
    print("mode=" + mode)
    print("status=" + STATUS)
    print("frequencies=" + str(len(fixture["frequencies_quarters"])))
    print("interval_M=" + str(fixture["interval"]["M"]))
    print("interval_N=" + str(fixture["interval"]["N"]))
    print("row_bound_R=6")
    print("actual_max_row_sum=" + str(max(actual)))
    print("semantic_firewalls=" + str(len(SEMANTIC_MUTATIONS)))
    print("hostile_rebound_firewalls=" + str(len(HOSTILE_REBOUND_MUTATIONS)))
    print("arithmetic_advance=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            summary("write", write_certificate())
        else:
            summary("check", check_certificate())
    except (CertificateFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC243_HARD_WINDOW_CERTIFICATE=FAIL: " + str(error))


if __name__ == "__main__":
    main()
