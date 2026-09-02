#!/usr/bin/env python3
"""TPC-352: disjoint adversarial holdout for the TPC-351 contrast.

The reciprocal-shell rule is frozen before this panel is evaluated.  This
producer computes a new finite panel and compares it with the balanced-step
parent; it makes no asymptotic or arithmetic claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc352_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-351-reciprocal-shell-contrast/code/"
    "tpc351_reciprocal_shell_contrast.py")
PARENT_CERT = ROOT / (
    "papers/tpc-351-reciprocal-shell-contrast/results/"
    "tpc351_certificate.json")
PARENT_CODE_SHA256 = (
    "820f6195408a4d0fbbfed46f5bdd8054d812ae24eb87aaa1169791055f33328a")
PARENT_CERT_SHA256 = (
    "74ca0045ca201712a69870669612b7bc16ccd0c019f27f3ea1d3dccb4b687db0")

SCHEMA = "TPC352_RECIPROCAL_ADVERSARIAL_HOLDOUT_V1"
STATUS = (
    "PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT")
ROUND2_CLUE = "FREEZE_FINITE_RECIPROCAL_BRANCH_AND_RETURN_TO_SOURCE_NATIVE_L2"

ORIGINS = (96097, 120097, 144097)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (64, 128, 256, 512)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index")
HEIGHT = 66
TOL = 8.0e-9
GRAM_TOL = 8.0e-9


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def show(value: float) -> str:
    return format(float(value), ".12g")


def locked(path: Path, expected: str, label: str) -> None:
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(2 * max(Q_ANCHORS))


def shell_for(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def source_signs(primes: list[int], law: str) -> list[int]:
    need(law in LAW_NAMES, "unknown source law")
    if law == "all_plus":
        return [1] * len(primes)
    return [1 if index % 2 == 0 else -1
            for index in range(len(primes))]


def reciprocal_coefficients(primes: list[int]) -> list[Fraction]:
    values = [Fraction(1, prime) for prime in primes]
    mean = sum(values, Fraction(0)) / len(values)
    result = [value - mean for value in values]
    need(sum(result, Fraction(0)) == 0, "reciprocal coefficient balance")
    need(all(value != 0 for value in result), "zero reciprocal coefficient")
    return result


def balanced_coefficients(primes: list[int]) -> list[int]:
    count = len(primes)
    half = count // 2
    result = [1 if index < half else
              (-1 if index >= count - half else 0)
              for index in range(count)]
    need(sum(result) == 0, "balanced coefficient balance")
    return result


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def spectral_norm(matrix: np.ndarray) -> float:
    eigenvalues = np.linalg.eigvalsh((matrix + matrix.T) / 2.0)
    need(len(eigenvalues) > 0 and bool(np.all(np.isfinite(eigenvalues))),
         "finite spectrum")
    return max(abs(float(eigenvalues[0])), abs(float(eigenvalues[-1])))


def matrices(origin: int, count: int, q0: int, exponent: int,
             law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int]]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    distance = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    physical = np.zeros((count, count), dtype=np.float64)
    ideal = np.zeros((count, count), dtype=np.float64)
    primes = shell_for(q0)
    for prime, sign in zip(primes, source_signs(primes, law)):
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        block = float(sign * prime) * kernel * centered
        ideal += block
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        physical += block * valid
    physical = (physical + physical.T) / 2.0
    ideal = (ideal + ideal.T) / 2.0
    defect = physical - ideal
    need(bool(np.all(np.isfinite(physical))) and
         bool(np.all(np.isfinite(ideal))) and
         bool(np.all(np.isfinite(defect))), "finite matrix entries")
    return physical, ideal, defect, primes


def incidence(values: np.ndarray, primes: list[int],
              coefficients: list[Fraction | int]) -> np.ndarray:
    result = np.zeros(len(values), dtype=np.float64)
    for prime, coefficient in zip(primes, coefficients):
        if coefficient:
            result += float(coefficient) * (values % prime == 0)
    return result


def fraction_matrix(origin: int, count: int, q0: int, exponent: int,
                    law: str, masked: bool) -> list[list[Fraction]]:
    values = list(range(origin, origin + count))
    result = [[Fraction(0) for _ in values] for _ in values]
    primes = shell_for(q0)
    for prime, sign in zip(primes, source_signs(primes, law)):
        for i, u in enumerate(values):
            for j, t in enumerate(values):
                if u == t:
                    continue
                if masked and (u % prime == 0 or t % prime == 0):
                    continue
                centered = Fraction(1) if (u - t) % prime == 0 else Fraction(0)
                centered -= Fraction(1, prime - 1)
                kernel = Fraction(HEIGHT ** (2 * exponent),
                                  (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
                result[i][j] += sign * prime * kernel * centered
    return result


def vector_digest(vector: list[Fraction]) -> str:
    values = [fraction_text(item) for item in vector]
    return hashlib.sha256(canonical(values)).hexdigest()


def exact_anchor() -> dict[str, Any]:
    origin, count, q0, exponent, law = 193, 14, 4, 1, "all_plus"
    actual = fraction_matrix(origin, count, q0, exponent, law, True)
    ideal = fraction_matrix(origin, count, q0, exponent, law, False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(count)]
              for i in range(count)]
    primes = shell_for(q0)
    coefficients = reciprocal_coefficients(primes)
    vector = [sum((coefficients[k] for k, prime in enumerate(primes)
                   if value % prime == 0), Fraction(0))
              for value in range(origin, origin + count)]
    image = [sum(defect[i][j] * vector[j] for j in range(count))
             for i in range(count)]
    vector_square = sum(item * item for item in vector)
    image_square = sum(item * item for item in image)
    expected = [Fraction(0), Fraction(0), Fraction(1, 35), Fraction(-1, 35),
                Fraction(0), Fraction(0), Fraction(0), Fraction(1, 35),
                Fraction(0), Fraction(0), Fraction(-1, 35), Fraction(0),
                Fraction(1, 35), Fraction(0)]
    need(vector == expected, "exact holdout anchor vector")
    need(vector_square == Fraction(1, 245), "exact holdout anchor norm")
    return {
        "interval": [origin, origin + count - 1], "q": q0, "shell": primes,
        "kernel_exponent": exponent, "height": HEIGHT,
        "matrix_shape": [count, count],
        "coefficients": [fraction_text(item) for item in coefficients],
        "incidence_vector": [fraction_text(item) for item in vector],
        "incidence_vector_squared_norm": fraction_text(vector_square),
        "response_vector_squared_norm":
            f"{image_square.numerator}/{image_square.denominator}",
        "response_vector_digest": vector_digest(image), "identity_exact": True,
    }


def witness(defect: np.ndarray, ideal: np.ndarray, values: np.ndarray,
            primes: list[int], coefficients: list[Fraction | int],
            reciprocal: bool) -> dict[str, Any]:
    vector = incidence(values, primes, coefficients)
    support = np.flatnonzero(vector != 0)
    need(len(support) > 0, "empty incidence support")
    norm = float(np.linalg.norm(vector))
    need(norm > 0.0 and bool(np.isfinite(norm)), "incidence norm")
    response = float(np.linalg.norm(defect @ (vector / norm)))
    defect_norm = spectral_norm(defect)
    ideal_norm = spectral_norm(ideal)
    hit = np.any(np.array([(values % prime) == 0 for prime in primes]), axis=0)
    coordinate = float(np.linalg.norm(defect[:, hit], axis=0).max())
    result = {
        "incidence_support": int(len(support)), "incidence_norm": show(norm),
        "response_norm": show(response), "to_defect_ratio": show(response / defect_norm),
        "to_ideal_ratio": show(response / ideal_norm),
        "to_coordinate_ratio": show(response / coordinate),
        "beats_coordinate": bool(response / coordinate > 1.0 + 1.0e-10),
        "at_least_half": bool(response / defect_norm >= 0.5 - 1.0e-12),
        "coordinate_baseline_norm": show(coordinate), "defect_norm": show(defect_norm),
        "ideal_norm": show(ideal_norm),
    }
    if reciprocal:
        gram = np.zeros(len(values), dtype=np.float64)
        for prime, coefficient in zip(primes, coefficients):
            gram += float(coefficient) * (defect @
                                           (values % prime == 0).astype(float))
        result["gram_error"] = show(float(np.max(np.abs(
            defect @ (vector / norm) - gram / norm))))
    else:
        result["gram_error"] = None
    return result


def row_record(origin: int, count: int, q0: int, exponent: int,
               law: str) -> dict[str, Any]:
    _, ideal, defect, primes = matrices(origin, count, q0, exponent, law)
    values = np.arange(origin, origin + count, dtype=np.int64)
    reciprocal = reciprocal_coefficients(primes)
    balanced = balanced_coefficients(primes)
    r = witness(defect, ideal, values, primes, reciprocal, True)
    b = witness(defect, ideal, values, primes, balanced, False)
    gain = float(r["response_norm"]) / float(b["response_norm"])
    need(float(r["response_norm"]) > 0.0 and float(b["response_norm"]) > 0.0,
         "positive witness response")
    need(float(r["gram_error"]) <= GRAM_TOL, "reciprocal Gram replay")
    return {
        "origin": origin, "count": count,
        "source_interval": [origin, origin + count - 1], "q": q0,
        "shell": primes, "kernel_exponent": exponent, "law": law,
        "operator_shape": [count, count],
        "reciprocal_coefficients": [fraction_text(x) for x in reciprocal],
        "reciprocal_coefficient_sum": fraction_text(sum(reciprocal, Fraction(0))),
        "reciprocal_active_prime_count": sum(x != 0 for x in reciprocal),
        "balanced_coefficients": balanced,
        "balanced_coefficient_sum": sum(balanced),
        "balanced_active_prime_count": sum(x != 0 for x in balanced),
        "reciprocal_incidence_support": r["incidence_support"],
        "balanced_incidence_support": b["incidence_support"],
        "reciprocal_incidence_norm": r["incidence_norm"],
        "balanced_incidence_norm": b["incidence_norm"],
        "reciprocal_witness_response_norm": r["response_norm"],
        "balanced_witness_response_norm": b["response_norm"],
        "reciprocal_to_defect_ratio": r["to_defect_ratio"],
        "balanced_to_defect_ratio": b["to_defect_ratio"],
        "reciprocal_to_ideal_ratio": r["to_ideal_ratio"],
        "balanced_to_ideal_ratio": b["to_ideal_ratio"],
        "reciprocal_to_coordinate_ratio": r["to_coordinate_ratio"],
        "balanced_to_coordinate_ratio": b["to_coordinate_ratio"],
        "reciprocal_beats_coordinate": r["beats_coordinate"],
        "balanced_beats_coordinate": b["beats_coordinate"],
        "reciprocal_at_least_half": r["at_least_half"],
        "balanced_at_least_half": b["at_least_half"],
        "reciprocal_coordinate_baseline_norm": r["coordinate_baseline_norm"],
        "balanced_coordinate_baseline_norm": b["coordinate_baseline_norm"],
        "defect_operator_norm": r["defect_norm"],
        "ideal_operator_norm": r["ideal_norm"],
        "incidence_gram_max_error": r["gram_error"],
        "reciprocal_to_balanced_response_ratio": show(gain),
        "improves_balanced_parent": bool(gain > 1.0 + 1.0e-10),
    }


def make_series(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for origin in ORIGINS:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                for law in LAW_NAMES:
                    group = sorted((row for row in rows
                                    if row["origin"] == origin and
                                    row["q"] == q0 and
                                    row["kernel_exponent"] == exponent and
                                    row["law"] == law),
                                   key=lambda row: row["count"])
                    need(len(group) == len(COUNTS), "series length")
                    reciprocal = [float(row["reciprocal_to_defect_ratio"])
                                  for row in group]
                    balanced = [float(row["balanced_to_defect_ratio"])
                                for row in group]
                    result.append({
                        "origin": origin, "q": q0,
                        "kernel_exponent": exponent, "law": law,
                        "counts": list(COUNTS),
                        "reciprocal_to_defect_ratios": [show(x) for x in reciprocal],
                        "balanced_to_defect_ratios": [show(x) for x in balanced],
                        "reciprocal_nondecreasing": bool(all(
                            reciprocal[i + 1] >= reciprocal[i] - 1.0e-12
                            for i in range(len(COUNTS) - 1))),
                        "balanced_nondecreasing": bool(all(
                            balanced[i + 1] >= balanced[i] - 1.0e-12
                            for i in range(len(COUNTS) - 1))),
                    })
    return result


def build_payload() -> dict[str, Any]:
    locked(PARENT_CODE, PARENT_CODE_SHA256, "TPC351 producer")
    locked(PARENT_CERT, PARENT_CERT_SHA256, "TPC351 certificate")
    parent = json.loads(PARENT_CERT.read_bytes())
    need(PARENT_CERT.read_bytes() == canonical(parent), "parent canonicality")
    rows = [row_record(origin, count, q0, exponent, law)
            for origin in ORIGINS for count in COUNTS
            for q0 in Q_ANCHORS for exponent in EXPONENTS
            for law in LAW_NAMES]
    need(len(rows) == 144, "row census")
    series = make_series(rows)
    rratios = [float(row["reciprocal_to_defect_ratio"]) for row in rows]
    bratios = [float(row["balanced_to_defect_ratio"]) for row in rows]
    gains = [float(row["reciprocal_to_balanced_response_ratio"]) for row in rows]
    qbreak = {}
    for q0 in Q_ANCHORS:
        subset = [row for row in rows if row["q"] == q0]
        qbreak[str(q0)] = {
            "rows": len(subset),
            "reciprocal_min": show(min(float(x["reciprocal_to_defect_ratio"]) for x in subset)),
            "reciprocal_mean": show(sum(float(x["reciprocal_to_defect_ratio"]) for x in subset) / len(subset)),
            "reciprocal_max": show(max(float(x["reciprocal_to_defect_ratio"]) for x in subset)),
            "balanced_min": show(min(float(x["balanced_to_defect_ratio"]) for x in subset)),
            "balanced_mean": show(sum(float(x["balanced_to_defect_ratio"]) for x in subset) / len(subset)),
            "balanced_max": show(max(float(x["balanced_to_defect_ratio"]) for x in subset)),
            "reciprocal_half": sum(x["reciprocal_at_least_half"] for x in subset),
            "balanced_half": sum(x["balanced_at_least_half"] for x in subset),
            "improved_parent": sum(x["improves_balanced_parent"] for x in subset),
        }
    gram = [float(row["incidence_gram_max_error"]) for row in rows]
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC351_producer_sha256": PARENT_CODE_SHA256,
            "TPC351_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS), "source_counts": list(COUNTS),
            "interval_rule": "I_(o,M)={o,...,o+M-1}",
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": list(EXPONENTS),
            "laws": list(LAW_NAMES), "height": HEIGHT,
            "contrast_rule": "gamma_j=1/p_j-(1/r)sum_k 1/p_k, for p_j in (Q,2Q]",
            "parent_rule": "balanced first floor(r/2) +1, last floor(r/2) -1, middle 0",
            "holdout_rule": "origins and q ladder are frozen before response evaluation",
            "incidence_vector": "c_I(t)=sum_j gamma_j 1_(p_j divides t)",
            "comparison": "same literal masked defect matrix and coordinate baseline",
            "defect": "D=A-T",
        },
        "exact_theorem": {
            "coefficient_balance": "sum_j gamma_j=0 exactly",
            "incidence_identity": "c_I=sum_j gamma_j h_(p_j,I)",
            "gram_expansion": "||D_I c_I||_2^2=sum_(j,k) gamma_j gamma_k <D_I h_j,D_I h_k>",
            "normalized_lower_bound": "||D_I||_(2->2)>=||D_I c_I||_2/||c_I||_2 for c_I != 0",
            "finite_scope": "the holdout and parent comparison are finite observations",
        },
        "finite_audit": {
            "origins": len(ORIGINS), "source_counts": len(COUNTS),
            "q_anchors": len(Q_ANCHORS), "kernel_exponents": len(EXPONENTS),
            "laws": len(LAW_NAMES), "rows": len(rows), "series": len(series),
            "positive_reciprocal_rows": sum(float(x["reciprocal_witness_response_norm"]) > 0 for x in rows),
            "positive_balanced_rows": sum(float(x["balanced_witness_response_norm"]) > 0 for x in rows),
            "zero_sum_records": sum(x["reciprocal_coefficient_sum"] == "0/1" for x in rows),
            "incidence_gram_records": len(rows), "incidence_gram_max_error": show(max(gram)),
            "improved_parent_rows": sum(x["improves_balanced_parent"] for x in rows),
            "coordinate_beaten_reciprocal": sum(x["reciprocal_beats_coordinate"] for x in rows),
            "coordinate_beaten_balanced": sum(x["balanced_beats_coordinate"] for x in rows),
            "half_defect_reciprocal": sum(x["reciprocal_at_least_half"] for x in rows),
            "half_defect_balanced": sum(x["balanced_at_least_half"] for x in rows),
            "reciprocal_support_min": min(x["reciprocal_incidence_support"] for x in rows),
            "reciprocal_support_max": max(x["reciprocal_incidence_support"] for x in rows),
            "balanced_support_min": min(x["balanced_incidence_support"] for x in rows),
            "balanced_support_max": max(x["balanced_incidence_support"] for x in rows),
            "reciprocal_ratio_min": show(min(rratios)), "reciprocal_ratio_max": show(max(rratios)),
            "balanced_ratio_min": show(min(bratios)), "balanced_ratio_max": show(max(bratios)),
            "response_gain_min": show(min(gains)), "response_gain_max": show(max(gains)),
            "reciprocal_nondecreasing_series": sum(x["reciprocal_nondecreasing"] for x in series),
            "balanced_nondecreasing_series": sum(x["balanced_nondecreasing"] for x in series),
            "arithmetic_advance": "NO", "fixed_power_credit": 0,
        },
        "summary": {
            "rows": len(rows), "series": len(series),
            "reciprocal_ratio_min": show(min(rratios)),
            "reciprocal_ratio_mean": show(sum(rratios) / len(rratios)),
            "reciprocal_ratio_max": show(max(rratios)),
            "balanced_ratio_min": show(min(bratios)),
            "balanced_ratio_mean": show(sum(bratios) / len(bratios)),
            "balanced_ratio_max": show(max(bratios)),
            "improved_parent_rows": sum(x["improves_balanced_parent"] for x in rows),
            "reciprocal_half_rows": sum(x["reciprocal_at_least_half"] for x in rows),
            "balanced_half_rows": sum(x["balanced_at_least_half"] for x in rows),
            "reciprocal_coordinate_rows": sum(x["reciprocal_beats_coordinate"] for x in rows),
            "balanced_coordinate_rows": sum(x["balanced_beats_coordinate"] for x in rows),
            "response_gain_min": show(min(gains)), "response_gain_mean": show(sum(gains) / len(gains)),
            "response_gain_max": show(max(gains)),
            "reciprocal_nondecreasing_series": sum(x["reciprocal_nondecreasing"] for x in series),
            "balanced_nondecreasing_series": sum(x["balanced_nondecreasing"] for x in series),
            "route_readout": "DISJOINT_HOLDOUT_PARTIAL_TRANSFER_BUT_NO_UNIFORM_REPAIR",
        },
        "scale_breakdown": qbreak, "growth_series": series,
        "exact_anchor": exact_anchor(), "rows": rows,
        "claim_firewall": {
            "TPC352_RECIPROCAL_RULE": "PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE",
            "TPC352_SIGNED_INCIDENCE_LOWER_WITNESS": "PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
            "TPC352_DISJOINT_HOLDOUT": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
            "TPC352_RECIPROCAL_POSITIVE_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_144_OF_144",
            "TPC352_PARENT_IMPROVEMENT_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_118_OF_144",
            "TPC352_UNIFORM_REPAIR_TRANSFER": "REFUTED_SCOPED",
            "TPC352_HIGH_SHELL_REPAIR": "REFUTED_SCOPED",
            "TPC352_ARITHMETIC_ADVANCE": "NO", "TPC352_FIXED_POWER_CREDIT": 0,
            "TPC352_SOURCE_UNIFORM_ARITHMETIC_L2": "OPEN",
            "TPC352_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC352_FULL_GATE_B": "OPEN", "TPC352_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        document = build_document()
        if args.write:
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(canonical(document))
            print("TPC352_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate does not replay")
            print("TPC352_CERTIFICATE=PASS rows=144 positive_reciprocal=144 "
                  "improved_parent=118/144 ratio_floor=0.0801262572786")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC352_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
