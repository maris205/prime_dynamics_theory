#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-350.

The checker intentionally does not import the producer.  It rebuilds the
literal matrices in reverse shell order, recomputes all 192 rows, and checks
the growth-series and fresh exact anchor.
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
PROJECT = ROOT / "papers/tpc-350-fresh-growth-signed-incidence"
PRODUCER = PROJECT / "code/tpc350_fresh_growth_signed_incidence.py"
RESULT = PROJECT / "results/tpc350_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-349-prime-balanced-signed-defect-witness/code/"
    "tpc349_prime_balanced_signed_defect_witness.py")
PARENT_CERT = ROOT / (
    "papers/tpc-349-prime-balanced-signed-defect-witness/results/"
    "tpc349_certificate.json")

PRODUCER_SHA256 = (
    "7819fb38be3f6d33688ca3a4caa1920da2dd8624805356411d8099fc069e185d")
PARENT_CODE_SHA256 = (
    "ed3b543a44a270301f3cc7543533c1ce35a6f9ea433e9581df19759b2bca3a03")
PARENT_CERT_SHA256 = (
    "baceb7b6cbf32fbbf84289d302551ed7f42abb45c39333a7d235a229c9a7a741")
CERTIFICATE_SHA256 = (
    "bc874009cfdd8fd7d6ea06d5d109a46d8bd9a732cd4933852f9176c5801bb086")

SCHEMA = "TPC350_FRESH_GROWTH_SIGNED_INCIDENCE_V1"
STATUS = (
    "PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT")
ORIGINS = (60097, 72097, 84097)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (36, 80, 128, 256)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index")
HEIGHT = 66
TOL = 8.0e-9


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


def close(given: Any, value: float) -> bool:
    try:
        return abs(float(given) - float(value)) <= TOL * max(1.0, abs(value))
    except (TypeError, ValueError):
        return False


