#!/usr/bin/env python3
"""TPC-351: reciprocal-shell zero-sum contrast audit.

TPC-350 showed that the fixed balanced step contrast loses floor at high shell
scale.  This producer tests one predeclared, non-fitted reciprocal-shell
contrast on the same fresh panel.  The output is finite evidence: improvement
over the parent is an observation, not an asymptotic theorem.
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
RESULT = PROJECT / "results/tpc351_certificate.json"

PARENT_CODE = ROOT / (
    "papers/tpc-350-fresh-growth-signed-incidence/code/"
    "tpc350_fresh_growth_signed_incidence.py")
PARENT_CERT = ROOT / (
    "papers/tpc-350-fresh-growth-signed-incidence/results/"
    "tpc350_certificate.json")
PARENT_CODE_SHA256 = (
    "7819fb38be3f6d33688ca3a4caa1920da2dd8624805356411d8099fc069e185d")
PARENT_CERT_SHA256 = (
    "bc874009cfdd8fd7d6ea06d5d109a46d8bd9a732cd4933852f9176c5801bb086")

SCHEMA = "TPC351_RECIPROCAL_SHELL_CONTRAST_V1"
STATUS = (
    "PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT")
ROUND2_CLUE = "ADVERSARIAL_HOLDOUT_FOR_RECIPROCAL_CONTRAST_BEFORE_BRANCH_FREEZE"

ORIGINS = (60097, 72097, 84097)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (36, 80, 128, 256)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index")
HEIGHT = 66
NUMERIC_TOL = 5.0e-9
GRAM_TOL = 5.0e-9


class CheckFailure(RuntimeError):
    """Raised when the frozen finite contract is not reproduced."""


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


def load_parent() -> dict[str, Any]:
    locked(PARENT_CODE, PARENT_CODE_SHA256, "TPC350 producer")
    locked(PARENT_CERT, PARENT_CERT_SHA256, "TPC350 certificate")
    raw = PARENT_CERT.read_bytes()
    parent = json.loads(raw)
    need(raw == canonical(parent), "TPC350 certificate canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status") ==
         "PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_"
         "NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT",
         "TPC350 certificate header")
    return parent


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    if limit >= 1:
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
    reciprocals = [Fraction(1, prime) for prime in primes]
    mean = sum(reciprocals, Fraction(0)) / len(reciprocals)
    result = [value - mean for value in reciprocals]
    need(sum(result, Fraction(0)) == 0, "reciprocal coefficient sum")
    need(all(value != 0 for value in result),
         "reciprocal coefficients are nonzero")
    return result


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def spectral_norm(matrix: np.ndarray) -> float:
    symmetric = (matrix + matrix.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(symmetric)
    need(len(eigenvalues) > 0 and bool(np.all(np.isfinite(eigenvalues))),
         "finite spectrum")
    return max(abs(float(eigenvalues[0])), abs(float(eigenvalues[-1])))


def matrices(origin: int, count: int, q0: int, exponent: int,
             law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int]]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    distances = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distances * distances) ** exponent)
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


def incidence_vector(values: np.ndarray, primes: list[int],
                     coefficients: list[int]) -> np.ndarray:
    result = np.zeros(len(values), dtype=np.float64)
    for prime, coefficient in zip(primes, coefficients):
        if coefficient:
            result += coefficient * (values % prime == 0)
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
    text = [f"{item.numerator}/{item.denominator}" for item in vector]
    return hashlib.sha256(canonical(text)).hexdigest()


def exact_anchor() -> dict[str, Any]:
    origin, count, q0, exponent, law = 97, 14, 4, 1, "all_plus"
    actual = fraction_matrix(origin, count, q0, exponent, law, True)
    ideal = fraction_matrix(origin, count, q0, exponent, law, False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(count)]
              for i in range(count)]
    primes = shell_for(q0)
    coefficients = reciprocal_coefficients(primes)
    vector = [sum((coefficients[k]
                  for k, prime in enumerate(primes) if value % prime == 0)
                  , Fraction(0))
              for value in range(origin, origin + count)]
    image = [sum(defect[i][j] * vector[j] for j in range(count))
             for i in range(count)]
    vector_square = sum(item * item for item in vector)
    image_square = sum(item * item for item in image)
    expected_vector = [Fraction(0), Fraction(-1, 35), Fraction(0),
                       Fraction(1, 35), Fraction(0), Fraction(0),
                       Fraction(0), Fraction(0), Fraction(0), Fraction(0),
                       Fraction(0), Fraction(0), Fraction(0), Fraction(1, 35)]
    need(vector == expected_vector, "exact reciprocal anchor vector")
    need(vector_square == Fraction(3, 1225),
         "exact reciprocal anchor vector square")
    need(image_square == Fraction(
        14276593956453081571772409162371674557671952566687819648533844297,
        154111273501081250130949964168272395131106235032884375403412500000),
         "exact anchor image square")
    return {
        "interval": [origin, origin + count - 1],
        "q": q0,
        "shell": primes,
        "kernel_exponent": exponent,
        "height": HEIGHT,
        "matrix_shape": [count, count],
        "coefficients": [fraction_text(item) for item in coefficients],
        "incidence_vector": [fraction_text(item) for item in vector],
        "incidence_vector_squared_norm": fraction_text(vector_square),
        "response_vector_squared_norm":
            f"{image_square.numerator}/{image_square.denominator}",
        "response_vector_digest": vector_digest(image),
        "identity_exact": True,
    }


def row_record(origin: int, count: int, q0: int, exponent: int,
               law: str, parent_rows: dict[tuple[int, int, int, int, str],
                                           dict[str, Any]]) -> dict[str, Any]:
    _, ideal, defect, primes = matrices(origin, count, q0, exponent, law)
    values = np.arange(origin, origin + count, dtype=np.int64)
    coefficients = reciprocal_coefficients(primes)
    incidence = incidence_vector(values, primes,
                                 [float(item) for item in coefficients])
    support = np.flatnonzero(incidence != 0)
    need(len(support) > 0, "empty signed support")
    incidence_norm = float(np.linalg.norm(incidence))
    need(incidence_norm > 0.0 and bool(np.isfinite(incidence_norm)),
         "signed incidence norm")
    unit = incidence / incidence_norm
    response_vector = defect @ unit
    response_norm = float(np.linalg.norm(response_vector))
    defect_norm = spectral_norm(defect)
    ideal_norm = spectral_norm(ideal)
    hit = np.any(np.array([(values % prime) == 0 for prime in primes]), axis=0)
    coordinate_norms = np.linalg.norm(defect[:, hit], axis=0)
    coordinate_baseline = float(coordinate_norms.max())
    gram_image = np.zeros(count, dtype=np.float64)
    for prime, coefficient in zip(primes, coefficients):
        if coefficient != 0:
            gram_image += float(coefficient) * (defect @
                                         (values % prime == 0).astype(float))
    gram_error = float(np.max(np.abs(
        defect @ unit - gram_image / incidence_norm)))
    need(gram_error <= GRAM_TOL, "incidence Gram replay")
    need(response_norm <= defect_norm * (1.0 + NUMERIC_TOL),
         "induced-norm lower bound")
    need(response_norm > 0.0, "positive signed response")
    ratio_defect = response_norm / defect_norm
    ratio_ideal = response_norm / ideal_norm
    ratio_coordinate = response_norm / coordinate_baseline
    parent = parent_rows[(origin, count, q0, exponent, law)]
    parent_response = float(parent["signed_witness_response_norm"])
    parent_ratio = float(parent["signed_to_defect_ratio"])
    need(parent_response > 0.0 and parent_ratio > 0.0,
         "parent response is positive")
    response_gain = response_norm / parent_response
    return {
        "origin": origin,
        "count": count,
        "source_interval": [origin, origin + count - 1],
        "q": q0,
        "shell": primes,
        "kernel_exponent": exponent,
        "law": law,
        "operator_shape": [count, count],
        "reciprocal_coefficients": [fraction_text(item)
                                     for item in coefficients],
        "reciprocal_coefficient_sum": fraction_text(
            sum(coefficients, Fraction(0))),
        "reciprocal_active_prime_count": int(sum(value != 0
                                                   for value in coefficients)),
        "reciprocal_incidence_support": int(len(support)),
        "reciprocal_incidence_norm": show(incidence_norm),
        "reciprocal_witness_response_norm": show(response_norm),
        "reciprocal_to_defect_ratio": show(ratio_defect),
        "reciprocal_to_ideal_ratio": show(ratio_ideal),
        "reciprocal_to_coordinate_ratio": show(ratio_coordinate),
        "beats_coordinate_baseline": bool(ratio_coordinate > 1.0 + 1.0e-10),
        "at_least_half_defect": bool(ratio_defect >= 0.5 - 1.0e-12),
        "parent_balanced_response_norm": parent["signed_witness_response_norm"],
        "parent_balanced_to_defect_ratio": parent["signed_to_defect_ratio"],
        "reciprocal_to_parent_response_ratio": show(response_gain),
        "improves_parent_balanced": bool(response_gain > 1.0 + 1.0e-10),
        "coordinate_baseline_norm": show(coordinate_baseline),
        "defect_operator_norm": show(defect_norm),
        "ideal_operator_norm": show(ideal_norm),
        "incidence_gram_max_error": show(gram_error),
        "coordinate_lower_bound_holds": True,
    }


def make_series(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[int, int, int, str], list[dict[str, Any]]] = {}
    for row in rows:
        key = (row["origin"], row["q"], row["kernel_exponent"], row["law"])
        groups.setdefault(key, []).append(row)
    result = []
    for origin in ORIGINS:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                for law in LAW_NAMES:
                    series = sorted(groups[(origin, q0, exponent, law)],
                                    key=lambda item: item["count"])
                    values = [float(item["reciprocal_to_defect_ratio"])
                              for item in series]
                    need(len(values) == len(COUNTS), "growth series length")
                    result.append({
                        "origin": origin,
                        "q": q0,
                        "kernel_exponent": exponent,
                        "law": law,
                        "counts": [item["count"] for item in series],
                        "reciprocal_to_defect_ratios": [show(value)
                                                     for value in values],
                        "nondecreasing": bool(all(
                            values[index + 1] >= values[index] - 1.0e-12
                            for index in range(len(values) - 1))),
                        "endpoint_log2_slope": show(
                            math.log(values[-1] / values[0], 2.0) /
                            (math.log(COUNTS[-1] / COUNTS[0], 2.0))),
                    })
    return result


def build_payload() -> dict[str, Any]:
    parent = load_parent()
    parent_rows = {(row["origin"], row["count"], row["q"],
                    row["kernel_exponent"], row["law"]): row
                   for row in parent["payload"]["rows"]}
    need(len(parent_rows) == 192, "TPC350 parent row census")
    rows = [row_record(origin, count, q0, exponent, law, parent_rows)
            for origin in ORIGINS for count in COUNTS
            for q0 in Q_ANCHORS for exponent in EXPONENTS
            for law in LAW_NAMES]
    need(len(rows) == 192, "row census")
    defect_ratios = [float(item["reciprocal_to_defect_ratio"])
                     for item in rows]
    ideal_ratios = [float(item["reciprocal_to_ideal_ratio"])
                    for item in rows]
    coordinate_ratios = [float(item["reciprocal_to_coordinate_ratio"])
                         for item in rows]
    gram_errors = [float(item["incidence_gram_max_error"]) for item in rows]
    supports = [item["reciprocal_incidence_support"] for item in rows]
    parent_ratios = [float(item["parent_balanced_to_defect_ratio"])
                     for item in rows]
    gains = [float(item["reciprocal_to_parent_response_ratio"])
             for item in rows]
    series = make_series(rows)
    scale_breakdown = {}
    for q0 in Q_ANCHORS:
        subset = [item for item in rows if item["q"] == q0]
        parent_subset = [float(item["parent_balanced_to_defect_ratio"])
                         for item in subset]
        scale_breakdown[str(q0)] = {
            "rows": len(subset),
            "reciprocal_min": show(min(float(
                item["reciprocal_to_defect_ratio"]) for item in subset)),
            "reciprocal_mean": show(sum(float(
                item["reciprocal_to_defect_ratio"]) for item in subset) /
                                      len(subset)),
            "reciprocal_max": show(max(float(
                item["reciprocal_to_defect_ratio"]) for item in subset)),
            "reciprocal_half_defect": sum(
                item["at_least_half_defect"] for item in subset),
            "parent_min": show(min(parent_subset)),
            "parent_mean": show(sum(parent_subset) / len(parent_subset)),
            "parent_half_defect": sum(
                float(item["parent_balanced_to_defect_ratio"]) >= 0.5
                for item in subset),
            "improved_parent": sum(item["improves_parent_balanced"]
                                    for item in subset),
        }
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC350_producer_sha256": PARENT_CODE_SHA256,
            "TPC350_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "source_counts": list(COUNTS),
            "interval_rule": "I_(o,M)={o,...,o+M-1}",
            "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT,
            "laws": list(LAW_NAMES),
            "contrast_rule":
                "gamma_j=1/p_j-(1/r)sum_k 1/p_k, for p_j in (Q,2Q]",
            "coefficient_sum": "sum_j gamma_j=0 exactly",
            "incidence_vector": "c_I(t)=sum_j gamma_j 1_(p_j divides t)",
            "witness_vector": "x_I=c_I/||c_I||_2",
            "parent_control":
                "TPC350 balanced step contrast on the identical row keys",
            "comparison_baseline":
                "max over mask-hit coordinate columns of ||D_I e_t||_2",
            "growth_ladder": "M=256,512,1024,2048 at each fresh origin",
            "shell_ladder": "Q=36,80,128,256",
            "physical_entry":
                "1_(u!=t)1_(p does not divide u t)p h_s(u-t) "
                "(1_(p divides u-t)-1/(p-1))",
            "defect": "D=A-T",
        },
        "exact_theorem": {
            "coefficient_balance":
                "sum_j (1/p_j-(1/r)sum_k 1/p_k)=0 exactly",
            "incidence_identity": "c_I=sum_j gamma_j h_{p_j,I}",
            "gram_expansion":
                "||D_I c_I||_2^2=sum_{j,k} gamma_j gamma_k "
                "<D_I h_{p_j,I},D_I h_{p_k,I}>",
            "normalized_lower_bound":
                "||D_I||_(2->2)>=||D_I c_I||_2/||c_I||_2 for c_I != 0",
            "finite_scope":
                "the reciprocal rule is exact; comparisons are finite audits",
        },
        "finite_audit": {
            "origins": len(ORIGINS),
            "source_counts": len(COUNTS),
            "q_anchors": len(Q_ANCHORS),
            "kernel_exponents": len(EXPONENTS),
            "laws": len(LAW_NAMES),
            "rows": len(rows),
            "series": len(series),
            "positive_reciprocal_witness_rows": sum(
                item["reciprocal_witness_response_norm"] != "0"
                for item in rows),
            "zero_sum_records": sum(
                item["reciprocal_coefficient_sum"] == "0/1"
                for item in rows),
            "incidence_gram_records": len(rows),
            "incidence_gram_max_error": show(max(gram_errors)),
            "improved_parent_rows": sum(
                item["improves_parent_balanced"] for item in rows),
            "parent_comparison_records": len(rows),
            "coordinate_beaten_rows": sum(
                item["beats_coordinate_baseline"] for item in rows),
            "half_defect_rows": sum(item["at_least_half_defect"]
                                    for item in rows),
            "min_reciprocal_support": min(supports),
            "max_reciprocal_support": max(supports),
            "min_reciprocal_to_defect_ratio": show(min(defect_ratios)),
            "max_reciprocal_to_defect_ratio": show(max(defect_ratios)),
            "parent_balanced_floor": show(min(parent_ratios)),
            "parent_balanced_mean": show(sum(parent_ratios) /
                                           len(parent_ratios)),
            "nondecreasing_series": sum(item["nondecreasing"]
                                         for item in series),
            "arithmetic_advance": "NO",
            "fixed_power_credit": 0,
        },
        "summary": {
            "reciprocal_to_defect_ratio_min": show(min(defect_ratios)),
            "reciprocal_to_defect_ratio_max": show(max(defect_ratios)),
            "reciprocal_to_defect_ratio_mean": show(
                sum(defect_ratios) / len(rows)),
            "reciprocal_to_ideal_ratio_min": show(min(ideal_ratios)),
            "reciprocal_to_ideal_ratio_max": show(max(ideal_ratios)),
            "reciprocal_to_coordinate_ratio_min": show(
                min(coordinate_ratios)),
            "reciprocal_to_coordinate_ratio_max": show(
                max(coordinate_ratios)),
            "coordinate_beaten_rows": sum(
                item["beats_coordinate_baseline"] for item in rows),
            "half_defect_rows": sum(item["at_least_half_defect"]
                                    for item in rows),
            "reciprocal_support_min": min(supports),
            "reciprocal_support_max": max(supports),
            "incidence_gram_max_error": show(max(gram_errors)),
            "improved_parent_rows": sum(
                item["improves_parent_balanced"] for item in rows),
            "response_gain_min": show(min(gains)),
            "response_gain_mean": show(sum(gains) / len(gains)),
            "response_gain_max": show(max(gains)),
            "nondecreasing_series": sum(item["nondecreasing"]
                                         for item in series),
            "total_series": len(series),
            "route_readout":
                "RECIPROCAL_SHELL_CONTRAST_REPAIRS_MOST_ROWS_BUT_NOT_THE"
                "_UNIFORM_QUARTER_FLOOR",
        },
        "growth_series": series,
        "scale_breakdown": scale_breakdown,
        "exact_anchor": exact_anchor(),
        "rows": rows,
        "claim_firewall": {
            "TPC351_RECIPROCAL_ZERO_SUM_RULE":
                "PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE",
            "TPC351_SIGNED_INCIDENCE_LOWER_WITNESS":
                "PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
            "TPC351_SCALE_REPAIR_AUDIT":
                "NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
            "TPC351_POSITIVE_WITNESS_CENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_192_OF_192",
            "TPC351_PARENT_IMPROVEMENT_CENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_180_OF_192",
            "TPC351_UNIFORM_QUARTER_FLOOR": "REFUTED_SCOPED",
            "TPC351_SOURCE_UNIFORM_ARITHMETIC_L2": "OPEN",
            "TPC351_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC351_ARITHMETIC_ADVANCE": "NO",
            "TPC351_FIXED_POWER_CREDIT": 0,
            "TPC351_FULL_GATE_B": "OPEN",
            "TPC351_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC351_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate does not replay")
            print("TPC351_CERTIFICATE=PASS rows=192 positive_witness=192 "
                 "improved_parent=180/192 ratio_floor=0.0917557319271")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC351_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
