#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-349.

This checker deliberately does not import the producer.  It rebuilds the
physical and ideal matrices in reverse shell order, reconstructs the balanced
signed incidence vector, and checks the stored row readout and exact anchor.
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
PROJECT = ROOT / "papers/tpc-349-prime-balanced-signed-defect-witness"
PRODUCER = PROJECT / "code/tpc349_prime_balanced_signed_defect_witness.py"
RESULT = PROJECT / "results/tpc349_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-348-position-aware-mask-defect-lower-witness/code/"
    "tpc348_position_aware_mask_defect_lower_witness.py")
PARENT_CERT = ROOT / (
    "papers/tpc-348-position-aware-mask-defect-lower-witness/results/"
    "tpc348_certificate.json")

PRODUCER_SHA256 = (
    "ed3b543a44a270301f3cc7543533c1ce35a6f9ea433e9581df19759b2bca3a03")
PARENT_CODE_SHA256 = (
    "fe29f0adeea6234c637a479ba2447068a1e6b1c91731761ed2d2af73464d20b8")
PARENT_CERT_SHA256 = (
    "5f0b1cb66431f6a57fa97335808f30fdbe86ffc0b31ce074d7a1dbbdc692a294")
CERTIFICATE_SHA256 = (
    "baceb7b6cbf32fbbf84289d302551ed7f42abb45c39333a7d235a229c9a7a741")

SCHEMA = "TPC349_PRIME_BALANCED_SIGNED_DEFECT_WITNESS_V1"
STATUS = (
    "PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_AUDIT")
ORIGINS = (40097, 48097)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
TOL = 4.0e-9


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


def close(given: Any, value: float) -> bool:
    try:
        return abs(float(given) - float(value)) <= 5.0e-9 * max(
            1.0, abs(float(value)))
    except (TypeError, ValueError):
        return False


def lock(path: Path, expected: str, label: str) -> None:
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


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
    need(law in LAW_NAMES, "unknown law")
    if law == "all_plus":
        return [1] * len(primes)
    if law == "alternating_index":
        return [1 if j % 2 == 0 else -1 for j in range(len(primes))]
    if law == "mod4_character":
        return [1 if p % 4 == 1 else -1 for p in primes]
    return [1 if j < len(primes) / 2 else -1
            for j in range(len(primes))]


def balanced_coefficients(primes: list[int]) -> list[int]:
    count = len(primes)
    half = count // 2
    result = [1 if j < half else (-1 if j >= count - half else 0)
              for j in range(count)]
    need(sum(result) == 0, "balanced coefficient sum")
    return result


def spectral_norm(matrix: np.ndarray) -> float:
    symmetric = (matrix + matrix.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(symmetric)
    need(len(eigenvalues) > 0 and bool(np.all(np.isfinite(eigenvalues))),
         "finite spectrum")
    return max(abs(float(eigenvalues[0])), abs(float(eigenvalues[-1])))


def reverse_matrices(origin: int, count: int, q0: int, exponent: int,
                     law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray,
                                         list[int]]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    distances = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distances * distances) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    physical = np.zeros((count, count), dtype=np.float64)
    ideal = np.zeros((count, count), dtype=np.float64)
    primes = shell_for(q0)
    pairs = list(zip(primes, source_signs(primes, law)))
    for prime, sign in reversed(pairs):
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
    return physical, ideal, physical - ideal, primes


