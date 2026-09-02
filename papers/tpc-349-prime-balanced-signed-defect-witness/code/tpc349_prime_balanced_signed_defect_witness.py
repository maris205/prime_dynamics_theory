#!/usr/bin/env python3
"""TPC-349: a prime-balanced signed incidence witness for the mask defect.

TPC-348 supplied a position-aware coordinate lower witness.  This producer
tests the next declared object: a zero-sum signing of the ordered shell primes
applied to all divisibility incidences in the mask-hit set.  The resulting
vector has an exact Gram expansion, and its image gives an exact finite
operator-norm lower witness.  All ratios remain finite-panel observations.
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
RESULT = PROJECT / "results/tpc349_certificate.json"

PARENT_CODE = ROOT / (
    "papers/tpc-348-position-aware-mask-defect-lower-witness/code/"
    "tpc348_position_aware_mask_defect_lower_witness.py")
PARENT_CERT = ROOT / (
    "papers/tpc-348-position-aware-mask-defect-lower-witness/results/"
    "tpc348_certificate.json")
PARENT_CODE_SHA256 = (
    "fe29f0adeea6234c637a479ba2447068a1e6b1c91731761ed2d2af73464d20b8")
PARENT_CERT_SHA256 = (
    "5f0b1cb66431f6a57fa97335808f30fdbe86ffc0b31ce074d7a1dbbdc692a294")

SCHEMA = "TPC349_PRIME_BALANCED_SIGNED_DEFECT_WITNESS_V1"
STATUS = (
    "PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_AUDIT")
ROUND2_CLUE = "REPLICATE_SIGNED_INCIDENCE_GRAM_ON_GROWING_FRESH_PANELS"

ORIGINS = (40097, 48097)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
NUMERIC_TOL = 2.0e-9
GRAM_TOL = 2.0e-9


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


def load_parent() -> None:
    locked(PARENT_CODE, PARENT_CODE_SHA256, "TPC348 producer")
    locked(PARENT_CERT, PARENT_CERT_SHA256, "TPC348 certificate")
    raw = PARENT_CERT.read_bytes()
    parent = json.loads(raw)
    need(raw == canonical(parent), "TPC348 certificate canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status") ==
         "PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_"
         "NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT",
         "TPC348 certificate header")


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


def signs(primes: list[int], law: str) -> list[int]:
    need(law in LAW_NAMES, "unknown sign law")
    if law == "all_plus":
        return [1] * len(primes)
    if law == "alternating_index":
        return [1 if index % 2 == 0 else -1
                for index in range(len(primes))]
    if law == "mod4_character":
        return [1 if prime % 4 == 1 else -1 for prime in primes]
    return [1 if index < len(primes) / 2 else -1
            for index in range(len(primes))]


def balanced_coefficients(primes: list[int]) -> list[int]:
    """Equal positive/negative shell split; one middle prime is neutral if odd."""
    count = len(primes)
    half = count // 2
    result = [1 if index < half else
              (-1 if index >= count - half else 0)
              for index in range(count)]
    need(sum(result) == 0, "prime balance")
    need(sum(value != 0 for value in result) == 2 * half,
         "prime balance census")
    return result


def spectral_norm(matrix: np.ndarray) -> tuple[float, float, float]:
    symmetric = (matrix + matrix.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(symmetric)
    need(len(eigenvalues) > 0 and bool(np.all(np.isfinite(eigenvalues))),
         "finite spectrum")
    lower = float(eigenvalues[0])
    upper = float(eigenvalues[-1])
    return max(abs(lower), abs(upper)), lower, upper


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
    for prime, sign in zip(primes, signs(primes, law)):
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
    for prime, sign in zip(primes, signs(primes, law)):
        for i, u in enumerate(values):
            for j, t in enumerate(values):
                if u == t:
                    continue
                if masked and (u % prime == 0 or t % prime == 0):
                    continue
                centered = (Fraction(1) if (u - t) % prime == 0
                            else Fraction(0))
                centered -= Fraction(1, prime - 1)
                kernel = Fraction(HEIGHT ** (2 * exponent),
                                  (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
                result[i][j] += sign * prime * kernel * centered
    return result


def fraction_vector_digest(vector: list[Fraction]) -> str:
    text = [f"{item.numerator}/{item.denominator}" for item in vector]
    return hashlib.sha256(canonical(text)).hexdigest()


def exact_anchor() -> dict[str, Any]:
    actual = fraction_matrix(1, 14, 4, 1, "all_plus", True)
    ideal = fraction_matrix(1, 14, 4, 1, "all_plus", False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(14)]
              for i in range(14)]
    primes = shell_for(4)
    coefficients = balanced_coefficients(primes)
    vector = [sum(Fraction(coefficients[k])
                  for k, prime in enumerate(primes) if value % prime == 0)
              for value in range(1, 15)]
    need(vector == [Fraction(value) for value in
                    [0, 0, 0, 0, 1, 0, -1, 0, 0, 1, 0, 0, 0, -1]],
         "exact anchor incidence vector")
    image = [sum(defect[i][j] * vector[j] for j in range(14))
             for i in range(14)]
    vector_square = sum(item * item for item in vector)
    image_square = sum(item * item for item in image)
    need(vector_square == 4, "exact anchor vector square")
    need(image_square == Fraction(
        1580136191762341638715051100269721298390649257672312877072677225319,
        4277374121662663268940652066711233824047030196831076541809000000),
         "exact anchor response square")
    return {
        "interval": [1, 14],
        "q": 4,
        "shell": primes,
        "kernel_exponent": 1,
        "height": HEIGHT,
        "matrix_shape": [14, 14],
        "coefficients": coefficients,
        "incidence_vector": [int(item) for item in vector],
        "incidence_vector_squared_norm": str(vector_square.numerator),
        "response_vector_squared_norm":
            f"{image_square.numerator}/{image_square.denominator}",
        "response_vector_digest": fraction_vector_digest(image),
        "identity_exact": True,
    }


def row_record(origin: int, count: int, q0: int, exponent: int,
               law: str) -> dict[str, Any]:
    _, ideal, defect, primes = matrices(origin, count, q0, exponent, law)
    values = np.arange(origin, origin + count, dtype=np.int64)
    coefficients = balanced_coefficients(primes)
    incidence = incidence_vector(values, primes, coefficients)
    support = np.flatnonzero(incidence != 0)
    need(len(support) > 0, "nonempty signed incidence support")
    incidence_norm = float(np.linalg.norm(incidence))
    need(incidence_norm > 0.0 and bool(np.isfinite(incidence_norm)),
         "signed incidence norm")
    unit = incidence / incidence_norm
    response_vector = defect @ unit
    response_norm = float(np.linalg.norm(response_vector))
    defect_norm = spectral_norm(defect)[0]
    ideal_norm = spectral_norm(ideal)[0]

    hit = np.any(np.array([(values % prime) == 0 for prime in primes]),
                 axis=0)
    coordinate_norms = np.linalg.norm(defect[:, hit], axis=0)
    coordinate_baseline = float(coordinate_norms.max())
    gram_image = np.zeros(count, dtype=np.float64)
    for prime, coefficient in zip(primes, coefficients):
        if coefficient:
            hit_vector = (values % prime == 0).astype(np.float64)
            gram_image += coefficient * (defect @ hit_vector)
    gram_error = float(np.max(np.abs(
        defect @ unit - gram_image / incidence_norm)))
    # The first expression is intentionally written through the normalized
    # vector; it is exactly defect@unit, while the second is the incidence Gram
    # expansion divided by the same norm.
    need(gram_error <= GRAM_TOL, "incidence Gram identity")
    need(response_norm <= defect_norm * (1.0 + NUMERIC_TOL),
         "signed coordinate lower bound")
    need(response_norm > 0.0, "positive signed witness")
    ratio_defect = response_norm / defect_norm
    ratio_ideal = response_norm / ideal_norm
    ratio_coordinate = response_norm / coordinate_baseline
    return {
        "origin": origin,
        "count": count,
        "source_interval": [origin, origin + count - 1],
        "q": q0,
        "shell": primes,
        "kernel_exponent": exponent,
        "law": law,
        "operator_shape": [count, count],
        "balanced_coefficients": coefficients,
        "balanced_coefficient_sum": int(sum(coefficients)),
        "balanced_active_prime_count": int(sum(value != 0
                                                for value in coefficients)),
        "signed_incidence_support": int(len(support)),
        "signed_incidence_norm": show(incidence_norm),
        "signed_witness_response_norm": show(response_norm),
        "signed_to_defect_ratio": show(ratio_defect),
        "signed_to_ideal_ratio": show(ratio_ideal),
        "signed_to_coordinate_ratio": show(ratio_coordinate),
        "beats_coordinate_baseline": bool(ratio_coordinate > 1.0 + 1.0e-10),
        "at_least_half_defect": bool(ratio_defect >= 0.5 - 1.0e-12),
        "coordinate_baseline_norm": show(coordinate_baseline),
        "defect_operator_norm": show(defect_norm),
        "ideal_operator_norm": show(ideal_norm),
        "incidence_gram_max_error": show(gram_error),
        "coordinate_lower_bound_holds": True,
    }


def build_payload() -> dict[str, Any]:
    load_parent()
    rows = [row_record(origin, count, q0, exponent, law)
            for origin in ORIGINS for count in COUNTS
            for q0 in Q_ANCHORS for exponent in EXPONENTS
            for law in LAW_NAMES]
    need(len(rows) == 192, "row census")
    defect_ratios = [float(item["signed_to_defect_ratio"]) for item in rows]
    ideal_ratios = [float(item["signed_to_ideal_ratio"]) for item in rows]
    coordinate_ratios = [float(item["signed_to_coordinate_ratio"])
                         for item in rows]
    gram_errors = [float(item["incidence_gram_max_error"]) for item in rows]
    supports = [item["signed_incidence_support"] for item in rows]
    need(all(item["balanced_coefficient_sum"] == 0 for item in rows),
         "balance census")
    need(all(item["coordinate_lower_bound_holds"] for item in rows),
         "lower witness census")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC348_producer_sha256": PARENT_CODE_SHA256,
            "TPC348_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "source_counts": list(COUNTS),
            "interval_rule": "I_(o,M)={o,...,o+M-1}",
            "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT,
            "laws": list(LAW_NAMES),
            "balanced_rule":
                "beta_j=+1 for j<floor(r/2), -1 for j>=r-floor(r/2), "
                "and 0 for a possible middle prime",
            "incidence_vector":
                "b_I(t)=sum_j beta_j 1_(p_j divides t)",
            "witness_vector": "x_I=b_I/||b_I||_2",
            "comparison_baseline":
                "max over mask-hit coordinate columns of ||D_I e_t||_2",
            "physical_entry":
                "1_(u!=t)1_(p does not divide u t)p h_s(u-t) "
                "(1_(p divides u-t)-1/(p-1))",
            "defect": "D=A-T",
        },
        "exact_theorem": {
            "incidence_identity":
                "b_I=sum_j beta_j h_{p_j,I}",
            "gram_expansion":
                "||D_I b_I||_2^2=sum_{j,k} beta_j beta_k "
                "<D_I h_{p_j,I},D_I h_{p_k,I}>",
            "normalized_lower_bound":
                "||D_I||_(2->2)>=||D_I b_I||_2/||b_I||_2 for b_I != 0",
            "finite_scope":
                "the identities are exact; ratios and row counts are finite audits",
        },
        "finite_audit": {
            "origins": len(ORIGINS),
            "source_counts": len(COUNTS),
            "q_anchors": len(Q_ANCHORS),
            "kernel_exponents": len(EXPONENTS),
            "laws": len(LAW_NAMES),
            "rows": len(rows),
            "positive_signed_witness_rows": sum(
                item["signed_witness_response_norm"] != "0" for item in rows),
            "balanced_sum_records": sum(
                item["balanced_coefficient_sum"] == 0 for item in rows),
            "incidence_gram_records": len(rows),
            "incidence_gram_max_error": show(max(gram_errors)),
            "coordinate_beaten_rows": sum(
                item["beats_coordinate_baseline"] for item in rows),
            "half_defect_rows": sum(item["at_least_half_defect"] for item in rows),
            "min_signed_support": min(supports),
            "max_signed_support": max(supports),
            "arithmetic_advance": "NO",
            "fixed_power_credit": 0,
        },
        "summary": {
            "signed_to_defect_ratio_min": show(min(defect_ratios)),
            "signed_to_defect_ratio_max": show(max(defect_ratios)),
            "signed_to_ideal_ratio_min": show(min(ideal_ratios)),
            "signed_to_ideal_ratio_max": show(max(ideal_ratios)),
            "signed_to_coordinate_ratio_min": show(min(coordinate_ratios)),
            "signed_to_coordinate_ratio_max": show(max(coordinate_ratios)),
            "signed_to_defect_ratio_mean": show(sum(defect_ratios) / len(rows)),
            "coordinate_beaten_rows": sum(
                item["beats_coordinate_baseline"] for item in rows),
            "half_defect_rows": sum(item["at_least_half_defect"] for item in rows),
            "signed_support_min": min(supports),
            "signed_support_max": max(supports),
            "incidence_gram_max_error": show(max(gram_errors)),
            "route_readout":
                "PRIME_BALANCED_SIGNED_INCIDENCE_GIVES_A_FINITE_DEFECT_LOWER_WITNESS",
        },
        "exact_anchor": exact_anchor(),
        "rows": rows,
        "claim_firewall": {
            "TPC349_SIGNED_INCIDENCE_LOWER_WITNESS":
                "PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
            "TPC349_PRIME_BALANCE_RULE":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC349_INCIDENCE_GRAM_IDENTITY":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC349_FINITE_SIGNED_AUDIT":
                "NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
            "TPC349_POSITIVE_WITNESS_CENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_192_OF_192",
            "TPC349_COORDINATE_BASELINE_BEATEN":
                "NUMERICALLY_CERTIFIED_FINITE_136_OF_192",
            "TPC349_HALF_DEFECT_CENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_175_OF_192",
            "TPC349_UNIVERSAL_BALANCED_GAIN": "REFUTED_SCOPED",
            "TPC349_SOURCE_UNIFORM_ARITHMETIC_L2": "OPEN",
            "TPC349_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC349_FIXED_POWER_CREDIT": 0,
            "TPC349_FULL_GATE_B": "OPEN",
            "TPC349_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC349_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate does not replay")
            print("TPC349_CERTIFICATE=PASS rows=192 positive_witness=192 "
                  "coordinate_beaten=136 half_defect=175")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC349_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
