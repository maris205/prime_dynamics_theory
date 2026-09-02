#!/usr/bin/env python3
"""Independent reverse-order replay for TPC-348.

The producer is not imported.  This checker rebuilds the physical, ideal, and
defect matrices, applies the coordinate lower-bound inequality independently,
and verifies the canonical certificate and exact rational anchor.
"""

from __future__ import annotations

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

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-348-position-aware-mask-defect-lower-witness"
PRODUCER = PROJECT / "code/tpc348_position_aware_mask_defect_lower_witness.py"
RESULT = PROJECT / "results/tpc348_certificate.json"
PARENT = ROOT / "papers/tpc-347-convolution-mask-defect-interface"
PARENT_CODE = PARENT / "code/tpc347_convolution_mask_defect_interface.py"
PARENT_CERT = PARENT / "results/tpc347_certificate.json"

PRODUCER_SHA256 = "fe29f0adeea6234c637a479ba2447068a1e6b1c91731761ed2d2af73464d20b8"
PARENT_CODE_SHA256 = "2b423b1863fa054b8987934824e0637e464ea5192ba560076abbcfc2394076fb"
PARENT_CERT_SHA256 = "fa7b97ece4dbd165bcf1d81df6b7c021422d9b448a418d036daba8d1f7d828a9"
SCHEMA = "TPC348_POSITION_AWARE_MASK_DEFECT_LOWER_WITNESS_V1"
STATUS = (
    "PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT")

ORIGINS = (40097, 48097)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
TOL = 5.0e-8
FORMULA_TOL = 5.0e-8


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


def close(actual: float, expected: Any, label: str,
          tolerance: float = TOL) -> None:
    a = float(actual)
    b = float(expected)
    need(math.isfinite(a) and math.isfinite(b) and
         abs(a - b) <= tolerance * max(1.0, abs(a), abs(b)), label)


def lock(path: Path, expected: str, label: str) -> None:
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " hash")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            first = p * p
            sieve[first:limit + 1:p] = b"\x00" * (
                (limit - first) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(160)


def shell(q: int) -> list[int]:
    return [p for p in PRIMES if q < p <= 2 * q]


def sign_vector(primes: list[int], law: str) -> list[int]:
    if law == "all_plus":
        return [1] * len(primes)
    if law == "alternating_index":
        return [1 if i % 2 == 0 else -1 for i in range(len(primes))]
    if law == "mod4_character":
        return [1 if p % 4 == 1 else -1 for p in primes]
    if law == "half_split":
        return [1 if i < len(primes) / 2 else -1
                for i in range(len(primes))]
    raise Failure("unknown law")


def norm2(matrix: np.ndarray) -> float:
    values = np.linalg.eigvalsh((matrix + matrix.T) / 2.0)
    need(len(values) > 0 and bool(np.all(np.isfinite(values))), "spectrum")
    return max(abs(float(values[0])), abs(float(values[-1])))


def rebuild(origin: int, count: int, q: int, exponent: int,
            law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int]]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    distance = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    physical = np.zeros((count, count), dtype=np.float64)
    ideal = np.zeros((count, count), dtype=np.float64)
    primes = shell(q)
    # Reverse shell order is independent of the producer's accumulation path.
    for prime, sign in reversed(list(zip(primes, sign_vector(primes, law)))):
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        block = float(sign * prime) * kernel * centered
        ideal += block
        allowed = ((differences != 0) &
                   (values[:, None] % prime != 0) &
                   (values[None, :] % prime != 0))
        physical += block * allowed
    physical = (physical + physical.T) / 2.0
    ideal = (ideal + ideal.T) / 2.0
    return physical, ideal, physical - ideal, primes


def hit_indices(values: np.ndarray, primes: list[int]) -> np.ndarray:
    mask = np.any(np.array([(values % p) == 0 for p in primes]), axis=0)
    indices = np.flatnonzero(mask)
    need(len(indices) > 0, "empty hit set")
    return indices