def incidence(values: np.ndarray, primes: list[int],
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
                centered = (Fraction(1) if (u - t) % prime == 0
                            else Fraction(0))
                centered -= Fraction(1, prime - 1)
                kernel = Fraction(HEIGHT ** (2 * exponent),
                                  (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
                result[i][j] += sign * prime * kernel * centered
    return result


def vector_digest(vector: list[Fraction]) -> str:
    text = [f"{item.numerator}/{item.denominator}" for item in vector]
    return hashlib.sha256(canonical(text)).hexdigest()


def check_anchor(anchor: dict[str, Any]) -> None:
    actual = fraction_matrix(1, 14, 4, 1, "all_plus", True)
    ideal = fraction_matrix(1, 14, 4, 1, "all_plus", False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(14)]
              for i in range(14)]
    primes = shell_for(4)
    coefficients = balanced_coefficients(primes)
    vector = [sum(Fraction(coefficients[k])
                  for k, prime in enumerate(primes) if value % prime == 0)
              for value in range(1, 15)]
    image = [sum(defect[i][j] * vector[j] for j in range(14))
             for i in range(14)]
    vector_square = sum(item * item for item in vector)
    image_square = sum(item * item for item in image)
    need(anchor.get("coefficients") == coefficients and
         anchor.get("incidence_vector") == [int(item) for item in vector] and
         anchor.get("incidence_vector_squared_norm") == "4" and
         anchor.get("response_vector_squared_norm") ==
         f"{image_square.numerator}/{image_square.denominator}" and
         anchor.get("response_vector_digest") == vector_digest(image) and
         anchor.get("identity_exact") is True, "exact anchor")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        lock(PRODUCER, PRODUCER_SHA256, "producer")
        lock(PARENT_CODE, PARENT_CODE_SHA256, "TPC348 producer")
        lock(PARENT_CERT, PARENT_CERT_SHA256, "TPC348 certificate")
        lock(RESULT, CERTIFICATE_SHA256, "certificate")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload")
        need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
             "certificate schema")
        need(document.get("payload_sha256") == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload digest")
        protocol = payload.get("protocol", {})
        need(protocol.get("origins") == list(ORIGINS) and
             protocol.get("source_counts") == list(COUNTS) and
             protocol.get("q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("height") == HEIGHT and
             protocol.get("laws") == list(LAW_NAMES), "protocol")
        rows = payload.get("rows", [])
        need(len(rows) == 192, "row census")
        by_key = {(r["origin"], r["count"], r["q"],
                   r["kernel_exponent"], r["law"]): r for r in rows}
        need(len(by_key) == 192, "row keys")
        positive = 0
        beaten = 0
        for origin in ORIGINS:
            for count in COUNTS:
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        for law in LAW_NAMES:
                            key = (origin, count, q0, exponent, law)
                            row = by_key[key]
                            _, ideal, defect, primes = reverse_matrices(
                                origin, count, q0, exponent, law)
                            values = np.arange(origin, origin + count,
                                               dtype=np.int64)
                            coefficients = balanced_coefficients(primes)
                            vector = incidence(values, primes, coefficients)
                            norm = float(np.linalg.norm(vector))
                            need(norm > 0.0, "zero signed vector")
                            response = float(np.linalg.norm(defect @
                                                            (vector / norm)))
                            defect_norm = spectral_norm(defect)
                            ideal_norm = spectral_norm(ideal)
                            hit = np.any(np.array([(values % p) == 0
                                                   for p in primes]), axis=0)
                            coordinate = float(np.linalg.norm(
                                defect[:, hit], axis=0).max())
                            need(row.get("balanced_coefficients") == coefficients and
                                 row.get("balanced_coefficient_sum") == 0 and
                                 row.get("signed_incidence_support") ==
                                 int(np.count_nonzero(vector)) and
                                 close(row.get("signed_incidence_norm"), norm) and
                                 close(row.get("signed_witness_response_norm"),
                                       response) and
                                 close(row.get("signed_to_defect_ratio"),
                                       response / defect_norm) and
                                 close(row.get("signed_to_ideal_ratio"),
                                       response / ideal_norm) and
                                 close(row.get("signed_to_coordinate_ratio"),
                                       response / coordinate) and
                                 close(row.get("defect_operator_norm"),
                                       defect_norm) and
                                 close(row.get("ideal_operator_norm"),
                                       ideal_norm), "reverse row mismatch")
                            gram = np.zeros(count, dtype=np.float64)
                            for p, coefficient in zip(primes, coefficients):
                                if coefficient:
                                    h = (values % p == 0).astype(np.float64)
                                    gram += coefficient * (defect @ h)
                            gram_error = float(np.max(np.abs(
                                defect @ (vector / norm) - gram / norm)))
                            need(gram_error <= TOL and close(
                                row.get("incidence_gram_max_error"), gram_error),
                                 "reverse Gram mismatch")
                            need(response <= defect_norm * (1.0 + TOL),
                                 "lower bound")
                            need(response > 0.0, "positive response")
                            positive += 1
                            if response / coordinate > 1.0 + 1.0e-10:
                                beaten += 1
        need(positive == 192 and beaten == 136, "aggregate census")
        check_anchor(payload.get("exact_anchor", {}))
        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC349_UNIVERSAL_BALANCED_GAIN") ==
             "REFUTED_SCOPED" and
             firewall.get("TPC349_ARITHMETIC_ADVANCE", "NO") == "NO" and
             firewall.get("TPC349_FIXED_POWER_CREDIT") == 0 and
             firewall.get("TPC349_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC349_TWIN_PRIME_RESULT") == "NONE",
             "claim firewall")
        print("TPC349_INDEPENDENT_CHECK=PASS rows=192 positive_witness=192 "
              "coordinate_beaten=136")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC349_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
