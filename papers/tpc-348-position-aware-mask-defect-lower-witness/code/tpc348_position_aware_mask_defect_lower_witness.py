#!/usr/bin/env python3
"""TPC-348: position-aware lower witnesses for the literal mask defect.

TPC-347 identified the physical prime-shell matrix with an unmasked convolution
plus a divisibility-mask defect.  This producer keeps that object fixed and
adds a deterministic lower-witness functional: restrict the columns of the
defect to interval positions hit by at least one active shell prime.  The
induced 2-norm dominates every such column norm, so the resulting finite
certificate is a genuine lower bound, not a spectral-norm proxy.  It remains a
finite scoped audit; no growing arithmetic estimate is asserted.
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
RESULT = PROJECT / "results/tpc348_certificate.json"

PARENT_CODE = ROOT / (
    "papers/tpc-347-convolution-mask-defect-interface/code/"
    "tpc347_convolution_mask_defect_interface.py")
PARENT_CERT = ROOT / (
    "papers/tpc-347-convolution-mask-defect-interface/results/"
    "tpc347_certificate.json")
PARENT_CODE_SHA256 = (
    "2b423b1863fa054b8987934824e0637e464ea5192ba560076abbcfc2394076fb")
PARENT_CERT_SHA256 = (
    "fa7b97ece4dbd165bcf1d81df6b7c021422d9b448a418d036daba8d1f7d828a9")

SCHEMA = "TPC348_POSITION_AWARE_MASK_DEFECT_LOWER_WITNESS_V1"
STATUS = (
    "PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT")
ROUND2_CLUE = "TEST_PRIME_BALANCED_DEFECT_WITNESSES_BEFORE_SOURCE_NATIVE_L2"

ORIGINS = (40097, 48097)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
NUMERIC_TOL = 2.0e-9
LOWER_TOL = 3.0e-9


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
    locked(PARENT_CODE, PARENT_CODE_SHA256, "TPC347 producer")
    locked(PARENT_CERT, PARENT_CERT_SHA256, "TPC347 certificate")
    raw = PARENT_CERT.read_bytes()
    parent = json.loads(raw)
    need(raw == canonical(parent), "TPC347 certificate canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status") ==
         "PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_"
         "NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT",
         "TPC347 certificate header")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
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


def hit_indices(values: np.ndarray, primes: list[int]) -> np.ndarray:
    hit = np.any(np.array([(values % prime) == 0 for prime in primes]),
                 axis=0)
    indices = np.flatnonzero(hit)
    need(len(indices) > 0, "nonempty mask-hit set")
    return indices


def direct_defect_column(values: np.ndarray, differences: np.ndarray,
                         kernel: np.ndarray, primes: list[int],
                         law: str, column: int) -> np.ndarray:
    """Evaluate D e_column from the exact left/right projection formula."""
    result = np.zeros(len(values), dtype=np.float64)
    target = values[column]
    for prime, sign in zip(primes, signs(primes, law)):
        centered = ((differences[:, column] % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        centered[column] = 0.0
        base = float(sign * prime) * kernel[:, column] * centered
        if target % prime == 0:
            # P e_column=0, hence the right-mask defect contributes -K e_column.
            result -= base
        else:
            # (P-I) acts only on output coordinates divisible by p.
            result -= base * (values % prime == 0)
    result[column] = 0.0
    return result


def exact_matrix(origin: int, count: int, q0: int, exponent: int,
                 law: str, masked: bool) -> list[list[Fraction]]:
    values = list(range(origin, origin + count))
    result = [[Fraction(0) for _ in values] for _ in values]
    for prime, sign in zip(shell_for(q0), signs(shell_for(q0), law)):
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


def fraction_matrix_digest(matrix: list[list[Fraction]]) -> str:
    text = [[f"{item.numerator}/{item.denominator}" for item in row]
            for row in matrix]
    return hashlib.sha256(canonical(text)).hexdigest()


def fraction_column_digest(column: list[Fraction]) -> str:
    text = [f"{item.numerator}/{item.denominator}" for item in column]
    return hashlib.sha256(canonical(text)).hexdigest()


def exact_anchor() -> dict[str, Any]:
    actual = exact_matrix(1, 6, 4, 1, "all_plus", True)
    ideal = exact_matrix(1, 6, 4, 1, "all_plus", False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(6)]
              for i in range(6)]
    hits = [index for index, value in enumerate(range(1, 7))
            if any(value % prime == 0 for prime in shell_for(4))]
    need(hits == [4], "exact anchor hit selector")
    column = [defect[i][hits[0]] for i in range(6)]
    square = sum(item * item for item in column)
    need(square == Fraction(1264004832717663389653333,
                           162252681195863096059456),
         "exact anchor witness square")
    return {
        "interval": [1, 6],
        "q": 4,
        "shell": shell_for(4),
        "kernel_exponent": 1,
        "height": HEIGHT,
        "matrix_shape": [6, 6],
        "hit_indices": hits,
        "witness_index": hits[0],
        "witness_position": 5,
        "witness_column_squared_norm":
            f"{square.numerator}/{square.denominator}",
        "witness_column_digest": fraction_column_digest(column),
        "identity_exact": True,
    }


def row_record(origin: int, count: int, q0: int, exponent: int,
               law: str) -> dict[str, Any]:
    actual, ideal, defect, primes = matrices(origin, count, q0, exponent, law)
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + differences.astype(np.float64) ** 2) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    ideal_norm = spectral_norm(ideal)[0]
    defect_norm = spectral_norm(defect)[0]
    columns = np.linalg.norm(defect, axis=0)
    hits = hit_indices(values, primes)
    first = int(hits[0])
    last = int(hits[-1])
    best = int(hits[int(np.argmax(columns[hits]))])
    best_norm = float(columns[best])
    first_norm = float(columns[first])
    last_norm = float(columns[last])
    formula_column = direct_defect_column(values, differences, kernel, primes,
                                           law, best)
    formula_error = float(np.max(np.abs(formula_column - defect[:, best])))
    need(formula_error <= NUMERIC_TOL, "position formula")
    need(best_norm <= defect_norm * (1.0 + LOWER_TOL),
         "coordinate lower bound")
    need(first_norm > 0.0 and best_norm > 0.0, "positive witness")
    return {
        "origin": origin,
        "count": count,
        "source_interval": [origin, origin + count - 1],
        "q": q0,
        "shell": primes,
        "kernel_exponent": exponent,
        "law": law,
        "operator_shape": [count, count],
        "mask_hit_count": int(len(hits)),
        "first_hit_index": first,
        "first_hit_position": int(values[first]),
        "first_hit_column_norm": show(first_norm),
        "first_hit_to_defect_ratio": show(first_norm / defect_norm),
        "first_hit_to_ideal_ratio": show(first_norm / ideal_norm),
        "last_hit_index": last,
        "last_hit_position": int(values[last]),
        "last_hit_column_norm": show(last_norm),
        "best_hit_index": best,
        "best_hit_position": int(values[best]),
        "best_hit_column_norm": show(best_norm),
        "best_hit_to_defect_ratio": show(best_norm / defect_norm),
        "best_hit_to_ideal_ratio": show(best_norm / ideal_norm),
        "global_column_max_norm": show(float(columns.max())),
        "defect_operator_norm": show(defect_norm),
        "ideal_operator_norm": show(ideal_norm),
        "position_formula_max_error": show(formula_error),
        "coordinate_lower_bound_holds": True,
    }


def build_payload() -> dict[str, Any]:
    load_parent()
    rows = [row_record(origin, count, q0, exponent, law)
            for origin in ORIGINS for count in COUNTS
            for q0 in Q_ANCHORS for exponent in EXPONENTS
            for law in LAW_NAMES]
    need(len(rows) == 192, "row census")
    best_defect = [float(item["best_hit_to_defect_ratio"]) for item in rows]
    best_ideal = [float(item["best_hit_to_ideal_ratio"]) for item in rows]
    first_defect = [float(item["first_hit_to_defect_ratio"]) for item in rows]
    first_ideal = [float(item["first_hit_to_ideal_ratio"]) for item in rows]
    hit_counts = [item["mask_hit_count"] for item in rows]
    formula_errors = [float(item["position_formula_max_error"])
                      for item in rows]
    need(all(item["coordinate_lower_bound_holds"] for item in rows),
         "lower witness census")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC347_producer_sha256": PARENT_CODE_SHA256,
            "TPC347_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "source_counts": list(COUNTS),
            "interval_rule": "I_(o,M)={o,...,o+M-1}",
            "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT,
            "laws": list(LAW_NAMES),
            "witness_set": "J_I={t in I: exists p in shell(q), p divides t}",
            "witness_selector": "argmax_{t in J_I} ||D_I e_t||_2; first-hit also stored",
            "physical_entry":
                "1_(u!=t)1_(p does not divide u t)p h_s(u-t) "
                "(1_(p divides u-t)-1/(p-1))",
            "defect": "D=A-T",
        },
        "exact_theorem": {
            "coordinate_lower_bound":
                "||D_I||_(2->2)>=||D_I e_t||_2 for every unit coordinate e_t",
            "mask_hit_lower_bound":
                "||D_I||_(2->2)>=max_{t in J_I}||D_I e_t||_2",
            "mask_hit_column_formula":
                "D_I e_t=-sum_{p|t}e_p R_I K_p e_t "
                "+sum_{p not|t}e_p R_I(P_p-I)K_p e_t",
            "selector": "J_I={t in I: exists active shell prime p with p|t}",
            "finite_scope":
                "the inequalities are exact; ratios and rows are finite audits",
        },
        "finite_audit": {
            "origins": len(ORIGINS),
            "source_counts": len(COUNTS),
            "q_anchors": len(Q_ANCHORS),
            "kernel_exponents": len(EXPONENTS),
            "laws": len(LAW_NAMES),
            "rows": len(rows),
            "positive_witness_rows": sum(
                item["best_hit_column_norm"] != "0" for item in rows),
            "position_formula_records": len(rows),
            "position_formula_max_error": show(max(formula_errors)),
            "min_mask_hit_count": min(hit_counts),
            "max_mask_hit_count": max(hit_counts),
            "best_hit_lower_bound_records": len(rows),
            "arithmetic_advance": "NO",
            "fixed_power_credit": 0,
        },
        "summary": {
            "best_hit_to_defect_ratio_min": show(min(best_defect)),
            "best_hit_to_defect_ratio_max": show(max(best_defect)),
            "best_hit_to_ideal_ratio_min": show(min(best_ideal)),
            "best_hit_to_ideal_ratio_max": show(max(best_ideal)),
            "first_hit_to_defect_ratio_min": show(min(first_defect)),
            "first_hit_to_defect_ratio_max": show(max(first_defect)),
            "first_hit_to_ideal_ratio_min": show(min(first_ideal)),
            "first_hit_to_ideal_ratio_max": show(max(first_ideal)),
            "mask_hit_count_min": min(hit_counts),
            "mask_hit_count_max": max(hit_counts),
            "position_formula_max_error": show(max(formula_errors)),
            "route_readout":
                "POSITION_AWARE_MASK_HIT_COLUMNS_CERTIFY_A_FINITE_DEFECT_LOWER_WITNESS",
        },
        "exact_anchor": exact_anchor(),
        "rows": rows,
        "claim_firewall": {
            "TPC348_COORDINATE_LOWER_WITNESS":
                "PROVED_EXACT_FINITE_LINEAR_ALGEBRA",
            "TPC348_MASK_HIT_SELECTOR": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC348_POSITION_FORMULA": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC348_FINITE_POSITION_AUDIT":
                "NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
            "TPC348_POSITIVE_WITNESS_CENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_192_OF_192",
            "TPC348_DEFECT_DISCARDABILITY": "REFUTED_SCOPED",
            "TPC348_SOURCE_UNIFORM_ARITHMETIC_L2": "OPEN",
            "TPC348_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC348_FIXED_POWER_CREDIT": 0,
            "TPC348_FULL_GATE_B": "OPEN",
            "TPC348_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC348_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate does not replay")
            print("TPC348_CERTIFICATE=PASS rows=192 positive_witness=192 "
                  "position_formula=192")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC348_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