def formula_column(values: np.ndarray, differences: np.ndarray,
                   kernel: np.ndarray, primes: list[int], law: str,
                   column: int) -> np.ndarray:
    result = np.zeros(len(values), dtype=np.float64)
    target = values[column]
    for prime, sign in reversed(list(zip(primes, sign_vector(primes, law)))):
        centered = ((differences[:, column] % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        centered[column] = 0.0
        base = float(sign * prime) * kernel[:, column] * centered
        if target % prime == 0:
            result -= base
        else:
            result -= base * (values % prime == 0)
    result[column] = 0.0
    return result


def exact_matrix(count: int, q: int, exponent: int,
                 masked: bool) -> list[list[Fraction]]:
    values = list(range(1, count + 1))
    result = [[Fraction(0) for _ in values] for _ in values]
    for prime in reversed(shell(q)):
        for i, u in enumerate(values):
            for j, t in enumerate(values):
                if u == t or (masked and (u % prime == 0 or t % prime == 0)):
                    continue
                centered = Fraction(int((u - t) % prime == 0))
                centered -= Fraction(1, prime - 1)
                kernel = Fraction(HEIGHT ** (2 * exponent),
                                  (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
                result[i][j] += prime * kernel * centered
    return result


def column_digest(column: list[Fraction]) -> str:
    text = [f"{x.numerator}/{x.denominator}" for x in column]
    return hashlib.sha256(canonical(text)).hexdigest()


def check_anchor(anchor: dict[str, Any]) -> None:
    actual = exact_matrix(6, 4, 1, True)
    ideal = exact_matrix(6, 4, 1, False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(6)]
              for i in range(6)]
    hits = [i for i, value in enumerate(range(1, 7))
            if any(value % p == 0 for p in shell(4))]
    need(hits == [4], "anchor hit selector")
    column = [defect[i][4] for i in range(6)]
    square = sum(x * x for x in column)
    need(anchor.get("hit_indices") == [4] and
         anchor.get("witness_index") == 4 and
         anchor.get("witness_position") == 5, "anchor selector")
    need(anchor.get("witness_column_squared_norm") ==
         f"{square.numerator}/{square.denominator}", "anchor square")
    need(anchor.get("witness_column_digest") == column_digest(column),
         "anchor column digest")
    need(anchor.get("identity_exact") is True, "anchor identity")


def check_row(row: dict[str, Any]) -> None:
    origin = int(row["origin"])
    count = int(row["count"])
    q = int(row["q"])
    exponent = int(row["kernel_exponent"])
    law = str(row["law"])
    physical, ideal, defect, primes = rebuild(origin, count, q, exponent, law)
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + differences.astype(np.float64) ** 2) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    hits = hit_indices(values, primes)
    columns = np.linalg.norm(defect, axis=0)
    best = int(hits[int(np.argmax(columns[hits]))])
    first = int(hits[0])
    last = int(hits[-1])
    dnorm = norm2(defect)
    inorm = norm2(ideal)
    best_norm = float(columns[best])
    first_norm = float(columns[first])
    last_norm = float(columns[last])
    formula_error = float(np.max(np.abs(
        formula_column(values, differences, kernel, primes, law, best) -
        defect[:, best])))
    need(best_norm <= dnorm * (1.0 + 2.0e-8), "coordinate inequality")
    need(formula_error <= FORMULA_TOL, "position formula")
    need(best_norm > 0.0, "positive witness")
    close(row["mask_hit_count"], len(hits), "hit count")
    close(row["first_hit_index"], first, "first index")
    close(row["first_hit_position"], values[first], "first position")
    close(row["last_hit_index"], last, "last index")
    close(row["last_hit_position"], values[last], "last position")
    close(row["best_hit_index"], best, "best index")
    close(row["best_hit_position"], values[best], "best position")
    close(row["first_hit_column_norm"], first_norm, "first norm")
    close(row["last_hit_column_norm"], last_norm, "last norm")
    close(row["best_hit_column_norm"], best_norm, "best norm")
    close(row["defect_operator_norm"], dnorm, "defect norm")
    close(row["ideal_operator_norm"], inorm, "ideal norm")
    close(row["first_hit_to_defect_ratio"], first_norm / dnorm,
          "first defect ratio")
    close(row["first_hit_to_ideal_ratio"], first_norm / inorm,
          "first ideal ratio")
    close(row["best_hit_to_defect_ratio"], best_norm / dnorm,
          "best defect ratio")
    close(row["best_hit_to_ideal_ratio"], best_norm / inorm,
          "best ideal ratio")
    close(row["global_column_max_norm"], float(columns.max()),
          "global column norm")
    close(row["position_formula_max_error"], formula_error,
          "formula error")
    need(row.get("coordinate_lower_bound_holds") is True,
         "lower-bound flag")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        lock(PRODUCER, PRODUCER_SHA256, "producer")
        lock(PARENT_CODE, PARENT_CODE_SHA256, "parent producer")
        lock(PARENT_CERT, PARENT_CERT_SHA256, "parent certificate")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload")
        need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
             "schema")
        need(document.get("payload_sha256") == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload digest")
        need(payload.get("parent_lock") == {
            "TPC347_certificate_sha256": PARENT_CERT_SHA256,
            "TPC347_producer_sha256": PARENT_CODE_SHA256}, "parent lock")
        need(payload.get("protocol", {}).get("origins") == list(ORIGINS) and
             payload.get("protocol", {}).get("source_counts") == list(COUNTS) and
             payload.get("protocol", {}).get("q_anchors") == list(Q_ANCHORS) and
             payload.get("protocol", {}).get("kernel_exponents") == list(EXPONENTS) and
             payload.get("protocol", {}).get("height") == HEIGHT, "protocol")
        expected_audit = {
            "arithmetic_advance": "NO",
            "best_hit_lower_bound_records": 192,
            "fixed_power_credit": 0,
            "kernel_exponents": 2,
            "laws": 4,
            "max_mask_hit_count": 169,
            "min_mask_hit_count": 30,
            "origins": 2,
            "position_formula_max_error": "2.0872192863e-14",
            "position_formula_records": 192,
            "positive_witness_rows": 192,
            "q_anchors": 4,
            "rows": 192,
            "source_counts": 3,
        }
        need(payload.get("finite_audit") == expected_audit, "audit census")
        rows = payload.get("rows", [])
        need(isinstance(rows, list) and len(rows) == 192, "row census")
        for row in rows:
            need(isinstance(row, dict), "row type")
            check_row(row)
        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC348_COORDINATE_LOWER_WITNESS") ==
             "PROVED_EXACT_FINITE_LINEAR_ALGEBRA" and
             firewall.get("TPC348_FINITE_POSITION_AUDIT") ==
             "NUMERICALLY_CERTIFIED_FINITE_192_ROWS" and
             firewall.get("TPC348_POSITIVE_WITNESS_CENSUS") ==
             "NUMERICALLY_CERTIFIED_FINITE_192_OF_192" and
             firewall.get("TPC348_SOURCE_UNIFORM_ARITHMETIC_L2") == "OPEN" and
             firewall.get("TPC348_UNIFORM_MASKED_OPERATOR_BOUND") == "OPEN" and
             firewall.get("TPC348_FIXED_POWER_CREDIT") == 0 and
             firewall.get("TPC348_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC348_TWIN_PRIME_RESULT") == "NONE", "firewall")
        check_anchor(payload.get("exact_anchor", {}))
        print("TPC348_INDEPENDENT_CHECK=PASS rows=192 positive_witness=192 "
              "position_formula=192")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC348_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