def locked(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED", label + " hash placeholder")
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def show(value: float) -> str:
    return format(float(value), ".12g")


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


def balanced_coefficients(primes: list[int]) -> list[int]:
    half = len(primes) // 2
    result = [1 if index < half else
              (-1 if index >= len(primes) - half else 0)
              for index in range(len(primes))]
    need(sum(result) == 0, "coefficient balance")
    return result


def spectral_norm(matrix: np.ndarray) -> float:
    eig = np.linalg.eigvalsh((matrix + matrix.T) / 2.0)
    need(len(eig) > 0 and bool(np.all(np.isfinite(eig))), "finite spectrum")
    return max(abs(float(eig[0])), abs(float(eig[-1])))


def reverse_matrices(origin: int, count: int, q0: int, exponent: int,
                     law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray,
                                         list[int]]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + differences.astype(np.float64) ** 2) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    physical = np.zeros((count, count), dtype=np.float64)
    ideal = np.zeros((count, count), dtype=np.float64)
    primes = shell_for(q0)
    for prime, sign in reversed(list(zip(primes, source_signs(primes, law)))):
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
                centered = Fraction(1) if (u - t) % prime == 0 else Fraction(0)
                centered -= Fraction(1, prime - 1)
                kernel = Fraction(HEIGHT ** (2 * exponent),
                                  (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
                result[i][j] += sign * prime * kernel * centered
    return result


def vector_digest(vector: list[Fraction]) -> str:
    text = [f"{item.numerator}/{item.denominator}" for item in vector]
    return hashlib.sha256(canonical(text)).hexdigest()


def check_anchor(anchor: dict[str, Any]) -> None:
    origin, count, q0, exponent, law = 97, 14, 4, 1, "all_plus"
    actual = fraction_matrix(origin, count, q0, exponent, law, True)
    ideal = fraction_matrix(origin, count, q0, exponent, law, False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(count)]
              for i in range(count)]
    primes = shell_for(q0)
    coefficients = balanced_coefficients(primes)
    vector = [sum(Fraction(coefficients[k])
                  for k, prime in enumerate(primes) if value % prime == 0)
              for value in range(origin, origin + count)]
    image = [sum(defect[i][j] * vector[j] for j in range(count))
             for i in range(count)]
    square = sum(item * item for item in image)
    need(anchor.get("interval") == [97, 110] and
         anchor.get("shell") == [5, 7] and
         anchor.get("coefficients") == [1, -1] and
         anchor.get("incidence_vector") ==
         [0, -1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] and
         anchor.get("incidence_vector_squared_norm") == "3" and
         anchor.get("response_vector_squared_norm") ==
         f"{square.numerator}/{square.denominator}" and
         anchor.get("response_vector_digest") == vector_digest(image) and
         anchor.get("identity_exact") is True, "exact anchor")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        locked(PRODUCER, PRODUCER_SHA256, "producer")
        locked(PARENT_CODE, PARENT_CODE_SHA256, "TPC349 producer")
        locked(PARENT_CERT, PARENT_CERT_SHA256, "TPC349 certificate")
        locked(RESULT, CERTIFICATE_SHA256, "certificate")
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
        by_key = {(row["origin"], row["count"], row["q"],
                   row["kernel_exponent"], row["law"]): row for row in rows}
        need(len(by_key) == 192, "row keys")
        positive = beaten = half = 0
        computed = []
        for origin in ORIGINS:
            for count in COUNTS:
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        for law in LAW_NAMES:
                            row = by_key[(origin, count, q0, exponent, law)]
                            _, ideal, defect, primes = reverse_matrices(
                                origin, count, q0, exponent, law)
                            values = np.arange(origin, origin + count,
                                               dtype=np.int64)
                            coefficients = balanced_coefficients(primes)
                            vector = incidence(values, primes, coefficients)
                            norm = float(np.linalg.norm(vector))
                            need(norm > 0.0, "zero signed vector")
                            unit = vector / norm
                            response = float(np.linalg.norm(defect @ unit))
                            defect_norm = spectral_norm(defect)
                            ideal_norm = spectral_norm(ideal)
                            hit = np.any(np.array([(values % prime) == 0
                                                   for prime in primes]), axis=0)
                            coordinate = float(np.linalg.norm(
                                defect[:, hit], axis=0).max())
                            gram = np.zeros(count, dtype=np.float64)
                            for prime, coefficient in zip(primes, coefficients):
                                if coefficient:
                                    gram += coefficient * (defect @
                                        (values % prime == 0).astype(float))
                            gram_error = float(np.max(np.abs(
                                defect @ unit - gram / norm)))
                            need(row.get("balanced_coefficients") == coefficients and
                                 row.get("balanced_coefficient_sum") == 0 and
                                 row.get("balanced_active_prime_count") ==
                                 sum(value != 0 for value in coefficients) and
                                 row.get("signed_incidence_support") ==
                                 int(np.count_nonzero(vector)) and
                                 close(row.get("signed_incidence_norm"), norm) and
                                 close(row.get("signed_witness_response_norm"), response) and
                                 close(row.get("signed_to_defect_ratio"),
                                       response / defect_norm) and
                                 close(row.get("signed_to_ideal_ratio"),
                                       response / ideal_norm) and
                                 close(row.get("signed_to_coordinate_ratio"),
                                       response / coordinate) and
                                 close(row.get("defect_operator_norm"), defect_norm) and
                                 close(row.get("ideal_operator_norm"), ideal_norm) and
                                 close(row.get("incidence_gram_max_error"),
                                       gram_error), "reverse row mismatch")
                            need(gram_error <= TOL and
                                 response <= defect_norm * (1.0 + TOL) and
                                 response > 0.0, "row witness bound")
                            positive += 1
                            if response / coordinate > 1.0 + 1.0e-10:
                                beaten += 1
                            if response / defect_norm >= 0.5 - 1.0e-12:
                                half += 1
                            computed.append({
                                "origin": origin, "count": count, "q": q0,
                                "kernel_exponent": exponent, "law": law,
                                "ratio": response / defect_norm,
                                "support": int(np.count_nonzero(vector)),
                            })
        need(positive == 192 and beaten == 70 and half == 91,
             "aggregate census")
        series = payload.get("growth_series", [])
        need(len(series) == 48, "growth series census")
        expected_series = {}
        for item in computed:
            key = (item["origin"], item["q"], item["kernel_exponent"],
                   item["law"])
            expected_series.setdefault(key, []).append(item)
        nondec = 0
        for item in series:
            key = (item.get("origin"), item.get("q"),
                   item.get("kernel_exponent"), item.get("law"))
            got = sorted(expected_series.get(key, []), key=lambda x: x["count"])
            ratios = [x["ratio"] for x in got]
            need(item.get("counts") == list(COUNTS) and
                 len(ratios) == 4 and
                 all(close(g, v) for g, v in zip(
                     item.get("signed_to_defect_ratios", []), ratios)),
                 "growth series mismatch")
            monotone = all(ratios[i + 1] >= ratios[i] - 1.0e-12
                            for i in range(3))
            need(item.get("nondecreasing") is monotone, "series monotonicity")
            slope = math.log(ratios[-1] / ratios[0], 2.0) / 3.0
            need(close(item.get("endpoint_log2_slope"), slope),
                 "series slope")
            nondec += monotone
        need(nondec == 24, "monotonic series census")
        audit = payload.get("finite_audit", {})
        need(audit.get("rows") == 192 and audit.get("series") == 48 and
             audit.get("positive_signed_witness_rows") == 192 and
             audit.get("balanced_sum_records") == 192 and
             audit.get("incidence_gram_records") == 192 and
             audit.get("coordinate_beaten_rows") == 70 and
             audit.get("half_defect_rows") == 91 and
             audit.get("min_signed_support") == 24 and
             audit.get("max_signed_support") == 294 and
             audit.get("nondecreasing_series") == 24 and
             audit.get("fixed_power_credit") == 0 and
             audit.get("arithmetic_advance") == "NO" and
             close(audit.get("min_signed_to_defect_ratio"),
                   min(item["ratio"] for item in computed)) and
             close(audit.get("max_signed_to_defect_ratio"),
                   max(item["ratio"] for item in computed)), "audit")
        check_anchor(payload.get("exact_anchor", {}))
        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC350_UNIFORM_QUARTER_FLOOR") ==
             "REFUTED_SCOPED" and
             firewall.get("TPC350_SIGNED_TO_DEFECT_FLOOR") ==
             "NUMERICALLY_CERTIFIED_FINITE_0.0657381187306" and
             firewall.get("TPC350_ARITHMETIC_ADVANCE") == "NO" and
             firewall.get("TPC350_FIXED_POWER_CREDIT") == 0 and
             firewall.get("TPC350_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC350_TWIN_PRIME_RESULT") == "NONE",
             "claim firewall")
        print("TPC350_INDEPENDENT_CHECK=PASS rows=192 positive_witness=192 "
              "ratio_floor=0.0657381187306 nondecreasing_series=24/48")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC350_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
