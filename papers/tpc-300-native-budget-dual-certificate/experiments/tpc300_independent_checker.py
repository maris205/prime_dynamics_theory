#!/usr/bin/env python3
"""Independent source-first replay for the TPC-300 dual certificate.

This file deliberately does not import the TPC-300 producer.  It freezes the
TPC-299 inputs, rebuilds the physical image and source Gram over Q, and
recomputes every rational dual fraction and provenance digest.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
mp.mp.dps = 90

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
UPSTREAM_CODE = ROOT / (
    "papers/tpc-299-native-profile-budget-frontier/code/"
    "tpc299_native_profile_budget_frontier_certificate.py")
UPSTREAM_RESULT = ROOT / (
    "papers/tpc-299-native-profile-budget-frontier/results/"
    "tpc299_certificate.json")
RESULT = PROJECT / "results/tpc300_certificate.json"
EXPECTED_UPSTREAM_CODE = (
    "94cb7f191378698de2f08157a475586864c59bba02621e447da98f5ffbbc7279")
EXPECTED_UPSTREAM_RESULT = (
    "9be51f5bcb93e3a297a70e1c12985d52aee2b74e5e3fe4a64fbf7d5a054c559e")
STATUS = (
    "PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY_AND_RECIPROCAL_"
    "MULTIPLIER_CORRECTION_PLUS_NUMERICALLY_CERTIFIED_FINITE_"
    "RATIONAL_DUAL_WITNESS_ATLAS")
SCHEMA = "TPC300_NATIVE_BUDGET_DUAL_CERTIFICATE_V1"

spec = importlib.util.spec_from_file_location(
    "upstream_tpc299_for_tpc300_replay", UPSTREAM_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-299 upstream unavailable")
UPSTREAM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(UPSTREAM)
ENGINE = UPSTREAM.ENGINE


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")).hexdigest()


def vector_digest(values: list[Fraction]) -> str:
    return hashlib.sha256(("".join(
        f"{value.numerator}/{value.denominator}\n" for value in values)).
        encode("ascii")).hexdigest()


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


def exact_solve(matrix: list[list[Fraction]],
                rhs: list[Fraction]) -> list[Fraction]:
    n = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    need(len(matrix) == n and all(len(row) == n for row in matrix),
         "exact square system")
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if augmented[row][column] != 0), None)
        need(pivot is not None, "singular replay system")
        augmented[column], augmented[pivot] = (
            augmented[pivot], augmented[column])
        scale = augmented[column][column]
        augmented[column] = [value / scale
                             for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    augmented[row][entry] -
                    factor * augmented[column][entry]
                    for entry in range(n + 1)]
    return [augmented[row][-1] for row in range(n)]


def replay_matrix(source_row: dict[str, Any]) -> tuple[list[int], list[Fraction],
                                                         list[list[Fraction]],
                                                         list[list[Fraction]]]:
    scale = int(source_row["scale"])
    height = int(source_row["H"])
    q0 = int(source_row["Q"])
    cutoff = int(source_row["comparison_cutoff_z"])
    exponent = int(source_row["kernel_exponent"])
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = UPSTREAM.shell_between(q0)
    columns = [UPSTREAM.PARENT.PARENT.PARENT.physical_output(
        indices, beta, height, prime, exponent) for prime in shell]
    profiles = UPSTREAM.source_profile_matrix(indices)
    profile_count = len(UPSTREAM.PROFILE_CUTOFFS)
    image = [[sum((columns[row][index] * profiles[index][column]
                   for index in range(len(indices))), Fraction(0))
              for column in range(profile_count)]
             for row in range(len(shell))]
    gram = [[sum((profiles[index][left] * profiles[index][right]
                  for index in range(len(indices))), Fraction(0))
             for right in range(profile_count)]
            for left in range(profile_count)]
    return shell, beta, image, gram


def verify_case(image: list[list[Fraction]], gram: list[list[Fraction]],
                beta_norm_squared: Fraction, target: list[Fraction],
                record: dict[str, Any]) -> None:
    k = int(record["k"])
    rho_record = record["ridge_parameter_rho"]
    rho = Fraction(int(rho_record["numerator"]),
                   int(rho_record["denominator"]))
    need(rho > 0 and k > 0, "dual case parameters")
    rows = len(image)
    V = [line[:k] for line in image]
    M = [line[:k] for line in gram[:k]]
    normal = [[sum((V[row][left] * V[row][right]
                    for row in range(rows)), Fraction(0)) +
               rho * M[left][right]
               for right in range(k)] for left in range(k)]
    rhs = [sum((V[row][column] * target[row]
                for row in range(rows)), Fraction(0))
           for column in range(k)]
    coefficients = exact_solve(normal, rhs)
    image_value = [sum((V[row][column] * coefficients[column]
                        for column in range(k)), Fraction(0))
                   for row in range(rows)]
    btv_c = sum((target[row] * image_value[row]
                 for row in range(rows)), Fraction(0))
    target_norm_squared = sum((value * value for value in target),
                              Fraction(0))
    radius_squared = Fraction(rows, 4)
    dual = (target_norm_squared - radius_squared - btv_c) / rho
    need(dual > 0, "nonpositive replay dual")
    need(fraction_digest(dual) == record["exact_dual_fraction_sha256"],
         "dual fraction digest")
    need(vector_digest(coefficients) ==
         record["exact_coefficient_vector_sha256"],
         "coefficient digest")
    ratio = dual / beta_norm_squared
    exact_ratio = mp.mpf(ratio.numerator) / ratio.denominator
    lower_ratio = mp.mpf(record["dual_budget_ratio"][0])
    upper_ratio = mp.mpf(record["dual_budget_ratio"][1])
    need(lower_ratio <= exact_ratio <= upper_ratio,
         "dual ratio enclosure")
    upper = mp.mpf(record["parent_primal_source_norm_squared"][1])
    tightness = (mp.mpf(dual.numerator) / dual.denominator) / upper
    need(tightness > mp.mpf("0.999999999"), "dual tightness")


def main() -> int:
    try:
        need(digest(UPSTREAM_CODE.read_bytes()) == EXPECTED_UPSTREAM_CODE,
             "upstream code provenance")
        need(digest(UPSTREAM_RESULT.read_bytes()) == EXPECTED_UPSTREAM_RESULT,
             "upstream result provenance")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload", {})
        need(payload.get("schema") == SCHEMA and
             document.get("payload_sha256") == hashlib.sha256(
                 canonical(payload)).hexdigest(), "certificate schema/hash")
        audit = payload.get("finite_audit", {})
        need(audit.get("dual_witness_cases") == 72 and
             audit.get("exact_rational_dual_cases") == 72 and
             audit.get("dual_tightness_floor_cases") == 72,
             "audit counts")
        source_rows, _ = UPSTREAM.load_rows()
        cert_rows = payload["rows"]
        cert_map = {row_key(row): row for row in cert_rows}
        need(len(source_rows) == 18 and len(cert_map) == 18,
             "row census")
        cases = 0
        for source_row in source_rows:
            record_row = cert_map[row_key(source_row)]
            shell, beta, image, gram = replay_matrix(source_row)
            beta_norm_squared = sum((value * value for value in beta),
                                    Fraction(0))
            targets = {
                "minimum": [Fraction(int(value))
                            for value in source_row["minimum_signed_label"]],
                "maxcut": [Fraction(int(value))
                           for value in source_row["maxcut_label"]],
                "plus": [Fraction(1) for _ in shell],
            }
            expected = {("threshold", name) for name in targets}
            expected.add(("full_prefix", "minimum"))
            seen: set[tuple[str, str]] = set()
            for record in record_row["dual_cases"]:
                key = (record["context"], record["target"])
                need(key in expected and key not in seen, "case key")
                seen.add(key)
                verify_case(image, gram, beta_norm_squared,
                            targets[key[1]], record)
                cases += 1
            need(seen == expected, "case coverage")
        need(cases == 72, "case total")
    except (Failure, OSError, ValueError, json.JSONDecodeError) as error:
        print("TPC300_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC300_INDEPENDENT_CHECK=PASS rows=18 cases=72 tight_cases=72 "
          "weighted_gt_9e-5=18 weighted_gt_1e-3=14 full_gt_1e-3=11")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
